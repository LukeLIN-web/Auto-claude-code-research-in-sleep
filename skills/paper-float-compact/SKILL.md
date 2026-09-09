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
# where is each float (and section) placed? The .aux already knows: \newlabel{lab}{{num}{page}}
python3 - <<'EOF'
import re
for lab,num,pg in re.findall(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{(\d+)\}', open("main.aux").read()):
    if lab.startswith(("fig:","tab:","sec:","app:")): print(f"p{int(pg):2d} {lab:28s} {num}")
EOF
# what does the page actually look like? (45-60 dpi is enough to see whitespace)
pdftoppm -png -r 50 -f <first> -l <last> main.pdf pages/p
```

The `.aux` map beats grepping caption words in `pdftotext`: one pass gives every
float, every section start, and the number each label renders as — the same
map re-run after an edit is the proof that no float was renumbered.

Read the rendered PNGs — tile 4–7 pages side by side into one PNG (PIL, a
red page-number tag per tile) so a whole section is judged in one look, then
zoom to 75–100 dpi only on the pages that look wrong.

You are looking for: floats alone on >40%-empty float pages, related floats split by a page break, small floats (< 0.55\textwidth)
stacked vertically with dead space beside them, and tables wrapped in
`\resizebox{\textwidth}` that are *narrower* than `\textwidth` (resizebox
MAGNIFIES those — a real bug, fix by deleting the resizebox).

## Step 1b: Audit the float barriers before blaming float sizes

If the document uses `placeins` (`\FloatBarrier` at section starts — common
in appendices), check whether the blank pages are barrier artifacts. Two
signatures, both seen on one manuscript (42 → 41 pages from fixing them, with
no content touched):

1. **A barrier fired with a float still deferred.** `\FloatBarrier` forces
   `\newpage` whenever `\@deferlist` is non-empty; the float lands at the top
   of the next page, the few lines of text that spilled with it follow, and
   the page is then ended — a page 70% blank, right before the section start.
2. **The barrier's own `\suppressfloats[t]`.** After the barrier, no top float
   may appear on the page where the new section starts. A section that opens
   with `[t]`-only tables therefore has every float pushed to the *following*
   page: three tables stacked with no text, and the section's figure alone on
   the page after that.

Diagnose in one compile, in a scratch copy:

```bash
sed -i 's/\\usepackage{placeins}/\\usepackage[verbose]{placeins}/' main.tex   # then latexmk
grep -n 'placeins' main.log | grep -E 'Must dump|stuck|lands on'
# "Float barrier ... processed on page 33, lands on page 34" + "Must dump some floats"
#   = signature 1 at that barrier; "Some floats are stuck" = it had to \clearpage.
```

Fixes, cheapest first — all zero content change:

- `\usepackage[above]{placeins}` removes the `\suppressfloats[t]` (signature 2).
  A section's own floats may then sit above its heading on the page where it
  starts; that is the only visible side effect, and it is what plain LaTeX does.
- For signature 1, make the pre-barrier float placeable *before* the barrier:
  `[t]` → `[htbp]` lets it drop in "here" under the page's existing top float
  when the top area is already taken (`\topfraction` × `\textheight` is the
  cap for *stacked* top floats, and a 9-line caption on the float above is
  often what pushes the sum over it). Removing that one barrier also works but
  lets the float drift under the next section's heading.
- `[below]` only matters for `b` floats; it does nothing for a `[t]` table.

Do this before any merge: the barrier fix is a package option plus one
specifier, and the merges you were about to plan may not be needed.

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

**Section tiling floor.** Before touching specifiers in a section, sum its
float heights (image × scale + caption lines × ~11.5pt) and its text, divide
by `\textheight`, and take the ceiling. If that equals the pages the section
occupies now, specifiers cannot help — the pieces simply do not tile — and
only a caption diet or a figure resize moves it. Worked case: a 5-page
appendix section with six floats (≈1876pt) and ≈1.3 pages of text; every
specifier combination on its six floats plus `\floatpagefraction` 0.8 gave
the identical page map. The caption diet on offer there was ≈10 lines
(≈125pt) against the ≈220pt a page needs, so it was reported as rejected
with those numbers rather than attempted.

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
   **Panels, not one tabular, whenever the rows are not on one protocol.** An
   identical column header is not enough: if the nominally same arm reads
   differently in the two tables (different answer weights, window cap,
   denominator marker), one tabular invites the cross-row comparison and
   then needs a group label plus a footnote to disown it. Two panels under a
   parent caption share the header definitions and keep the comparisons
   apart. Stack full-width panels with `\par\medskip` between them; the
   parent float carries no `\label` of its own.
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

**Run the variants in scratch copies, in parallel, never in the shared
checkout.** Each variant is an `rsync` of the paper dir (minus `.git` and
build products) plus a few `sed` lines, built with `latexmk`; one build is
about a minute, and 4–6 run side by side. Print one line per variant — page
count, the page the body ends on, Overfull count — plus the `.aux` float map
from Step 1, and compare maps, not impressions. A hypothesis that "looks
obvious" from the render (an `[H]` figure dragging a subsection to a new
page) was falsified this way in one round: the `[H]` was irrelevant, the
float page above it was the cause. Only the winning variant's edits go into
the real checkout, through the project's own build script.

Prove the edit changed nothing but placement:

```bash
# body/reference pages untouched (text-identical to the baseline build)
cmp <(pdftotext -f 1 -l <last body page> base/main.pdf -) <(pdftotext -f 1 -l <same> main.pdf -)
# no float renumbered: diff the .aux label→(number,page) maps; only pages may move
```

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
- `\FloatBarrier` is itself a page-waster in two ways (Step 1b): a deferred
  float at the barrier forces a mostly-blank page, and the barrier's
  `\suppressfloats[t]` cascades a section's `[t]` floats to the next page.
  `[verbose]` placeins names the barrier; `[above]` + one `[htbp]` fixed both.
- Two deferred floats that together just clear `\floatpagefraction` form a
  float page and all text moves off it; raising the fraction only helps if
  their sum is actually below the new threshold — measure the two heights
  from the render before assuming.
- The shared checkout may change under you mid-session (figures regenerated,
  captions touched): re-grep the exact on-disk string before every Edit, and
  re-check that a rewritten caption still matches the *current* figure.
