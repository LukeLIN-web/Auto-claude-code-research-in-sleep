# Sources

This skill fuses two upstream skills (2026-11-15, user: one skill, not two).

## 1. Research-Paper-Writing-Skills (Peng Sida's notes)

Copied from https://github.com/Master-cai/Research-Paper-Writing-Skills
(`research-paper-writing/`, commit 77e7c2c1ba06f7d71844873147665437a03aac1b, 2026-11-01; still upstream HEAD on 2026-11-03).
MIT License, Copyright (c) 2026 Master-cai; see `LICENSE`. Writing knowledge from Prof. Peng Sida's open notes,
https://pengsida.notion.site/c1a22465a0fa4b15a12985223916048e (「论文写作模板」) and the pages it links.

To update: re-copy from upstream, then re-apply the local changes below (`diff -r` against a fresh upstream clone
shows them).

### Local changes

1. `SKILL.md`: `description` rewritten and a "Scope in this fork" section added after the title, restricting use to
   introduction structure, Experiments and figures (user ruling 2026-11-01).
2. Notes content upstream did not port, added 2026-11-03 from the Notion pages as fetched that day:
   - `SKILL.md`: "Writing Order" (the notes' 11-step table); Paragraph Clarity Check gains the transition and
     abrupt-noun questions and the encode -> analyze -> improve -> decode step (「如何改一篇论文的写作」); a Figures
     entry in Section Guides; the Introduction outline in Output Contract.
   - `references/introduction.md`: "From story to sentence plan" (「如何使用copilot和gpt辅助英语写作」, section on
     planning granularity); the loose-contributions note in Pipeline Version 2.
   - `references/examples/introduction/writing-plan-manhattansdf.md`, new (「写作思路典例」, Introduction part), and
     its entries in both example indexes.
   - `references/experiments.md`: variants as baselines for a new task; demos aimed at the downstream community
     (「怎么做吸引人的demo和application」); the reason for the ablation package and its sensitivity tables.
   - `references/figures.md`, new (「论文画图」 callout and the first-impression callout). Its section "What the
     Group's Published Figures Do" is not from the notes: it was read off the Figure 1 and method figure of ten of
     the group's arXiv papers and the notes' two good examples (user 2026-11-03, in place of the private template).
   - `references/paper-review.md`: rejection signal 1.3 (「怎么改论文」).

Not ported: the deadline timeline and lab progress table, the Copilot/GPT prompting screenshots, the private figure
template, the linked PDFs (Bill Freeman, SIGGRAPH paper chairs, Writing Science), the Related Work and Method
parts of 「写作思路典例」, and the notes' call to discuss traditional methods in the Introduction (ported 2026-11-03,
removed the same day: the user does not want it).

## 2. Best-Paper-Writing-Skill (award-paper corpus)

Copied from https://github.com/gulucaptain/Best-Paper-Writing-Skill
(`skills/bestpaper-writing/`, commit b9eff99a2130bea960ef1050eacf9f40cb792dd4, 2026-11-01).
CC BY 4.0 (repository `LICENSE`, copied here as `LICENSE-CC-BY-4.0`); parts MIT (the base skill is source 1, `LICENSE`), see `NOTICE.md`.
Exemplar sentences under `references/exemplars/` are quoted from published papers and must not be copied into new papers.
To update, diff a fresh upstream clone against the files listed below and re-apply.

Where its files went:

- `scripts/`, `assets/`, `evals/`, `references/{routing,claim-calibration,style-rules,corpus-profile,intake-form,latex-output}.md`,
  `references/corpus/`, `references/exemplars/`: moved here unchanged.
- `references/{introduction,abstract,method,experiments,figures}.md`: fused with the file of the same name from
  source 1 under one outline (2026-11-15). Its numbered sections became named ones; pointers elsewhere use the names.
  Dropped as duplicates of source 1: the backward-then-forward section and the label table of `introduction.md`
  (labels `A:V1` etc. now sit on the headings of Parts A to C), the "before writing" questions of `abstract.md`.
  From source 1, the "Experiment Section Decomposition" diagram was dropped in favour of the six-move skeleton.
- `SKILL.md`: its Steps 0 to 8 are the workflow; source 1's core workflow, execution rules and output contract are
  folded into Steps 1, 4, 5, 7 and 8 and into "Rules".
- `LICENSE-base-skill`: identical to `LICENSE`, dropped.
