"""Tests for skills/figure-spec/scripts/verify_figure.py — the deterministic
content-lock diff + print-size gate behind /figure-spec.

Covers both authoring paths: renderer-style output (one <text> per label line)
and hand-authored SVG (one <text> per label, tspans for wrapping).
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "figure-spec" / "scripts" / "verify_figure.py"

spec = importlib.util.spec_from_file_location("verify_figure", SCRIPT)
assert spec is not None and spec.loader is not None
vf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vf)


BLUEPRINT = {
    "figure_id": "fig_test",
    "source": "test",
    "nodes": [
        {"id": "enc", "label_exact": "Audio Encoder"},
        {"id": "dec", "label_exact": "Coarse\nScan"},
    ],
    "edges": [{"from": "enc", "to": "dec", "label_exact": "tokens"}],
    "groups": [{"label_exact": "Stage 1", "node_ids": ["enc", "dec"]}],
    "annotations": ["+9.7 pts"],
    "forbidden_tokens": ["TODO"],
}


def svg(body: str, viewbox: str = "0 0 500 350") -> str:
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}">{body}</svg>'


FULL_BODY = (
    '<text font-size="18">Audio Encoder</text>'
    '<text font-size="18">Coarse</text>'
    '<text font-size="18">Scan</text>'
    '<text font-size="14">tokens</text>'
    '<text font-size="16">Stage 1</text>'
    '<text font-size="16">+9.7 pts</text>'
)


def test_clean_pass_renderer_style():
    report = vf.verify(BLUEPRINT, svg(FULL_BODY), print_width_pt=500, min_pt=8.0)
    assert report["clean"], report
    assert report["size_gate_ran"]


def test_clean_pass_hand_svg_tspan_style():
    body = FULL_BODY.replace(
        '<text font-size="18">Coarse</text><text font-size="18">Scan</text>',
        '<text font-size="18"><tspan>Coarse</tspan> <tspan>Scan</tspan></text>',
    )
    report = vf.verify(BLUEPRINT, svg(body), print_width_pt=500, min_pt=8.0)
    assert report["clean"], report


def test_missing_label_detected():
    body = FULL_BODY.replace('<text font-size="18">Audio Encoder</text>', "")
    report = vf.verify(BLUEPRINT, svg(body), None, 8.0)
    assert report["missing_labels"] == ["Audio Encoder"]
    assert not report["clean"]


def test_partial_multiline_label_is_missing():
    body = FULL_BODY.replace('<text font-size="18">Scan</text>', "")
    report = vf.verify(BLUEPRINT, svg(body), None, 8.0)
    assert "Coarse\nScan" in report["missing_labels"]
    # the surviving "Coarse" line alone is accounted for, not invented
    assert "Coarse" not in report["unaccounted_text"]


def test_invented_text_detected():
    body = FULL_BODY + '<text font-size="18">Bonus Module</text>'
    report = vf.verify(BLUEPRINT, svg(body), None, 8.0)
    assert report["unaccounted_text"] == ["Bonus Module"]
    assert not report["clean"]


def test_forbidden_token_case_insensitive():
    bp = dict(BLUEPRINT, annotations=["+9.7 pts", "todo: tune"])
    body = FULL_BODY + '<text font-size="16">todo: tune</text>'
    report = vf.verify(bp, svg(body), None, 8.0)
    assert report["forbidden_hits"] == [("TODO", "todo: tune")]


def test_size_gate_fails_small_print():
    # 14 units on a 500-unit canvas printed at 245pt -> 6.86pt < 8
    report = vf.verify(BLUEPRINT, svg(FULL_BODY), print_width_pt=245, min_pt=8.0)
    assert report["size_failures"]
    assert not report["clean"]
    printed = dict(report["sizes"])["tokens"]
    assert abs(printed - 14 * 245 / 500) < 1e-9


def test_size_gate_skipped_without_width():
    report = vf.verify(BLUEPRINT, svg(FULL_BODY), print_width_pt=None, min_pt=8.0)
    assert not report["size_gate_ran"]
    assert report["clean"]


def test_pt_unit_font_size_converts():
    body = FULL_BODY.replace(
        '<text font-size="14">tokens</text>',
        '<text font-size="10.5pt">tokens</text>',
    )
    report = vf.verify(BLUEPRINT, svg(body), print_width_pt=500, min_pt=8.0)
    printed = dict(report["sizes"])["tokens"]
    assert abs(printed - 10.5 * (4 / 3) * 500 / 500) < 1e-9


def test_scale_transform_shrinks_text():
    body = FULL_BODY.replace(
        '<text font-size="14">tokens</text>',
        '<g transform="translate(10, 20) scale(0.5)">'
        '<text font-size="14">tokens</text></g>',
    )
    report = vf.verify(BLUEPRINT, svg(body), print_width_pt=500, min_pt=8.0)
    assert ("tokens", 7.0) in report["size_failures"]


def test_skew_transform_is_error():
    body = FULL_BODY.replace(
        '<text font-size="14">tokens</text>',
        '<g transform="skewX(20)"><text font-size="14">tokens</text></g>',
    )
    report = vf.verify(BLUEPRINT, svg(body), None, 8.0)
    assert any("skewX" in err for err in report["errors"])


def test_inherited_and_missing_font_size():
    body = (
        '<g style="font-size: 20px">' + FULL_BODY.replace(' font-size="14"', "", 1)
        + "</g>"
    )
    report = vf.verify(BLUEPRINT, svg(body), print_width_pt=500, min_pt=8.0)
    assert report["clean"], report

    bare = FULL_BODY.replace(' font-size="14"', "", 1)
    report = vf.verify(BLUEPRINT, svg(bare), print_width_pt=500, min_pt=8.0)
    assert any("no resolvable font-size" in err for err in report["errors"])


def test_missing_viewbox_blocks_size_gate():
    raw = svg(FULL_BODY).replace(' viewBox="0 0 500 350"', "")
    report = vf.verify(BLUEPRINT, raw, print_width_pt=500, min_pt=8.0)
    assert any("viewBox" in err for err in report["errors"])
    assert not report["size_gate_ran"]


def test_blueprint_validation_via_file(tmp_path):
    bad = {
        "figure_id": "x",
        "nodes": [{"id": "a", "label_exact": "A"}, {"id": "a", "label_exact": "B"}],
        "edges": [{"from": "a", "to": "ghost"}],
        "surprise_key": 1,
    }
    path = tmp_path / "bad.json"
    path.write_text(json.dumps(bad), encoding="utf-8")
    _, errors = vf.load_blueprint(str(path))
    joined = "\n".join(errors)
    assert "duplicate node id" in joined
    assert "unknown node" in joined
    assert "surprise_key" in joined


def test_cli_end_to_end(tmp_path):
    bp_path = tmp_path / "blueprint.json"
    bp_path.write_text(
        json.dumps(dict(BLUEPRINT, print_width_mm=84)), encoding="utf-8"
    )
    svg_path = tmp_path / "fig.svg"
    svg_path.write_text(svg(FULL_BODY), encoding="utf-8")

    ok = subprocess.run(
        [sys.executable, str(SCRIPT), str(bp_path), "--blueprint-only"],
        capture_output=True, text=True,
    )
    assert ok.returncode == 0, ok.stdout + ok.stderr

    # 84mm print width -> 238pt: 14-unit text prints at 6.7pt -> gate fails
    gated = subprocess.run(
        [sys.executable, str(SCRIPT), str(bp_path), str(svg_path)],
        capture_output=True, text=True,
    )
    assert gated.returncode == 1
    assert "PRINT-SIZE FAILURES" in gated.stdout

    passing = subprocess.run(
        [sys.executable, str(SCRIPT), str(bp_path), str(svg_path),
         "--print-width-pt", "500"],
        capture_output=True, text=True,
    )
    assert passing.returncode == 0, passing.stdout + passing.stderr
    assert "VERDICT: PASS" in passing.stdout
