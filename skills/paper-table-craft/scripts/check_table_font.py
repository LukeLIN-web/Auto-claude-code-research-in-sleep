"""Measure the printed type size of every table in a compiled paper.

usage: check_table_font.py <compiled.pdf> [--pages 5,14-17] [--table tab:main|3|G.1 ...]
                           [--aux main.aux] [--floor 7.5]

Prints one line per table: its number, page, body size (the size most of its
characters are set in) and smallest size, then a `body sizes differ` line when
the tables are not all set in one size. Exit 1 when a table's smallest size is
under the floor (7.5 pt), or a table cannot be measured, or a requested table
is not found.

A table is found by its caption ("Table 3." / "Table G.1:" opening a text
block) and its horizontal rules: the rules of one tabular share their left and
right ends, and the group of them nearest the caption (below it, or above it
for a caption set below; groups beside it are its subtables) bounds the table.
Every character inside those bounds counts, except sub- and superscripts
(raised or lowered against the largest span of their line, or flagged
superscript by the PDF) and lone marks such as `*`, `†`, `◦`: those
legitimately print near 6 pt. Notes set under the bottom rule are outside the
bounds. A table with no horizontal rules is reported as not measured.

--table takes a printed number (`3`, `G.1`) or a `\\label` (`tab:main`), which
is resolved through the .aux written next to the PDF (or --aux). --pages counts
PDF pages from 1.
"""
import argparse
import collections
import re
import sys
from pathlib import Path

import pymupdf

CAPTION = re.compile(r"^(Table|Figure|Fig\.)\s+([A-Z]?\.?\d+(?:\.\d+)*)\s*[.:]")
SUBCAPTION = re.compile(r"^\([a-z]\)")
MARKS = set("*∗†‡§¶◦°•⋆⋄♯♭✓✗×")
RULE_MIN = 20.0   # pt; shorter horizontal strokes are underlines, cmidrule pieces, glyph parts
END_TOL = 1.0     # pt; rules of one tabular share their ends to within this
NEAR = 40.0       # pt; how far a table's first rule may sit from its caption


def parse_pages(spec, n):
    pages = set()
    for part in spec.split(","):
        a, _, b = part.partition("-")
        pages.update(range(int(a), int(b or a) + 1))
    return sorted(p for p in pages if 1 <= p <= n)


def label_numbers(aux):
    """\\newlabel{tab:x}{{3}{5}...} -> {'tab:x': '3'}"""
    out = {}
    for m in re.finditer(r"\\newlabel\{([^}]*)\}\{\{([^{}]*)\}", aux.read_text(errors="replace")):
        out[m.group(1)] = m.group(2).strip()
    return out


def horizontal_rules(page):
    rules = []
    for d in page.get_drawings():
        for it in d["items"]:
            if it[0] == "l":
                p, q = it[1], it[2]
                if abs(p.y - q.y) < 0.3 and abs(p.x - q.x) >= RULE_MIN:
                    rules.append((min(p.x, q.x), max(p.x, q.x), (p.y + q.y) / 2))
            elif it[0] == "re":
                r = it[1]
                if r.height < 1.5 and r.width >= RULE_MIN:
                    rules.append((r.x0, r.x1, (r.y0 + r.y1) / 2))
    return rules


def captions(blocks):
    """(kind, number, bbox) for each block whose first line opens a caption."""
    out = []
    for b in blocks:
        if b.get("type") != 0 or not b["lines"]:
            continue
        m = CAPTION.match("".join(s["text"] for s in b["lines"][0]["spans"]).strip())
        if m:
            out.append((m.group(1), m.group(2), pymupdf.Rect(b["bbox"])))
    return out


def rule_groups(rules, caps):
    """Rules sharing both ends form one tabular; a caption between two of them splits it."""
    groups = []
    for x0, x1, y in sorted(rules, key=lambda r: r[2]):
        for g in groups:
            if abs(g["x0"] - x0) <= END_TOL and abs(g["x1"] - x1) <= END_TOL:
                split = any(c[2].y0 > g["ys"][-1] and c[2].y1 < y and c[2].x0 < x1 and c[2].x1 > x0
                            for c in caps)
                if not split:
                    g["ys"].append(y)
                    break
        else:
            groups.append({"x0": x0, "x1": x1, "ys": [y]})
    return [pymupdf.Rect(g["x0"], g["ys"][0], g["x1"], g["ys"][-1]) for g in groups if len(g["ys"]) >= 2]


def table_bounds(cap, groups, blocks, mid):
    """The rule groups of the table a caption names: the nearest below it, else above.

    A caption that crosses the page middle heads a full-width float; one that
    does not keeps to its column. A group further than NEAR from the caption
    still belongs to it when only subcaptions ("(a) ...") sit in between.
    Groups beside the nearest one (overlapping it vertically) are its
    side-by-side subtables.
    """
    if cap.x0 < mid < cap.x1:
        column = groups
    elif cap.x1 <= mid:
        column = [g for g in groups if g.x1 <= mid + 3]
    else:
        column = [g for g in groups if g.x0 >= mid - 3]
    texts = [(pymupdf.Rect(b["bbox"]), "".join(s["text"] for s in b["lines"][0]["spans"]).strip())
             for b in blocks if b.get("type") == 0 and b["lines"]]

    def reaches(g, top, bottom):
        if bottom - top <= NEAR:
            return True
        between = [t for r, t in texts if r.y0 >= top - 1 and r.y1 <= bottom + 1
                   and min(r.x1, g.x1) > max(r.x0, g.x0)]
        return bottom - top <= 4 * NEAR and all(SUBCAPTION.match(t) for t in between)

    below = [g for g in column if g.y0 >= cap.y1 - 1 and reaches(g, cap.y1, g.y0)]
    above = [g for g in column if g.y1 <= cap.y0 + 1 and reaches(g, g.y1, cap.y0)]
    for cands, gap in ((below, lambda g: g.y0 - cap.y1), (above, lambda g: cap.y0 - g.y1)):
        if cands:
            near = min(cands, key=gap)
            return [g for g in cands if g.y0 <= near.y1 and g.y1 >= near.y0]
    return []


def sizes_in(blocks, bounds):
    """(size, text) of every span inside the bounds that is not a script or a lone mark.

    A script is a span set smaller than a neighbour it touches vertically, on
    another baseline: a sub- or superscript, a fraction's numerator or
    denominator, a limit under a sum.
    """
    spans = []
    for b in blocks:
        if b.get("type") != 0:
            continue
        for line in b["lines"]:
            for s in line["spans"]:
                r = pymupdf.Rect(s["bbox"])
                c = (r.tl + r.br) / 2
                if s["text"].strip() and any(pymupdf.Rect(g.x0 - 3, g.y0 - 1, g.x1 + 3, g.y1 + 1).contains(c)
                                             for g in bounds):
                    spans.append((r, s))

    def script(r, s):
        if s["flags"] & 1 or set(s["text"].strip()) <= MARKS:
            return True
        for r2, s2 in spans:
            if (s2["size"] >= s["size"] + 1 and abs(s2["origin"][1] - s["origin"][1]) > 0.5
                    and min(r.y1, r2.y1) > max(r.y0, r2.y0)
                    and max(r2.x0 - r.x1, r.x0 - r2.x1) < 1.5 * s2["size"]):
                return True
        return False

    return [(s["size"], s["text"].strip()) for r, s in spans if not script(r, s)]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("pdf")
    ap.add_argument("--pages", help="PDF pages to read, e.g. 5,14-17 (default: all)")
    ap.add_argument("--table", action="append", default=[], help="printed number or \\label; repeatable")
    ap.add_argument("--aux", help="the .aux that resolves --table labels (default: next to the PDF)")
    ap.add_argument("--floor", type=float, default=7.5)
    a = ap.parse_args()

    doc = pymupdf.open(a.pdf)
    want = set()
    if a.table:
        aux = Path(a.aux) if a.aux else Path(a.pdf).with_suffix(".aux")
        labels = label_numbers(aux) if aux.is_file() else {}
        for t in a.table:
            if ":" in t and t not in labels:
                sys.exit(f"{t}: no such \\label in {aux}")
            want.add(labels.get(t, t))
    pages = parse_pages(a.pages, len(doc)) if a.pages else range(1, len(doc) + 1)

    rows, found, bad = [], set(), False
    for pno in pages:
        page = doc[pno - 1]
        blocks = page.get_text("dict")["blocks"]
        caps = captions(blocks)
        groups = rule_groups(horizontal_rules(page), caps)
        for kind, num, cap in caps:
            if kind != "Table" or (want and num not in want) or num in found:
                continue
            found.add(num)
            bounds = table_bounds(cap, groups, blocks, page.rect.width / 2)
            sizes = sizes_in(blocks, bounds) if bounds else []
            if not sizes:
                bad = True
                print(f"Table {num:<5} p.{pno:<3} not measured: no horizontal rules next to its caption")
                continue
            chars = collections.Counter()
            for size, text in sizes:
                chars[round(size, 1)] += len(text)
            body = chars.most_common(1)[0][0]
            low, text = min(sizes)
            flag = ""
            if low < a.floor:
                bad, flag = True, f"  UNDER {a.floor} pt: {text[:40]!r}"
            rows.append((num, body))
            print(f"Table {num:<5} p.{pno:<3} body {body:4.1f} pt  min {low:4.1f} pt{flag}")

    missing = sorted(want - found)
    for num in missing:
        print(f"Table {num}: caption not found" + (" on the pages read" if a.pages else ""))
    by_body = collections.defaultdict(list)
    for num, body in rows:
        by_body[body].append(num)
    if len(by_body) > 1:
        print("body sizes differ: " + "; ".join(f"{b:.1f} pt ({', '.join(n)})" for b, n in sorted(by_body.items())))
    if not rows and not missing:
        print("no table captions found")
    sys.exit(1 if bad or missing else 0)


if __name__ == "__main__":
    main()
