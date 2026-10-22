---
name: paper-figure-craft
description: "What a paper figure is allowed to say and how it has to look in print — one figure states one conclusion, every quantity a reader compares gets its own visual channel (never a downgrade to an annotation), and every printed glyph lands in 7.5–11 pt at the width it is actually included at (\\columnwidth or \\textwidth in a two-column venue). Carries the user's figure rulings that hold for every paper (caption below the graphic, no numbers and no cross-float pointers in captions, n never printed on a figure, numbers only from an SSOT, the WYSIWYG width law, no Δ over two drawn levels, nothing drawn over an error bar, no symbol before its definition's page). A paper's own settled designs, palette and hand-drawn figures live in its repo. Use when the user says 这个图怎么画, 换个画法, 图太挤, 字太小, caption 写什么, 加一个面板, 'redesign this figure', 'the labels collide', 'can we plot X instead'. Not for running the build: commands and paths live in the project's paper CLAUDE.md."
argument-hint: "[figure-label-or-script]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob
---

# Paper Figure Craft: one conclusion, one channel per quantity, legible in print

Working on: **$ARGUMENTS**

## Why this exists

The prose carries no results numbers (memory `paper-prose-rules` §1), so a
figure is a number-of-record and has to stand alone. Two failures follow, and
they are independent — a figure can pass one and fail the other:

- **A figure asked to say two things** demotes one of them. The second quantity
  becomes a text annotation on top of the first, and a reader who is scanning
  never reads it.
- **A figure that looks right on screen** is included at a fraction of the page
  and shrinks its type with it. 8 pt drawn at 9.71 in wide, included at
  `\textwidth`, printed at 4.6 pt. That happened on an earlier paper.

## Where the rulings live

- **This skill**: the user's rulings that hold for every paper.
- **The paper's repo** (its paper / figures CLAUDE.md, or its memory): that
  paper's settled designs and the alternatives already rejected for them, its
  palette, its hand-drawn figures under a content lock, its build. Read it
  before redesigning a figure there. A design it records as settled is not
  re-proposed; reopening it needs the user. (qwen3omni: `paper/figures/CLAUDE.md`
  and memory `paper-figure-palette`; agent-harness: `paperwriting/scripts/CLAUDE.md`.)
- qwen3omni's `paper/` tree has been read-only since 2026-10-01. The
  settled designs this skill used to carry for it (`fig:loc_conversion`'s
  rejected alternatives, `fig:architecture`'s content lock and forbidden tokens)
  are in `git show 9d700a3:skills/paper-figure-craft/SKILL.md`.

## The one test

> **One figure = one conclusion you can state in a sentence, and every quantity
> the reader is asked to compare gets its own visual channel — position, length,
> or thickness. Never an annotation.**

The ruling that set this (user, 2026-08-01) was made on an alluvial figure:
ribbon thickness carries the *flow* (share of questions that moved), a paired
Δ-accuracy bar row on a shared ± axis carries the *effect*. Two quantities, two
channels. Every alternative compared for it — side-by-side bars, Δ printed onto
the ribbons, a 2×2 transition matrix, a 2×2 heatmap — either merged the two
quantities into one channel or turned the effect into an annotation.

## Rulings (do not relitigate; cite the date if asked to reverse)

| Ruling | Date | Note |
|---|---|---|
| **Caption below the graphic** — `\caption` after `\includegraphics`. (Tables and algorithms take it on top.) | 2026-08-05 | The user issued the opposite instruction once, watched the sweep land, and withdrew it the same day. Say this before acting on a repeat. |
| **Caption carries no numbers and no pointer at another float.** Banned: `\ref{}`, `\S`, Appendix, `Table~`, `Figure~`, "the text". 1200 chars. | — | Figure captions are usually hand-written in `sections/`, so nothing sees them until compile: run the project's caption checker over every `\caption{}` if it has one. |
| **A fired caption gate means rewrite the caption whole.** | — | Never raise the cap, never patch the tail. |
| **No Δ where the figure already draws both compared levels.** A bar-top `Δ +4.2`, or a `net +190` that subtracts two labelled bars, is the table's banned Δ column in figure clothing — delete it, the reader subtracts. Δ stays only when it is a *plotted* quantity with its own axis and error bars: there it is the figure's one significance channel, a case tables cannot have because tables may not print intervals at all. | 2026-08-23 | Bold-if-significant rides on the Δ label, so it dies with it; how the prose then words significance is memory `paper-prose-rules` §1. Keep the Δ computation and its SSOT assertions in the generator: what is deleted is the presentation, not the evidence. Check the paper does not already use Δ for something else. |
| **An error bar is a quantity; nothing is drawn over it.** A value label that lands on a whisker — above all one wearing a white `bbox` to punch through it — deletes the figure's second quantity. The label clears the *whisker cap*, not the bar top, and needs no white box once it does. Raising the whisker's z-order is **not** the fix: it only redraws the line through the digits. | 2026-09-21 | Found on a latency figure whose stage medians sat at `median + 0.35` behind a white box, cutting a gap in every median→p95 stem. The user read it as the bars covering the whiskers; the label was the occluder. Holds for any interval mark: CI cap, percentile whisker, band edge. |
| **`n` is never printed on a figure, subset or not.** A subset is named in words (`long-clip bucket only`, in the caption or a label), never sized. | 2026-09-09 | User: 图的规则不允许标子集. Same day as the table ruling. |
| **Numbers come from an SSOT** — the paper's data files or per-item result artifacts — and a figure is never hand-edited to change a number. | — | Edit the source, rerun the build. |
| **WYSIWYG width law**: `figsize` width **is** the printed width — the include fraction × the width the float occupies: `\columnwidth` for a column float in a two-column venue, `\textwidth` for `figure*` or in a one-column venue. | — | Otherwise `\includegraphics` scales the type along with the drawing. Take both widths from the compiled document (recipe below), never from memory of another venue. |
| **Every printed glyph in 7.5–11 pt** (body text is 10). Do not shrink type to fit; change the layout. | — | Declared ≠ printed, and the ratio cannot be computed from `figsize` when `savefig.bbox="tight"` crops the canvas. |
| **A schematic's labels are structure and symbols only** — config constants and explanations live in the prose, never printed on the drawing, and never relocated into the caption. Scopes the 2026-08-03 rule to data plots. | 2026-09-21 | See **What a caption is**. |
| **A symbol may be drawn on a figure only if the reader has met its definition by the page the figure lands on.** Reading order is the compiled PDF's, not the `.tex` order. A figure that prints in §1 carries none of §3's notation: the label is the word the caption or the preceding prose already uses (`block ranking`, `candidate windows`, `localization LoRA`). Neither a gloss on the canvas nor a definition in the caption repairs an early symbol; only the word does. | 2026-09-21 | User: 「gm, rm,k 啥意思,你这就不符合 paper-jargon-pass」. The test is `paper-jargon-pass`'s figure reader, who holds this figure, its caption and the pages before it, nothing after. A figure in an appendix may use what the body defined. |
| **A figure defines its own symbols where they appear; the caption is not the symbol table.** Each symbol is glossed at the mark that draws it (an edge labelled `M blocks × 600 s` defines $M$; a badge `LoRA φloc` says what φ is). Caption = bold title + one clause per panel side, ~300 chars. | 2026-08-30 | "Self-representative" was the user's word. A symbol left undefined in the figure is fixed *in the figure* — widen the badge, extend the label — never by growing the caption back. For a symbol whose definition comes *after* the figure's page there is no gloss to widen: it is replaced by the word (row above). |
| **One hue = one meaning within a figure, across panels too.** A data colour may not share hue with the structural accent. A legend chip must be drawn exactly like some mark in the figure; magnification marks (zoom outline + cone) are grey dashed so a solid accent outline reads as selection only. | 2026-08-30 | A panel that draws one series in the hue that means *our method* in the next panel reads as our method. Recolour it in its own role's hue and direct-label it at the curve end. |
| **No em dashes in figure labels** — the user reads them as AI-generated. Use `·`, a comma, or a colon; sweep the SVG and its blueprint together. | 2026-08-30 | Prose has its own dash rule (two pairs = split); this one is absolute for label text. |

## Colour

The palette is the project's, and colour preferences are not rulings of this
skill (user, 2026-09-01, deleting two such "rulings"). Read it where the project
keeps it — qwen3omni: memory `paper-figure-palette` (its 2026-09-24 palette
replaced the gold / brick / olive set and that set's lightness ladder);
agent-harness: role in `paper_data.ROLE`, colour in the figure template.

Two things hold whatever the palette: one hue = one meaning (above), and two
series a reader must tell apart inside one panel get a second channel — marker
or line style — when their colours sit close in lightness. Compute the lightness
instead of eyeballing it, then settle it with `pdftoppm` at print size:

```python
import matplotlib.colors as mc
def L(h):                                     # WCAG relative luminance
    f = lambda c: c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4
    return sum(k*f(c) for k, c in zip((0.2126, 0.7152, 0.0722), mc.to_rgb(h)))
cr = lambda a, b: round((max(L(a), L(b))+0.05)/(min(L(a), L(b))+0.05), 2)
```

Derive tints with a `blend` from the palette's constants so each hue keeps one
authority; never type a second hex in a figure script.

## Measuring the printed size (do this, do not estimate)

Read the two widths off the compiled document once per venue:

```latex
% after \begin{document}; then: grep -E 'COLW=' main.log   (pt; /72.27 for inches)
\typeout{COLW=\the\columnwidth\space TEXTW=\the\textwidth}
```

(CVPR's author kit measured 6.875 in / 3.28 in on 2026-10-15; ICLR's `\textwidth`
is 5.5 in.) Then the WYSIWYG law is checked with one number:
`scale = frac × W / pdf_width_in`, where `W` is the width the float occupies and
`frac` the fraction it is included at.

```python
import fitz                                   # pymupdf
p = fitz.open("figures/<figure>.pdf")[0]
s = frac * W_in / (p.rect.width / 72)         # W_in: \columnwidth or \textwidth, in inches
sz = [sp["size"] * s for b in p.get_text("dict")["blocks"]
      for l in b.get("lines", []) for sp in l["spans"] if sp["text"].strip()]
print(round(p.rect.width / 72, 2), round(s, 3), round(min(sz), 2), round(max(sz), 2))
```

Five things this catches that nothing else does:

- **`frac` is not always what the `\includegraphics` line says.** A figure inside
  a `minipage` is included at the *minipage's* width — `width=\linewidth` in a
  `0.52\textwidth` minipage is `frac = 0.52`.
- **In a two-column venue, `\linewidth` in a `figure` is the column.** A figure
  drawn for the full text width and dropped into a column float prints at about
  half its type size. Decide column float or `figure*` before drawing, and draw
  at that width.
- **`savefig.bbox="tight"` crops the canvas**, so the PDF is narrower than
  `figsize` and the scale must come from the *PDF*, never from `figsize`.
- **The failure signature is `pdf_width_in ≠ frac × W`.** Both live cases found
  on one sweep (0.91× and 0.914×, tick labels and in-bar numbers near 7 pt) had
  hardcoded `fontsize=6.0` / `6.5` / `8` instead of using the project's style
  module's type ladder. `grep -n 'fontsize=[0-9]' fig_*.py` is the whole audit.
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
lives in prose — `baseline`, `pp`, a paired interval — does not, however useful a
definition would be to a reader holding the figure alone. **A caption is not
required to be self-contained.** That requirement is the only door a glossary
comes through, and what it buys is one word with N authorities, sitting in the
least-scanned strings in the paper. (User ruling, 2026-08-26: "the body explains
it, so do not define it in the caption.")

The 1200-char gate is a backstop, not a target. **Aim at ~600.** What overflows
is reliably the protocol paragraph, and it belongs in the section the figure sits
in. One caption ending in a reading instruction — *"each panel's y-axis is
windowed to its own range: read curves within a panel"* — is not an incomplete
caption but a figure whose panels cannot be compared; fix the axes, not the
sentence.

And the reciprocal rule, which is where the duplication actually shows up
(user ruling, 2026-08-03): **on a data plot, appendix prose does not repeat a
number the figure already draws.** Bar-value labels, Δ annotations, flip counts,
error bars, curve endpoints, a rate in a panel title — the prose gives the
direction and whether it was decided, and points. An error bar is sufficient; do
not transcribe the interval into the sentence. Before cutting, open the
corresponding `fig_*.py` and read what it actually labels — one paragraph
routinely mixes drawn numbers with numbers that have no other home.

**On a schematic the arrow points the other way** (user, 2026-09-21). A method,
protocol or architecture figure draws no measurement, so a constant printed on
it — `600 s blocks, fixed by the clock`, `K = 8 candidate windows`, `keep top
B = 3`, `32 frames + full audio per 75 s window`, `no lookahead · one worker` —
is prose copied onto the canvas, and a second authority for a value that will
change. **Strip it; the prose is its home**, and config constants are already
allowed there. What stays is structure and symbols: group names, row names,
stage names, axis tick names, a symbol badge (`LoRA φloc`), a one-word gloss on a
mark that has no other name (`reserved`). A symbol, though, only where the reader
has already met it (rulings table).

- **The test**: delete the label — is the structure still recognisable? Then it
  goes. What survives the test stays, in the shortest word that works.
- **Check the prose has a landing spot before deleting.** If it does not, write
  the prose first. Do **not** move it into the caption: the caption is the
  graphic's legend, not a second body text.
- **Worked case** (2026-09-21): a streaming-pipeline schematic went from 39 text
  runs to 24 — block numbers, row names, stage names, the badge and `reserved`
  stayed; everything cut was already in its appendix section, line for line.

## Redesign checklist

Reach for these in order; the first two fix most complaints.

1. **Count the conclusions.** Two conclusions is two figures, or one figure with
   two rows on a shared axis — not one panel with an annotation layer.
2. **Count the channels.** One quantity per channel. If a quantity is currently
   text on top of another quantity's mark, that is the bug.
3. **Then fix legibility**, in this order: increase the panel (in a two-column
   venue, consider `figure*`), shorten the labels, rotate or stagger ticks, drop
   a redundant series — **not** reduce the font size.
4. **Render at print size and look**: `pdftoppm -scale-to-x $(printed_inches ×
   200)`. The three failures that survive every other check are colliding x-tick
   labels, a long annotation overflowing its panel, and an auto tick locator
   dropping a level and printing decimals.

## Hard stops

- **Never edit a compiled figure PDF** (a clone's `figures/`, a preview).
  Edit the generator, rerun the build; the compiled copy is overwritten.
- **Never hardcode a clone's directory** in a script — discover it, as the
  project's path helper does.
- **An asset nothing references is a live defect** — it is rebuilt and pushed on
  every build. Check with `ls figures/*.pdf` against
  `grep -rho 'figures/[a-z_0-9]*\.pdf' sections/`.
- **Never delete a scope qualifier from a caption to make it fit.** Rewrite it;
  if the qualifier genuinely does not fit, it was prose to begin with.

## Mechanics live in the project — point, do not copy

| Need | Owner |
|---|---|
| build commands, which python, output paths, the style module (`TEXT_W`, type ladder) | the project's paper CLAUDE.md |
| caption rules as an executable predicate | the project's caption checker, if it has one |
| caption position, `.bib`, co-author macros | memory `paper-layout-and-citation-rules` |
| what the prose may say about a figure | skill `paper-prose-tighten`, memory `paper-prose-rules` |
| tables | skill `paper-table-craft` |
| where a float lands, two-column placement | skill `paper-float-compact` |

Sweep across figures, not just within one: one benchmark, one spelling; one
convention per mark in every figure that uses it; and no number a figure already
draws repeated in the prose. Those are invisible from a single figure.
