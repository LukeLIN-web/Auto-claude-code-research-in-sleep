---
name: figure-spec
description: "Generate publication-quality method / architecture / workflow / pipeline figures as editable vector SVG under a blueprint content lock: every label is frozen upfront, the rendered SVG is hard-diffed against the lock, and a print-size gate enforces readable type at the final printed width. Two render paths: deterministic JSON (FigureSpec) → SVG renderer for quick figures, or hand-authored SVG for Figure-1-grade layouts. Use when user says \"方法图\", \"架构图\", \"method figure\", \"Figure 1\", \"workflow 图\", \"pipeline 图\", \"确定性矢量图\", \"figure spec\", \"draw architecture\". Preferred over AI illustration for formal method/architecture figures."
argument-hint: "[description-of-diagram]"
allowed-tools: Bash(*), Read, Write, Edit, mcp__codex__codex
---

# FigureSpec: Blueprint-Locked Vector Figures

Generate publication-quality **method / Figure-1 overviews**, **architecture diagrams**, **workflow pipelines**, **audit cascades**, and **system topology** figures as editable SVG vector graphics — under a **content lock**: the figure's text is frozen in a `blueprint.json` before any drawing, the rendered SVG is hard-diffed against it, and a print-size gate rejects type that would print below readable size.

The content-lock discipline is adapted from ARIS-Movie-Director's [`/method-figure`](https://github.com/wanshuiyin/ARIS-Movie-Director/blob/main/skills/method-figure/SKILL.md) (blueprint → render → blind-transcribe panel → hard diff). The vector route keeps the blueprint and the hard diff but needs **no cross-model transcription panel**: SVG text is machine-readable, so a deterministic script replaces the two-reviewer blind transcription, and the aesthetic freedom lost by not using an image model is regained by the hand-authored SVG path.

## When to Use This Skill

**Use `figure-spec`** for:
- Paper method / Figure-1 overview figures (the figure reviewers judge first)
- System architecture diagrams (layered, hub-and-spoke, multi-plane)
- Workflow / pipeline figures
- Audit cascade / flow-control diagrams
- Any structured diagram where node positions, connections, and groupings are semantically important
- Figures that need to be edited/tweaked later (SVG is plain text)
- Figures where determinism matters (same spec → same SVG)

**Two render paths, one contract** — both start from the same blueprint and must pass the same verifier:
- **Path A — FigureSpec renderer**: JSON spec → deterministic SVG. Fast, layout handled for you, plain aesthetics. Default for internal/report figures and first drafts.
- **Path B — hand-authored SVG**: the agent writes the SVG directly. Full typographic and layout control — use for the paper's Figure 1, where Path A's flat boxes undersell the work. A Path A render makes a good starting scaffold.

**Do NOT use for:**
- Data plots (bar/line/scatter) — use `/paper-figure`
- Natural/qualitative illustrations (photos, generated samples) — use `/paper-illustration`
- Quick state-machine / flowchart — use `/mermaid-diagram` (lighter syntax)

## The Content Lock (blueprint.json)

Before any layout or drawing, freeze WHAT the figure says:

```json
{
  "figure_id": "fig_method",
  "source": "paper/method.tex §3 — where every label/number below comes from",
  "print_width_mm": 84,
  "nodes": [
    {"id": "enc", "label_exact": "Audio Encoder", "sublabel_exact": "frozen"},
    {"id": "scan", "label_exact": "Coarse\nScan"}
  ],
  "edges": [{"from": "enc", "to": "scan", "label_exact": "tokens"}],
  "groups": [{"label_exact": "Stage 1", "node_ids": ["enc", "scan"]}],
  "annotations": ["+9.7 pts on OVB"],
  "forbidden_tokens": ["TODO", "lorem"]
}
```

Rules (fail-closed, from `/method-figure`):
- **Every string the figure will show is locked here** — node labels, edge labels, group titles, legends, headline claims and numbers (as `annotations`). The verifier rejects any rendered text that is not in the blueprint, so there is no "harmless extra caption" escape hatch.
- **Never invent** a node, claim, or number while drawing. If the method source doesn't state it, escalate to the user — don't make it up.
- `source` records where the content came from (traceability); `print_width_mm` records the intended `\includegraphics` width and drives the print-size gate — one declaration, used by both the gate and the LaTeX include.
- What the deterministic verifier **cannot** check for hand-authored SVG: edge topology (which arrow connects what). That is exactly what the visual review step is scoped to.

## Core Properties

- **Content-locked**: every rendered string is hard-diffed against `blueprint.json` — a one-character drift fails the figure (both paths)
- **Print-size gated**: glyph sizes are checked at the declared `\includegraphics` width, mechanizing `figure-craft.md`'s scale rule
- **Deterministic** (Path A): identical FigureSpec JSON always produces identical SVG output (for a fixed renderer version + fonts)
- **Editable**: SVG output is plain-text, can be post-edited by hand or programmatically
- **Validated**: renderer enforces schema, rejects malformed specs with clear error messages
- **Shape-aware**: edge clipping works correctly for rect/rounded/circle/ellipse/diamond
- **CJK support**: multi-line labels with proper Chinese character width estimation
- **No external API**: runs fully local, no network, no API keys

## Tool Location

Phase 3.1 (Arch C) move: the canonical implementation now lives at
`skills/figure-spec/scripts/figure_renderer.py` (this SKILL's own
`scripts/` subdirectory). A backwards-compatible shim at
`tools/figure_renderer.py` forwards to the canonical file via
`os.execv`, so existing users with `.aris/tools/figure_renderer.py`
or a manually copied `tools/figure_renderer.py` keep working
unchanged.

Resolve `$FIGURE_RENDERER` with the hybrid chain (layer 0 prefers the
self-contained location for the owning SKILL; layers 1-4 are the
shared-runtime chain documented in
[`shared-references/integration-contract.md`](../shared-references/integration-contract.md) §2,
Policy A — skill-local gate):

```bash
# Layer 0: self-contained (CC 1.0+ exposes $CLAUDE_SKILL_DIR).
FIGURE_RENDERER=""
if [ -n "${CLAUDE_SKILL_DIR:-}" ] && [ -f "$CLAUDE_SKILL_DIR/scripts/figure_renderer.py" ]; then
  FIGURE_RENDERER="$CLAUDE_SKILL_DIR/scripts/figure_renderer.py"
fi
# Layers 1-4: shared-runtime chain (legacy compatibility + non-CC hosts).
if [ -z "$FIGURE_RENDERER" ]; then
  cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)" || exit 1
  if [ -z "${ARIS_REPO:-}" ] && [ -f .aris/installed-skills.txt ]; then
      ARIS_REPO=$(awk -F'\t' '$1=="repo_root"{print $2; exit}' .aris/installed-skills.txt 2>/dev/null) || true
  fi
  if [ -z "${ARIS_REPO:-}" ] && [ -f "$HOME/.aris/repo" ]; then
      ARIS_REPO=$(cat "$HOME/.aris/repo" 2>/dev/null) || true
  fi
  FIGURE_RENDERER=".aris/tools/figure_renderer.py"
  [ -f "$FIGURE_RENDERER" ] || FIGURE_RENDERER="tools/figure_renderer.py"
  [ -f "$FIGURE_RENDERER" ] || { [ -n "${ARIS_REPO:-}" ] && FIGURE_RENDERER="$ARIS_REPO/tools/figure_renderer.py"; }
  [ -f "$FIGURE_RENDERER" ] || FIGURE_RENDERER=""
fi
[ -z "$FIGURE_RENDERER" ] && {
  echo "ERROR: figure_renderer.py not resolved (layer 0: \$CLAUDE_SKILL_DIR/scripts/; layers 1-4: .aris/tools/, tools/, \$ARIS_REPO/tools/, \$ARIS_REPO/tools/ via ~/.aris/repo)." >&2
  echo "       /figure-spec cannot produce SVG output. Fix: rerun bash tools/install_aris.sh or smart_update.sh (refreshes ~/.aris/repo), or copy the helper from \$ARIS_REPO/skills/figure-spec/scripts/." >&2
  exit 1
}
```

The deterministic verifier `verify_figure.py` ships in the same `scripts/`
directory. After resolving `$FIGURE_RENDERER`:

```bash
FIGURE_VERIFIER="$(dirname "$FIGURE_RENDERER")/verify_figure.py"
# legacy layers resolve the renderer via the tools/ shim, which has no verifier next to it:
[ -f "$FIGURE_VERIFIER" ] || FIGURE_VERIFIER="${ARIS_REPO:-.}/skills/figure-spec/scripts/verify_figure.py"
[ -f "$FIGURE_VERIFIER" ] || { echo "ERROR: verify_figure.py not found next to the renderer nor under \$ARIS_REPO/skills/figure-spec/scripts/ — rerun the install script to pick it up." >&2; exit 1; }
```

Invoke:

```bash
python3 "$FIGURE_RENDERER" render <spec.json> --output <out.svg>
python3 "$FIGURE_RENDERER" validate <spec.json>
python3 "$FIGURE_RENDERER" schema
python3 "$FIGURE_VERIFIER" <blueprint.json> <fig.svg>          # content diff + size gate
python3 "$FIGURE_VERIFIER" <blueprint.json> --blueprint-only   # lint the lock itself
```

## Workflow

### Step 1: Understand the Goal, Then Freeze the Blueprint

From `$ARGUMENTS` (description or path to `PAPER_PLAN.md` / `NARRATIVE_REPORT.md` / the paper's method section), identify:
- **Purpose**: method overview, architecture, workflow, pipeline, audit cascade, topology?
- **Main entities**: what are the boxes?
- **Relationships**: how do they connect? (uses, produces, calls, verifies, chains)
- **Grouping**: do entities cluster into named regions?
- **Hierarchy vs network**: stacked layers, left-to-right flow, or central hub?

Write these down as `figures/specs/<id>_blueprint.json` (schema in "The Content
Lock" above) — labels verbatim from the source, claims/numbers only if the
source states them — and lint it:

```bash
python3 "$FIGURE_VERIFIER" figures/specs/<id>_blueprint.json --blueprint-only
```

For a paper's Figure 1, show the blueprint to the user before drawing anything.
Content changes after this point mean editing the blueprint and re-verifying —
never silently diverging from it in the drawing.

### Step 2, Path A: Draft the FigureSpec JSON

Copy every label **verbatim** from the blueprint into the spec (the Step 4
verifier catches any divergence, including a one-character typo).

Canvas sizing guide:
- Single-column figure: ~500×350 px
- Two-column (full-width): ~900×500 px
- Tall topology: ~700×700 px

Start from a template based on the diagram type:

**Architecture (stacked rows)**:
```json
{
  "canvas": {"width": 900, "height": 520},
  "nodes": [
    {"id": "layer1_label", "label": "Layer 1", "x": 450, "y": 60, ...},
    {"id": "node_a", "label": "A", "x": 180, "y": 120, ...},
    {"id": "node_b", "label": "B", "x": 350, "y": 120, ...}
  ],
  "edges": [...],
  "groups": [
    {"label": "Layer 1", "node_ids": ["node_a", "node_b"], "fill": "#F0F9FF", "stroke": "#BAE6FD"}
  ]
}
```

**Workflow (left-to-right chain)**:
```json
{
  "canvas": {"width": 900, "height": 300},
  "nodes": [
    {"id": "step1", "label": "Step 1", "x": 100, "y": 150, "shape": "rounded"},
    {"id": "step2", "label": "Step 2", "x": 280, "y": 150, "shape": "rounded"}
  ],
  "edges": [
    {"from": "step1", "to": "step2", "label": "produces"}
  ]
}
```

**Decision diamond**:
```json
{"id": "check", "label": "Passes?", "shape": "diamond", "x": 450, "y": 200}
```

### Step 2, Path B: Hand-Author the SVG (Figure-1 grade)

Write the SVG directly (optionally starting from a Path A render as scaffold).
Full freedom on gradients, rounded cards, icons, typography — the craft rules
in [`../shared-references/figure-craft.md`](../shared-references/figure-craft.md)
(pale fills, no red+green, subtle consistent shadows, fewer words) apply. Four
mechanical rules keep the SVG verifiable:

1. **One locked label = one `<text>` element** — use `<tspan>` for line
   wrapping, never split one label across two `<text>` elements. (Multi-line
   labels may alternatively be one `<text>` per line, matching Path A's
   renderer output — the verifier accepts both.)
2. **Explicit `font-size`** on every text element or an ancestor (`px`, `pt`,
   or unitless; no `em`/`%`).
3. **No skew transforms on text**; `scale()` is allowed and is factored into
   the size gate.
4. **Root `<svg>` must carry a `viewBox`** — the print-size gate maps viewBox
   units to the printed width declared in the blueprint.

White background, no dark theme for a paper/README figure.

### Step 3: Render and Validate (Path A; Path B goes straight to Step 4)

```bash
# Validate first ($FIGURE_RENDERER was resolved in "Tool Location" above)
python3 "$FIGURE_RENDERER" validate /tmp/spec.json

# Render to SVG
python3 "$FIGURE_RENDERER" render /tmp/spec.json --output figures/fig_arch.svg
```

If validation fails, inspect the error (missing field, duplicate ID, overlap warning, invalid hex color) and fix the JSON.

### Step 4: Deterministic Verify (both paths — the figure is not done until this passes)

```bash
python3 "$FIGURE_VERIFIER" figures/specs/<id>_blueprint.json figures/fig_arch.svg
```

This replaces `/method-figure`'s cross-model blind-transcribe panel with a
deterministic diff, and enforces `figure-craft.md`'s scale rule mechanically:

- **Content diff** — every locked label present (typo = fail), every rendered
  text accounted for (invented text = fail), no forbidden token.
- **Print-size gate** — using the blueprint's `print_width_mm` (override with
  `--print-width-mm/-in/-pt`), every glyph must print at ≥ `--min-pt`
  (default 8.0 — a hard floor below typical caption size; the full craft rule
  is ≥ body text, so pass `--min-pt 9` or `10` to enforce it for your venue).

Fix the **source** (spec JSON or SVG), never bypass the verifier. Re-run until
`VERDICT: PASS`. Then convert for LaTeX:

```bash
rsvg-convert -f pdf figures/fig_arch.svg -o figures/fig_arch.pdf
# (alternatives if rsvg-convert is absent: cairosvg, inkscape --export-type=pdf)
```

The `\includegraphics` width must equal the blueprint's `print_width_mm` —
that is the single declaration the size gate certified.

### Step 5: Visual Review (topology + aesthetics — content is already proven)

Open the SVG/PDF and check what the deterministic verifier cannot see:
- **Topology matches the blueprint**: every blueprint edge is drawn, arrows
  point the stated direction, nothing extra (the text diff can't see arrows —
  this check is exactly what it delegates to eyes)
- **No overlaps**: nodes don't collide with each other or group boundaries
- **Readability**: labels aren't clipped; visual hierarchy is consistent
- **Edge clarity**: arrows hit nodes at clean angles, labels near edges are legible
- **Group alignment**: background rectangles frame their members cleanly
- **Color distinction**: categories are visually distinct in both color and grayscale

If issues found: Path A — edit the JSON spec (never the generated SVG) and
re-render; Path B — edit the SVG, then **re-run Step 4** (any edit can
introduce content drift; the verifier is cheap).

### Step 6: Iterate with Codex Review (Optional, for High-Stakes Figures)

For paper architecture figures, invoke cross-model review:

```
mcp__codex__codex:
  model: gpt-5.6-sol
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    Review this SVG figure for a technical paper (method / architecture / workflow diagram).

    Content lock: /path/to/blueprint.json
    Rendered: /path/to/fig.svg

    Label text and print sizes are already machine-verified against the lock —
    do not re-check spelling or font size. Evaluate:
    1. Clarity (C): can a reader understand the system from this figure alone?
    2. Readability (R): label placement, crowding, visual hierarchy
    3. Semantic accuracy (S): do the DRAWN arrows/groupings match the
       blueprint's edges and groups? (this is the one content check no script covers)

    Score each axis 1-10 and list specific issues to fix.
```

Iterate until all three axes ≥ 7/10. The ARIS tech report figures went through 5 rounds of this loop to reach C:7/R:7/S:8.

## Schema Quick Reference

### Blueprint (content lock — both paths)

| Field | Required | Notes |
|-------|----------|-------|
| `figure_id` | ✓ | |
| `source` | ✓ | Where every label/number comes from (traceability) |
| `print_width_mm` | | Intended `\includegraphics` width; drives the size gate |
| `nodes[]` | ✓ | `id` + `label_exact` (`\n` for line breaks), optional `sublabel_exact` |
| `edges[]` | | `from`/`to` node ids, optional `label_exact` |
| `groups[]` | | `label_exact` + `node_ids` |
| `annotations[]` | | Every other locked string: legends, headline claims/numbers |
| `forbidden_tokens[]` | | Case-insensitive substrings that must NOT appear |

### FigureSpec (Path A renderer input)

Run `python3 "$FIGURE_RENDERER" schema` (resolve $FIGURE_RENDERER per "Tool Location" above) for the authoritative schema.

### Nodes

| Field | Required | Default | Notes |
|-------|----------|---------|-------|
| `id` | ✓ | — | Unique |
| `label` | ✓ | — | `\n` for multi-line |
| `x`, `y` | ✓ | — | Center coordinates |
| `width`, `height` | | 120, 50 | |
| `shape` | | `rounded` | `rect` / `rounded` / `circle` / `ellipse` / `diamond` |
| `fill`, `stroke` | | auto from palette | `#RRGGBB` |
| `text_color` | | `#333333` | |
| `font_size` | | 14 | Override style default |

### Edges

| Field | Default | Notes |
|-------|---------|-------|
| `from`, `to` | required | Same = self-loop |
| `label` | — | Short edge label |
| `style` | `solid` | `solid` / `dashed` / `dotted` |
| `color` | `#555555` | |
| `curve` | `false` | Curved path |

### Groups

Rectangular background regions framing a set of nodes:
```json
{"label": "Layer Name", "node_ids": ["a", "b", "c"], "fill": "#EFF6FF", "stroke": "#BFDBFE"}
```

## Design Patterns

### Pattern 1: Layered Architecture
Stack rows of related nodes, each row is a group, add inter-layer arrows with semantic labels (`uses↓`, `produces↑`, `checks↓`).

### Pattern 2: Hub-and-Spoke
Central node (e.g., Executor), peripheral nodes (skills, tools), solid arrows for primary relations, dashed for feedback.

### Pattern 3: Pipeline with Feedback
Left-to-right main flow, feedback arrows curve below with `curve: true`.

### Pattern 4: Audit Cascade
Three-stage horizontal cascade with inputs feeding in from top, outputs exiting right, each stage in its own group.

## Anti-Patterns

- **Don't use groups as hierarchy**: groups frame peer nodes, not containment
- **Don't nest groups**: renderer draws them as background rectangles; nested groups look like Russian dolls
- **Don't cross-draw long diagonals**: if an arrow crosses 3+ rows, rethink the layout
- **Don't mix font sizes for same role**: keep one size per node category

## Output Contract

- `figures/specs/<id>_blueprint.json` — the content lock (source of truth for the figure's text)
- SVG file in `figures/` (vector, editable, hand-tweakable)
- Path A: FigureSpec JSON saved in `figures/specs/` for reproducibility
- PDF version via `rsvg-convert` (or cairosvg/inkscape) for LaTeX inclusion, included at the blueprint's `print_width_mm`
- **A figure is DONE only when `verify_figure.py` exits 0** against the current SVG

## Integration with Other Skills

- **`/paper-writing`** (Workflow 3): when `illustration: figurespec` (default for architecture figures), this skill handles Phase 2b
- **`/paper-figure`**: handles data plots; they complement each other (data + architecture = complete figure set). Its craft SSOT [`figure-craft.md`](../shared-references/figure-craft.md) governs Path B styling too
- **`/paper-illustration`**: for figures that need natural/qualitative imagery (photos, generated samples) — no longer the route for method/architecture figures
- **`/mermaid-diagram`**: lighter alternative for simple flowcharts

## Review Tracing

After each `mcp__codex__codex` or `mcp__codex__codex-reply` reviewer call, save the trace following `shared-references/review-tracing.md` (Policy C — forensic; never silently skip). Use `save_trace.sh` (resolved per the chain in `shared-references/integration-contract.md` §2) or write files directly to `.aris/traces/<skill>/<date>_run<NN>/`. Respect the `--- trace:` parameter (default: `full`).
