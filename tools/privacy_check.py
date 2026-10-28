#!/usr/bin/env python3
"""privacy_check.py — block personal paths and private-repo details from entering this public repo.

Scans only ADDED lines (and commit messages), so existing placeholders such as
`/Users/yourname/...` in upstream docs never trip it.

Two pattern layers:
  1. Generic regexes below — safe to publish (they name no real value).
  2. Private literals — real repo names, directory names, emails. These must NOT be committed,
     or this file becomes the leak. They are read, one per line (case-insensitive, `#` comments), from:
       - `$(git rev-parse --git-path info/private-patterns)`  (local, untracked)
       - the PRIVATE_PATTERNS environment variable           (CI, from a repository secret)

Usage:
  privacy_check.py --staged             # pre-commit: staged diff
  privacy_check.py --message FILE       # commit-msg: the message being written
  privacy_check.py --range BASE HEAD    # CI: diff + commit messages in BASE..HEAD

A line containing `privacy-ok` is exempt (for lines that must name a category, e.g. a banlist).
Exit 1 on any finding.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

GENERIC = [
    (r"/Users/(?!yourname\b|me\b|username\b|<|\$|\{)[A-Za-z0-9._-]+", "absolute macOS home path"),
    (r"(?:~|\$HOME|\$\{HOME\})/Desktop/(?!Auto-claude-code-research-in-sleep\b)", "local ~/Desktop path"),
    (r"job[- ]?search[- ](?:repo|repository)", "private job-search repo reference"),
    (r"求职仓库", "private job-search repo reference"),
]

SELF = {"tools/privacy_check.py"}


def git(*args: str) -> str:
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout


def private_literals() -> list[str]:
    lines: list[str] = []
    try:
        p = Path(git("rev-parse", "--git-path", "info/private-patterns").strip())
        if p.is_file():
            lines += p.read_text(encoding="utf-8").splitlines()
    except subprocess.CalledProcessError:
        pass
    lines += os.environ.get("PRIVATE_PATTERNS", "").splitlines()
    return [l.strip() for l in lines if l.strip() and not l.strip().startswith("#")]


def build_rules() -> list[tuple[re.Pattern, str]]:
    rules = [(re.compile(rx, re.I), why) for rx, why in GENERIC]
    rules += [(re.compile(re.escape(lit), re.I), "private literal") for lit in private_literals()]
    return rules


def added_lines(diff: str):
    """Yield (path, line_no, text) for each added line of a unified diff with -U0."""
    path, line_no = None, 0
    for raw in diff.splitlines():
        if raw.startswith("+++ "):
            path = raw[6:] if raw.startswith("+++ b/") else None
        elif raw.startswith("@@"):
            m = re.search(r"\+(\d+)", raw)
            line_no = int(m.group(1)) if m else 0
        elif raw.startswith("+") and path:
            yield path, line_no, raw[1:]
            line_no += 1


def scan(items, rules) -> list[str]:
    hits = []
    for where, text in items:
        if "privacy-ok" in text:
            continue
        for rx, why in rules:
            if rx.search(text):
                # never echo the matched private value back into CI logs
                hits.append(f"{where}: {why}")
                break
    return hits


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--staged", action="store_true")
    g.add_argument("--message")
    g.add_argument("--range", nargs=2, metavar=("BASE", "HEAD"))
    a = ap.parse_args(argv)
    rules = build_rules()

    items: list[tuple[str, str]] = []
    if a.message:
        msg = Path(a.message).read_text(encoding="utf-8")
        items += [(f"commit message line {i}", l) for i, l in enumerate(msg.splitlines(), 1) if not l.startswith("#")]
    else:
        diff_args = ["diff", "--cached"] if a.staged else ["diff", a.range[0], a.range[1]]
        diff = git(*diff_args, "-U0", "--no-color", "--no-ext-diff")
        items += [(f"{p}:{n}", t) for p, n, t in added_lines(diff) if p not in SELF]
        if a.range:
            for sha in git("rev-list", f"{a.range[0]}..{a.range[1]}").split():
                for i, l in enumerate(git("log", "-1", "--format=%B", sha).splitlines(), 1):
                    items.append((f"commit {sha[:7]} message line {i}", l))

    hits = scan(items, rules)
    if hits:
        print("privacy_check: personal / private-repo details found (this repo is public):", file=sys.stderr)
        for h in hits:
            print(f"  {h}", file=sys.stderr)
        print("Replace with a placeholder (e.g. <OUT>, ~/path/to/...), or mark an intentional line with `privacy-ok`.",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
