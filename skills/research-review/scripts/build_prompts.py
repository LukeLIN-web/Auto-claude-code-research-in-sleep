#!/usr/bin/env python3
"""Write research-review's prompt files from the templates in shared-references.

Each template is the body of its fenced block in shared-references, copied byte
for byte; only its bracketed fields are filled, and the script stops if one is
left. The prompts therefore always carry the current templates, never a stale
or paraphrased copy.

Round 1 writes <out>/logic_prompt.txt (the persona) and, unless --logic-only,
<out>/structure_prompt.txt (P4 and the FLOAT AND ARGUMENT MAP block).
--round N (N >= 2) writes <out>/logic_prompt_roundN.txt and
<out>/structure_prompt_roundN.txt: the updated brief, and for the structure
thread the FLOAT AND ARGUMENT MAP block again.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REFS = Path(__file__).resolve().parents[2] / "shared-references"
PERSONAS = {"P1": "## 2. P1", "P2": "## 3. P2"}
INPUT_FIELDS = (
    "[MANUSCRIPT / PROJECT CONTEXT]",
    "[FULL ANONYMOUS MANUSCRIPT — plain text or extracted PDF text]",
    "[PATHS TO MANUSCRIPT FILES]",
)
UNFILLED = re.compile(r"\[[A-Z]{2,}[^\]\n]*\]")

LOGIC_HEAD = (
    "Read the review brief at {brief}.\n"
    "Executor notes are not evidence beyond the files they cite, so verify the\n"
    "referenced artifacts before judging. Trust nothing the author tells you —\n"
    "verify everything yourself.\n\n"
)
STRUCTURE_HEAD = (
    "Read the review brief at {brief}.\n"
    "Trust nothing the author tells you — verify everything yourself.\n\n"
)
FOLLOW_UP_HEAD = (
    "Read the updated review brief at {brief}.\n"
    "Focus on unresolved weaknesses and whether the revision actually fixed them.\n"
)


def fence(name: str, heading: str) -> str:
    """Body of the first fenced block after the line that starts with `heading`."""
    lines = (REFS / name).read_text(encoding="utf-8").split("\n")
    try:
        start = next(i for i, line in enumerate(lines) if line.startswith(heading))
        opening = next(i for i in range(start + 1, len(lines)) if lines[i].startswith("```"))
        closing = next(i for i in range(opening + 1, len(lines)) if lines[i].startswith("```"))
    except StopIteration:
        sys.exit(f"build_prompts: no fenced block under '{heading}' in {REFS / name}")
    return "\n".join(lines[opening + 1:closing])


def fill(text: str, fields: dict[str, str]) -> str:
    for field, value in fields.items():
        text = text.replace(field, value)
    left = sorted(set(UNFILLED.findall(text)))
    if left:
        sys.exit(f"build_prompts: unfilled template fields {left}; shared-references renamed one?")
    return text


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True, type=Path, help="directory the prompt files are written to")
    ap.add_argument("--brief", required=True, help="absolute path of this round's review brief")
    ap.add_argument("--venue", help="fills [VENUE]; required in round 1")
    ap.add_argument("--input", action="append", default=[],
                    help="a line after 'Review brief: <brief>' in the template's input field, "
                         "e.g. 'Manuscript: <abs path> (the compiled PDF; the whole submission)'; repeatable")
    ap.add_argument("--persona", choices=sorted(PERSONAS), default="P1", help="logic thread persona")
    ap.add_argument("--section-policy", default=str(REFS / "manuscript-craft.md"),
                    help="fills P4's [SECTION POLICY]; default: shared-references/manuscript-craft.md")
    ap.add_argument("--logic-only", action="store_true", help="an idea or project: no structure thread")
    ap.add_argument("--round", type=int, default=1, help="2 or more writes the follow-up prompts")
    args = ap.parse_args()

    threads = ["logic"] if args.logic_only else ["logic", "structure"]
    float_map = fence("review-float-map.md", "## The block")
    if args.round > 1:
        head = FOLLOW_UP_HEAD.format(brief=args.brief)
        prompts = {"logic": head, "structure": head + "\n" + float_map + "\n"}
        names = {t: f"{t}_prompt_round{args.round}.txt" for t in threads}
    else:
        if not args.venue:
            ap.error("--venue is required in round 1")
        fields = {
            "[VENUE]": args.venue,
            "[SECTION POLICY]": args.section_policy,
            **{f: "\n".join([f"Review brief: {args.brief}", *args.input]) for f in INPUT_FIELDS},
        }
        persona = fence("reviewer-personas.md", PERSONAS[args.persona])
        structure = fence("reviewer-personas.md", "## 8. P4")
        prompts = {
            "logic": LOGIC_HEAD.format(brief=args.brief) + fill(persona, fields) + "\n",
            "structure": STRUCTURE_HEAD.format(brief=args.brief) + fill(structure, fields)
            + "\n\n" + float_map + "\n",
        }
        names = {t: f"{t}_prompt.txt" for t in threads}

    args.out.mkdir(parents=True, exist_ok=True)
    for thread in threads:
        path = args.out / names[thread]
        path.write_text(prompts[thread], encoding="utf-8")
        print(f"{path}  {path.stat().st_size} B")


if __name__ == "__main__":
    main()
