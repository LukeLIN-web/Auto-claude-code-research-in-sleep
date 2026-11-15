# Writing Rules in Review: the reviewer checks the manuscript against the rule files

User ruling 2026-11-15, 「paper writing 更新了一些规矩, 你把这个规矩也让 review 检查」: a
manuscript review checks the paper against the writing rules, e.g. that our
method's rows in a table are shaded.

The rules already have owners: the `research-paper-writing` skill, `paper-table-craft` and
`paper-figure-craft`, and the project's own paper rules, which win where they disagree (the
precedence `research-paper-writing/SKILL.md` already states). This file does not restate a
single rule. It owns two things: which rule files a manuscript review brief lists, and the
block that asks the reviewer to check the manuscript against them. A rule changed in its
owner reaches the next review with no edit here.

Callers: `research-review` sends the block. It goes at the end of the prompt, after FLOAT
AND ARGUMENT MAP, in the first round and in every follow-up brief. The Codex, gemini-review
and claude-review mirrors inline it, as they inline FLOAT AND ARGUMENT MAP. `paper-polish`
gives its editor the same file list, so a polish neither breaks these rules nor misses the
ones it may fix.

The rules a script can check are checked by `research-paper-writing/scripts/check_figures.py`
and `check_draft.py`, which `research-review` runs before the reviewer is called. The block
covers the rest, which need reading.

## What the brief lists

Under a heading `Writing rules`, the absolute path of each of these files:

1. `research-paper-writing/SKILL.md` and its section guides `references/introduction.md`,
   `references/experiments.md`, `references/figures.md` and
   `references/distinguish-prior-work.md`;
2. `paper-table-craft/SKILL.md` and `paper-figure-craft/SKILL.md`;
3. the project's paper rules: the paper's `CLAUDE.md`, the `CLAUDE.md` of its tables,
   figures and scripts directories where they exist, and every rule file these point to
   that the reviewer can read.

Paths only. A rule file's path is structural metadata (`reviewer-independence.md`); a
summary of its rules, or a word on which of them the draft breaks, is executor framing.
A reviewer that cannot read local files gets each file's full text pasted verbatim under
its path instead.

## The block

```text
=== WRITING RULES (manuscripts; one required named field at the end of your reply) ===
The brief lists rule files under "Writing rules". Read them, then check the
manuscript, main text and appendix, against every rule they state. Where a
project rule file and a general one disagree, the project rule holds. Check only
rules written in those files: a style preference of your own is not a finding.
Output a field named "Rule violations" with one line per rule broken:
  <rule: file, section, and a short quote of the rule> — every place that breaks
  it (file:line, or Table/Figure N as the compiled PDF numbers it) — what at that
  place breaks it.
A rule broken in many places is one line that lists every place. Write "none" if
no rule is broken. A rule violation does not enter your score unless it would
sink the paper.
```

## Acting on a violation

Spot-check each anchor and drop the ones that do not hold. Fix what holds where it is
produced: a generated table or caption in its generator, never in the output. Text the
project's rules reserve for the authors (the title, the abstract, the contribution list)
is reported to the authors, not rewritten, and so is a fix that would change a claim, a
number or what a float shows.

A rule the reviewer reads two ways, or two rule files that contradict each other with no
stated precedence, is a defect in the rules: report it to the author and fix the owner
file, not the manuscript.
