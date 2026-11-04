# Source

Copied from https://github.com/Master-cai/Research-Paper-Writing-Skills
(`research-paper-writing/`, commit 77e7c2c1ba06f7d71844873147665437a03aac1b, 2026-11-01; still upstream HEAD on 2026-11-03).
MIT License, Copyright (c) 2026 Master-cai; see `LICENSE`. Writing knowledge from Prof. Peng Sida's open notes,
https://pengsida.notion.site/c1a22465a0fa4b15a12985223916048e (「论文写作模板」) and the pages it links.

To update: re-copy from upstream, then re-apply the local changes below (`diff -r` against a fresh upstream clone
shows them).

## Local changes

1. `SKILL.md`: `description` rewritten and a "Scope in this fork" section added after the title, restricting use to
   introduction structure, Experiments and figures (user ruling 2026-11-01).
2. Notes content upstream did not port, added 2026-11-03 from the Notion pages as fetched that day:
   - `SKILL.md`: "Writing Order" (the notes' 11-step table); Paragraph Clarity Check gains the transition and
     abrupt-noun questions and the encode -> analyze -> improve -> decode step (「如何改一篇论文的写作」); a Figures
     entry in Section Guides; the Introduction outline in Output Contract.
   - `references/introduction.md`: "From story to sentence plan" (「如何使用copilot和gpt辅助英语写作」, section on
     planning granularity); the traditional-methods note in Technical-Challenge Version 1; the loose-contributions
     note in Pipeline Version 2.
   - `references/examples/introduction/writing-plan-manhattansdf.md`, new (「写作思路典例」, Introduction part), and
     its entries in both example indexes.
   - `references/experiments.md`: variants as baselines for a new task; demos aimed at the downstream community
     (「怎么做吸引人的demo和application」); the reason for the ablation package and its sensitivity tables.
   - `references/figures.md`, new (「论文画图」 callout and the first-impression callout).
   - `references/paper-review.md`: rejection signal 1.3 (「怎么改论文」).

Not ported: the deadline timeline and lab progress table, the Copilot/GPT prompting screenshots, the private figure
template, the linked PDFs (Bill Freeman, SIGGRAPH paper chairs, Writing Science), and the Related Work and Method
parts of 「写作思路典例」.
