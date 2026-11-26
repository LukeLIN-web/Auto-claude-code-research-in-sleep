"""research-review's prompt files carry the shared-references templates unchanged.

The expected text is rebuilt here from the fences by a separate regex, so a
fault in the script's own fence walk does not pass the test.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS = REPO_ROOT / "skills"
SCRIPT = SKILLS / "research-review" / "scripts" / "build_prompts.py"
REFS = SKILLS / "shared-references"

BRIEF = "/review/RESEARCH_REVIEW_REQUEST.md"
INPUT = "Manuscript: /review/main.pdf (the compiled PDF; the whole submission)"
POLICY = "/review/manuscript-craft.md"


def fence_body(name: str, heading: str) -> str:
    text = (REFS / name).read_text(encoding="utf-8")
    match = re.search(re.escape(heading) + r"[^\n]*\n.*?^```[^\n]*\n(.*?)\n^```", text, re.S | re.M)
    assert match, (name, heading)
    return match.group(1)


def fill(template: str) -> str:
    input_field = f"Review brief: {BRIEF}\n{INPUT}"
    for field, value in {
        "[VENUE]": "NeurIPS",
        "[SECTION POLICY]": POLICY,
        "[MANUSCRIPT / PROJECT CONTEXT]": input_field,
        "[PATHS TO MANUSCRIPT FILES]": input_field,
        "[FULL ANONYMOUS MANUSCRIPT — plain text or extracted PDF text]": input_field,
    }.items():
        template = template.replace(field, value)
    return template


def run(script: Path, out: Path, *extra: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(script), "--out", str(out), "--brief", BRIEF, *extra],
        capture_output=True, text=True,
    )


def round1(script: Path, out: Path, *extra: str) -> subprocess.CompletedProcess:
    return run(script, out, "--venue", "NeurIPS", "--input", INPUT, "--section-policy", POLICY, *extra)


def test_round1_prompts_are_the_filled_fences(tmp_path: Path) -> None:
    assert round1(SCRIPT, tmp_path).returncode == 0
    logic = (tmp_path / "logic_prompt.txt").read_text(encoding="utf-8")
    structure = (tmp_path / "structure_prompt.txt").read_text(encoding="utf-8")
    float_map = fence_body("review-float-map.md", "## The block")

    assert logic.startswith(f"Read the review brief at {BRIEF}.\n")
    assert logic.endswith("\n\n" + fill(fence_body("reviewer-personas.md", "## 2. P1")) + "\n")
    assert structure.startswith(f"Read the review brief at {BRIEF}.\n")
    assert structure.endswith(
        "\n\n" + fill(fence_body("reviewer-personas.md", "## 8. P4")) + "\n\n" + float_map + "\n"
    )
    for prompt in (logic, structure):
        assert not re.search(r"\[[A-Z]{2,}[^\]\n]*\]", prompt)


def test_p2_and_logic_only(tmp_path: Path) -> None:
    assert round1(SCRIPT, tmp_path, "--persona", "P2", "--logic-only").returncode == 0
    assert not (tmp_path / "structure_prompt.txt").exists()
    logic = (tmp_path / "logic_prompt.txt").read_text(encoding="utf-8")
    assert logic.endswith("\n\n" + fill(fence_body("reviewer-personas.md", "## 3. P2")) + "\n")


def test_follow_up_round_points_at_the_updated_brief(tmp_path: Path) -> None:
    assert run(SCRIPT, tmp_path, "--round", "2").returncode == 0
    head = f"Read the updated review brief at {BRIEF}.\n"
    assert (tmp_path / "logic_prompt_round2.txt").read_text(encoding="utf-8").startswith(head)
    structure = (tmp_path / "structure_prompt_round2.txt").read_text(encoding="utf-8")
    assert structure.startswith(head)
    assert structure.endswith("\n" + fence_body("review-float-map.md", "## The block") + "\n")


def test_a_field_left_unfilled_stops_the_script(tmp_path: Path) -> None:
    script = tmp_path / "skills" / "research-review" / "scripts" / "build_prompts.py"
    refs = tmp_path / "skills" / "shared-references"
    script.parent.mkdir(parents=True)
    refs.mkdir(parents=True)
    shutil.copy(SCRIPT, script)
    for name in ("reviewer-personas.md", "review-float-map.md", "manuscript-craft.md"):
        shutil.copy(REFS / name, refs / name)
    personas = refs / "reviewer-personas.md"
    text = personas.read_text(encoding="utf-8")
    personas.write_text(text.replace("[VENUE]", "[TARGET VENUE]", 1), encoding="utf-8")

    result = round1(script, tmp_path / "out")
    assert result.returncode != 0
    assert "[TARGET VENUE]" in result.stderr
    assert not (tmp_path / "out" / "logic_prompt.txt").exists()
