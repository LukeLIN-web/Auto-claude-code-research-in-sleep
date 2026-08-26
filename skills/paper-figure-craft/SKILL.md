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
