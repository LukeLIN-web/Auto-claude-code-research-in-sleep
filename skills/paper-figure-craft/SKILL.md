---
name: paper-figure-craft
description: "What a paper figure is allowed to say and how it has to look in print — one figure states one conclusion, every quantity a reader compares gets its own visual channel (never a downgrade to an annotation), and every printed glyph lands in 7.5–11 pt at the width it is actually included at. Carries this repo's frozen figure rulings (caption below the graphic, no numbers and no cross-float pointers in captions, n unmarked when the denominator is full, numbers only from an SSOT, the WYSIWYG width law, the settled fig:loc_conversion design and its rejected alternatives, fig:architecture is a hand-written SVG under a content lock). Use when the user says 这个图怎么画, 换个画法, 图太挤, 字太小, caption 写什么, 加一个面板, 'redesign this figure', 'the labels collide', 'can we plot X instead'. Not for running the build: commands, paths and font-measurement live in paper/CLAUDE.md and the paper-figure-and-table-build memory."
argument-hint: "[figure-label-or-script]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob
---

# Paper Figure Craft: one conclusion, one channel per quantity, legible in print

Working on: **$ARGUMENTS**

## Why this exists

The prose carries no results numbers (`paper/CLAUDE.md`, 2026-08-01), so a
figure is a number-of-record and has to stand alone. Two failures follow, and
they are independent — a figure can pass one and fail the other:

- **A figure asked to say two things** demotes one of them. The second quantity
  becomes a text annotation on top of the first, and a reader who is scanning
  never reads it.
- **A figure that looks right on screen** is included at a `\textwidth`
  fraction and shrinks its type with it. 8 pt drawn at 9.71 in wide, included
  at `\textwidth`, printed at 4.6 pt. That happened here.

## The one test

> **One figure = one conclusion you can state in a sentence, and every quantity
> the reader is asked to compare gets its own visual channel — position, length,
> or thickness. Never an annotation.**

This is the ruling behind `fig:loc_conversion` (user, 2026-08-01): an alluvial
row where ribbon thickness is the *flow* (share of questions that moved) over a
paired Δ-accuracy bar row for the *effect*, on a shared ± axis. Two quantities,
two channels.

Compared and **rejected** for that figure: four side-by-side bars; Δ printed
onto the ribbons; adding Both-hit / Both-miss bars to the lower row; a 2×2
transition matrix; a 2×2 heatmap. Every one of them either merges the two
quantities into one channel or turns the effect into an annotation. **The design
is settled — do not re-propose an alternative; reopening it needs the user.**

## Frozen rulings (do not relitigate; cite the date if asked to reverse)

| Ruling | Date | Note |
|---|---|---|
| **Caption below the graphic** — `\caption` after `\includegraphics`. (Tables and algorithms take it on top.) | 2026-08-05 | The user issued the opposite instruction once, watched the sweep land, and withdrew it the same day. Say this before acting on a repeat. |
| **Caption carries no numbers and no pointer at another float.** Banned: `\ref{}`, `\S`, Appendix, `Table~`, `Figure~`, "the text". 1200 chars. | — | Figure captions are hand-written in `sections/`, so nothing sees them until compile: `check_captions.py` applies `tab_common.check_caption` to every `\caption{}` in every clone. One predicate, two firing points. |
| **A fired caption gate means rewrite the caption whole.** | — | Never raise the cap, never patch the tail. |
| **No Δ where the figure already draws both compared levels.** A bar-top `Δ +4.2`, or a `net +190` that subtracts two labelled bars, is the table's banned Δ column in figure clothing — delete it, the reader subtracts. Δ stays only when it is a *plotted* quantity with its own axis and error bars (`fig:loc_conversion`'s bottom row, the paired-difference rows of `fig_montage_coverage` / `fig_selection_topb`): there it is the figure's one significance channel, a case tables cannot have because tables may not print intervals at all. | 2026-08-23 | Bold-if-significant rides on the Δ label, so it dies with it — significance moves to the prose words *significant* / *directional*. Keep the Δ computation and its SSOT assertions in the generator: what is deleted is the presentation, not the evidence. And `Δ` already means the 600 s block length in this paper. |
| **`n` is unmarked when the denominator is full**; marked, with the reason, only for a subset or a gap. | — | |
| **Numbers come from an SSOT** — `paper/data/*.json` or the per-question artefacts under `outputs/eval/` — and a figure is never hand-edited to change a number. | — | Edit the source, rerun the build. |
| **WYSIWYG width law**: `figsize` width **is** the printed width — `TEXT_W` (in `paper_plot_style.py`) × the `\textwidth` fraction the figure is included at. | — | Otherwise `\includegraphics` scales the type along with the drawing. |
| **Every printed glyph in 7.5–11 pt** (body text is 10). Do not shrink type to fit; change the layout. | — | Declared ≠ printed, and the ratio cannot be computed from `figsize` when `savefig.bbox="tight"` crops the canvas. Measurement recipe: memory `paper-figure-and-table-build`. |
| **`fig:architecture` is a hand-written SVG under a content lock**, not matplotlib. | 2026-08-17 | Edit `paper/scripts/fig_arch.svg`; any wording change moves in lockstep with `fig_arch_blueprint.json` or the build rejects the drift. |
| **A figure defines its own symbols where they appear; the caption is not the symbol table.** `fig:architecture`'s caption dropped its `Symbols:` paragraph: each symbol is glossed at the mark that draws it (`M blocks × 600 s` on the edge defines $M$; the badge text `LoRA φloc` says what φ is). Caption = bold title + one clause per panel side, ~300 chars. | 2026-08-30 | "Self-representative" was the user's word. A symbol left undefined in the figure is fixed *in the figure* — widen the badge, extend the label — never by growing the caption back. |
| **One hue = one meaning within a figure.** A media/data color may not share hue with the structural accent: audio moved off light blue to teal `#79c9b2` because `C_OURS` (`#c89336` since 2026-09-01, `#2a78d6` when the ruling was made) is the pipeline/selection accent everywhere. A legend chip must be drawn exactly like some mark in the figure — the white-box-with-blue-border `kept` chip matched nothing and died; kept-ness is direct-labelled next to its marks, and magnification marks (zoom outline + cone) are grey dashed so a solid blue outline reads as selection only. | 2026-08-30 | Route side rails (the Question→Stage-I conditioning edge) down the *empty* margin, away from the corner the panel connectors use. |
| **Lightness before hue.** Two series a reader must tell apart need a *relative-luminance* step, not just a different hue; compute it before choosing. Saturation is not pushed to the maximum, and one figure has one dominant plus one or two accents. | 2026-09-01 | Issued on a shipped figure whose two curves were gold `#c89336` (L 0.334) and grass green `#88B83D` (L 0.399) — different hues, same lightness, 「根本看不出来」. Recipe and worked cases: **Choosing the colours** below. |
| **No em dashes in figure labels** — the user reads them as AI-generated. Use `·`, a comma, or a colon; sweep the SVG and the blueprint together. | 2026-08-30 | Prose has its own dash rule (two pairs = split); this one is absolute for label text. |

## Choosing the colours: lightness first

The palette is the user's, not derived from anything (memory
`paper-figure-palette`): three hues — `C_OURS` gold `#c89336` for our method,
`C_BASE` brick red `#C1272D`, `C_ALT` olive/grass green `#88B83D` — plus, since
2026-09-01, the neutrals and the light tints that make a **lightness ladder**
possible: 深黑/灰黑, 中灰, 浅嫩绿, 浅粉红/珊瑚红. Reach for the neutrals whenever a
figure has more series than the three hues can separate; that is what they are
for. This is how to pick inside it (user, 2026-09-01):

1. **明度关系 > 色相关系.** Establish the layers first: dominant, secondary and
   background must carry a clear **lightness** difference. Whether the colour is
   pretty is second.
2. **Do not run the saturation to the maximum.** Pure blue `#0000FF` + pure red
   `#FF0000` reads badly because both sit at full chroma and high visual energy.
   Brick red and olive green *are* the desaturated forms — `#FF0000` → `#A94F45`,
   `#00FF00` → `#68734A`, `#0000FF` → `#526B82`. Pressed toward grey and black,
   colours stop stealing from each other.
3. **Warm/cool contrast is allowed; a hard collision is not.** Blue+red is the
   most direct warm/cool collision and both are bright and pure, so the boundary
   detonates. Brick red + olive green is dark-warm-red + dark-yellow-green: the
   hue and temperature difference survives at a fraction of the energy.
4. **Do not let several colours all play lead.** The shape that works is
   off-white background + **one dominant** + **one or two accents** + auxiliary
   greys/greyed hues — not red, blue, green and yellow all at 100%.
5. Low-saturation dark colours hold up across print, projector and screen alike,
   which is why the academic look lives on brick red + olive green on white.

> **"鲜艳" ≠ "好看"; "高对比" ≠ "高级".** The polished look is moderate contrast
> + reduced saturation + controlled lightness + a small amount of accent.

**Compute the luminance; do not eyeball it.** Two hues can sit far apart on the
wheel and still be the same lightness, which is exactly the failure that shipped:

```python
import matplotlib.colors as mc
def L(h):                                     # WCAG relative luminance
    f = lambda c: c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4
    return sum(k*f(c) for k, c in zip((0.2126, 0.7152, 0.0722), mc.to_rgb(h)))
cr = lambda a, b: round((max(L(a), L(b))+0.05)/(min(L(a), L(b))+0.05), 2)
```

Luminances of the pieces, so a candidate can be placed without recomputing:
灰黑 `#292827` **0.021**, brick `#C1272D` **0.130**, 中灰 `#8a8984` **0.250**,
珊瑚红 `#d9797d` **0.299**, gold `#c89336` **0.334**, olive `#88B83D` **0.399**,
浅嫩绿 `#bad68e` **0.605**. Gold-vs-olive is a ratio of **1.15** — that is the
pair the user rejected; gold-vs-brick is **2.13** and reads cleanly. Aim for
**≥2.1 on every pair a reader must separate inside one panel**, and derive tints
and steps with `blend` so each hue keeps one authority; never type a second hex.

**The move that makes room is not a fourth hue — it is roles.** Three hues cannot
separate five series, and every attempt to squeeze another step out of the gold
fails: the band a line can live in on white is roughly L 0.02–0.35, and gold
already sits at the top of it. `fig_bench_length` (2026-09-01, the worked case)
carries five series and resolves to **three levels**:

| role | mark | L |
|---|---|---|
| the deployed system — **the one dominant** | gold `C_OURS`, thickest line, filled marker, CI band | 0.334 |
| its ablation tier (localization only) | 灰黑 `blend(INK1, 0.42, INK2)`, thinner | 0.021 |
| the single-forward comparator | brick `C_BASE`, open marker | 0.130 |

Two devices did that, and they generalise:

- **One role, one hue; realisations differ by marker.** The whole-clip baseline
  and the always-fits montage are the same role and are **never in the same
  panel**, so they share `C_BASE` and separate on open square vs open triangle
  plus the legend text. Collapsing them freed a whole hue.
- **The non-hero series go neutral.** An ablation tier is auxiliary; a near-black
  neutral separates from everything (5.38 against gold, 2.52 against brick) and
  cannot compete for the lead the way a second saturated colour does. Hold its
  line weight below the hero's so the darkest mark is not also the heaviest.

Two failed attempts worth not repeating: a second gold one step darker
(`#795a24`) lands on brick red's lightness (1.09), and a desaturated tan scores
better against brick on paper but is illegible against gold on the page. Settle
it with `pdftoppm` at print size and look — not with more arithmetic.

**A hue may not mean two things in one figure, and that includes across panels.**
`fig_keepcap_sweep`'s third panel drew one of the port's own benchmarks in gold
while gold meant *main backbone* in the other two; both of that panel's curves
now sit in the port's own hue (brick + 珊瑚红 `blend(C_BASE, 0.38, white)`, ratio
1.66) with the identity direct-labelled at the curve end.

## Measuring the printed size (do this, do not estimate)

The WYSIWYG law is checked with one number: `scale = frac × TEXT_W / pdf_width_in`,
where `frac` is the `\textwidth` fraction the figure is included at.

```python
import fitz                                   # pymupdf env
p = fitz.open("figures/keepcap_sweep.pdf")[0]
s = frac * 6.5 / (p.rect.width / 72)          # TEXT_W from paper_plot_style
sz = [sp["size"] * s for b in p.get_text("dict")["blocks"]
      for l in b.get("lines", []) for sp in l["spans"] if sp["text"].strip()]
print(round(p.rect.width / 72, 2), round(s, 3), round(min(sz), 2), round(max(sz), 2))
```

Four things this catches that nothing else does:

- **`frac` is not always what the `\includegraphics` line says.** A figure inside
  a `minipage` is included at the *minipage's* width — `width=\linewidth` in a
  `0.52\textwidth` minipage is `frac = 0.52`.
- **`savefig.bbox="tight"` crops the canvas**, so the PDF is narrower than
  `figsize` and the scale must come from the *PDF*, never from `figsize`.
- **The failure signature is `pdf_width_in ≠ frac × TEXT_W`.** Two live cases,
  both invisible on screen: a 6.78 in canvas included at 6.175 in (0.91×, tick
  labels at 6.92 pt) and a 6.54 in canvas at 5.98 in (0.914×, in-bar numbers at
  7.32 pt). The fix was to draw at the width the page uses and let
  `paper_plot_style`'s `declared_pt` / `PT_TITLE…PT_ANN` ladder set the type —
  **both figures had hardcoded `fontsize=6.0` / `6.5` / `8` instead of using it.**
  `grep -n 'fontsize=[0-9]' fig_*.py` is the whole audit.
- **Read the second-smallest size, not the smallest.** Superscript markers and
  subscripts (`*`, `‡`, `A$_1$`) legitimately sit near 6 pt and produced three
  false alarms out of five on the first sweep.

## What a caption is

The legend for *this* graphic: the title, the symbols, the axes, what a panel
is. Not how to read the conclusion, not the reservations on that reading —
those are the prose of the section the figure sits in, and for an appendix
figure, that appendix section.

*This* graphic is the whole scope. A symbol drawn on a panel is the figure's own
and gets defined here even when the prose defines it later; a term that only ever
lives in prose — `arm`, `pp`, a paired interval — does not, however useful a
definition would be to a reader holding the figure alone. **A caption is not
required to be self-contained.** That requirement is the only door a glossary
comes through, and what it buys is one word with N authorities, sitting in the
least-scanned strings in the paper. (Repo ruling, 2026-08-26: "the body explains
it, so do not define it in the caption.")

The 1200-char gate is a backstop, not a target. **Aim at ~600.** What overflows
is reliably the protocol paragraph, and it belongs in the section the figure sits
in. One caption ending in a reading instruction — *"each panel's y-axis is
windowed to its own range: read curves within a panel"* — is not an incomplete
caption but a figure whose panels cannot be compared; fix the axes, not the
sentence.

And the reciprocal rule, which is where the duplication actually shows up
(`paper/CLAUDE.md`, 2026-08-03): **appendix prose does not repeat a number the
figure already draws.** Bar-value labels, Δ annotations, flip counts, error
bars, curve endpoints, a rate in a panel title — the prose gives the direction
and whether it was decided, and points. An error bar is sufficient; do not
transcribe the interval into the sentence. Before cutting, open the
corresponding `fig_*.py` and read what it actually labels — one paragraph
routinely mixes drawn numbers with numbers that have no other home.

## Redesign checklist

Reach for these in order; the first two fix most complaints.

1. **Count the conclusions.** Two conclusions is two figures, or one figure with
   two rows on a shared axis — not one panel with an annotation layer.
2. **Count the channels.** One quantity per channel. If a quantity is currently
   text on top of another quantity's mark, that is the bug.
3. **Then fix legibility**, in this order: increase the panel, shorten the
   labels, rotate or stagger ticks, drop a redundant series — **not** reduce the
   font size.
4. **Render at print size and look**: `pdftoppm -scale-to-x $(printed_inches ×
   200)`. The three failures that survive every other check are colliding x-tick
   labels, a long annotation overflowing its panel, and an auto tick locator
   dropping a level and printing decimals.

## Hard stops

- **Never edit a PDF in a clone's `figures/`.** Edit the generator, rerun the
  build; the clone copy is what compiles and it is overwritten.
- **Never hardcode a clone's hex directory** in a script — clones are discovered
  by `paper_paths.py` and their number changes.
- **`paper/figures/` is a derived Chinese-captioned preview for humans.** It is
  not what the paper compiles, and it must never reach a clone: a figure that is
  suddenly ~28 MB when its neighbours are ~20 KB is a preview that leaked into
  the compile directory (CJK font, unsubsettable). Fix by rerunning that
  figure's generator only.
- **An asset nothing references is a live defect.** `teaser.pdf` was rebuilt
  and pushed to Overleaf on every build with no `\includegraphics` anywhere in
  the paper. Check with
  `ls figures/*.pdf` against `grep -rho 'figures/[a-z_0-9]*\.pdf' sections/`.
- **Never delete a scope qualifier from a caption to make it fit.** Rewrite it;
  if the caliber genuinely does not fit, it was prose to begin with.

## Mechanics live elsewhere — point, do not copy

| Need | Owner |
|---|---|
| build commands, which python, output paths | `paper/CLAUDE.md` (出图), `paper/scripts/build_figs.sh` |
| width/font measurement, `save_fig`, `TEXT_W`, `declared_pt` | `paper/scripts/paper_plot_style.py`, memory `paper-figure-and-table-build` |
| caption rules as executable predicate | `paper/scripts/tab_common.py` + `check_captions.py` |
| caption position, `.bib`, co-author macros | memory `paper-layout-and-citation-rules` |
| what the prose may say about a figure | skill `paper-prose-tighten`, `paper/CLAUDE.md` |
| tables | skill `paper-table-craft` |

Sweep across figures, not just within one: one benchmark, one spelling; one
convention per mark in every figure that uses it; and no number a figure already
draws repeated in the prose. Those are invisible from a single figure.
