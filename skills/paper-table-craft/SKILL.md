---
name: paper-table-craft
description: "What belongs in a paper table — a cell is a value, never a sentence; a caption opens with the takeaway, then is the table's own legend, never a glossary or a restatement of its rows. Carries the user's table rulings that hold for every paper (no CIs or p-values, no Δ column beside both compared levels, caption above, no n column) and the cut classes for a table that has grown prose. Use when the user says 表太啰嗦, 删减表格, 这个表怎么写, caption 太长, 表里能不能写 CI, 这行要不要留, 加一列, 表不一致, 乱七八糟, 行名不统一, 'trim this table', 'what goes in the caption', 'the rows are inconsistent', when table cells have turned into sentences, and right after a table is made from a paragraph or a row is added or renamed (step 6's sweep). Not for building the table (the project's paper CLAUDE.md)."
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
rounding helper, the caption checker — live in its repo (its tables CLAUDE.md).

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
| **A table that prints both compared levels carries no Δ column or Δ row.** Same-row pair (`Baseline | Ours`) or same-block pair (`Native` / `\method`) — the reader subtracts. Keep a difference cell only when the comparator's own level is *not* printed there, or when the cell is an interaction rather than a printed pair. | 2026-08-23 | A bold-if-significant mark riding on the difference cell dies with it. Delete the caption's `$\Delta$ =` sentence and its `bold marks ... excludes zero` sentence too — including the parent float's caption when the table is split into subtables. Working mirrors of the table (`.md` next to the generator) may keep printing Δ. |
| **No p-values.** Not computed, not reported, not transcribed from an older result page. | 2026-07-30 | Significance reads off the paired interval and nothing else. |
| **Caption above the tabular** — `\caption`+`\label` before `\begin{tabular}`. | 2026-08-05 | The user issued the opposite instruction once, watched the full sweep land, and withdrew it the same day. If asked again to move captions below, say this first, then act. |
| **Caption carries no numbers, no pointer at another float.** Banned: `\ref{}`, `\S`, Appendix, `Table~`, `Figure~`, "the text". 1200 chars hard cap. | — | Enforce it, do not remember it: `paper-compile`'s `scripts/check_tex.py` checks generated and hand-written captions alike for the pointers, the cap and a number in the bold takeaway. A number in a name (`Model-2B`, a version) is not one. The legend after the takeaway is read by eye. Until 2026-11-23 the script checked no numbers, and a step count (`the N,000-step <model>`) passed every build in an appendix takeaway. |
| **A fired caption gate means rewrite the caption whole.** Never raise the cap, never patch the tail. | — | Captions bloat by accretion; one had reached 2.8 KB before the cap. |
| **`n` is not a column and not a row.** A group size is bookkeeping, not a value a reader compares down; a table whose rows are subsets prints the accuracies alone. The caption says what the groups *are*; the prose says the shape (`a small group`, `the in-domain majority`); the counts stay in the working mirror and the result page. A count column under another name (`Events`, a `(1312)` in a header) is still a count column. | 2026-09-09 | User: 不要汇报 n, and the same day for every table: 也一起撤了. The subset exemption is gone — a subset is named by its row label, not counted. |
| **Every accuracy, recall, coverage and success cell prints at one decimal, in every table.** Rounded half-up from the *exact ratio*, never from a score already stored at two decimals. | 2026-09-09 | Trigger: one column printed `47.9` and `58.36`. Re-rounding a stored score whose hundredths digit is 5 goes wrong (63.25 is 494/781 = 63.252 → 63.3), so the cell is printed from its count and denominator by the project's one rounding helper. Bold / underline tie on the printed one-decimal value. Non-score quantities (a token ratio, seconds) are outside this rule. |
| **A small table whose columns another table already has is merged into that table**, as rows (in a block of their own when they share a condition), not printed beside it. Its reprinted rows (the base, our method) are dropped, since the host table prints them already; the prose points at the host table. | 2026-11-20 | User, after two appendix tables that reprinted a larger table's rows on its own columns were merged into it: 「记住 并进去是好的」. Under a frozen float numbering, merge only tables whose numbers nothing frozen cites. |
| **A table whose one value column takes two or three labels is prose.** A list of comparisons, settings or variants with a categorical column (which test, which split, which server) is read down and found to repeat one label on most rows; printed as a table, the few distinct labels read as a menu picked row by row. The labels are not picked row by row: a rule assigns them (paired data gets one test, unpaired data another), and a table of rows has no place to print the rule. State the rule instead. Delete the table and write one sentence per label, each opening with the property that decides the label (`Every other paired comparison runs <test A> ...`, `Comparisons without pairs run <test B> ...`), its rows listed inside the sentence. | 2026-11-23 | Found on an appendix table of which statistical test each remaining comparison used: eight rows, five with the same test, and a takeaway that listed the three tests. User: 「每个配对检验都不一样是好事吗」, then 「这是有逻辑的」: the choices follow a logic, and the paper prints the logic, not the list. If no rule can be named for why the rows differ, that is a finding for the author, not something to word around. The tests followed from whether each comparison had pairs, which the table had no column for and the sentences state first. Keep every row's fact (unit, quantity) in its sentence; delete the generator function and the caption entry with the table; under a frozen float numbering, delete only a table whose removal moves no frozen number. A table whose rows differ in several columns stays a table. |
| **A benchmark's question or episode count is not a column header.** Delete the `(n)` sub-header row under the benchmark columns: the body names each benchmark's denominator once, in Settings, and that is the paper's one printing. Fold a qualifier that changes how the column is *read* (`0--10 d`, `5-class`, a subtask or split name) into the title line. | 2026-08-23 | User: 不要写 (⟨n⟩) (⟨n⟩) 这些数字, 正文里写一次就够了. This is the prose-facing half of step 6's *no number reported in two tables*. |
| **A unit goes in the column header, not in the caption or the cells.** `Bench-A (s)`, `Bench-B (s)`, `Memory (GB)`; the cells are bare numbers. When every column shares one unit, each header still carries it. | 2026-11-21 | User: 单位应该尽量写到列上面. Trigger: a timing table whose headers were bare benchmark names and whose only unit was the caption's `Median seconds per call`. The caption keeps what is measured (`median time per call`) and drops the unit word. A column whose rows differ in unit (a limit in seconds on some rows, in solver iterations on others) keeps the unit in the cell. Percent scores need no `(%)` when the paper's tables print them bare throughout. |
| **One table, one naming pattern; the rows a sentence compares sit together.** Row labels in a table share one grammar (`<data>, <qualifier>, <qualifier>`, not `X, held-out split` beside `Y on the held-out split`) and name every row on one axis: all by training data, or all by system. The method's row keeps the method's name, and the legend says what it is on the table's axis (`<Method>'s <model>: trained on all of its data`). The rows one sentence compares are adjacent. A condition several rows share opens a block (`\midrule`); it is not a suffix repeated on rows scattered through the table. A system that appears in two tables carries the same label in both, defined once in the generator. Where a frozen table already prints a label, the others follow its pattern. The caption names a row by its printed label, never by a third name (`the N,000-step <model>` for a row printed `…, Nk steps`). | 2026-11-23 | Trigger: an appendix table of training data whose five rows had each been named on the day its experiment landed, copied verbatim from a results table. It had two qualifier grammars, one row named by model among rows named by data, and the two rows of each comparison in different halves of the table. The labels were also defined twice in the generator. User: 「这一坨乱七八糟的为啥都不一致」. |
| **One quantity, one number format, in every table and in the prose.** A count printed `284k` in one table is not `284,113` in the table beside it or `6,000 steps` in the paragraph that reads it. A column never mixes formats (`15k` beside `27,182`): when one cell needs its digits, decide for the whole column, and keep the exact value in the result page. A `k` cell is a number: it right-aligns like any other. | 2026-11-23 | Same table: its sample and step counts printed in full while the table beside it, on the same models, printed `k` (an earlier ruling, 「用 k 来表示, 省略 3 位数后面的」). User, after the table was fixed: 「散文里最好也写 <N>k」, then 「可以, 改」 for every training-step count in the appendix. A generator whose number-or-word test read `284k` as a word had left-aligned a whole table of `k` cells. |
| **A table's printed type size is measured, never scaled into place.** The floor is the figures' floor, 7.5 pt. | — | `\resizebox{\textwidth}{!}` sets the type size by an accident of the table's own width — one build measured 10.96 pt (magnified past the 9.96 pt body text), 8.90 and 8.41 against 8.97 everywhere else. Fix an overflowing table by the gutter (`\tabcolsep`) or by structure; in a two-column venue, by `table*` before squeezing a wide table into a column. |
| **One owner per mark.** Bold, underline, the zero convention and any difference cell come from one helper the generators share. | — | Four generators had reimplemented `lo > 0 or hi < 0`, and the zero convention had drifted three ways (`0.00`, `+0.00`, `\pm0.00`) — a reader comparing two tables reads the same mark as two different things. |
| **An empty result cell prints `--`, and the legend reads `--: not reported`.** Never `not run`, `not evaluated`, or `not run or not reported`. One wording covers both a cell we did not run and a cell a cited paper did not report. | 2026-11-16 | User: 那个"-"别叫 not run，叫 not reported. Fix it in the caption generator and sweep every table that uses `--`. A cell that cannot exist in its row (a memory figure for a method that keeps no cache) keeps its own legend, `--: not applicable`. |
| **Every cell in a comparison table is on the same protocol.** A number borrowed from another paper is marked (`*` or `†`, with its citation) and sits where the project's rule puts it (for example only in a `base` cell, or in its own block ranked per the project's tables CLAUDE.md); a paired difference only between same-protocol measured cells. | — | Memory `no-protocol-switch-to-rescue-arm`. Marks borrowed from another paper's table are transcribed, never glossed (memory `borrowed-table-marks-transcribe-only`). |
| **A row or column is printed only if a sentence reads it.** Before printing a row or a column, name the sentence (the caption's opening, or the prose that cites the table) it is evidence for. One no sentence reads does not stay as it is. If its numbers favor the method, add the sentence that reads it ("On <benchmark>, it also outperforms <baseline>"), in the strength the test supports (user, same day: 「没有句子读, 对我们有利的, 我们可以加句子」). If they favor neither side (a count, a derived quantity), delete it, together with its caption legend item and any pointer that named it. The cut is a whole row or a whole column: while a row and a column both stay, the cell where they meet stays printed, read or not; never blank a single cell to `--` (user, same day: 「如果列/行在的话, 不要单独删格子」). A setup or protocol table keeps the rows that define the setup a claim is about; a quantity derived from two other rows is not one of them. | 2026-11-21 | Found on an appendix table of training data per variant: of seven rows the prose read four, and one unread row, derived from two others, differed in almost every column and made matched variants look unmatched. User: 「表/图 里的, 不支持论点的也要删」. This is the table form of the prose rule that every reported number supports a stated point; `paper-figure-craft` carries the figure form. Delete in the generator's row selection; a row whose numbers weigh against a claim goes to the author, not to the cut. |

## What a caption is

**First sentence: the takeaway** (user, 2026-11-01), the table's one conclusion in
the prose's own words, no number. A takeaway that carries two conclusions may be
two bold sentences (user 2026-11-16「能拆成两句粗体」). A takeaway never carries an exception
(`leads on all but Bench-6`, `except Baseline-C`); `paper-prose-tighten` class 14
says how to restate it. Its subject is the method, as in the paper's result
sentences: `<Method> trains on fewer samples than Baseline-B`,
not `Baseline-B trains on more samples than <Method>`
(user 2026-11-23「还是应该用 <method> 作为主语」; the takeaway had been
rewritten for consistency and still led with the baseline). Then the legend for *this* float: what is
measured, the symbols, the definition of each column. Nothing that defers to
prose; a takeaway is not a restatement of rows, but a row-by-row recital is.

**The takeaway is what only this float shows**, not the summary result another
float already prints (user 2026-11-23「caption 不就是应该说 提升是分布在多数⟨unit⟩上吗.
不然都看不懂.」). Before writing it, ask what a reader learns here that the
summary table cannot tell them, and write that. A float that splits a result
(per object, per task, per subset, per step) states what the split shows:
whether the gain is spread across most units or comes from a few, and where it
reverses. Restating the aggregate (`<Method> significantly outperforms
Baseline-A on Bench-B`) leaves the reader unable to see why the float exists.
When the float carries its own test (a test over units, not over samples),
the takeaway may add it in the strength it supports (`... on most objects,
and significantly so compared object by object`). Change the prose sentence
that cites the float in the same edit, so the caption is never stronger than
the text. If nothing beyond the aggregate can be named, the float has no
takeaway of its own, and that goes to the author as a question about whether
to keep it.

Three ways it stops being that:

- **It restates its own rows.** "Both pruned variants share the same dense backbone at
  the same sparsity and layer schedule" — three rows of the table, in a sentence.
- **It becomes a glossary.** A caption defines only what exists nowhere else:
  its own column names, its own axes, its own marks (`\ddag`, bold, `---`), and
  the symbols drawn on the panels. A term the prose already defines — `baseline`,
  `ensemble`, `pp`, a paired interval, a grid spacing — gets no clause here, however
  useful one would be to a reader holding the float alone. **A caption is not
  required to be self-contained.** That requirement is the only door a glossary
  comes through, and what it buys is one word with N authorities, sitting in the
  least-scanned strings in the paper. A term's landing place is the one sentence
  of prose that defines it. (User ruling, 2026-08-26: "the body explains it, so
  do not define it in the caption.")
- **It explains how to read the conclusion**, or what reservations that reading
  carries. That is prose; for an appendix float, the prose of the section it
  sits in.

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
| **T1 Narrated cell** | a `so that…` / `which…` clause hanging off a value: `every training sample fits one tile (median extent well under its size), so a training forward has the form of one deployed forecast step` | keep the value, drop the clause — then grep the method section, which almost always already says it |
| **T2 Provenance assurance** | `step 1500, selected by a pre-specified stopping rule inside epoch 2`; `step 1200, the run's endpoint`; `winner's hash frozen to disk before any test number was computed` | a checkpoint's *identity* is configuration and stays as a bare value; how it was chosen, and what it was **not** chosen by, goes |
| **T3 Pointer row** | `leakage and duplicate probes pass every pre-registered gate (details in the text below)` | delete the row; the text below is right there |
| **T4 Sub-slice bookkeeping** | a second bound on a subset hung off the main bound (`$V\leq0.037$ … ; $\leq0.008$ on the 2,918 training molecules`) | the main bound is the constraint |
| **T5 False pivot in a cell** | `assigned from the labelled events' empirical onset-time law (rank-matched quantiles), not drawn uniformly` | delete from the pivot on |
| **T6 Split pair** | `Positive-label share` / `Negative-label share`; `Target` / `Loss masking` | one row |
| **T7 Deployed-vs-training disclaimer** | `The deployed pruning mask (k channels per layer) is not retrained on` | a protocol fact the method section states in its own voice; keep it there, not in a cell |
| **T8 Another table's rows** | a results table reproducing the five external-reference rows of the main table verbatim, marks and all | one table owns a comparison; the second points at it. The duplicate is invisible from either table alone — it is `paper-prose-tighten`'s class 7 with floats instead of paragraphs |

## Hard stops

- **Grep before deleting a row.** Two ways a row is load-bearing from outside:
  the body cites the table for that specific fact (`… empirical onset-time law
  (Table~\ref{tab:repro})`), or the row is where a threshold used elsewhere is
  *defined* (a `0.40` collapse gate quoted 200 lines later in the appendix).
  `grep -n "tab:<label>"` across `sections/`, then grep the row's distinguishing
  noun.
- **Never delete a protocol fact**: a scoring rule (`exact set match, no partial
  credit`), a denominator rule, a train/dev/test separation, a budget that makes
  a comparison fair.
- **Never hardcode a number in a generator.** Numbers come from the paper's SSOT
  (data files or result pages read mechanically).

## Procedure

1. `head -2` the `.tex`. An `AUTO-GENERATED` header means edit the generator
   and rerun the build; a hand edit is overwritten. The project's paper
   CLAUDE.md lists the hand-authored tables.
2. Run the hard stops' row grep and read every hit: those are the rows you may
   not delete.
3. Classify every cell T1–T8. Prefer deleting a clause over rewriting a cell.
4. Rewrite the caption **whole**, from the three-way test above. Do not edit it
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
6. **Sweep the table against itself, its siblings and the prose that reads it.**
   No other pass does this. A prose polish edits the section's `.tex`, and a
   generated table that the section `\input`s stays outside it, caption and
   labels included. A float review asks whether each float serves an argument,
   not whether it agrees with itself. Read the compiled page and check:
   - within the table: one label pattern on one axis, compared rows adjacent,
     shared conditions as blocks; the caption names rows as printed and its
     takeaway's subject is the method;
   - across tables: one benchmark, one spelling; one label for one system; one
     convention per mark (bold = decided); one number format per quantity; no
     number reported in two tables;
   - against the prose: the sentences that cite the table name its rows and
     print its quantities the way the table does.

   These are invisible from a single cell and are where the real defects were.
   Run this sweep whenever a table is made from a paragraph or a results row is
   added or renamed. Labels coined one experiment at a time drift apart even
   when each is fine on the day it is coined.
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
