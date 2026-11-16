r"""Fail on caption-rule breaks, repo-internal paths and out-of-order float references in the .tex a paper compiles.

usage: check_tex.py <root.tex> [--aux main.aux] [--leak REGEX]     exit 1 and list each hit, 0 if clean

Reads the root file and every file it reaches through \input / \include, so a
template's instruction document or a stale section that nothing inputs is not
read. Three checks, one owner each:

- Captions (rule in paper-table-craft / paper-figure-craft): no pointer at
  another float or the prose (\ref{}, \S, Appendix, Table~, Figure~, "the
  text"), and at most 1200 characters. Generated and hand-written captions are
  checked alike. Commented-out text is ignored.
- Repo-internal paths: the .tex ships to Overleaf, co-authors and the
  submission source with its comments, so no line of it, comments included, may
  name result pages, run outputs, scripts or machines. --leak replaces the
  default pattern; add the project's host names there.
- Float reference order (manuscript-craft final-pass checklist): within each
  numbering series (figures, tables, algorithms; an appendix's "A.1, A.2" is its
  own series), the floats' first references in reading order come in numbering
  order, so Figure 4 is never cited before Figure 3; a float never referenced
  counts as referenced last. Numbers and kinds come from the compile's .aux
  (cleveref's type, else hyperref's anchor), so compile first; --aux defaults to
  the .aux beside the root file.
"""
import argparse
import os
import re
import sys

CAPTION_MAX_CHARS = 1200
CAPTION_BANNED = (
    (r"\\ref\{", r"\ref{} to another label"),
    (r"\\S(?![a-zA-Z])", r"\S section pointer"),
    (r"\bApp(?:endix)?\b", "appendix pointer"),
    (r"(?:Table|Figure)~", "pointer at another float"),
    (r"\bthe text\b", "deferral to the prose"),
)
LEAK = r"(docs/|outputs/|eval_res|/shared/|/home/|[A-Za-z_]+\.py\b)"
INPUT = r"\\(?:input|include)\{([^}]+)\}"
REF = r"\\(?:ref|[cC]ref|[aA]utoref|labelcref|[cC]refrange)\*?\{([^}]+)\}"
FLOATS = ("figure", "table", "algorithm")


def uncomment(tex):
    return re.sub(r"(?<!\\)%.*", "", tex)


def walk(root):
    """(path, line number, uncommented text) in reading order, each \\input / \\include expanded where it stands."""
    base, seen = os.path.dirname(os.path.abspath(root)), set()

    def visit(path):
        if path in seen or not os.path.isfile(path):
            return
        seen.add(path)
        for i, line in enumerate(open(path, encoding="utf-8").read().splitlines(), 1):
            for k, part in enumerate(re.split(INPUT, uncomment(line))):  # text, name, text, ...
                if k % 2:
                    p = os.path.join(base, part)
                    yield from visit(p if p.endswith(".tex") else p + ".tex")
                else:
                    yield path, i, part

    yield from visit(os.path.abspath(root))


def tex_files(root):
    """The root file and everything it reaches through \\input / \\include, in reading order."""
    return list(dict.fromkeys(path for path, _, _ in walk(root)))


def captions(tex):
    r"""The text inside every \caption{...} / \captionof{...}{...}, braces matched."""
    for m in re.finditer(r"\\caption(?:of\{[a-z]+\})?(?:\[[^]]*\])?\{", tex):
        depth = 0
        for k in range(m.end() - 1, len(tex)):
            depth += {"{": 1, "}": -1}.get(tex[k], 0)
            if depth == 0:
                yield tex[m.end():k]
                break


def float_numbers(aux):
    """label -> (kind, series, n, printed) for every figure, table and algorithm the compile numbered."""
    text = open(aux, encoding="utf-8", errors="replace").read()
    kinds = dict(re.findall(r"^\\newlabel\{([^}]*)@cref\}\{\{\[(\w+)\]", text, re.M))
    out = {}
    for line in text.splitlines():
        m = re.match(r"\\newlabel\{([^}@]*)\}\{\{([^{}]*)\}", line)
        anchor = re.search(r"\{(\w+)\.[^{}]*\}\{[^{}]*\}\}\s*$", line)
        kind = m and (kinds.get(m[1]) or anchor and anchor[1])
        num = m and re.fullmatch(r"(.*?)(\d+)", m[2])
        if kind in FLOATS and num:
            out[m[1]] = (kind, num[1], int(num[2]), m[2])
    return out


def order_hits(root, aux):
    """Hits where a float's first reference comes before that of a lower-numbered float in its series."""
    base, floats, first = os.path.dirname(os.path.abspath(root)), float_numbers(aux), {}
    for path, i, text in walk(root):
        for group in re.findall(REF, text):
            for label in (s.strip() for s in group.split(",")):
                if label in floats and label not in first:
                    first[label] = f"{os.path.relpath(path, base)}:{i}"
    name = lambda label: f"{floats[label][0].capitalize()} {floats[label][3]} ({label})"
    rank = {label: k for k, label in enumerate(first)}  # reading order of first references; never cited ranks last
    hits, skipped = [], set()
    for label in first:
        kind, series, n, _ = floats[label]
        for other in sorted(floats, key=lambda o: floats[o][2]):
            k, s, m, _ = floats[other]
            if (k, s) == (kind, series) and m < n and rank.get(other, len(rank)) > rank[label] and other not in skipped:
                skipped.add(other)  # one hit per float jumped over, at the first reference that jumps it
                later = f"first referenced at {first[other]}" if other in first else "never referenced"
                hits.append(f"{first[label]}: {name(label)} is first referenced before {name(other)}, {later}")
    return hits, len(floats)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root")
    ap.add_argument("--aux", help="the compile's .aux (default: beside the root file)")
    ap.add_argument("--leak", default=LEAK)
    a = ap.parse_args()
    base, hits, n = os.path.dirname(os.path.abspath(a.root)), [], 0
    files = tex_files(a.root)
    for path in files:
        rel, src = os.path.relpath(path, base), open(path, encoding="utf-8").read()
        for cap in captions(uncomment(src)):
            n += 1
            for pattern, what in CAPTION_BANNED:
                if re.search(pattern, cap):
                    hits.append(f"{rel}: caption carries a {what}: {cap[:60]}…")
            if len(cap) > CAPTION_MAX_CHARS:
                hits.append(f"{rel}: caption is {len(cap)} chars, over {CAPTION_MAX_CHARS}; rewrite it whole")
        for i, line in enumerate(src.splitlines(), 1):
            if re.search(a.leak, line):
                hits.append(f"{rel}:{i}: repo-internal path: {line.strip()[:100]}")
    aux = a.aux or os.path.splitext(a.root)[0] + ".aux"
    if os.path.isfile(aux):
        order, n_floats = order_hits(a.root, aux)
        hits += order
    else:
        hits.append(f"no .aux at {aux}: compile first, or pass --aux <outdir>/main.aux")
        n_floats = 0
    for h in hits:
        print(h)
    print(f"{n} captions, {n_floats} numbered floats and {len(files)} files read; {len(hits)} hits")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
