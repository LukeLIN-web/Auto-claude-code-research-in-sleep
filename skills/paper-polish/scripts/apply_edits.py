#!/usr/bin/env python3
"""Apply the taken edits of one scratch file to the real file, paragraph by paragraph.

usage: apply_edits.py <base.tex> <edited.tex> <target.tex> [--reject 40-45,80] [--write]

BASE is the copy the editor started from, EDITED its scratch copy (same line count), TARGET the real file, which
other sessions may have changed since. --reject restores those lines of EDITED from BASE first (the edits step 5
rejected: dropped, not repaired). BASE lines are matched to TARGET by a line diff, so lines other sessions added,
removed or changed elsewhere, even next to an edit, do not get in the way. Per paragraph of BASE: if another session
changed a line the editor also changed, all of the paragraph's edits are dropped and their version stays; if it
changed only other lines of the paragraph, the edits are applied and the paragraph is listed for the owner to check
again as merged (an edit may have leaned on the line they rewrote). Lines the edit made exactly `%CUT` are removed.
Prints each paragraph's outcome and the diff against TARGET; with --write it writes TARGET. Exit 1 if any paragraph
was dropped or needs the second check.
"""
import argparse
import difflib
import sys
from pathlib import Path

from check_edits import paragraphs, ranges


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("base", type=Path)
    ap.add_argument("edited", type=Path)
    ap.add_argument("target", type=Path)
    ap.add_argument("--reject", default="")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    base = a.base.read_text(encoding="utf-8").split("\n")
    edited = a.edited.read_text(encoding="utf-8").split("\n")
    target = a.target.read_text(encoding="utf-8").split("\n")
    if len(base) != len(edited):
        sys.exit(f"line count differs {len(base)} -> {len(edited)}: the editor must keep one line per original line")
    for i in ranges(a.reject):
        edited[i - 1] = base[i - 1]
    where = {}
    for tag, i1, i2, j1, _ in difflib.SequenceMatcher(None, base, target, autojunk=False).get_opcodes():
        if tag == "equal":
            where.update((i1 + k, j1 + k) for k in range(i2 - i1))
    result, cut, flagged = list(target), set(), 0
    for para in paragraphs(base):
        changed = [i for i in para if base[i - 1] != edited[i - 1]]
        if not changed:
            continue
        theirs = [i for i in para if i - 1 not in where]
        if set(theirs) & set(changed):
            flagged += 1
            print(f"DROPPED L{para[0]}-{para[-1]}: another session changed line(s) {sorted(set(theirs) & set(changed))}"
                  " the editor changed too; their version of the paragraph stays")
            continue
        for i in changed:
            j = where[i - 1]
            result[j] = edited[i - 1]
            if edited[i - 1] == "%CUT":
                cut.add(j)
        print(f"applied L{para[0]}-{para[-1]} (lines {changed})")
        if theirs:
            flagged += 1
            print(f"    another session changed line(s) {theirs} of this paragraph: re-check the merged paragraph (§ 5)")
    result = [line for j, line in enumerate(result) if j not in cut]
    sys.stdout.writelines(difflib.unified_diff([l + "\n" for l in target], [l + "\n" for l in result],
                                               str(a.target), "merged", n=0))
    if a.write:
        a.target.write_text("\n".join(result), encoding="utf-8")
        print(f"wrote {a.target}")
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main())
