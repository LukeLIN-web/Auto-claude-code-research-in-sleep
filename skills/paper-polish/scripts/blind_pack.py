#!/usr/bin/env python3
"""Build the blind-read inputs of a polish (step 1 and the acceptance read), split across parallel readers.

usage: blind_pack.py <clone> <compiled.pdf> <compiled.aux> <scope.tsv> <outdir>
                     [--readers N] [--macro '\\method=OurMethod' ...]

Writes into OUTDIR:
  pdf_pages.txt        the whole compiled PDF as page-ordered text (pdftotext -layout), the context every reader gets;
  figure_canvases.txt  the text on every figure PDF the .tex files include;
  in_scope-<k>.txt     reader k's sentences, roughly as printed, with ids; k = 1..N;
  ids.tsv              id, file:line, reader, for the owner.
A macro the polish does not map stays in the text as written (\\method); pass --macro for each one the paper defines.

SCOPE.TSV is polish_scope.py's output (file, line, ...), with the rows the polish must not touch removed.
Ids are a letter per file in reading order plus a counter (A1, A2, B1, ...). Readers get contiguous runs of
sentences of about equal printed length, cut where the section heading changes when one is near.
Without --readers, N = ceil(chars / 4000), at most 4: one reader on 3-4 KB of in-scope text took 4-8 minutes,
on 12-13 KB 17-30 minutes in one long turn, and once ran into the output cap and lost the whole turn.
"""
import argparse
import math
import re
import subprocess
from pathlib import Path

from polish_scope import input_order

HEAD = re.compile(r"\\(?:(?:sub)*section|paragraph)\*?\{([^}]*)\}|\\caption\{")
FORMAT = re.compile(r"\\(?:emph|textbf|textit|textsc|texttt|underline|paragraph|section|subsection|caption|mbox)\*?\{([^{}]*)\}")
HEADER = (
    "In-scope sentences for reader {k} of {n} (text roughly as printed; [cite] marks a citation; the ids are for "
    "your ledger).\nScope: the sentences written or moved since the last polish; the other readers have the rest. "
    "Everything else in pdf_pages.txt is context: read it in page order as a reviewer would, but write entries "
    "only for the ids below (an entry may name another place as the cause of a stall in one of them). For a "
    "sentence in a restructured paragraph, also ask whether it reads right where it now stands: its link to the "
    "sentences before and after it, and its referents.\n"
)


def printed(s, labels, macros):
    s = re.sub(r"(?<!\\)%.*$", "", s)
    s = re.sub(r"\\label\{[^}]*\}", "", s)
    s = re.sub(r"\\(?:c|C)?(?:ref|eqref|autoref)\{([^}]*)\}", lambda m: labels.get(m[1].split(",")[0], "??"), s)
    s = re.sub(r"~?\\cite[tp]?\*?(?:\[[^\]]*\])?\{[^}]*\}", " [cite]", s)
    for name, value in macros:
        s = s.replace(name + "{}", value).replace(name, value)
    s = re.sub(r"(?<!\\)\$", "", s)
    s = re.sub(r"([_^])\{([^{}]*)\}", r"\1\2", s)
    for _ in range(3):
        s = FORMAT.sub(r"\1", s)
    s = s.replace("\\%", "%").replace("\\&", "&").replace("\\$", "$").replace("~", " ").replace("\\,", " ")
    s = s.replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", s).strip()


def headings(lines, labels):
    """For each 1-based line, the nearest heading above it, or its float's caption while inside a float."""
    out, section, caption, kind = {}, "", "", "Float"
    for i, line in enumerate(lines, 1):
        begin = re.search(r"\\begin\{(table|figure|algorithm)", line)
        if begin:
            kind = begin[1].capitalize()
        m = HEAD.search(line)
        if m and m[1] is not None:
            section, caption = m[1], ""
        elif m:
            near = re.search(r"\\label\{([^}]*)\}", "\n".join(lines[max(0, i - 6):i + 5]))
            label = near[1] if near else ""
            name = {"tab": "Table", "fig": "Figure", "alg": "Algorithm"}.get(label.split(":")[0], kind)
            caption = f"{name} {labels.get(label, '')} caption (read it as its own unit)".replace("  ", " ")
        out[i] = caption or section
        if re.search(r"\\end\{(table|figure|algorithm)", line):
            caption = ""
    return out


def run(*cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout


def main():
    ap = argparse.ArgumentParser()
    for name in ("clone", "pdf", "aux", "scope", "outdir"):
        ap.add_argument(name, type=Path)
    ap.add_argument("--main", default="main.tex")
    ap.add_argument("--readers", type=int)
    ap.add_argument("--macro", action="append", default=[], help="NAME=TEXT, e.g. '\\method=OurMethod'")
    a = ap.parse_args()
    macros = [tuple(m.split("=", 1)) for m in a.macro]
    labels = dict(re.findall(r"\\newlabel\{([^}]*)\}\{\{([^}]*)\}", a.aux.read_text(errors="replace")))

    files, items, cache = [], [], {}
    for row in a.scope.read_text().splitlines():
        rel, line = row.split("\t")[:2]
        if rel not in cache:
            text = (a.clone / rel).read_text(encoding="utf-8", errors="replace").split("\n")
            cache[rel] = (text, headings(text, labels))
            files.append(rel)
        text, heads = cache[rel]
        n = int(line)
        letter = chr(ord("A") + files.index(rel)) if len(files) <= 26 else f"F{files.index(rel) + 1}_"
        items.append({"rel": rel, "line": n, "head": heads[n], "letter": letter, "text": printed(text[n - 1], labels, macros)})
    counters = {}
    for it in items:
        counters[it["letter"]] = counters.get(it["letter"], 0) + 1
        it["id"] = f"{it['letter']}{counters[it['letter']]}"

    total = sum(len(it["text"]) for it in items)
    n = a.readers or max(1, min(4, math.ceil(total / 4000)))
    target, groups, size = total / n, [[]], 0
    for i, it in enumerate(items):
        new_head = i and (it["head"], it["rel"]) != (items[i - 1]["head"], items[i - 1]["rel"])
        if len(groups) < n and groups[-1] and (size >= target or (size >= 0.8 * target and new_head)):
            groups.append([])
            size = 0
        groups[-1].append(it)
        size += len(it["text"])

    a.outdir.mkdir(parents=True, exist_ok=True)
    ids = []
    for k, group in enumerate(groups, 1):
        rows, last = [], None
        for it in group:
            if (it["rel"], it["head"]) != last:
                rows.append(f"\n== {it['head'] or Path(it['rel']).stem}")
                last = (it["rel"], it["head"])
            rows.append(f"{it['id']}. {it['text']}")
            ids.append(f"{it['id']}\t{it['rel']}:{it['line']}\t{k}")
        (a.outdir / f"in_scope-{k}.txt").write_text(HEADER.format(k=k, n=len(groups)) + "\n".join(rows) + "\n")
    (a.outdir / "ids.tsv").write_text("\n".join(ids) + "\n")

    pages = int(re.search(r"Pages:\s+(\d+)", run("pdfinfo", str(a.pdf)))[1])
    (a.outdir / "pdf_pages.txt").write_text("".join(
        f"======== PDF page {p} ========\n" + run("pdftotext", "-layout", "-f", str(p), "-l", str(p), str(a.pdf), "-")
        for p in range(1, pages + 1)))
    canvases, seen = [], set()
    for rel in input_order(a.clone, a.main):
        for target in re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", (a.clone / rel).read_text(errors="replace")):
            pdf = a.clone / (target if target.endswith(".pdf") else target + ".pdf")
            if pdf.exists() and pdf not in seen:
                seen.add(pdf)
                canvases.append(f"== Figure canvas: {target}\n" + run("pdftotext", "-layout", str(pdf), "-"))
    (a.outdir / "figure_canvases.txt").write_text("\n".join(canvases))
    print(f"{len(items)} sentences, {total} chars -> {len(groups)} readers: "
          + ", ".join(f"{len(g)} ({sum(len(it['text']) for it in g)} chars)" for g in groups))


if __name__ == "__main__":
    main()
