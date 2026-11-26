---
name: paper-jargon-pass
description: "Use when a paper reads fine to the author but a reviewer would stall on it — 论文术语审查/没定义就用的词和数字/审稿人读不懂/统一术语/undefined notation/jargon audit for papers. Catches terms and notation used before they are defined (figure canvases included), lab-internal vocabulary leaked into English, config numbers that arrive before the thing they configure is named, one word with several meanings, artifact-lineage phrases only the outputs/ tree can translate, and 废话/无中生有. Voice, cohesion and clarity rewriting is /paper-polish, which calls this skill. Three passes — assembly check, blind read of the compiled PDF, verify against code/data and rewrite."
argument-hint: "[paper 目录或 clone 目录,默认自动发现]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob
---

# 论文术语盲读审查(装配检查 → 盲读 PDF → 查证改写)

审查对象:**$ARGUMENTS**

## 何时用

单独审一篇论文:下表四步全做,顺序不变。被 `/paper-polish` 调用时只跑它点名的那一趟,不做验收(见它的 § 6)。

## 顺序

**顺序不可颠倒。** 先盲读、后看代码和实验产物。你(或作者)一旦读过 pipeline 的实现,就再也看不见术语了——每个自造词都会自动被脑补成"显然的意思",这正是它当初被写出来的原因。第一趟的唯一目的是保留"看不懂"这个信号,它一次性、不可再生。

| 趟 | 开始时读 |
|---|---|
| 第 0 趟:装配检查 | [references/pass0-assembly.md](references/pass0-assembly.md) |
| 第一趟:盲读 | [references/pass1-blind-read.md](references/pass1-blind-read.md)、[references/entry-types.md](references/entry-types.md) |
| 第二趟:查证 + 改写 | [references/pass2-verify-rewrite.md](references/pass2-verify-rewrite.md)、[references/entry-types.md](references/entry-types.md) |
| 验收 | [references/acceptance.md](references/acceptance.md) |
