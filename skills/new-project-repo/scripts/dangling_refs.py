#!/usr/bin/env python3
"""List file names that a repo's rule files mention but the repo does not contain.

    python3 dangling_refs.py <repo> [rule-file-name ...]

Rule files default to CLAUDE.md, AGENTS.md and CONTRIBUTING.md at any depth. A mention is a
backticked token ending in a file extension; it resolves when a tracked file has that basename.
"""
import re
import subprocess
import sys
from pathlib import Path

MENTION = re.compile(r"`([^`\s]+\.(?:md|py|sh|ya?ml|json|toml|tex|bib))`")
PLACEHOLDER = re.compile(r"[<>*{}$]")


def main() -> int:
    repo = Path(sys.argv[1])
    names = set(sys.argv[2:]) or {"CLAUDE.md", "AGENTS.md", "CONTRIBUTING.md"}
    tracked = subprocess.run(["git", "-C", str(repo), "ls-files"], capture_output=True, text=True, check=True).stdout.split("\n")
    have = {Path(p).name for p in tracked if p}
    missing = 0
    for path in sorted(p for p in tracked if Path(p).name in names):
        text = (repo / path).read_text()
        gone = sorted({Path(m).name for m in MENTION.findall(text) if not PLACEHOLDER.search(m)} - have)
        if gone:
            missing += len(gone)
            print(f"{path}: {' '.join(gone)}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
