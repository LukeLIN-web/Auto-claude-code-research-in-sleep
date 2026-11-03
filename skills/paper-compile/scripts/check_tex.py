r"""Fail on caption-rule breaks and repo-internal paths in the .tex a paper compiles.

usage: check_tex.py <root.tex> [--leak REGEX]     exit 1 and list each hit, 0 if clean

Reads the root file and every file it reaches through \input / \include, so a
template's instruction document or a stale section that nothing inputs is not
read. Two checks, one owner each:

- Captions (rule in paper-table-craft / paper-figure-craft): no pointer at
  another float or the prose (\ref{}, \S, Appendix, Table~, Figure~, "the
  text"), and at most 1200 characters. Generated and hand-written captions are
  checked alike. Commented-out text is ignored.
- Repo-internal paths: the .tex ships to Overleaf, co-authors and the
  submission source with its comments, so no line of it, comments included, may
  name result pages, run outputs, scripts or machines. --leak replaces the
  default pattern; add the project's host names there.
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


def uncomment(tex):
    return re.sub(r"(?<!\\)%.*", "", tex)


def tex_files(root):
    """The root file and everything it reaches through \\input / \\include, in reading order."""
    base, seen, order = os.path.dirname(os.path.abspath(root)), set(), []

    def visit(path):
        if path in seen or not os.path.isfile(path):
            return
        seen.add(path)
        order.append(path)
        for name in re.findall(r"\\(?:input|include)\{([^}]+)\}", uncomment(open(path, encoding="utf-8").read())):
            p = os.path.join(base, name)
            visit(p if p.endswith(".tex") else p + ".tex")

    visit(os.path.abspath(root))
    return order


def captions(tex):
    r"""The text inside every \caption{...} / \captionof{...}{...}, braces matched."""
    for m in re.finditer(r"\\caption(?:of\{[a-z]+\})?(?:\[[^]]*\])?\{", tex):
        depth = 0
        for k in range(m.end() - 1, len(tex)):
            depth += {"{": 1, "}": -1}.get(tex[k], 0)
            if depth == 0:
                yield tex[m.end():k]
                break


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root")
    ap.add_argument("--leak", default=LEAK)
    a = ap.parse_args()
    base, hits, n = os.path.dirname(os.path.abspath(a.root)), [], 0
    for path in tex_files(a.root):
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
    for h in hits:
        print(h)
    print(f"{n} captions and {len(tex_files(a.root))} files read; {len(hits)} hits")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
