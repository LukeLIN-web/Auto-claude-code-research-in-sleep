# Float Map: every figure and table serves an argument

User ruling, 2026-11-03: 「每个图表都应该服务论点」. Every figure and every table
in a paper must serve an argument the paper makes. A reviewer prompt over a
manuscript carries the block below verbatim at the end of the prompt (after
SCOPE LIMITS where the prompt has it), in every round, so each round rebuilds
the map against the current files. Callers:
`research-review` and `auto-paper-improvement-loop`. The Codex, gemini-review and
claude-review mirrors inline the block, as they inline SCOPE LIMITS.

The reviewer builds the map. The executor does not pass on its own map or its
reading of what a float shows: that is a summary of file contents, which
[`reviewer-independence.md`](reviewer-independence.md) forbids. The brief gives
the entry `.tex` file and the directories that hold the figures and tables.
Spot-check the returned entries' anchors as you would any other finding.

## The block

```text
=== FLOAT MAP (manuscripts; a required named field at the end of your reply) ===
Every figure and every table must serve an argument the paper makes: a
contribution, a motivation, or a stated advantage of the method. Build the map
yourself from the manuscript. Output a field named "Float map" with one line per
figure and per table, main text and appendix, numbered as the compiled PDF
prints them:
  <Figure/Table N> — what it shows, with its decisive numbers — the argument it
  serves (quote that sentence and give its location) — the sections that cite
  it, or "cited only in its own appendix section".
Setup and protocol tables serve reproducibility; say so instead of forcing a
claim onto them. Under "Flagged", list with its anchor every float that:
  1. serves no argument (a result no claim rests on);
  2. is cited only in its own appendix section;
  3. does not support the sentence that cites it, e.g. a baseline or an
     undeployed variant holds the decisive cell of the column that sentence
     leans on;
  4. is the only evidence for a main-text argument yet sits in the appendix.
A flagged float is a Critical Weakness only if it would sink the paper.
```

## Acting on a flagged float

Tie it to its argument: cite it from the sentence that makes the argument, put
that argument in its caption's opening, or move it next to that sentence. A
float no argument needs is cut or moved to the appendix. A float holding
unfavorable numbers is never cut by an automated fix: report it to the author,
who decides.

## Field note

2026-11-03, the first pass of this map on a CVPR draft: two appendix tables were
cited only in their own appendix sections, one of them a negative result no claim
rested on; a baseline deployed without the orchestrator held the best cell of a
table cited for the advantage of keeping the orchestrator; the deployed variant
was not the best row on the training-distribution columns of its own ablation, so
the case for deploying it rested on the other columns alone; and the
introduction's motivation rested only on an appendix figure.
