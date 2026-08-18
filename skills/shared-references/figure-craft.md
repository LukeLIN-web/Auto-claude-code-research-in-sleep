# Figure Craft: Practitioner Rules for Camera-Ready Plots

`writing-principles.md` says *why* Figure 1 matters. This file says **what to
actually set** so a plot survives being shrunk into a two-column PDF and printed.

Source: practitioner notes in
[LukeLIN-web/blogs — How-to-write-paper](https://github.com/LukeLIN-web/blogs/blob/master/How-to-write-paper.md),
distilled into rules. Where it conflicts with a venue's own guide, the venue wins.

## When to Read

- Before writing the first `matplotlib` line in `paper-figure`.
- Before drawing a method / architecture / pipeline figure in `figure-spec`
  (either path — renderer or hand-authored SVG) or `paper-illustration`.
- During the figure pass of `auto-paper-improvement-loop` or any figure review.

## 0. The economics

Reviewers read **title → abstract → intro → figures**. Almost nobody reads the
prose under a results table. Consequences that drive the whole workflow:

- **Figures and tables are the paper.** Build them *before* writing any results
  prose; the prose is written last and is the least load-bearing text.
- Most of the writing budget is figure work. Budget accordingly — this is the
  part of the paper least replaceable by a language model.
- Concentrate the headline evidence into **one** figure (real-world setting +
  overall benchmark + per-modality breakdown), rather than spreading it thin.
  Information density per figure should be high; steal layout ideas from the
  best-looking papers in the area.

## 1. Hard defaults

These are not stylistic preferences — defaults ship too thin and too small for
print, and a figure is shrunk again when it lands in a column.

| Property | Default | Rule |
|---|---|---|
| Line width | `lines.linewidth = 2.0` | thin lines look cheap and vanish in print |
| Base font | ≥ body text size **after scaling** | see the scale rule below |
| Tick labels | explicit `fontsize`, never default | `plt.xticks(..., fontsize=20)` on a 5-inch canvas |
| Marker size | large enough to read at 45 % scale | |
| Grid | off unless it carries information | |
| Title inside figure | **never** | the title lives in `\caption{}` |
| Output | vector PDF | never ship raster into LaTeX |

**The scale rule.** Figure font size must be judged *on the printed page*, not
in the plotting window. If a figure is saved 5 in wide and included at
`0.48\textwidth` (≈ 3.3 in), everything shrinks by ~0.66 — so a 10 pt label
prints at ~6.6 pt and is unreadable. Either:

- set source fonts to `body_size / scale_factor` (e.g. 15–20 pt source for a
  10 pt body at 0.66 scale), or
- save the figure at the exact final width and use body-size fonts directly.

Checkable statement of the same rule: **the rendered glyph height in the
compiled PDF must be at least the body-text glyph height.** Zooming should not
be required to read an axis.
For `figure-spec` SVG figures this check is mechanical: `verify_figure.py`'s
print-size gate computes every glyph's printed size from the SVG viewBox and
the declared include width, and fails the figure below the floor.

Corollary: fewer words. Big fonts and long labels do not coexist — cut label
text until it fits at the enlarged size.

## 2. Color

- **Never red + green together** — red-green deficiency is the most common CVD.
- Colors within one figure must be **clearly separable**, not neighboring hues.
- **Bars: pale / pastel fills**, with a darker edge if separation is needed.
  Saturated primary bars read as a slide, not a paper.
- Verify in grayscale; add hatch / line style / marker so color is never the
  only channel carrying meaning.

## 3. Bars, lines, radar

- **Put the number on top of each bar.** A reviewer should not have to trace a
  value back to the y-axis.
- Capitalize the first letter of every label, legend entry and axis title.
- Rounded corners on boxes and blocks; sharp rectangles look harsh. A soft
  shadow prevents the "cheap clip-art" look — but keep it subtle and *consistent*
  across every figure (a flat NeurIPS-style figure with no shadows anywhere is
  also fine; what is not fine is mixing).
- Speedups and ratios are `$\times$`, never a letter `x`.
- Radar / spider charts exist in matplotlib and are a good fit for
  "methods × many metrics"; keep the axis count small.
- **Kill the default legend when it fights the layout.** Drawing your own legend
  (colored squares + short text, placed centrally in a single row) usually reads
  better than the auto-placed box, and lets one legend serve a multi-axis figure.

## 4. Tooling: generate → typeset → export

The split that works in practice:

1. **Plot the data in code** (matplotlib; `ggplot2` gives finer control than
   `seaborn` if you already work in R). Code owns the numbers — never hand-place
   data points. One script per figure, re-runnable when data changes.
2. **Typeset in a layout tool** (PowerPoint / Keynote / draw.io / Figma) for
   fonts, legends, icons, callouts and multi-panel assembly. This is where the
   "big fonts, few words" pass happens, and it is much faster than fighting
   matplotlib's text layout.
3. **Export vector, then crop.** Export/print to PDF with the *crop* option —
   otherwise the page's white margins get embedded and the figure appears tiny
   after `\includegraphics`.

Notes on specific tools:

- **draw.io**: import the plot, draw a rectangle, pick fills with an eyedropper
  from the plot, add text — that is your legend. It renders LaTeX math, so
  formulas inside a diagram stay consistent with the paper.
- **Vector reuse**: figures copied out of a talk deck or a screenshot-of-a-vector
  often stay vector. Verify by zooming in the final PDF; re-draw anything that
  turns into pixels. (Reusing *someone else's* figure needs permission and a
  citation — copy the technique, not the artwork.)
- **Formula check**: paste any LaTeX drawn inside a figure into a live renderer
  before exporting, so a diagram never carries a formula the paper does not.
- **Icons**: a vector icon library (e.g. iconfont) makes pipeline diagrams
  legible at a glance. Keep icons monochrome and same-weight.

## 5. W&B is a data source, not a figure source

Weights & Biases export is unreliable for camera-ready output: PDF exports come
out with black frames, SVG exports go transparent in slide tools, and page
screenshots capture spinners and loading state. Treat W&B as the **store**, not
the renderer:

- Pull the run history via the API/CSV and replot locally with the style above.
- In-app, `Smoothing` is what produces the shaded-variance band; hidden runs
  stay hidden in exports; expression math only works *within* one curve
  (cross-curve arithmetic needs a Vega custom chart), so compute derived series
  in your own script instead.
- Report / Compare views are for *reading*, not for shipping.

## 6. AI-generated diagrams

Image models draft a pipeline figure quickly, and that is a legitimate use —
**for a draft**. Text rendering, alignment and arrow semantics are not yet
camera-ready, so the output is a sketch to redraw in a vector tool, never the
shipped asset. See `paper-illustration` for the sanctioned path.

A prompt shape that produces a usable draft — the key move is that the module
list is *given*, and creativity is explicitly forbidden:

```text
Draw a clean NeurIPS/ICLR-style scientific figure.
Follow the MODULE LIST exactly: do not invent components, do not reinterpret,
do not add creativity.

GLOBAL RULES
- Flat style, no gradients/gloss, consistent thin line weights, pastel palette
- Rounded rectangles for blocks; arrows show data flow; short labels only
- Horizontal left→right (or top→bottom if inherently sequential)
- Each module appears exactly once, in the listed order

MODULE LIST
1. Inputs: ...
2. Preprocessing / encoding: ...
3. Core blocks / stages: ...
4. Special mechanisms: ...
5. Output head: ...
NOTES: branch/merge constraints, blocks that must stay one tall block, ...
```

## 7. Critique loop

Render the figure, screenshot it at printed size, and hand the image to a
vision-capable model with the question *"what would a NeurIPS reviewer find
wrong with this figure or table?"*. This catches scale, spacing and label
problems that are invisible while the plotting script is in front of you.
Compare against a figure from a paper you admire in the same subarea.

## 8. Checklist

- [ ] Every glyph in the compiled PDF is ≥ body-text size (no zooming needed).
- [ ] Line widths ≥ 2.0; markers readable at final scale.
- [ ] No red-green pairing; readable in grayscale; non-color channel present.
- [ ] Bars pale-filled, values printed on top, labels capitalized.
- [ ] No title inside the figure; caption self-contained in LaTeX.
- [ ] Vector PDF, cropped — no white margin, no embedded raster text.
- [ ] Figure font family matches the paper body font.
- [ ] Multipliers rendered as `$\times$`.
- [ ] Legend readable and not overlapping data; hand-drawn if the default fights.
- [ ] Figure regenerable from a committed script + data file.

## Related

- `writing-principles.md` § Figure Design — why Figure 1 carries the paper.
- `manuscript-craft.md` § Floats — where figures/tables go in the LaTeX source.
- `taste-calibration.md` — how to *grade* a figure once these mechanics pass.
