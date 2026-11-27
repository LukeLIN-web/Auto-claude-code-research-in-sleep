# Float and Argument Map: every float serves an argument, every argument has main-text evidence

Two user rulings, the two directions of one map between arguments and evidence:

- 2026-11-03, 「每个图表都应该服务论点」: every figure and every table in a paper
  must serve an argument the paper makes.
- 2026-11-11, 「main 正文应该所有论点都至少有一两个论据，不应该有论点的论据全在附录。main
  正文应该 self contain」: the main text is self-contained. Every argument it
  makes carries at least one or two pieces of its evidence in the main text
  itself. The appendix may add evidence (more settings, breakdowns, protocol
  details); it never holds all of it, and "see Appendix C" alone supports nothing.

A third ruling, 2026-11-19, picks the medium the evidence takes: a figure
before a table, a table before prose (`manuscript-craft.md` §4 owns it and its
test). The block below checks it as flags 4 and 5.

A fourth, 2026-11-20: an appendix float or section needs no citation from
another section. One cited only where it sits is not flagged, and no pointer to
it is asked for (the block's flag for it was removed).

A fifth, 2026-11-21, 「如果一个东西没有支持任何论点, 就应该删了」: the same test
at every size below a float. A sentence, a number, a paragraph or a reported
experiment that supports no argument is deleted (`paper-prose-tighten`, The One
Test, owns the rule and what counts as supporting). The block reports these as
flag 6.

A sixth, the same day, 「表/图 里的, 不支持论点的也要删」: the test also holds
inside a table. A table's row or column that no sentence reads does not stay
as it is: where its numbers favor the method a sentence is added that reads it,
otherwise it is deleted (`paper-table-craft` carries it as a ruling). Flag 6
reports these too. A figure's panel, group or series needs no sentence of its
own (2026-11-24, the author dropped that requirement); the figure as a whole
still serves an argument.

A seventh, 2026-11-23, 「更多训练没有变好的, 又没判清楚, 属于是暴露缺点, 应该隐藏」:
a variant that gives the method more of what it already uses (a second round,
more steps, more data) and comes out no better, with the comparison unsettled,
is hidden. It supports no argument, since an unsettled result proves neither
that one round is enough nor that more would hurt, and it shows a reader where
the method stops improving. The block reports these as flag 7.

An eighth, 2026-11-27, 「就不知道哪来的这个数」「不要出现这种乱七八糟的数字」: every
printed number can be traced by the reader. A value solved from another
quantity is printed as the rule that fixes it, a setting the authors chose
carries its reason, and a cell holds one number at its neighbours' precision.
The block reports these as flag 8.

This file owns the first two rules, for writing and for review. The writing skill
(`research-paper-writing`) applies them when it builds a
paper's claim–evidence map; a page limit never moves an argument's decisive
evidence to the appendix, so cut elsewhere. A reviewer prompt over a manuscript
carries the block below verbatim at the end of the prompt (after SCOPE LIMITS
where the prompt has it), in every round, so each round rebuilds the map against
the current files. Callers: `research-review`, in its structure thread after the
P4 persona (`reviewer-personas.md` §8), and `auto-paper-improvement-loop`.
The Codex, gemini-review and claude-review mirrors inline the block, as they
inline SCOPE LIMITS.

The reviewer builds the map. The executor does not pass on its own map or its
reading of what a float shows or where an argument's evidence sits: that is a
summary of file contents, which
[`reviewer-independence.md`](reviewer-independence.md) forbids. The brief gives
the entry `.tex` file and the directories that hold the figures and tables.
Spot-check the returned entries' anchors as you would any other finding.

## The block

```text
=== FLOAT AND ARGUMENT MAP (manuscripts; two required named fields at the end of your reply) ===
Every figure and every table must serve an argument the paper makes: a
contribution, a motivation, or a stated advantage of the method. Build the map
yourself from the manuscript. Output a field named "Float map" with one line per
figure and per table, main text and appendix, numbered as the compiled PDF
prints them:
  <Figure/Table N> — what it shows, with its decisive numbers — the argument it
  serves (quote that sentence and give its location) — the sections that cite
  it.
Setup and protocol tables serve reproducibility; say so instead of forcing a
claim onto them.
The main text must be self-contained: every argument it makes carries at least
one or two pieces of its evidence in the main text itself. The appendix may add
evidence (more settings, breakdowns, protocol details); it never holds all of
it. Output a field named "Argument map" with one line per argument the main text
makes (a contribution, a motivation, a stated advantage, a result claim, a
design choice justified by a result):
  <quote the sentence, give its location> — its main-text evidence: a main-text
  figure or table, a number with its comparison in main-text prose, or a
  citation for a claim about prior work (give each location) — its appendix
  evidence, if any.
Under "Flagged", list with its anchor every float that:
  1. serves no argument (a result no claim rests on);
  2. does not support the sentence that cites it, e.g. a baseline or an
     undeployed variant holds the decisive cell of the column that sentence
     leans on;
and every main-text argument that:
  3. has no supporting evidence in the main text: its evidence sits only in the
     appendix (e.g. the sentence rests on "see Appendix C" alone) or nowhere.
and every float or passage in the wrong medium (a figure before a table, a
table before prose):
  4. a table whose conclusion is a shape a figure would show: a trend over an
     ordered variable, a ranking or gap among a few arms, a distribution, a
     breakdown into parts, a trade-off between two quantities;
  5. a prose passage, main text or appendix, that walks through values,
     settings or parallel items one by one where a table or figure would hold
     them.
and every passage or part of a float, main text or appendix, that supports
no argument:
  6. a sentence, a number, a paragraph, a reported experiment, or a part of a
     table (a row or a column) that
     states no argument the paper makes, is not evidence for one, does not
     define what one is about (a term, the setup, a protocol constant) and
     does not bound one (a denominator, a scope limit, a result that weighs
     against it). A row or column is evidence only if a sentence, in the
     prose or in the caption's opening, reads it. Quote it or name it, give
     its location and say in one line what it is.
and every reported variant that extends the method and does not improve it:
  7. a row, a series or a paragraph for a variant that gives the method more
     of what it already uses (another round, more training steps, more data,
     a larger model, a longer schedule) whose result is not better than the
     method's and is not settled either way by the paper's own test. It
     supports no argument and shows a reader where the method stops
     improving. Name it, give its location and its numbers against the
     method's, and say whether any sentence of the main text rests on it.
and every printed number a reader cannot trace:
  8. a number in a table cell, a caption or a sentence whose origin the
     paper does not give, or whose form is noisier than what it says: a
     setting solved from another quantity and printed as the solved value
     ("the top 31.4%", picked so that two sets come out the same size); a
     threshold or fraction the authors chose, with no reason or citation
     beside it; a count pair "N of M" in a table cell; more digits than
     the neighbouring numbers carry. Quote it, give its location and say
     which kind it is.
An appendix float or section needs no citation from the main text or from
another appendix section: one cited only where it sits is fine. Do not flag
it and do not ask for a pointer to it.
A flagged float or argument is a Critical Weakness only if it would sink the paper.
```

## Acting on a flagged float or argument

A flagged float: tie it to its argument. Cite it from the sentence that makes
the argument, put that argument in its caption's opening, or move it next to
that sentence. A float no argument needs is cut or moved to the appendix. A
float holding unfavorable numbers is never cut by an automated fix: report it to
the author, who decides.

A flagged argument: bring its decisive evidence into the main text. Move the
float, or the row or panel that carries the argument, next to the sentence; or,
where the project's rules let main-text prose carry numbers, state the decisive
number with its comparison and keep the full table in the appendix. An argument
with no evidence anywhere is narrowed to what the evidence supports or gets an
experiment. Dropping an argument from the main text, or moving it to the
appendix together with its evidence, changes what the paper claims: report it to
the author, who decides.

A passage that supports no argument (flag 6): spot-check it against the One
Test of `paper-prose-tighten`, then delete it. Two kinds are reported to the
author and not deleted: a passage the author asked for by name, and a result
that weighs against a claim, which bounds that claim and is no orphan. When the
flagged passage is the only prose that names a breakdown or a setting (a list
of perturbation types no table splits by), the report asks the author one
question: add the breakdown, or delete the passage.

A row or column of a table that supports no argument (flag 6), by what its numbers show:
- they favor the method (ours is higher there, significant or not): keep the
  part and add the sentence that reads it, next to the sentence that cites the
  float ("On <benchmark>, it also outperforms <baseline>"), in the strength the
  test supports. The author's ruling, 2026-11-21: 「没有句子读, 对我们有利的,
  我们可以加句子」. In a frozen main text the sentence goes in the appendix.
- they favor neither side (a count, a quantity derived from other rows, a
  setting nothing compares): delete the row or column in the
  table's generator, with its caption legend item and any pointer that named
  it.
- they weigh against a claim, or the author asked for the part by name: report
  it to the author, who decides.
A cell the prose reads elsewhere keeps its float. The cut is always a whole
row or column: while a row and a column both stay, the cell
where they meet stays printed, read or not (the author, same day: 「如果列/行
在的话, 不要单独删格子」).

A variant that extends the method and does not improve it (flag 7): hide it.
Take its row or series out in the float's generator, with its caption legend
item, and take out the paragraph that reads it; keep both for a later version
behind the generator's switch or as commented source, not deleted. Float numbers
stay as they are. Before hiding, check three things and report instead of
hiding when one fails:
- a main-text sentence rests on the result (a design choice justified by it, a
  pointer that quotes its number): the sentence and the result go or stay
  together, and in a frozen main text they stay;
- the comparison is settled by the paper's test (the variant is significantly
  better or significantly worse on what it was run for): a settled result is
  evidence and is handled as any other float part;
- the author asked for the variant by name.
Do not add an explanation of why the variant did not improve in its place: a
cause the paper has not tested opens a second line of attack (the same author,
same day: 「如果没啥好处宁可不说」).

A number a reader cannot trace (flag 8), by kind:
- a solved value (a fraction, a threshold or a step count computed so that
  two quantities match): print the rule in its place ("as many as the kept
  frames"), not the value the rule produced.
- a setting the authors chose (a threshold, a fraction, a cap): keep the
  value and give its reason or its source in one sentence of the prose next
  to it. A caption does not carry the reason.
- a count pair `N of M` in a cell: print the one number the column is about,
  and drop the column when no sentence reads it (flag 6).
- more digits than the neighbours carry: round to their precision.
Numbers change in the float's generator, never in its output.

A float or passage in the wrong medium: redraw the table as a figure that shows
the shape, or move the paragraph's values into a table or figure and keep its
takeaway sentence in the prose. Numbers come from the same data files and the
claim stays the same.
