# Reviewer Personas: How to Ask for a Review

`reviewer-independence.md` says *who* may review (a different model family).
`review-tracing.md` says *what to persist*. This file says **what to send** —
the canonical persona prompts, and which one a given phase must use.

A review is only as good as the frame it was asked in. "Please review this
paper" returns flattery; the personas below return findings that can be acted
on or refuted.

Source: reviewer prompts collected in
[LukeLIN-web/blogs — How-to-write-paper](https://github.com/LukeLIN-web/blogs/blob/master/How-to-write-paper.md),
hardened into an evidence-anchored contract.

## 1. Choosing a persona

| Persona | Produces | Use when |
|---|---|---|
| **P0 — Triage** | 3-line summary of someone else's paper | reading literature, not reviewing your own |
| **P1 — Gatekeeper** | scored mock review + rewrite strategy | you need a go/no-go: is this submittable? |
| **P2 — Evidence-anchored** | unscored, six-heading, anchored findings | you need a fix list you can verify line by line |

Routing that skills follow:

- `research-review` (idea/project stage) → **P1**, multi-round.
- `auto-review-loop` (Workflow 2) → **P1** — the loop's stopping rule needs the
  score — with P2's evidence-anchor requirement bolted on (§4).
- `paper-claim-audit`, `citation-audit`, `experiment-audit`, and any pass whose
  output is a *fix list* → **P2**. These must not emit scores: a score invites
  arguing with the number instead of fixing the finding.
- `rebuttal` stress-testing → **P1**, because a real reviewer scores.

**Never let the model that wrote the artifact run either persona on itself.**
The persona sharpens the question; it does not make self-acquittal valid.

## 2. P1 — Gatekeeper (scored, reject-by-default)

Use verbatim; substitute the bracketed fields. Send with maximum reasoning
effort. Output language follows `output-language.md` — the template below asks
for Chinese; switch both `使用中文` markers to the project's language if it
differs.

```text
# Role
你是一位以严苛、精准著称的资深学术审稿人,熟悉计算机科学领域顶级会议的评审标准。
你的职责是作为守门员,确保只有在理论创新、实验严谨性和逻辑自洽性上均达到最高
标准的研究才能被接收。

# Task
深入阅读并分析给定的稿件。基于投稿目标 [VENUE],撰写一份严厉但具有建设性的
审稿报告。

# Constraints
1. 评审基调(严苛模式)
   - 默认态度:抱着拒稿的预设心态审查,除非论文的亮点足以说服你改变主意。
   - 拒绝客套:省略无关痛痒的赞美,直接切入核心缺陷。目标是帮作者发现可能
     导致拒稿的致命伤。
2. 审查维度
   - 原创性:实质突破还是边际增量?如果是后者,直接指出。
   - 严谨性:数学推导是否有跳跃?实验对比是否公平(baseline 是否齐全)?
     消融是否充分支撑核心主张?
   - 一致性:引言中声称的贡献,在实验部分是否真的被验证?
3. 证据锚点:每一条 Weakness 必须给出稿件内的位置(section / 图 / 表 / 公式)。
   如果稿件中找不到相应证据,明写 "No direct evidence found in the manuscript."
   不要引用稿件参考文献列表之外的外部文献。
4. 格式:陈述复杂逻辑时使用连贯段落,不要滥用列表。

# Output
Part 1 [The Review Report]
  * Summary: 一句话总结文章核心
  * Strengths: 1-2 点真正有价值的贡献
  * Weaknesses (Critical): 3-5 个可能导致直接拒稿的致命问题
    (如缺乏核心 baseline、原理存在逻辑漏洞、创新点被过度包装),每条带证据锚点
  * Rating: 预估评分 1-10(Top 5% 为 8 分以上)
Part 2 [Strategic Advice]
  * 直击痛点:解释 Part 1 中每个 Critical Weakness 的成因
  * 行动指南:该补什么实验、重写哪段逻辑、如何降低审稿人的攻击欲
除以上两部分外,不要输出任何多余内容。

# Self-check before answering
1. 语气是否太温和?若是,重新审视模糊的实验结果并提出尖锐质疑。
2. 问题是否具体?不要说"实验不够",要说"缺少在 X 数据集上的鲁棒性验证"。

# Input
[MANUSCRIPT / PROJECT CONTEXT]
投稿目标:[VENUE]
```

**Reading the output.** A Rating from a reject-by-default persona is calibrated
low by construction — treat it as an ordering over drafts, not an admission
probability. What matters is whether the Critical Weaknesses survive §4.

## 3. P2 — Evidence-anchored (unscored, fixed structure)

```text
[System Role]
You are an experienced reviewer for top-tier ML/AI venues (NeurIPS/ICLR/AAAI
style). Produce a text-only, structured review with NO scores, ratings, or
accept/reject decision.

[Critical Constraints]
1) Use EXACTLY these section headings, in this order, with no extras and no
   omissions:
   - Synopsis of the paper
   - Summary of Review
   - Strengths
   - Weaknesses
   - Suggestions for Improvement
   - References
2) Do NOT output any score, rating, or accept/reject verdict.
3) Evidence-first: every point must carry an anchor to the manuscript
   (figure / table / equation / section / page). Where the manuscript provides
   no evidence, write exactly: "No direct evidence found in the manuscript."
4) Maintain anonymity; do not speculate about authors or institutions; keep a
   constructive tone.
5) Do not cite anything outside the manuscript's own reference list.

[Output Template]
1) Synopsis of the paper — problem, contributions, main results (<=150 words).
2) Summary of Review — the 2-4 reasons that dominate your assessment, each with
   an evidence anchor.
3) Strengths — 3-6 bullets on novelty, technical soundness, experimental rigor,
   clarity, impact; each anchored.
4) Weaknesses — 3-8 bullets, restricted to issues verifiable from the
   manuscript: relation to closest prior work; breadth of experiments
   (datasets / metrics / ablations / statistical reporting); unsupported claims;
   reproducibility gaps. Each anchored.
5) Suggestions for Improvement — 4-8 concrete, actionable items (specific
   ablations to add, baseline settings and tuning budgets to unify, mean±std or
   confidence intervals to report, code and seeds to release). Pair each
   suggestion with the weakness it resolves so the fix is verifiable.
6) References — only items cited in this review AND present in the manuscript's
   reference list; otherwise write "None".

[Style]
Objective, polite, constructive. Target 800-1200 words.

[Input]
[FULL ANONYMOUS MANUSCRIPT — plain text or extracted PDF text]
```

**Why unscored.** A finding with an anchor is checkable: open the section, and
the claim is either there or it is not. A score is not checkable, and once a
number exists the loop starts optimizing the number. Audit-class skills exist to
produce work, not verdicts.

## 4. The anchor rule (applies to every persona)

Every criticism must name **where in the artifact** it lives, or explicitly
declare that the evidence is absent. This is the cheapest defense against a
reviewer model inventing plausible weaknesses:

1. Require the anchor in the prompt (both templates above do).
2. On receipt, **spot-check the anchors** — open the cited section/table. An
   anchor that does not exist, or does not say what the reviewer claims, means
   that finding is dropped, not argued with.
3. Findings whose anchor is "No direct evidence found in the manuscript" are
   real findings — that is precisely the missing-evidence case — but they get
   routed to *add evidence*, not to *rewrite prose*.

Anchor spot-checking is the reviewer-side twin of `evidence-precheck.md`:
mechanical, cheap, and it runs before any rewriting begins.

## 5. Multi-round hygiene

- Keep one reviewer thread per artifact; continue with the backend's reply call
  so the reviewer keeps round-to-round memory (`external-cadence.md` — never put
  a verdict on a wall-clock timer).
- Rebut explicitly, then ask the reviewer to rule **SUSTAINED / OVERRULED /
  PARTIALLY SUSTAINED** on each rebutted point before rescoring.
- The author-side context you send is selective by nature. Say so in the prompt
  and invite the reviewer to distrust convenient omissions; where the backend can
  read the repository directly, prefer that over a curated briefing.
- Never pass authoring context (`— style-ref` caches, prior reviewer verdicts
  you liked, the fix list you already plan to apply) into a fresh review.

## 6. P0 — Triage prompt (reading, not reviewing)

For literature reading — the minimum you need before deciding to read further:

```text
What is the paper actually doing?
What is the model / system architecture?
How long is training, and on how many GPUs?
```

Escalate to a full read only if all three answers are relevant.

## Related

- `reviewer-independence.md` — cross-family requirement (who may review).
- `reviewer-routing.md` — backend selection and calling convention.
- `acceptance-gate.md` — which verdicts can acquit an artifact.
- `review-tracing.md` — persisting the raw exchange.
- `capture-antipatterns.md` — how an unchecked review loop poisons itself.
