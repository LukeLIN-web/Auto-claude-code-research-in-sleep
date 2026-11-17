#!/usr/bin/env python3
"""Apply the taken edits of one scratch file to the real file, by a three-way merge (git merge-file).

usage: apply_edits.py <base.tex> <edited.tex> <target.tex> [--reject 40-45,80] [--write]

BASE is the copy the editor started from, EDITED its scratch copy, TARGET the real file, which other sessions may
have changed since. --reject restores those lines of EDITED from BASE first (the edits step 5 rejected: dropped, not
repaired). Lines that are exactly `%CUT` are removed after the merge. Prints the diff against TARGET; with --write
it writes TARGET, and only when the merge has no conflict (a conflict means someone changed the same lines: re-run
the check on their version instead of merging by hand).
"""
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

from check_edits import ranges


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
    if len(base) != len(edited):
        sys.exit(f"line count differs {len(base)} -> {len(edited)}: the editor must keep one line per original line")
    for i in ranges(a.reject):
        edited[i - 1] = base[i - 1]
    with tempfile.TemporaryDirectory() as d:
        ours, merged = Path(d, "ours"), Path(d, "merged")
        ours.write_text("\n".join(edited), encoding="utf-8")
        r = subprocess.run(["git", "merge-file", "-p", str(ours), str(a.base), str(a.target)], capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout[:4000])
            sys.exit(f"merge conflict ({r.returncode}) in {a.target}; nothing written")
        merged.write_text("\n".join(l for l in r.stdout.split("\n") if l != "%CUT"), encoding="utf-8")
        print(subprocess.run(["diff", str(a.target), str(merged)], capture_output=True, text=True).stdout)
        if a.write:
            a.target.write_text(merged.read_text(encoding="utf-8"), encoding="utf-8")
            print(f"wrote {a.target}")


if __name__ == "__main__":
    main()
