# Reviewer Personas: How to Ask for a Review

`reviewer-independence.md` says *what may be sent* — raw artifacts, never the
executor's digest. `reviewer-routing.md` says *who may review* — backend, model
family, reasoning tier. `review-tracing.md` says *what to persist*. This file
says **how to frame the ask**: the canonical persona prompts, and which one a
given phase must use.

A review is only as good as the frame it was asked in. "Please review this
paper" returns flattery; the personas below return findings that can be acted
on or refuted.

Source: reviewer prompts collected in
[LukeLIN-web/blogs — How-to-write-paper](https://github.com/LukeLIN-web/blogs/blob/master/How-to-write-paper.md),
hardened into an evidence-anchored contract. P1 is kept in the Chinese it was
authored in; P2 is English. Neither is translated in either direction — a
persona template is sent verbatim, and `output-language.md` does not localize
it. The machine-read markers inside them (`Score:`, `Verdict:` and its enum, and
the `No direct evidence found in the manuscript.` sentinel) stay English in both,
per that file's "Machine-parsed markers" rule.

## 1. Choosing a persona

| Persona | Produces | Use when |
|---|---|---|
| **P0 — Triage** (§6) | three-question read/skip decision on someone else's paper | reading literature, not reviewing your own |
| **P1 — Gatekeeper** (§2) | scored mock review + rewrite strategy | you need a go/no-go: is this submittable? |
| **P2 — Evidence-anchored** (§3) | unscored, six-heading, anchored findings | you need a fix list you can verify line by line |

Skills that send a persona template:

- `research-review` → **P1** by default, multi-round; `— persona: P2` when the
  deliverable is a fix list rather than a verdict.
- `auto-review-loop` (Workflow 2) → **P1** — the loop's stopping rule needs the
  score — with P2's evidence-anchor requirement bolted on (§4). The loop
  *parses* the reply, so P1's Output block is machine-read: see the field
  contract in §2.
- `paper-claim-audit` → **P2**. It must not emit a score: a score invites
  arguing with the number instead of fixing the finding.

Skills that do **not** send a persona template, and must not be listed as if
they did. Each owns a machine-readable output contract that the six-heading
review shape would break; they inherit **§4 (the anchor rule) only**:

- `citation-audit` — a per-entry verdict ledger (`CITATION_AUDIT.json`).
- `experiment-audit` — a PASS/WARN/FAIL check table.
- `rebuttal` Phase 6 — stress-tests a response draft, not a manuscript.

Do not move a skill into the first list without wiring the pointer into its
`SKILL.md` in the same change. A routing table that names skills which never
read it is a second authority, not a routing table.

**Never let the model that wrote the artifact run either persona on itself.**
The cross-family requirement and its fallback table live in
`reviewer-routing.md`. The persona sharpens the question; it does not make
self-acquittal valid.

## 2. P1 — Gatekeeper (scored, reject-by-default)

Use verbatim; substitute the bracketed fields. **Do not translate the template**
— it is sent as written whatever the project's output language, and the field
names inside it are machine-read (see the field contract below). The reviewer's
reasoning tier is **not** set here either: it comes from the tier table in
`reviewer-routing.md` (deep-audit skills run `max`), and a skill's
`— effort:` never moves it (`effort-contract.md`).

**Field contract.** `auto-review-loop` parses this reply: `Score: X/10` and
`Verdict: ready | almost | not ready` must each appear exactly once, spelled as
below. A caller may require additional named fields — the loop asks for a
memory update and for verified/unverified claim lists. The template's closing
rule bans *prose* outside the two parts, not caller-required fields.

**Proposal-stage variant.** When the artifact is an idea or project context
rather than a manuscript there is no reference list and there are no sections:
anchors name the supplied context files instead, and Constraint 3's
external-literature ban is **lifted** — prior-work coverage is the whole point
of a review at that stage. State which variant is in force in the prompt.

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
   稿件自己提出了某个主张却没有给出支撑时,原样写下这一句:
   "No direct evidence found in the manuscript."
   这句话只表示**稿件缺证据**,不是用来提一条你自己也没有依据的批评:
   既锚不到具体位置、又不属于稿件侧证据缺口的意见,直接丢掉,不要写进来。
   不要引用稿件参考文献列表之外的外部文献。
4. 格式:陈述复杂逻辑时使用连贯段落,不要滥用列表。

# Output
Part 1 [The Review Report]
  * Summary: 一句话总结文章核心
  * Strengths: 真正有价值的贡献,最多 2 点
  * Weaknesses (Critical): 最多 5 个可能导致直接拒稿的致命问题
    (如缺乏核心 baseline、原理存在逻辑漏洞、创新点被过度包装),每条带证据锚点。
    只写真实存在的问题;如果不足 3 条,写 "Fewer than three fatal issues found"
    然后停下,不要为了凑数补条目。
  * Score: X/10(Top 5% 为 8 分以上)
  * Verdict: ready | almost | not ready
Part 2 [Strategic Advice]
  * 直击痛点:解释 Part 1 中每个 Critical Weakness 的成因
  * 行动指南:该补什么实验、重写哪段逻辑、如何降低审稿人的攻击欲
除以上两部分外,不要输出任何多余的**散文**。调用方明确点名要求的具名字段不算
多余内容,仍须照常输出。

# Self-check before answering
1. 语气是否太温和?若是,重新审视模糊的实验结果并提出尖锐质疑。
2. 问题是否具体?不要说"实验不够",要说"缺少在 X 数据集上的鲁棒性验证"。

# Input
[MANUSCRIPT / PROJECT CONTEXT]
投稿目标:[VENUE]
```

**Reading the output.** A Score from a reject-by-default persona is calibrated
low by construction — treat it as an ordering over drafts, not an admission
probability. `auto-review-loop` thresholds on it anyway (`>= 6` **and** a
verdict other than `not ready`) because a loop needs a stopping rule, not
because 6 means anything absolute. What matters is whether the Critical
Weaknesses survive §4.

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
   (figure / table / equation / section / page). Where the manuscript makes a
   claim it does not support, write exactly:
   "No direct evidence found in the manuscript."
   That sentinel reports a gap in the manuscript. It is NOT a way to file a
   point you have no basis for: if you can neither anchor a point nor state it
   as a manuscript-side evidence gap, drop the point.
4) Report only what the manuscript actually warrants. The bullet ranges below
   are ceilings, not quotas — returning fewer is correct when fewer are real.
5) Maintain anonymity; do not speculate about authors or institutions; keep a
   constructive tone.
6) Do not cite anything outside the manuscript's own reference list.

[Output Template]
1) Synopsis of the paper — problem, contributions, main results (<=150 words).
2) Summary of Review — the 2-4 reasons that dominate your assessment, each with
   an evidence anchor.
3) Strengths — up to 6 bullets on novelty, technical soundness, experimental
   rigor, clarity, impact; each anchored.
4) Weaknesses — up to 8 bullets, restricted to issues verifiable from the
   manuscript: relation to closest prior work; breadth of experiments
   (datasets / metrics / ablations / statistical reporting); unsupported claims;
   reproducibility gaps. Each anchored.
5) Suggestions for Improvement — up to 8 concrete, actionable items (specific
   ablations to add, baseline settings and tuning budgets to unify, mean±std or
   confidence intervals to report, code and seeds to release). Pair each
   suggestion with the weakness it resolves so the fix is verifiable.
6) References — only items cited in this review AND present in the manuscript's
   reference list; otherwise write "None".

[Style]
Objective, polite, constructive. Target 1000-1500 words. Spend the budget on
anchors and on the fix each suggestion resolves, not on restating the paper.

[Input]
[FULL ANONYMOUS MANUSCRIPT — plain text or extracted PDF text]
```

**Why unscored.** A finding with an anchor is checkable: open the section, and
the claim is either there or it is not. A score is not checkable, and once a
number exists the loop starts optimizing the number. Audit-class skills exist to
produce work, not verdicts.

## 4. The anchor rule (P1 and P2)

Every criticism must either name **where in the artifact** it lives, or be
stated as a gap in the artifact's own evidence. Nothing else may be emitted.
This is the cheapest defense against a reviewer model inventing plausible
weaknesses — which is also why neither template carries a minimum bullet count:
a floor is an instruction to invent.

On receipt, every finding lands in exactly one of three cases:

1. **Anchored, and the anchor checks out.** A real finding. Fix it.
2. **Anchored, but the anchor is wrong** — the cited section / table does not
   exist, or does not say what the reviewer claims. **Spot-check the anchors**
   by opening each cited location. A finding that fails this is *dropped, not
   argued with*. Speculation with no basis at all lands here too.
3. **`No direct evidence found in the manuscript.`** — the sentinel means *the
   manuscript makes a claim it does not support*, never *the reviewer has no
   basis for this criticism*. Both templates forbid the second use explicitly,
   so the string carries one meaning only. These are real findings, and they
   route to **add evidence**, not to *rewrite prose*.

Anchor spot-checking is the reviewer-side twin of `evidence-precheck.md`:
mechanical, cheap, and it runs before any rewriting begins.

## 5. Multi-round hygiene

- Keep one reviewer thread per artifact; continue with the backend's reply call
  so the reviewer keeps round-to-round memory (`external-cadence.md` — never put
  a verdict on a wall-clock timer).
- **Do not rebut in prose.** `reviewer-independence.md` forbids sending the
  executor's account of what changed, its reading of the previous critique, or
  any assertion that the current approach is sound. Instead re-submit the
  artifact and ask the reviewer to re-check each prior point *against the
  current files* and rule **SUSTAINED / OVERRULED / PARTIALLY SUSTAINED** before
  rescoring. The ruling has to come from re-reading, not from being argued with.
- A round inside an open thread is a **continuation**. Anything else is a
  **fresh review** and starts from an empty thread: never carry authoring
  context into one (`— style-ref` caches, prior reviewer verdicts you liked,
  the fix list you already plan to apply).
- The author-side context you send is selective by nature. Say so in the prompt
  and invite the reviewer to distrust convenient omissions; where the backend can
  read the repository directly, prefer that over a curated briefing.

## 6. P0 — Triage prompt (reading, not reviewing)

P0 produces no criticisms and no anchors, so §4 does not apply to it. For
literature reading — the minimum you need before deciding to read further:

```text
What is the paper actually doing?
What is the model / system architecture?
If it trains anything: how long, and on how many GPUs?
```

Escalate to a full read if **any** answer is relevant to your work. A paper
that trains nothing — a benchmark, a prompting method, a survey — simply has no
third answer, and that is not a reason to skip it.

## Related

- `reviewer-independence.md` — what may be sent to a reviewer (raw artifacts,
  never the executor's digest); the source of §5's no-prose-rebuttal rule.
- `reviewer-routing.md` — backend, model family, and reasoning tier.
- `effort-contract.md` — why a skill's `— effort:` never moves the reviewer tier.
- `output-language.md` — why these templates are English.
- `evidence-precheck.md` — the author-side twin of the anchor spot-check.
- `acceptance-gate.md` — which verdicts can acquit an artifact.
- `review-tracing.md` — persisting the raw exchange.
- `capture-antipatterns.md` — how an unchecked review loop poisons itself.
