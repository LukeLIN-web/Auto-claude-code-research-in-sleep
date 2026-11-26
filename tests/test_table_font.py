"""Tests for skills/paper-table-craft/scripts/check_table_font.py — the printed
type-size gate for tables (floor 7.5 pt) behind /paper-table-craft step 5.

The PDFs are drawn with pymupdf: a caption block, booktabs-like horizontal
rules sharing their ends, and cell text at known sizes.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

pymupdf = pytest.importorskip("pymupdf")

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "paper-table-craft" / "scripts" / "check_table_font.py"


def table(page, top, caption, size, rows=("Method 71.4 58.2", "Baseline 60.1 55.0"), x0=72, x1=300):
    """A caption above three rules, with one header and `rows` set at `size` pt."""
    page.insert_text((x0, top), caption, fontsize=9)
    y = top + 14
    for ry in (y, y + 14, y + 14 + 14 * len(rows) + 4):
        page.draw_line((x0, ry), (x1, ry), width=0.6)
    page.insert_text((x0 + 4, y + 10), "System Bench-A Bench-B", fontsize=size)
    for i, row in enumerate(rows):
        page.insert_text((x0 + 4, y + 26 + 14 * i), row, fontsize=size)
    return y + 14 + 14 * len(rows) + 4


def run(pdf, *args):
    return subprocess.run([sys.executable, str(SCRIPT), str(pdf), *args],
                          capture_output=True, text=True, check=False)


@pytest.fixture
def paper(tmp_path):
    doc = pymupdf.open()
    page = doc.new_page(width=612, height=792)
    bottom = table(page, 80, "Table 1. Ours leads on both benchmarks.", 8)
    # a raised superscript after a cell: excluded as a script
    page.insert_text((150, bottom - 8), "2", fontsize=5.5)
    page.insert_text((72, bottom + 40), "Body prose that cites Table 2 in passing.", fontsize=10)
    table(page, bottom + 90, "Table 2. A table set too small.", 6)
    pdf = tmp_path / "main.pdf"
    doc.save(pdf)
    (tmp_path / "main.aux").write_text(
        "\\newlabel{tab:main}{{1}{1}{Ours leads}{table.caption.1}{}}\n"
        "\\newlabel{tab:small}{{2}{1}{A table}{table.caption.2}{}}\n"
    )
    return pdf


def test_every_table_measured_and_small_one_flagged(paper):
    r = run(paper)
    assert r.returncode == 1, r.stdout
    lines = r.stdout.splitlines()
    assert lines[0].startswith("Table 1") and "body  8.0 pt  min  8.0 pt" in lines[0]
    assert lines[0].endswith("8.0 pt"), "the 5.5 pt superscript must not set the minimum"
    assert lines[1].startswith("Table 2") and "UNDER 7.5 pt" in lines[1]
    assert lines[2].startswith("body sizes differ")


def test_select_by_label_through_aux(paper):
    r = run(paper, "--table", "tab:main")
    assert r.returncode == 0, r.stdout
    assert r.stdout.splitlines() == [next(l for l in run(paper).stdout.splitlines() if l.startswith("Table 1"))]


def test_select_by_printed_number_and_floor(paper):
    assert run(paper, "--table", "2").returncode == 1
    assert run(paper, "--table", "2", "--floor", "5.5").returncode == 0


def test_missing_table_and_unknown_label_fail(paper):
    r = run(paper, "--table", "7")
    assert r.returncode == 1 and "Table 7: caption not found" in r.stdout
    r = run(paper, "--table", "tab:nope")
    assert r.returncode == 1 and "no such \\label" in (r.stdout + r.stderr)


def test_table_without_rules_is_not_measured(tmp_path):
    doc = pymupdf.open()
    page = doc.new_page(width=612, height=792)
    page.insert_text((72, 80), "Table 1. No rules at all.", fontsize=9)
    page.insert_text((76, 100), "System Bench-A", fontsize=8)
    pdf = tmp_path / "bare.pdf"
    doc.save(pdf)
    r = run(pdf)
    assert r.returncode == 1 and "not measured" in r.stdout
