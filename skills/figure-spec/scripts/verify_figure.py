#!/usr/bin/env python3
"""verify_figure.py — deterministic content + print-size verification for /figure-spec.

Checks a rendered SVG figure against a blueprint.json content lock:

  1. CONTENT  — every locked label appears in the SVG (as one <text> element,
     or as consecutive per-line <text> elements the renderer emits for
     multi-line labels); every SVG text run is accounted for by some locked
     label (no invented text); no forbidden token appears.
  2. PRINT SIZE — given the intended print width, every text element renders
     at >= --min-pt on the printed page (the mechanical form of the scale rule
     in shared-references/figure-craft.md §1).

The blueprint is the vector-route adaptation of ARIS-Movie-Director
/method-figure's content lock: because SVG text is machine-readable, the
cross-model blind-transcribe panel is replaced by this deterministic diff.
Topology (which arrow connects what) is NOT machine-verified for hand-authored
SVG — that stays with the visual review step.

Usage:
  verify_figure.py <blueprint.json> <figure.svg> [--print-width-mm N |
      --print-width-in N | --print-width-pt N] [--min-pt 8.0]
  verify_figure.py <blueprint.json> --blueprint-only

Exit codes: 0 clean · 1 findings · 2 usage/parse error.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import xml.etree.ElementTree as ET

MM_PER_INCH = 25.4
PT_PER_INCH = 72.0
# CSS: 1pt = 4/3 px (SVG user units at 96 dpi)
UNITS_PER_PT = 4.0 / 3.0

BLUEPRINT_KEYS = {
    "figure_id", "source", "nodes", "edges", "groups", "annotations",
    "forbidden_tokens", "print_width_mm",
}


def normalize(text: str) -> str:
    """Collapse all whitespace (incl. newlines) to single spaces and strip."""
    return re.sub(r"\s+", " ", text).strip()


def label_forms(label: str) -> tuple[str, list[str]]:
    """A locked label's whole normalized form and its per-line forms.

    Accepts literal two-character "\\n" as a line break (the FigureSpec
    renderer convention) as well as a real newline.
    """
    raw = label.replace("\\n", "\n")
    lines = [normalize(line) for line in raw.split("\n") if normalize(line)]
    return normalize(raw), lines


# ------------------------------------------------------------
# Blueprint
# ------------------------------------------------------------

def load_blueprint(path: str) -> tuple[dict, list[str]]:
    """Load and structurally validate a blueprint. Returns (blueprint, errors)."""
    errors: list[str] = []
    try:
        with open(path, encoding="utf-8") as fh:
            bp = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"blueprint unreadable: {exc}"]
    if not isinstance(bp, dict):
        return {}, ["blueprint root must be a JSON object"]

    for key in bp:
        if key not in BLUEPRINT_KEYS:
            errors.append(f"unknown blueprint key: {key!r}")

    node_ids: set[str] = set()
    for i, node in enumerate(bp.get("nodes", [])):
        nid = node.get("id")
        if not nid or not isinstance(nid, str):
            errors.append(f"nodes[{i}] missing string id")
            continue
        if nid in node_ids:
            errors.append(f"duplicate node id: {nid!r}")
        node_ids.add(nid)
        if not normalize(str(node.get("label_exact", ""))):
            errors.append(f"node {nid!r} missing label_exact")

    for i, edge in enumerate(bp.get("edges", [])):
        for end in ("from", "to"):
            ref = edge.get(end)
            if ref not in node_ids:
                errors.append(f"edges[{i}].{end} references unknown node: {ref!r}")

    for i, group in enumerate(bp.get("groups", [])):
        if not normalize(str(group.get("label_exact", ""))):
            errors.append(f"groups[{i}] missing label_exact")
        for ref in group.get("node_ids", []):
            if ref not in node_ids:
                errors.append(f"groups[{i}].node_ids references unknown node: {ref!r}")

    for i, ann in enumerate(bp.get("annotations", [])):
        if not isinstance(ann, str) or not normalize(ann):
            errors.append(f"annotations[{i}] must be a non-empty string")

    if not node_ids:
        errors.append("blueprint has no nodes — nothing is locked")
    return bp, errors


def locked_labels(bp: dict) -> list[str]:
    """All exact strings the figure is allowed (and required) to show."""
    labels: list[str] = []
    for node in bp.get("nodes", []):
        if node.get("label_exact"):
            labels.append(str(node["label_exact"]))
        if node.get("sublabel_exact"):
            labels.append(str(node["sublabel_exact"]))
    for edge in bp.get("edges", []):
        if edge.get("label_exact"):
            labels.append(str(edge["label_exact"]))
    for group in bp.get("groups", []):
        if group.get("label_exact"):
            labels.append(str(group["label_exact"]))
    labels.extend(str(a) for a in bp.get("annotations", []))
    return labels


# ------------------------------------------------------------
# SVG parsing
# ------------------------------------------------------------

def localname(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def parse_font_size(el: ET.Element) -> tuple[float | None, str | None]:
    """Explicit font-size on this element, in SVG user units.

    Returns (units, error). (None, None) means no explicit size here.
    """
    value = el.get("font-size")
    if value is None:
        style = el.get("style", "")
        match = re.search(r"font-size\s*:\s*([^;]+)", style)
        if match:
            value = match.group(1)
    if value is None:
        return None, None
    value = value.strip()
    match = re.fullmatch(r"([0-9.]+)\s*([a-z%]*)", value)
    if not match:
        return None, f"unparsable font-size: {value!r}"
    number = float(match.group(1))
    unit = match.group(2)
    if unit in ("", "px"):
        return number, None
    if unit == "pt":
        return number * UNITS_PER_PT, None
    return None, f"font-size unit {unit!r} not resolvable (use px, pt, or unitless)"


def parse_transform_scale(transform: str) -> tuple[float | None, str | None]:
    """Conservative (min-axis) scale factor of a transform attribute.

    translate/rotate preserve glyph size; scale/matrix are handled; skew makes
    glyph size ill-defined and returns an error.
    """
    scale = 1.0
    for name, args in re.findall(r"([a-zA-Z]+)\s*\(([^)]*)\)", transform):
        values = [float(v) for v in re.split(r"[\s,]+", args.strip()) if v]
        if name in ("translate", "rotate"):
            continue
        if name == "scale":
            sx = abs(values[0])
            sy = abs(values[1]) if len(values) > 1 else sx
            scale *= min(sx, sy)
        elif name == "matrix" and len(values) == 6:
            a, b, c, d = values[:4]
            scale *= min(math.hypot(a, b), math.hypot(c, d))
        else:
            return None, f"transform {name!r} not resolvable for text size"
    return scale, None


def collect_texts(root: ET.Element) -> tuple[list[dict], list[str]]:
    """All <text> runs with normalized content and effective font size (units).

    Effective size = min over the element and any tspan that overrides it,
    multiplied by the cumulative ancestor scale. Errors are unresolvable sizes.
    """
    texts: list[dict] = []
    errors: list[str] = []

    def walk(el: ET.Element, inherited: float | None, scale: float) -> None:
        size, err = parse_font_size(el)
        if err:
            errors.append(f"<{localname(el.tag)}>: {err}")
        own = size if size is not None else inherited
        tf_scale, tf_err = parse_transform_scale(el.get("transform", ""))
        if tf_err:
            errors.append(f"<{localname(el.tag)}>: {tf_err}")
            tf_scale = 1.0
        scale = scale * tf_scale

        if localname(el.tag) == "text":
            content = normalize("".join(el.itertext()))
            if content:
                sizes = [own] if own is not None else []
                for tspan in el.iter():
                    if localname(tspan.tag) == "tspan":
                        ts, ts_err = parse_font_size(tspan)
                        if ts_err:
                            errors.append(f"<tspan> in {content[:30]!r}: {ts_err}")
                        if ts is not None:
                            sizes.append(ts)
                if not sizes:
                    errors.append(
                        f"text {content[:40]!r} has no resolvable font-size "
                        f"(set it explicitly on the element or an ancestor)"
                    )
                    texts.append({"content": content, "units": None, "scale": scale})
                else:
                    texts.append(
                        {"content": content, "units": min(sizes), "scale": scale}
                    )
            return

        for child in el:
            walk(child, own, scale)

    walk(root, None, 1.0)
    return texts, errors


def viewbox_width(root: ET.Element) -> float | None:
    viewbox = root.get("viewBox")
    if not viewbox:
        return None
    parts = [p for p in re.split(r"[\s,]+", viewbox.strip()) if p]
    if len(parts) != 4:
        return None
    return float(parts[2])


# ------------------------------------------------------------
# Verification
# ------------------------------------------------------------

def verify(
    bp: dict,
    svg_text: str,
    print_width_pt: float | None,
    min_pt: float,
) -> dict:
    """Run all checks. Returns a report dict; report['clean'] is the verdict."""
    report: dict = {
        "errors": [],
        "missing_labels": [],
        "unaccounted_text": [],
        "forbidden_hits": [],
        "size_failures": [],
        "sizes": [],           # (content, printed_pt) for every text, when gated
        "size_gate_ran": False,
    }

    try:
        root = ET.fromstring(svg_text)
    except ET.ParseError as exc:
        report["errors"].append(f"SVG unparsable: {exc}")
        report["clean"] = False
        return report

    texts, text_errors = collect_texts(root)
    report["errors"].extend(text_errors)
    svg_contents = [t["content"] for t in texts]
    svg_set = set(svg_contents)

    # --- CONTENT: locked labels present ---
    wholes: set[str] = set()
    all_lines: set[str] = set()
    for label in locked_labels(bp):
        whole, lines = label_forms(label)
        wholes.add(whole)
        all_lines.update(lines)
        if whole not in svg_set and not all(line in svg_set for line in lines):
            report["missing_labels"].append(label)

    # --- CONTENT: no invented text ---
    for content in svg_contents:
        if content not in wholes and content not in all_lines:
            report["unaccounted_text"].append(content)

    # --- CONTENT: forbidden tokens ---
    for token in bp.get("forbidden_tokens", []):
        needle = str(token).casefold()
        for content in svg_contents:
            if needle and needle in content.casefold():
                report["forbidden_hits"].append((token, content))

    # --- PRINT SIZE ---
    if print_width_pt is not None:
        vb_width = viewbox_width(root)
        if vb_width is None or vb_width <= 0:
            report["errors"].append(
                "SVG has no usable viewBox — print-size gate impossible "
                "(add viewBox=\"0 0 W H\" to the root <svg>)"
            )
        else:
            report["size_gate_ran"] = True
            for t in texts:
                if t["units"] is None:
                    continue  # already an error above
                printed = t["units"] * t["scale"] * print_width_pt / vb_width
                report["sizes"].append((t["content"], printed))
                if printed < min_pt:
                    report["size_failures"].append((t["content"], printed))

    report["clean"] = not (
        report["errors"]
        or report["missing_labels"]
        or report["unaccounted_text"]
        or report["forbidden_hits"]
        or report["size_failures"]
    )
    return report


def print_report(report: dict, min_pt: float) -> None:
    def section(title: str, rows: list) -> None:
        print(f"\n{title} ({len(rows)})")
        for row in rows:
            print(f"  - {row}")

    if report["errors"]:
        section("ERRORS", report["errors"])
    if report["missing_labels"]:
        section("MISSING LOCKED LABELS", report["missing_labels"])
    if report["unaccounted_text"]:
        section(
            "UNACCOUNTED SVG TEXT (not in the blueprint — add it there or delete it)",
            report["unaccounted_text"],
        )
    if report["forbidden_hits"]:
        section(
            "FORBIDDEN TOKENS",
            [f"{tok!r} in {content!r}" for tok, content in report["forbidden_hits"]],
        )
    if report["size_gate_ran"]:
        smallest = sorted(report["sizes"], key=lambda r: r[1])[:5]
        section(
            f"SMALLEST PRINTED TEXT (gate: >= {min_pt} pt)",
            [f"{pt:5.2f} pt  {content[:60]!r}" for content, pt in smallest],
        )
        if report["size_failures"]:
            section(
                "PRINT-SIZE FAILURES",
                [f"{pt:5.2f} pt  {content[:60]!r}"
                 for content, pt in report["size_failures"]],
            )
    else:
        print("\nprint-size gate SKIPPED — no print width given "
              "(blueprint print_width_mm or --print-width-*)")

    print("\nVERDICT:", "PASS" if report["clean"] else "FAIL")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("blueprint")
    parser.add_argument("svg", nargs="?")
    parser.add_argument("--blueprint-only", action="store_true",
                        help="validate the blueprint structure and stop")
    parser.add_argument("--print-width-mm", type=float)
    parser.add_argument("--print-width-in", type=float)
    parser.add_argument("--print-width-pt", type=float)
    parser.add_argument("--min-pt", type=float, default=8.0,
                        help="hard floor for printed glyph size (default 8.0; "
                             "figure-craft.md's full rule is >= body text — "
                             "raise to your venue's body size to enforce it)")
    args = parser.parse_args(argv)

    bp, bp_errors = load_blueprint(args.blueprint)
    if bp_errors:
        for err in bp_errors:
            print(f"BLUEPRINT ERROR: {err}")
        return 2
    if args.blueprint_only:
        labels = locked_labels(bp)
        print(f"blueprint OK: {len(bp.get('nodes', []))} nodes, "
              f"{len(bp.get('edges', []))} edges, {len(labels)} locked strings")
        return 0
    if not args.svg:
        print("ERROR: an SVG path is required unless --blueprint-only", file=sys.stderr)
        return 2

    print_width_pt = None
    if args.print_width_pt is not None:
        print_width_pt = args.print_width_pt
    elif args.print_width_in is not None:
        print_width_pt = args.print_width_in * PT_PER_INCH
    elif args.print_width_mm is not None:
        print_width_pt = args.print_width_mm / MM_PER_INCH * PT_PER_INCH
    elif bp.get("print_width_mm"):
        print_width_pt = float(bp["print_width_mm"]) / MM_PER_INCH * PT_PER_INCH

    try:
        with open(args.svg, encoding="utf-8") as fh:
            svg_text = fh.read()
    except OSError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    report = verify(bp, svg_text, print_width_pt, args.min_pt)
    print_report(report, args.min_pt)
    return 0 if report["clean"] else 1


if __name__ == "__main__":
    sys.exit(main())
