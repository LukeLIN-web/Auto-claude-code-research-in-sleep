---
name: paper-table-craft
description: "What belongs in a paper table and what does not — a cell is a value, never a sentence; a caption is the table's own legend, never a glossary or a restatement of its rows. Carries this repo's frozen table rulings (no confidence intervals and no p-values in any table, caption above the tabular, no numbers and no cross-float pointers in captions, n unmarked when the denominator is full, same-protocol-only comparison cells) and the cell-level cut classes for a table that has grown prose. Use when the user says 表太啰嗦, 删减表格, 这个表怎么写, caption 太长, 表里能不能写 CI, 这行要不要留, 加一列, 'trim this table', 'what goes in the caption', or when a config/results table's cells have turned into sentences. Not for building the table: generation, SSOT and build commands live in paper/scripts/CLAUDE.md and the paper-figure-and-table-build memory."
argument-hint: "[table-label-or-file]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob
---

# Paper Table Craft: a cell is a value, not a sentence

Working on: **$ARGUMENTS**

## Why this exists

The prose in this paper does not carry results numbers — that is a standing
ruling (`paper/CLAUDE.md`, 2026-08-01: 正文只定性,数字的家是表和图). Everything
the prose gave up lands here. A table is therefore the paper's number-of-record
and has to be readable standing alone, which is exactly the pressure that turns
it into a paragraph in two columns: a cell acquires a `so that…` clause, a
caption acquires a glossary, and by the third revision the table explains itself
instead of showing itself.

The failure is invisible from inside because every addition is individually
true. It is visible from the column: nobody reads down a column of sentences.

## The one test

For every cell:

> **Is this a value, or a sentence explaining a value?**

Keep the value. A clause that explains it either already exists in the prose
(check — it usually does) or belongs there, not here.

For every column:

> **Does a reader compare down it?**

If nothing is compared, it is not a column. Two rows carrying halves of one
fact are one row.

## Frozen rulings (do not relitigate; cite the date if asked to reverse)

| Ruling | Date | Note |
|---|---|---|
| **No confidence intervals in any table.** No `95% CI` column, no `[lo, hi]` in a Δ cell, none in the caption either. | 2026-08-01 | Significance is carried by the *weight* of the number: `tab_common.delta_bold` bolds a paired difference iff the clustered interval excludes zero. The intervals themselves stay in `paper/data/*_ci.json`. |
| **No p-values.** Not computed, not reported, not transcribed from an older result page. | 2026-07-30 | Significance reads off the video-clustered interval and nothing else. |
| **Caption above the tabular** — `\caption`+`\label` before `\begin{tabular}`. | 2026-08-05 | The user issued the opposite instruction once, watched the full sweep land, and withdrew it the same day. If asked again to move captions below, say this first, then act. |
| **Caption carries no numbers, no pointer at another float.** Banned: `\ref{}`, `\S`, Appendix, `Table~`, `Figure~`, "the text". 1200 chars hard cap. | — | Enforced, not remembered: `tab_common.check_caption`, fired at `write_table` for generated tables and at `check_captions.py` for every compiled `.tex`. |
| **A fired caption gate means rewrite the caption whole.** Never raise the cap, never patch the tail. | — | Captions bloat by accretion; they had reached 2.8 KB before the cap. |
| **`n` is unmarked when the denominator is full.** Mark it only for a subset, a dropped-item set, or a gap — and say why. | — | |
| **A table's printed type size is measured, never scaled into place.** `\small` prints at **8.97 pt** in this class; the floor is the figures' floor, 7.5 pt. | — | `\resizebox{\textwidth}{!}` sets the type size by an accident of the table's own width — measured on one build: 10.96 pt (`tab:main`, *magnified* past the 9.96 pt body text), 8.90, 8.41, against 8.97 everywhere else. Fix an overflowing table by the gutter (`\tabcolsep`) or by structure; never by scaling. |
| **One owner for the paired-difference cell**: `tab_common.delta_bold`. | — | Four generators had reimplemented `lo > 0 or hi < 0`, and the zero convention had drifted three ways across tables (`0.00`, `+0.00`, `\pm0.00`) — a reader comparing two tables reads the same mark as two different things. |
| **Every cell in a comparison table is on the same protocol.** A mixed-source official number is allowed only in a `base` cell, marked with `*` and its citation; paired Δ only between same-protocol measured cells. | — | See memory `main-table-official-anchor-mixed-source`, `no-protocol-switch-to-rescue-arm`. |

## What a caption is

The legend for *this* float: the title, the symbols, the definition of each
column. Nothing that defers to prose, nothing a row already shows.

Four ways it stops being that:

- **It restates its own rows.** "Both adapters share the same frozen backbone at
  the same rank and attachment points" — three rows of the table, in a sentence.
- **It becomes a glossary.** A term used in one row, where that row is already
  self-evident (`$1135$ / $1135$ / $1134$ over the three slots` defines "gold
  slot" by showing it), needs no definition. A term used across several rows and
  not inferable from any of them — `chain` — earns exactly one clause.
- **It explains how to read the conclusion**, or what reservations that reading
  carries. That is prose; for an appendix float, the prose of the section it
  sits in.
- **It points somewhere.** The gate blocks this, and the reason is that a
  caption is the least-scanned string in the paper: a cross-reference survives
  the table being renamed, moved, or deleted, and comes back as `??`.

The 1200-char gate is a backstop, not a target. **Aim at ~600**, and treat a
caption within a few characters of the cap as already broken rather than nearly
fine: one was found at 1197/1200, where any future wording fix would have failed
the build. The excess is reliably the same thing — the protocol argument for why
the table is a fair comparison. That argument belongs in the paragraph the float
sits in; the caption keeps only the marks and row terms a reader needs without
leaving the table.

## Cell-level cut classes

When a table has grown prose, these are the shapes, in descending yield.

| Class | Shape | Fix |
|---|---|---|
| **T1 Narrated cell** | a `so that…` / `which…` clause hanging off a value: `every training clip fits one 600 s block (30–598 s, median 297 s), so a coarse training forward has the form of one deployed glance` | keep the value, drop the clause — then grep the method section, which almost always already says it |
| **T2 Provenance assurance** | `step 2000, selected by a pre-specified stopping rule inside epoch 1`; `step 900, the run's endpoint`; `winner's hash frozen to disk before any test number was computed` | a checkpoint's *identity* is configuration and stays as a bare value; how it was chosen, and what it was **not** chosen by, goes |
| **T3 Pointer row** | `slot and letter probes pass every pre-registered gate (details in the text below)` | delete the row; the text below is right there |
| **T4 Sub-slice bookkeeping** | a second bound on a subset hung off the main bound (`$V\leq0.041$ … ; $\leq0.009$ on the 3,404 training chains`) | the main bound is the constraint |
| **T5 False pivot in a cell** | `assigned from the gold windows' empirical start-time law (rank-matched quantiles), not drawn uniformly` | delete from the pivot on |
| **T6 Split pair** | `Gold slot balance` / `Gold letter balance`; `Target` / `Loss masking` | one row |
| **T8 Another table's rows** | a results table reproducing the five external-reference rows of the main table verbatim, marks and all | one table owns a comparison; the second points at it. The duplicate is invisible from either table alone — it is `paper-prose-tighten`'s class 7 with floats instead of paragraphs |
| **T7 Deployed-vs-training disclaimer** | `The deployed grid (8×75 s per block) is not retrained on` | a protocol fact the method section states in its own voice; keep it there, not in a cell |

## Hard stops

- **Grep before deleting a row.** Two ways a row is load-bearing from outside:
  the body cites the table for that specific fact (`… empirical start-time law
  (Table~\ref{tab:repro})`), or the row is where a threshold used elsewhere is
  *defined* (the `0.40` collapse gate is quoted 200 lines later in the
  appendix). `grep -n "tab:<label>"` across `sections/`, then grep the row's
  distinguishing noun.
- **Never delete a protocol fact**: a scoring rule (`exact set match, no partial
  credit`), a denominator rule, a train/dev/test separation, a budget that makes
  a comparison fair.
- **Generated or hand-authored?** `head -2` the `.tex`. An `AUTO-GENERATED`
  header means edit the generator and rerun the build — a hand edit is
  overwritten. The hand-authored ones are `tab:repro` and the `tab:audiotraceav`
  parent float in `sections/08_appendix.tex`, and `tables/08_minicpm_avoc.tex`.
- **Never hardcode a number in a `tab_*.py`.** Numbers come from
  `paper/data/*.json` or `outputs/eval/*`. `tab:main` reads exactly one source:
  `paper/data/headline.json`.

## Procedure

1. Decide generated vs hand-authored (`head -2`).
2. `grep -n "tab:<label>"` in `sections/` and read every hit — that is the list
   of rows you may not delete.
3. Classify every cell T1–T7. Prefer deleting a clause over rewriting a cell.
4. Rewrite the caption **whole**, from the four-way test above. Do not edit it
   in place; that is how it grew.
5. Compile, and require all four: `rc=0`, **zero** `Overfull \hbox` in
   `main.log`, `check_captions.py` clean, and the **printed type size measured**
   — every table at the same pt, none under 7.5:

   ```python
   # pymupdf env; find the page by a string unique to the table
   import fitz
   for p in fitz.open("main.pdf"):
       if "Compressed-audio descent" not in p.get_text(): continue
       for b in p.get_text("dict")["blocks"]:
           for l in b["lines"]:
               for sp in l["spans"]:
                   print(round(sp["size"], 2), sp["text"][:30])
   ```

   Read the **second** smallest size, not the smallest: superscript marks
   (`*`, `‡`, `◦`) and subscripts legitimately sit near 6 pt.
6. **Sweep across tables, not just within one.** One benchmark, one spelling;
   one convention per mark (bold = decided) in every table that uses it; no
   number reported in two tables. These are invisible from a single float and
   are where the real defects were.
7. Report what was cut by class and, separately, **what was kept because
   something else cites it**.

## Mechanics live elsewhere — point, do not copy

| Need | Owner |
|---|---|
| caption rules as executable predicate | `paper/scripts/tab_common.py` (`check_caption`, `CAPTION_MAX_CHARS`, `_CAPTION_BANNED`) |
| writing a table into every clone, `\input` wiring | `tab_common.write_table` / `ensure_input` |
| build + which python + local TeX Live | `paper/CLAUDE.md`, memory `paper-figure-and-table-build` |
| caption position, `.bib`, co-author macros | memory `paper-layout-and-citation-rules` |
| what the prose may say about a table | skill `paper-prose-tighten`, `paper/CLAUDE.md` |
