---
name: paper-figure-craft
description: "What a paper figure may say and how it must look in print — one figure states one conclusion, every quantity a reader compares gets its own visual channel, and every printed glyph lands in 7.5–11 pt at the width it is actually included at. Carries the user's figure rulings that hold for every paper (captions, numbers only from an SSOT, no Δ over two drawn levels, nothing drawn over an error bar). Use when the user says 这个图怎么画, 换个画法, 图太挤, 字太小, 看不出任务区别, 包装, teaser / showcase 图, caption 写什么, 加一个面板, 'redesign this figure', 'the labels collide', 'can we plot X instead'. Not for running the build (the project's paper CLAUDE.md)."
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
  re-proposed; reopening it needs the user. (For example its `paper/figures/CLAUDE.md`
  or a palette memory.)

## The one test

> **One figure = one conclusion you can state in a sentence, and every quantity
> the reader is asked to compare gets its own visual channel — position, length,
> or thickness. Never an annotation.**

The ruling that set this (user, 2026-08-01) was made on an alluvial figure:
ribbon thickness carries the *flow* (share of samples that moved), a paired
Δ-accuracy bar row on a shared ± axis carries the *effect*. Two quantities, two
channels. Every alternative compared for it — side-by-side bars, Δ printed onto
the ribbons, a 2×2 transition matrix, a 2×2 heatmap — either merged the two
quantities into one channel or turned the effect into an annotation.

## A showcase figure is packaging (user, 2026-11-01)

A gallery of tasks, scenes or inputs (a benchmark overview, a teaser) exists to
**sell the breadth**: the reader should see at a glance how the panels differ and
why each one is hard. A grid of scenes labelled only by dataset name fails that.
The user's model: ScheduleGen (arXiv 2610.39429) Figure 1, whose caption claims
it "can handle long-horizon contact manipulation, challenging reset
distributions, cluttered layouts, and multi-arm scenarios", one panel each.

- **Each panel's headline names its challenge** in the field's own vocabulary:
  a short noun phrase such as *fine-grained categories*, *heavy
  occlusion*, *cluttered layouts*, *low-light capture*,
  *multi-object scenes*, *distribution shift*, *mid-sequence domain change*,
  *rare / long-tail / out-of-vocabulary classes*. The dataset name drops
  to a small chip on the image.
- **The caption's first sentence lists the challenges as one span** ("Our
  evaluation spans A, B, C and D"), then says what a panel is.
- **Pick the instance that shows the challenge, and show it the way it
  happens.** A temporal challenge (a change during execution, a recovery) gets a
  before / after pair from the same episode, not a start frame. Take inputs that
  stress the claim (gulucaptain/Best-Paper-Writing-Skill `references/figures.md`,
  showcase type).
- **Packaging never outruns the evidence.** Each headline must be true of the
  instance drawn: check its split, corruption type or track in the benchmark's
  own definition and in the sample's metadata. A clean control sample cannot carry
  *mid-sequence domain change*; a fog case is *weather corruption*,
  not *visual corruption* in general.

## A qualitative example shows a measured mechanism (user, 2026-11-21)

A paired rollout or a single case is drawn to show *how* two systems differ.
The ruling is in the table below; this is how to build one.

1. **Inventory the mechanisms first.** List every statement of the form *system
   A does X more often than system B* that the paper's results support, each with
   its test. Only a tested, detected one gets an example. A reading that came out
   undetected gets no figure, and is recorded as undetected where the results
   live so it is not re-read later.
2. **No reading yet: take it from the recorded runs before drawing.** State the
   behaviour as a per-episode yes / no on recorded quantities (a logged
   scalar, a discrete decision the system made), read it over the whole paired set, and test it
   the way the page's outcome was tested. A definition fixed after looking at
   the data is labelled post hoc on the result page, with what had been seen.
3. **One mechanism, one example figure.** The same mechanism measured in two
   comparisons is one figure, in the comparison whose two runs share a start
   state, so the reader sees one difference.
4. **Pick the example by a written rule, and let the generator assert it.** The
   rule goes in the figure's spec. The generator checks that the example is an
   instance of the reading: the behaviour is *yes* for one system and *no* for
   the other in the read's own per-episode records, not only that the outcomes
   differ.
5. **Draw the measured quantity as its own channel.** Frames alone show an
   outcome. Under them goes a trace of the quantity the reading is defined on,
   one line per system on a shared time axis, with a dot at each frame's time so
   the two channels are tied together.
6. **The caption's takeaway is the set-level statement**, in the strength the
   test supports, followed by *one such state:* and the legend. The numbers go in
   the prose that cites the figure.
7. **Before promising the figure, check the frames can be had.** Runs that
   stored states but no images need a re-render from those states; find out
   whether the renderer covers that task family before scoping the work.

## Rulings (do not relitigate; cite the date if asked to reverse)

| Ruling | Date | Note |
|---|---|---|
| **Caption below the graphic** — `\caption` after `\includegraphics`. (Tables and algorithms take it on top.) | 2026-08-05 | The user issued the opposite instruction once, watched the sweep land, and withdrew it the same day. Say this before acting on a repeat. |
| **Caption carries no numbers and no pointer at another float.** Banned: `\ref{}`, `\S`, Appendix, `Table~`, `Figure~`, "the text". 1200 chars. | — | Figure captions are usually hand-written in `sections/`, so nothing sees them until compile: `paper-compile`'s `scripts/check_tex.py` checks every `\caption{}` the paper inputs. |
| **A fired caption gate means rewrite the caption whole.** | — | Never raise the cap, never patch the tail. |
| **No Δ where the figure already draws both compared levels.** A bar-top `Δ +3.1`, or a `net +142` that subtracts two labelled bars, is the table's banned Δ column in figure clothing — delete it, the reader subtracts. Δ stays only when it is a *plotted* quantity with its own axis and error bars: there it is the figure's one significance channel, a case tables cannot have because tables may not print intervals at all. | 2026-08-23 | Bold-if-significant rides on the Δ label, so it dies with it; how the prose then words significance is memory `paper-prose-rules` §1. Keep the Δ computation and its SSOT assertions in the generator: what is deleted is the presentation, not the evidence. Check the paper does not already use Δ for something else. |
| **An error bar is a quantity; nothing is drawn over it.** A value label that lands on a whisker — above all one wearing a white `bbox` to punch through it — deletes the figure's second quantity. The label clears the *whisker cap*, not the bar top, and needs no white box once it does. Raising the whisker's z-order is **not** the fix: it only redraws the line through the digits. | 2026-09-21 | Found on a latency figure whose stage medians sat at `median + 0.35` behind a white box, cutting a gap in every median→p95 stem. The user read it as the bars covering the whiskers; the label was the occluder. Holds for any interval mark: CI cap, percentile whisker, band edge. |
| **`n` is never printed on a figure, subset or not.** A subset is named in words (`large-molecule bucket only`, in the caption or a label), never sized. | 2026-09-09 | User: 图的规则不允许标子集. Same day as the table ruling. |
| **A qualitative example shows a mechanism that has been measured, or it is not drawn.** A paired rollout, a before / after strip or a single case exists to show *how* two systems differ. Before drawing one, name the measured reading, taken over the whole set and tested, that says what the difference is (one system abstains, backs off, attends to the right object more often). The example is then picked, and its frames or traces chosen, to show that quantity happening. A strip whose only message is *ours succeeds, theirs does not* repeats the outcome table with one sample and leaves the reader asking why, with nothing in the paper to answer. No measured mechanism: measure it first from the recorded runs, or leave the figure out. | 2026-11-21 | User: 「应该放确定机制的, 展示机制的图, 而不是展示一个不清楚的机制」, on a paired example strip whose two rows differed only in the final outcome; asked why ours was better, the paper had no measured answer. The caption's takeaway is then the mechanism, in the strength the measurement supports, not the single outcome. |
| **Numbers come from an SSOT** — the paper's data files or per-item result artifacts — and a figure is never hand-edited to change a number. | — | Edit the source, rerun the build. |
| **WYSIWYG width law**: `figsize` width **is** the printed width — the include fraction × the width the float occupies: `\columnwidth` for a column float in a two-column venue, `\textwidth` for `figure*` or in a one-column venue. | — | Otherwise `\includegraphics` scales the type along with the drawing. Take both widths from the compiled document (recipe below), never from memory of another venue. |
| **Every printed glyph in 7.5–11 pt** (body text is 10). Do not shrink type to fit; change the layout. | — | Declared ≠ printed, and the ratio cannot be computed from `figsize` when `savefig.bbox="tight"` crops the canvas. |
| **A schematic's labels are structure and symbols only** — config constants and explanations live in the prose, never printed on the drawing, and never relocated into the caption. Scopes the 2026-08-03 rule to data plots. | 2026-09-21 | See **What a caption is**. |
| **A symbol may be drawn on a figure only if the reader has met its definition by the page the figure lands on.** Reading order is the compiled PDF's, not the `.tex` order. A figure that prints in §1 carries none of §3's notation: the label is the word the caption or the preceding prose already uses (`member ranking`, `candidate members`, `bias-correction head`). Neither a gloss on the canvas nor a definition in the caption repairs an early symbol; only the word does. | 2026-09-21 | User: 「gm, rm,k 啥意思,你这就不符合 paper-jargon-pass」. The test is `paper-jargon-pass`'s figure reader, who holds this figure, its caption and the pages before it, nothing after. A figure in an appendix may use what the body defined. |
| **A figure defines its own symbols where they appear; the caption is not the symbol table.** Each symbol is glossed at the mark that draws it (an edge labelled `M members × T h` defines $M$; a badge `head φ_bc` says what φ is). Caption = bold title + one clause per panel side, ~300 chars. | 2026-08-30 | "Self-representative" was the user's word. A symbol left undefined in the figure is fixed *in the figure* — widen the badge, extend the label — never by growing the caption back. For a symbol whose definition comes *after* the figure's page there is no gloss to widen: it is replaced by the word (row above). |
| **One hue = one meaning within a figure, across panels too.** A data colour may not share hue with the structural accent. A legend chip must be drawn exactly like some mark in the figure; magnification marks (zoom outline + cone) are grey dashed so a solid accent outline reads as selection only. | 2026-08-30 | A panel that draws one series in the hue that means *our method* in the next panel reads as our method. Recolour it in its own role's hue and direct-label it at the curve end. |
| **No em dashes in figure labels** — the user reads them as AI-generated. Use `·`, a comma, or a colon; sweep the SVG and its blueprint together. | 2026-08-30 | Prose has its own dash rule (two pairs = split); this one is absolute for label text. |

## Colour

The palette's values are the project's, and which hue a paper likes is not a
ruling of this skill (user, 2026-09-01, deleting two such "rulings"). Read it
where the project keeps it (a palette memory, or a role table plus the figure
template).

**Categories get hues, never a grey ramp** (user, 2026-11-20, on a stacked bar
whose four parts were four greys from near-black to near-white: 「不要用这么丑的
颜色」).

- Series or stacked parts that are different *kinds* of thing each take a
  distinct hue from the palette's categorical set. A ramp, of greys or of tints
  of one hue, is for an ordered quantity only (a dose, a round number); on
  nominal categories it reads as a magnitude that is not there and prints as a
  dull monochrome block.
- Grey is for what the figure de-emphasises: a baseline, a remainder (`other`,
  the part the conclusion is not about), structure. At most one or two greys in
  a figure, never the whole of it.
- No near-black fills. Fills are mid-tone, light enough that the label on them
  is set in the ink colour; a part that needs white text is too dark.
- A palette with too few categorical hues gets new ones added at its one
  authority, each checked against the hues that already carry a meaning (`ours`,
  the structural accent). Falling back to the neutrals because the palette "ran
  out" is the failure this rule names.
- Tints of one hue with a grey remainder do not meet this rule: the user saw
  exactly that as the first fix and rejected it the same day (「还是太灰了」).
  Sub-cases of one outcome still get a hue each, and so does the remainder.
- A second panel on the same rows is coloured too, in the hue of the part whose
  meaning it shares, not left in neutral grey.

Two more things hold whatever the palette: one hue = one meaning (above), and two
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

**The first sentence is the takeaway** (user, 2026-11-01, replacing the earlier
"no conclusion in the caption"): the bold opening states the one conclusion the
figure carries, in the prose's own words and strength (`significant`, a
direction), never stronger than the text that cites the figure and never a
number. A schematic's takeaway is what the method changes. The takeaway is what
only this figure shows, not the summary result a table already prints: a
breakdown figure (per object, per task, per subset) states what the split shows
(`paper-table-craft`, "The takeaway is what only this float shows"). Then the legend for
*this* graphic: what is measured, the symbols, the axes, what a panel is. The
reservations on that reading are prose of the section the figure sits in.

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
it — `T h lead steps, fixed by the clock`, `M = 8 members`, `keep top
K = 3`, `n fields per step`, `one worker` —
is prose copied onto the canvas, and a second authority for a value that will
change. **Strip it; the prose is its home**, and config constants are already
allowed there. What stays is structure and symbols: group names, row names,
stage names, axis tick names, a symbol badge (`head φ_bc`), a one-word gloss on a
mark that has no other name (`reserved`). A symbol, though, only where the reader
has already met it (rulings table).

- **The test**: delete the label — is the structure still recognisable? Then it
  goes. What survives the test stays, in the shortest word that works.
- **Check the prose has a landing spot before deleting.** If it does not, write
  the prose first. Do **not** move it into the caption: the caption is the
  graphic's legend, not a second body text.
- **Worked case** (2026-09-21): an ensemble-pipeline schematic went from 39 text
  runs to 24 — member numbers, row names, stage names, the badge and `reserved`
  stayed; everything cut was already in its appendix section, line for line.

## Redesign checklist

Reach for these in order; the first two fix most complaints.

0b. **For a qualitative example, name the measured mechanism it shows.** None
   measured means no example figure yet; how to build one is in **A qualitative
   example shows a measured mechanism**.
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
