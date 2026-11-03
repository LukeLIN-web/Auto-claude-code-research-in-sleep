"""Fail on a paragraph whose last line is shorter than half the column width.

usage: check_runts.py <compiled.pdf>        exit 1 and list each runt, 0 if none

The rule is judged on the compiled PDF, not the .tex: every edit reflows its
paragraph, so a runt fixed by hand comes back unnoticed unless something reads
the PDF. The fix is cutting words until the line is absorbed into the one above,
never \\looseness, \\vspace or spacing tricks.

Body-size text only (the most common font size by characters); captions and
tables set smaller are not read. Works for one- and two-column layouts: a line
that ends left of the page middle is in the left column, one that starts right
of it in the right column, and one that crosses it is full width; each column
gets its own margins. A runt is a body line that starts at its column's left
margin, is under half the column width, follows a full justified line, is not
bold (run-in \\paragraph heads) or a section number, and ends its paragraph:
the next line in the column starts at most 2.5 em from the margin (an indented
or flush new paragraph, a heading) or there is none. A line followed by a
centred display equation does not end its paragraph.
"""
import collections
import re
import sys

import pymupdf

HEADING = re.compile(r"^([A-Z]|\d+)(\.\d+)*(\s|$)")


def body_size(doc):
    sizes = collections.Counter()
    for page in doc:
        for b in page.get_text("dict")["blocks"]:
            for line in b.get("lines", []):
                for s in line["spans"]:
                    sizes[round(s["size"], 1)] += len(s["text"])
    return sizes.most_common(1)[0][0]


def columns_of(page, body):
    """{column: [(y, x0, x1, text, bold)]} for the body-size lines of one page, top to bottom."""
    mid = page.rect.width / 2
    lines = []
    for b in page.get_text("dict")["blocks"]:
        for line in b.get("lines", []):
            spans = [s for s in line["spans"] if s["text"].strip()]
            if spans and collections.Counter(round(s["size"], 1) for s in spans).most_common(1)[0][0] == body:
                lines.append((line["bbox"], spans))
    # A page is two-column when body lines start right of the middle; on a one-column page a short last
    # line ends left of the middle too, so the column has to be decided per page, not per line.
    two = sum(bbox[0] >= mid - 5 for bbox, _ in lines) >= 5
    cols = collections.defaultdict(dict)
    for (x0, _, x1, y), spans in lines:
        col = "full" if not two else "left" if x1 <= mid + 5 else "right" if x0 >= mid - 5 else "full"
        r = cols[col].setdefault(round(y), [x0, x1, "", True])
        r[0], r[1] = min(r[0], x0), max(r[1], x1)
        r[2] += "".join(s["text"] for s in spans)
        r[3] = r[3] and all(s["flags"] & 16 for s in spans)
    return {c: [(y, *rows[y]) for y in sorted(rows) if not rows[y][2].strip().isdigit()]  # page number
            for c, rows in cols.items()}


def main(pdf):
    doc = pymupdf.open(pdf)
    body = body_size(doc)
    pages = [columns_of(p, body) for p in doc]
    lefts, rights = collections.defaultdict(collections.Counter), collections.defaultdict(collections.Counter)
    for cols in pages:
        for c, rows in cols.items():
            for _, x0, x1, _, _ in rows:
                lefts[c][round(x0)] += 1
                rights[c][round(x1)] += 1
    margins = {c: (lefts[c].most_common(1)[0][0], rights[c].most_common(1)[0][0]) for c in lefts}

    hits = []
    for pno, cols in enumerate(pages, 1):
        for c, rows in cols.items():
            L, R = margins[c]
            for i, (y, x0, x1, text, bold) in enumerate(rows):
                if i == 0 or bold or abs(x0 - L) > 3 or x1 - x0 >= (R - L) / 2:
                    continue
                if HEADING.match(text.strip()) and len(text.strip()) < 12 or text.strip().isupper():
                    continue
                if rows[i - 1][2] < R - 3:  # the line above is not a full justified line
                    continue
                if i + 1 < len(rows) and rows[i + 1][1] - L > 2.5 * body:  # a display follows
                    continue
                hits.append(f"p{pno} {c}: …{rows[i - 1][3][-40:]} / {text.strip()}")
    for h in hits:
        print(h)
    print(f"runts (last line < half the column width): {len(hits)}")
    return 1 if hits else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    sys.exit(main(sys.argv[1]))
