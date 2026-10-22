---
name: paper-table-craft
description: "What belongs in a paper table and what does not — a cell is a value, never a sentence; a caption is the table's own legend, never a glossary or a restatement of its rows. Carries the user's table rulings that hold for every paper (no confidence intervals and no p-values in any table, no Δ column when the table already prints both compared levels, caption above the tabular, no numbers and no cross-float pointers in captions, no n column or row, one decimal from the exact ratio, same-protocol-only comparison cells, type size measured and never scaled into place) and the cell-level cut classes for a table that has grown prose. Use when the user says 表太啰嗦, 删减表格, 这个表怎么写, caption 太长, 表里能不能写 CI, 这行要不要留, 加一列, 'trim this table', 'what goes in the caption', or when a config/results table's cells have turned into sentences. Not for building the table: generation, SSOT and build commands live in the project's paper CLAUDE.md."
argument-hint: "[table-label-or-file]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob
---

# Paper Table Craft: a cell is a value, not a sentence

Working on: **$ARGUMENTS**

## Why this exists

The prose of a paper does not carry results numbers — a standing user ruling
(memory `paper-prose-rules` §1: 正文只定性,数字的家是表和图). Everything the
prose gave up lands here. A table is therefore the paper's number-of-record and
has to be readable standing alone, which is exactly the pressure that turns it
into a paragraph in two columns: a cell acquires a `so that…` clause, a caption
acquires a glossary, and by the third revision the table explains itself instead
of showing itself.

The failure is invisible from inside because every addition is individually
true. It is visible from the column: nobody reads down a column of sentences.

This skill carries the rulings that hold for every paper. A paper's own
mechanics — which tables are hand-authored, which data file a table reads, the
rounding helper, the caption checker — live in its repo (qwen3omni:
`paper/tables/CLAUDE.md`, read-only since 2026-10-01, with its specifics as they
stood in `git show 9d700a3:skills/paper-table-craft/SKILL.md`; agent-harness:
`paperwriting/tables/CLAUDE.md`).

## The one test

For every cell:

> **Is this a value, or a sentence explaining a value?**

Keep the value. A clause that explains it either already exists in the prose
(check — it usually does) or belongs there, not here.

For every column:

> **Does a reader compare down it?**

If nothing is compared, it is not a column. Two rows carrying halves of one
fact are one row.

## Rulings (do not relitigate; cite the date if asked to reverse)

| Ruling | Date | Note |
|---|---|---|
| **No confidence intervals in any table.** No `95% CI` column, no `[lo, hi]` in a Δ cell, none in the caption either. | 2026-08-01 | The intervals stay in the SSOT. How the prose words significance is memory `paper-prose-rules` §1. |
| **A table that prints both compared levels carries no Δ column or Δ row.** Same-row pair (`Whole clip | c2f windows`) or same-block pair (`Native streaming` / `\method`) — the reader subtracts. Keep a difference cell only when the comparator's own level is *not* printed there, or when the cell is an interaction rather than a printed pair. | 2026-08-23 | A bold-if-significant mark riding on the difference cell dies with it. Delete the caption's `$\Delta$ =` sentence and its `bold marks ... excludes zero` sentence too — including the parent float's caption when the table is split into subtables. Working mirrors of the table (`.md` next to the generator) may keep printing Δ. |
| **No p-values.** Not computed, not reported, not transcribed from an older result page. | 2026-07-30 | Significance reads off the paired interval and nothing else. |
| **Caption above the tabular** — `\caption`+`\label` before `\begin{tabular}`. | 2026-08-05 | The user issued the opposite instruction once, watched the full sweep land, and withdrew it the same day. If asked again to move captions below, say this first, then act. |
| **Caption carries no numbers, no pointer at another float.** Banned: `\ref{}`, `\S`, Appendix, `Table~`, `Figure~`, "the text". 1200 chars hard cap. | — | Enforce it, do not remember it: run the project's caption checker on generated and hand-written captions alike, if it has one. |
| **A fired caption gate means rewrite the caption whole.** Never raise the cap, never patch the tail. | — | Captions bloat by accretion; one had reached 2.8 KB before the cap. |
| **`n` is not a column and not a row.** A group size is bookkeeping, not a value a reader compares down; a table whose rows are subsets prints the accuracies alone. The caption says what the groups *are*; the prose says the shape (`a small group`, `the covered majority`); the counts stay in the working mirror and the result page. A count column under another name (`Events`, a `(1458)` in a header) is still a count column. | 2026-09-09 | User: 不要汇报 n, and the same day for every table: 也一起撤了. The subset exemption is gone — a subset is named by its row label, not counted. |
| **Every accuracy, recall, coverage and success cell prints at one decimal, in every table.** Rounded half-up from the *exact ratio*, never from a score already stored at two decimals. | 2026-09-09 | Trigger: one column printed `51.7` and `62.28`. Re-rounding a stored score whose hundredths digit is 5 goes wrong (60.25 is 479/795 = 60.252 → 60.3), so the cell is printed from its count and denominator by the project's one rounding helper. Bold / underline tie on the printed one-decimal value. Non-score quantities (a token ratio, seconds) are outside this rule. |
| **A benchmark's question or episode count is not a column header.** Delete the `(n)` sub-header row under the benchmark columns: the body names each benchmark's denominator once, in Settings, and that is the paper's one printing. Fold a qualifier that changes how the column is *read* (`1--4h`, `10-way`, a subtask or split name) into the title line. | 2026-08-23 | User: 不要写 (1549) (2700) 这些数字, 正文里写一次就够了. This is the prose-facing half of step 6's *no number reported in two tables*. |
| **A table's printed type size is measured, never scaled into place.** The floor is the figures' floor, 7.5 pt. | — | `\resizebox{\textwidth}{!}` sets the type size by an accident of the table's own width — one build measured 10.96 pt (magnified past the 9.96 pt body text), 8.90 and 8.41 against 8.97 everywhere else. Fix an overflowing table by the gutter (`\tabcolsep`) or by structure; in a two-column venue, by `table*` before squeezing a wide table into a column. |
| **One owner per mark.** Bold, underline, the zero convention and any difference cell come from one helper the generators share. | — | Four generators had reimplemented `lo > 0 or hi < 0`, and the zero convention had drifted three ways (`0.00`, `+0.00`, `\pm0.00`) — a reader comparing two tables reads the same mark as two different things. |
| **Every cell in a comparison table is on the same protocol.** A number borrowed from another paper is marked (`*` or `†`, with its citation) and sits where the project's rule puts it (qwen3omni: only in a `base` cell; agent-harness: its own block, not ranked against same-protocol rows); a paired difference only between same-protocol measured cells. | — | Memory `no-protocol-switch-to-rescue-arm`. Marks borrowed from another paper's table are transcribed, never glossed (memory `borrowed-table-marks-transcribe-only`). |

## What a caption is

The legend for *this* float: the title, the symbols, the definition of each
column. Nothing that defers to prose, nothing a row already shows.

Four ways it stops being that:

- **It restates its own rows.** "Both adapters share the same frozen backbone at
  the same rank and attachment points" — three rows of the table, in a sentence.
- **It becomes a glossary.** A caption defines only what exists nowhere else:
  its own column names, its own axes, its own marks (`\ddag`, bold, `---`), and
  the symbols drawn on the panels. A term the prose already defines — `baseline`,
  `chain`, `pp`, a paired interval, a block length — gets no clause here, however
  useful one would be to a reader holding the float alone. **A caption is not
  required to be self-contained.** That requirement is the only door a glossary
  comes through, and what it buys is one word with N authorities, sitting in the
  least-scanned strings in the paper. A term's landing place is the one sentence
  of prose that defines it. (User ruling, 2026-08-26: "the body explains it, so
  do not define it in the caption.")
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
| **T7 Deployed-vs-training disclaimer** | `The deployed grid (8×75 s per block) is not retrained on` | a protocol fact the method section states in its own voice; keep it there, not in a cell |
| **T8 Another table's rows** | a results table reproducing the five external-reference rows of the main table verbatim, marks and all | one table owns a comparison; the second points at it. The duplicate is invisible from either table alone — it is `paper-prose-tighten`'s class 7 with floats instead of paragraphs |

## Hard stops

- **Grep before deleting a row.** Two ways a row is load-bearing from outside:
  the body cites the table for that specific fact (`… empirical start-time law
  (Table~\ref{tab:repro})`), or the row is where a threshold used elsewhere is
  *defined* (a `0.40` collapse gate quoted 200 lines later in the appendix).
  `grep -n "tab:<label>"` across `sections/`, then grep the row's distinguishing
  noun.
- **Never delete a protocol fact**: a scoring rule (`exact set match, no partial
  credit`), a denominator rule, a train/dev/test separation, a budget that makes
  a comparison fair.
- **Generated or hand-authored?** `head -2` the `.tex`. An `AUTO-GENERATED`
  header means edit the generator and rerun the build — a hand edit is
  overwritten. The project's paper CLAUDE.md lists the hand-authored ones.
- **Never hardcode a number in a generator.** Numbers come from the paper's SSOT
  (data files or result pages read mechanically).

## Procedure

1. Decide generated vs hand-authored (`head -2`).
2. `grep -n "tab:<label>"` in `sections/` and read every hit — that is the list
   of rows you may not delete.
3. Classify every cell T1–T8. Prefer deleting a clause over rewriting a cell.
4. Rewrite the caption **whole**, from the four-way test above. Do not edit it
   in place; that is how it grew.
5. Compile, and require all four: `rc=0`, **zero** `Overfull \hbox` in
   `main.log`, the project's caption checker clean, and the **printed type size
   measured** — every table at the same pt, none under 7.5:

   ```python
   # pymupdf; find the page by a string unique to the table
   import fitz
   for p in fitz.open("main.pdf"):
       if "<a string unique to the table>" not in p.get_text(): continue
       for b in p.get_text("dict")["blocks"]:
           for l in b.get("lines", []):
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

## Mechanics live in the project — point, do not copy

| Need | Owner |
|---|---|
| generators, the rounding and mark helpers, which python, build | the project's paper CLAUDE.md |
| caption rules as an executable predicate | the project's caption checker, if it has one |
| caption position, `.bib`, co-author macros | memory `paper-layout-and-citation-rules` |
| what the prose may say about a table | skill `paper-prose-tighten`, memory `paper-prose-rules` |
| where a float lands, two-column placement | skill `paper-float-compact` |
