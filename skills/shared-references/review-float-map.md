# Float and Argument Map: every float serves an argument, every argument has main-text evidence

Two user rulings, the two directions of one map between arguments and evidence:

- 2026-11-03, 「每个图表都应该服务论点」: every figure and every table in a paper
  must serve an argument the paper makes.
- 2026-11-11, 「main 正文应该所有论点都至少有一两个论据，不应该有论点的论据全在附录。main
  正文应该 self contain」: the main text is self-contained. Every argument it
  makes carries at least one or two pieces of its evidence in the main text
  itself. The appendix may add evidence (more settings, breakdowns, protocol
  details); it never holds all of it, and "see Appendix C" alone supports nothing.

This file owns both rules, for writing and for review. The writing skills
(`research-paper-writing`, `bestpaper-writing`) apply them when they build a
paper's claim–evidence map; a page limit never moves an argument's decisive
evidence to the appendix, so cut elsewhere. A reviewer prompt over a manuscript
carries the block below verbatim at the end of the prompt (after SCOPE LIMITS
where the prompt has it), in every round, so each round rebuilds the map against
the current files. Callers: `research-review` and `auto-paper-improvement-loop`.
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
  it, or "cited only in its own appendix section".
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
  2. is cited only in its own appendix section;
  3. does not support the sentence that cites it, e.g. a baseline or an
     undeployed variant holds the decisive cell of the column that sentence
     leans on;
and every main-text argument that:
  4. has no supporting evidence in the main text: its evidence sits only in the
     appendix (e.g. the sentence rests on "see Appendix C" alone) or nowhere.
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

## Field note

2026-11-03, the first pass of the float map on a CVPR draft: two appendix tables
were cited only in their own appendix sections, one of them a negative result no
claim rested on; a baseline deployed without the orchestrator held the best cell
of a table cited for the advantage of keeping the orchestrator; the deployed
variant was not the best row on the training-distribution columns of its own
ablation, so the case for deploying it rested on the other columns alone; and
the introduction's motivation rested only on an appendix figure.
