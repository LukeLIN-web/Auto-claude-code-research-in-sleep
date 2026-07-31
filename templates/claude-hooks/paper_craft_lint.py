#!/usr/bin/env python3
"""PostToolUse advisory lint: catch the mechanical paper-craft mistakes on write.

Why a hook and not a skill rule: most of the paper-craft corpus is *taste*
(narrative, figure design, review framing) and belongs in
`skills/shared-references/{manuscript-craft,figure-craft}.md`, where a model reads
it while drafting. A small subset is **mechanically checkable and easy to forget
mid-edit** — those are the checks below. They fire on the file the model just
wrote, at the moment the mistake is cheapest to fix, instead of at compile time
three hours later.

SSOT: `skills/shared-references/manuscript-craft.md` §5 and `figure-craft.md` §1-3.
This file is a DERIVED enforcement layer — if a rule changes, change it there
first, then mirror it here. Do not add rules here that are not in those files.

Scope: `.tex` files, and `.py` files that import matplotlib (figure scripts).
Advisory only — the write already happened; exit 2 surfaces the notes to the
model as feedback, it never reverts or blocks anything. Repository docs
(`skills/`, `docs/`, `templates/`) are skipped: they quote these patterns as
examples.

Install: merge templates/claude-hooks/paper_craft_lint.json into
.claude/settings.json (PostToolUse, matcher "Write|Edit|MultiEdit").
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MAX_FINDINGS = 12

# (compiled pattern, message). Patterns are deliberately narrow: a false positive
# costs the model attention on every write, so precision beats recall here.
TEX_RULES = [
    (re.compile(r"[A-Za-z0-9] +\\(?:cite[tp]?|ref|eqref)\{"),
     r"missing '~' before a reference — write Table~\ref{...} / ~\cite{...} so the "
     r"number cannot break onto the next line"),
    (re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{[^}]*\.(?:png|jpe?g|PNG|JPE?G)\}"),
     "raster image included directly — ship vector PDF (compose the raster into a "
     "PDF first if it is truly unavoidable)"),
    (re.compile(r"\b\d+(?:\.\d+)?\s?x[ -](?:faster|slower|speedup|smaller|larger|higher|lower)\b"),
     r"multiplier written as the letter 'x' — use $\times$"),
    (re.compile(r"\\mathcal\{[a-z]"),
     r"\mathcal takes uppercase only — lowercase renders wrong or errors"),
    (re.compile(r"\\textcolor\{(?:red|blue|green|orange|magenta)\}"),
     "co-author color macro still in the source — strip all of these before "
     "submission (arXiv publishes the .tex)"),
    (re.compile(r"^\s*%\s*(?:TODO|FIXME|XXX|HACK)\b", re.MULTILINE),
     "draft note left in the .tex — arXiv publishes the source, including comments"),
]

PY_RULES = [
    (re.compile(r"\b(?:plt\.title|ax\.set_title|axes?\[[^\]]*\]\.set_title)\("),
     "title inside the figure — the title belongs in the LaTeX \\caption{}"),
    (re.compile(r"savefig\([^)]*\.png"),
     "figure saved as PNG — save vector PDF for LaTeX inclusion"),
]


def findings_for(path: Path, text: str) -> list[str]:
    suffix = path.suffix.lower()
    if suffix == ".tex":
        rules = TEX_RULES
    elif suffix == ".py" and ("matplotlib" in text or "pyplot" in text):
        rules = PY_RULES
        # Red+green in one figure script: the most common CVD failure.
        if re.search(r"['\"]red['\"]", text) and re.search(r"['\"]green['\"]", text):
            rules = rules + [(re.compile(r"['\"]red['\"]"),
                              "red and green in the same figure — the most common "
                              "color-vision deficiency cannot separate them")]
    else:
        return []

    out: list[str] = []
    lines = text.splitlines()
    for rx, msg in rules:
        for m in rx.finditer(text):
            line_no = text.count("\n", 0, m.start()) + 1
            snippet = lines[line_no - 1].strip()[:90] if line_no <= len(lines) else ""
            out.append(f"  {path.name}:{line_no}: {msg}\n      | {snippet}")
            break  # one report per rule per file — this is a nudge, not a report card
    return out


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    file_path = (payload.get("tool_input") or {}).get("file_path")
    if not file_path:
        return 0

    path = Path(file_path)
    parts = set(path.parts)
    if parts & {"skills", "docs", "templates", ".git", "node_modules"}:
        return 0  # repo docs quote these patterns as examples

    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return 0

    found = findings_for(path, text)
    if not found:
        return 0

    print("paper-craft lint (advisory — see shared-references/manuscript-craft.md §5, "
          "figure-craft.md §1-3):", file=sys.stderr)
    print("\n".join(found[:MAX_FINDINGS]), file=sys.stderr)
    return 2  # PostToolUse: surface to the model; the write is NOT reverted


if __name__ == "__main__":
    sys.exit(main())
