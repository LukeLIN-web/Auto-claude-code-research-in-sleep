#!/usr/bin/env python3
"""List the scope of a polish: every prose line of the .tex files the main file inputs.

usage: polish_scope.py <clone> [<base-commit>] [--main main.tex] > scope.tsv

Without BASE (the polish's default, SKILL.md § 0) every prose line is listed. With BASE, only the lines whose last
change is a commit after it, for a caller that asks for exactly that. A prose line is any non-blank, non-comment line that is not a tabular row or only layout
commands; headings, captions and \\item lines count. Output, one row per line: file, line, commit, author, text,
with files in the order the main file inputs them. Delete the rows the polish must not touch (the frozen spans:
the author column helps find a co-author's lines, but an edit made through a shared editor may carry anyone's
name) before passing the file to blind_pack.py.
"""
import argparse
import re
import subprocess
from pathlib import Path

INPUT = re.compile(r"\\(?:input|include|subfile)\{([^}]+)\}")
# A line that is only layout commands (\begin, \midrule, \centering, \includegraphics ...) or a tabular row is not
# prose; headings, captions and \item lines are.
LAYOUT = re.compile(r"\s*(?:\\(?!(?:sub)*section|paragraph|caption|item)[a-zA-Z]+\*?(?:\[[^\]]*\]|\([^)]*\)|\{[^{}]*\})*\s*)+")
TABULAR = re.compile(r"(?<!\\)&|\\\\\s*$")


def git(clone, *args):
    return subprocess.run(["git", "-C", str(clone), *args], capture_output=True, text=True, check=True).stdout


def input_order(clone, main):
    """Files reachable from MAIN through \\input/\\include, depth first, in reading order."""
    seen, order = set(), []

    def visit(rel):
        path = clone / rel
        if not (path.suffix == ".tex" and path.exists()):
            path = clone / (rel + ".tex")
        rel = str(path.relative_to(clone))
        if rel in seen or not path.exists():
            return
        seen.add(rel)
        order.append(rel)
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            code = re.sub(r"(?<!\\)%.*$", "", line)
            for target in INPUT.findall(code):
                visit(target.strip())

    visit(main)
    return order


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clone", type=Path)
    ap.add_argument("base", nargs="?")
    ap.add_argument("--main", default="main.tex")
    a = ap.parse_args()
    newer = set(git(a.clone, "rev-list", f"{a.base}..HEAD").split()) if a.base else None
    tracked = set(git(a.clone, "ls-files", "*.tex").split())
    for rel in input_order(a.clone, a.main):
        if rel not in tracked or rel == a.main:
            continue
        sha = author = line_no = None
        for row in git(a.clone, "blame", "--line-porcelain", "HEAD", "--", rel).split("\n"):
            m = re.match(r"^([0-9a-f]{40}) \d+ (\d+)", row)
            if m:
                sha, line_no = m[1], int(m[2])
            elif row.startswith("author "):
                author = row[7:]
            elif row.startswith("\t"):
                text = row[1:]
                prose = text.strip() and not text.lstrip().startswith("%") and not TABULAR.search(text) \
                    and not LAYOUT.fullmatch(text)
                if prose and (newer is None or sha in newer):
                    print(f"{rel}\t{line_no}\t{sha[:7]}\t{author}\t{text}")


if __name__ == "__main__":
    main()
