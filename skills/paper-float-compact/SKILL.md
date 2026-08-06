---
name: paper-float-compact
description: "Use when a paper's figures/tables sprawl across half-empty pages or the user asks to merge floats (合并表图 / 两个 subfigure / minipage 并排 / 大砍 caption). Consolidates related floats, cuts bloated captions, and repacks pages — verified by rendering the compiled PDF."
argument-hint: "[paper-dir-or-main.tex] [optional: which sections/floats]"
allowed-tools: Bash(*), Read, Grep, Glob, Write, Edit
---

# Paper Float Compaction

Merge related floats, cut bloated captions, and repack LaTeX pages — driven by
measurement (pdfinfo + page renders), not guesswork. A merge that "looks nice"
but exceeds `\textheight` silently produces an overflowing float or a lonely
float page, so every step below is budget-first.

## Step 0: Establish the page budget

```bash
grep -n "textwidth\|textheight\|fraction" <style>.sty main.tex
```

Record `\textwidth` and `\textheight` in pt (TMLR: 468pt x 650pt), and the float
fractions (`\topfraction`, `\bottomfraction`, `\floatpagefraction`). Every
decision below is "does image-height + caption-height fit the budget".

## Step 1: Inventory — map every float to its page, then look at the pages

```bash
# where is each float placed?
pdftotext main.pdf - | awk -v pat="<caption first words>" 'BEGIN{p=1} /\f/{p++} index($0,pat){print p; exit}'
# what does the page actually look like? (low DPI is enough to see whitespace)
pdftoppm -png -r 50 -f <first> -l <last> main.pdf pages/p
```

Read the rendered PNGs. You are looking for: floats alone on >40%-empty float
pages, related floats split by a page break, small floats (< 0.55\textwidth)
stacked vertically with dead space beside them, and tables wrapped in
`\resizebox{\textwidth}` that are *narrower* than `\textwidth` (resizebox
MAGNIFIES those — a real bug, fix by deleting the resizebox).

## Step 2: Compute feasibility BEFORE editing

For each candidate pair:

```bash
pdfinfo figures/<f>.pdf | grep "Page size"   # natural size in pt
```

- printed image height = chosen width x (h/w of the PDF)
- caption height ≈ (chars / chars-per-line) x ~11.5pt; ~95 chars/line at
  \small full width
- Two floats share one float page only if sum + `\floatsep` ≤ `\textheight`.
- Top-float stacking is capped by `\topfraction` x `\textheight`, which is
  *stricter* than a float page.
- Print-size floor: shrinking a figure below its natural (matplotlib) size
  shrinks fonts below design size — measure legibility by rendering the final
  page at 100 dpi and reading the smallest labels (target ≥ 7.5pt printed).

If images alone exceed the budget, the merge is infeasible unless captions are
cut (Step 4) or the figure is redesigned — say so instead of forcing it.

## Step 3: Merge toolbox (cheapest ref-churn first)

1. **Co-paging via float specifiers — zero source restructuring.** Deferred
   `[htbp]` floats form a solo float page as soon as `\floatpagefraction`
   (default 0.5) is met; that is where half-empty float pages come from.
   Remove `p` (use `[t]`) to force top placement with text beneath; use `[tp]`
   when two floats should share a float page; consider
   `\renewcommand{\bottomfraction}{0.5}` so mid-size floats can close a text
   page. Zero reference churn.
2. **Figure + table side by side in one float — zero ref churn.** Two minipages
   inside one `figure` env, `\captionof{figure}` / `\captionof{table}` (needs
   `caption`/`subcaption` package). Both keep their own numbers and labels.
   Good for a narrow figure and a narrow table from the same topic cluster.
3. **Two same-family tables → one float with `subtable` panels.** Each table
   becomes a `\begin{subtable}{\textwidth}` fragment with its own caption and
   label; a parent `table` float wraps both with a one-sentence parent caption.
   `\ref{tab:x}` then renders as "11a" — prose references keep working. If the
   tables are AUTO-GENERATED, change the *generator* to emit the fragment; the
   parent wrapper lives in the section .tex. Delete panel-caption words the
   parent caption now carries (e.g. the benchmark name).
4. **Two figures → one figure with subfigures** only when a shared caption
   genuinely helps; co-paging (1) achieves the same visual result without
   renumbering.

`subcaption` note: the caption package prints "Standard document class
detected" and leaves existing caption style alone — verify via the log.

## Step 4: Caption diet (大砍 caption)

A caption is the float's own legend: title + symbol/axis/column/panel
definitions. Everything else moves out. Cut:

- interpretation and conclusions → section prose;
- caveats and protocol notes → section prose;
- anything the figure already draws (legend entries, panel titles, axis
  labels) — open the fig script or read the rendered figure first;
- content duplicated from a sibling float's caption (after a merge, the parent
  caption owns the shared setup).

Discipline:

- **Grep before deleting.** Every sentence you cut is either (a) verifiably
  present in prose/figure already, or (b) relocated into the section's prose in
  the same edit, or (c) demonstrably disposable meta-narration. Unique facts
  (a percentage, a protocol detail) must land in prose, never vanish.
- Rewrite the caption whole; don't trim word-by-word.
- Don't upgrade claims while shortening.
- Respect house caption rules (e.g. no cross-references, no result numbers,
  length gates) — run the project's caption checker if it has one.

## Step 5: Verify loop (never trust the first compile)

```bash
./compile.sh   # or latexmk; must end with 0 undefined references
pdfinfo main.pdf | grep Pages          # page count vs baseline
# re-map float→page (Step 1), re-render every affected page,
pdftoppm -png -r 50 -f <n> -l <m> main.pdf pages/v
# and inspect shrunk figures at print size:
pdftoppm -png -r 100 -f <page> -l <page> main.pdf pages/z
```

Iterate: a merged float that lands alone and centered on a page means 'p' was
chosen — check height vs `\topfraction`, then adjust specifier or shave the
caption/figure a few pt. Expect 2–4 compile-inspect rounds; margins are often
within 10pt of the budget.

## Step 6: Report

State page count before/after, each merge made (and the ref form it produces,
e.g. "Table 11a"), each caption cut with where its content went, and the
merges you rejected with the pt arithmetic that rules them out. Leave pushing
(Overleaf sync etc.) to the user unless told otherwise.

## Footguns learned the hard way

- `\resizebox{\textwidth}{!}` on a narrow table magnifies it (fonts blow up).
- A 460pt float + long captions cannot top-place at `\topfraction 0.7`-ish
  defaults; check the style file — some (TMLR: 0.95) are generous.
- Two ~330pt floats fit a float page together but NOT as two top floats
  (`\topfraction` < 1 and both must clear it jointly).
- Auto-generated tables: edit generators, rerun, and confirm any
  "ensure_input"-style idempotent section injection still finds its anchor.
- Floats never cross a `\FloatBarrier`/section boundary — merges must stay
  within one section, and cross-section pairings hurt findability anyway.
- The shared checkout may change under you mid-session (figures regenerated,
  captions touched): re-grep the exact on-disk string before every Edit, and
  re-check that a rewritten caption still matches the *current* figure.
