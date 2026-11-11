---
name: rebuttal
description: "Workflow 4: Submission rebuttal pipeline. Parses external reviews, enforces coverage and grounding, drafts a safe text-only rebuttal under venue limits, and manages follow-up rounds. Use when user says \"rebuttal\", \"reply to reviewers\", \"ICML rebuttal\", \"OpenReview response\", or wants to answer external reviews safely."
argument-hint: "[paper-path-or-review-bundle]"
allowed-tools: Bash(*), Read, Grep, Glob, Write, Edit, Skill, mcp__codex__codex, mcp__codex__codex-reply, mcp__manual_review__review, mcp__manual_review__review_reply, mcp__antigravity__antigravity, mcp__antigravity__antigravity-reply, mcp__grok__grok, mcp__grok__grok-reply, mcp__claude-review__review, mcp__claude-review__review_reply, mcp__claude-review__review_start, mcp__claude-review__review_reply_start, mcp__claude-review__review_status
---

# Workflow 4: Rebuttal

> **Before each reviewer slot**, follow [Selectable Reviewers](../shared-references/reviewer-backends.md):
> resolve invocation → `.aris/reviewer.json` → Claude Code default (Codex MCP)
> with `reviewer_route.py` through the canonical helper resolver, preserving this
> slot's tier, fresh contexts, source/image inputs and deterministic gates.
> Codex examples/pins below apply only to `backend=codex`; other routes use their
> own first-call/reply contract. Save the route and actual returned identity;
> unavailable selections are `REVIEW_UNAVAILABLE`. Classify acceptance from actual
> families/completion/scope. Forward invocation reviewer/model/effort overrides
> to reviewer-bearing children. Generation workers are unchanged.


Prepare and maintain a grounded, venue-compliant rebuttal for: **$ARGUMENTS**

## Scope

This skill is optimized for:
- **text-only rebuttal** under strict character/word limits (e.g. ICML single-document)
- **per-reviewer thread responses** where each reviewer renders independently (e.g. OpenReview-style)
- **multiple reviewers** with shared and reviewer-specific concerns
- **follow-up rounds** after the initial rebuttal
- safe drafting with **no fabrication**, **no overpromise**, and **full issue coverage**

This skill does **not**:
- run new experiments automatically
- generate new theorem claims automatically
- edit or upload a revised PDF
- submit to OpenReview / CMT / HotCRP

If the user already has new results, derivations, or approved commitments, the skill can incorporate them as **user-confirmed evidence**.

## Lifecycle Position

```text
Workflow 1:   idea-discovery
Workflow 1.5: experiment-bridge
Workflow 2:   auto-review-loop (pre-submission)
Workflow 3:   paper-writing
Workflow 4:   rebuttal (post-submission external reviews)
```

## Constants

- **VENUE = `ICML`** — Default venue. Override if needed.
- **RESPONSE_MODE = `TEXT_ONLY`** — v1 default.
- **REVIEWER_MODEL = `gpt-6-astra`** — Default model for the Codex backend. Used for internal stress-testing. Manual backend uses a model the user chooses — it must be a recognized model from a different family (OpenAI, Anthropic, Google, DeepSeek, Moonshot/Kimi, Qwen).
- **REVIEWER_BACKEND = `codex`** — Default: Codex MCP (xhigh). Override with `— reviewer: oracle-pro` for Oracle MCP, or `— reviewer: manual` for Manual Review MCP. If manual-review MCP is unavailable, stop and print the install command; do not fall back to Codex. See `shared-references/reviewer-routing.md`.
- **MAX_INTERNAL_DRAFT_ROUNDS = 2** — draft → lint → revise.
- **VENUE_MODE = `single_document`** — `single_document` for one shared author response, or `per_reviewer_thread` when each reviewer thread renders independently. Confirm the venue/interface before drafting if unclear. Affects Phase 4/7 output shape.
- **STRESS_TEST_ROUNDS_BASE = 1** — One external reviewer critique round on the full response set. Add focused rounds for `reviewer_priority: pivotal` responses, terminating when the reviewer returns no new substantive issues. Hard cap at 5.
- **MAX_FOLLOWUP_ROUNDS = 3** — per reviewer thread.
- **AUTO_EXPERIMENT = false** — When `true`, automatically invoke `/experiment-bridge` to run supplementary experiments when the strategy plan identifies reviewer concerns that require new empirical evidence. When `false` (default), pause and present the evidence gap to the user for manual handling.
- **QUICK_MODE = false** — When `true`, only run Phase 0-3 (parse reviews, atomize concerns, build strategy). Outputs `ISSUE_BOARD.md` + `STRATEGY_PLAN.md` and stops — no drafting, no stress test. Useful for quickly understanding what reviewers want before deciding how to respond.
- **REBUTTAL_DIR = `rebuttal/`**
- **RENDER_HTML = true** — When `true` (default), Phase 9 renders each canonical response file to HTML. Set `false`, or pass `— render html: false`, to skip.

> Override: `/rebuttal "paper/" — venue: NeurIPS, character limit: 5000`

## Reviewer Calling Convention

When calling the reviewer for stress-testing, branch on REVIEWER_BACKEND:

**If REVIEWER_BACKEND = `codex`:**
  Use `mcp__codex__codex` for new review threads.
  Use `mcp__codex__codex-reply` for follow-up rounds (reuse threadId).

**If REVIEWER_BACKEND = `manual`:**
  Use `mcp__manual_review__review` for new review threads with:
    prompt: [exact same prompt that would go to Codex]
    config: {"model_reasoning_effort": "xhigh", "executor_model": "<actual executor model>", "require_reviewer_model": true}
  Save the returned `threadId`.
  Use `mcp__manual_review__review_reply` for follow-up rounds with:
    threadId: [saved manual-review threadId]
    prompt: [follow-up prompt]
    config: {"model_reasoning_effort": "xhigh", "executor_model": "<actual executor model>", "require_reviewer_model": true}

Prompt fidelity: the manual prompt must be exactly the same text that Codex would receive.
Review tracing applies equally to both backends.

## Required Inputs

1. **Paper source** — PDF, LaTeX directory, or narrative summary
2. **Raw reviews** — pasted text, markdown, or PDF with reviewer IDs
3. **Venue rules** — venue name, character/word limit, text-only or revised PDF allowed, rendering mode (one shared response or independent reviewer threads)
4. **Current stage** — initial rebuttal or follow-up round

If venue rules, limit, or rendering mode are missing, **stop and ask** before drafting.

## Safety Model

Three hard gates — if any fails, do NOT finalize:

1. **Provenance gate** — every factual statement maps to: `paper`, `review`, `user_confirmed_result`, `user_confirmed_derivation`, or `future_work`. No source = blocked.
2. **Commitment gate** — every promise maps to: `already_done`, `approved_for_rebuttal`, or `future_work_only`. Not approved = blocked.
3. **Coverage gate** — every reviewer concern ends in: `answered`, `deferred_intentionally`, or `needs_user_input`. No issue disappears.

## Reference Files

Detailed rules live next to this file. Each phase below names the file it requires; read it at that point, not from memory.

| File | Read at | Covers |
|---|---|---|
| [references/rhetoric.md](references/rhetoric.md) | Phase 4, Phase 8 | 话术: answer shape, thanks opener, persuading moves (P1–P4), refuting moves (R1–R10), anti-patterns, phrase bank, co-author and user-edit lessons (C1–C27), user rulings on cost and run wording (C28–C29), drafting moves from co-author text (C30–C33), secondary evidence only when asked (C34) |
| [references/comparison-rules.md](references/comparison-rules.md) | Phase 4, Phase 5 lint 13 | minimum evidence, one metric per reply, one measurement setup for every arm, intervals, ties, weak number vs best of the rest, words agree with numbers |
| [references/wording-pass.md](references/wording-pass.md) | Phase 6.5, Phase 8 | wording pass on the finished draft, for the drafter: order of the steps, reconcile, tighten filler, reword (delete → replace → define), one owner per number; what is never touched; acceptance; lessons L1–L11 from the first run |
| [references/blind-read.md](references/blind-read.md) | Phase 6.5 blind read and acceptance read — handed to the blind-read subagent, which gets no other method file | who the reader is, the three signals to record, ledger format |
| [references/followup-and-endgame.md](references/followup-and-endgame.md) | Phase 7, Phase 8 | posting order, delta replies, nudges, score requests, AC closing note, co-author comments on a shared draft |
| [references/misconduct-reporting.md](references/misconduct-reporting.md) | Phase 2 (`bad_faith_suspected`), on user request | strict vs malicious triage, evidence pack, channel and timing, note to the AC, what never to do |
| [references/case-vqtoken-neurips2025.md](references/case-vqtoken-neurips2025.md) | with rhetoric.md | worked example: a NeurIPS 2025 thread, what worked and what failed |

## Artifacts

The response text is **authored in exactly one place** — the canonical file(s) for the active `VENUE_MODE`. Every other representation is a **derived view**: regenerated mechanically from its source whenever the source changes, and never hand-edited. All edits (internal revise rounds, stress-test fixes, follow-ups) land in the canonical file. Do not create any response-bearing file outside this table.

The rule covers **measurements** of the response, not only its text. Character counts, word counts and per-file lengths are derived facts that own no file: measure them at the moment a decision depends on them, and let the number die with the check. A count written into any document is wrong as soon as the response is edited, and whoever reads it next — including you on resume — will take it for fact.

| File | Mode | Role |
|---|---|---|
| `REBUTTAL_STATE.md` | both | canonical — phase, venue rules, round, stress-test verdicts. Never record anything measurable from the response files (character or word counts, per-file lengths) |
| `REVIEWS_RAW.md`, `FOLLOWUP_LOG.md` | both | canonical — verbatim reviewer text |
| `ISSUE_BOARD.md` | both | canonical — atomized concerns |
| `STRATEGY_PLAN.md` | both | canonical — themes, response modes, budgets |
| `REVISION_PLAN.md` | both | canonical — promised paper edits (checklist) and the internal log of errors no reviewer raised |
| `REBUTTAL_DRAFT.md` | single_document | **canonical response text** — the only authored copy; over-limit material inline, marked `[OPTIONAL — cut if over limit]` |
| `PASTE_READY.txt` | single_document | derived — `REBUTTAL_DRAFT.md` minus `[OPTIONAL]` blocks, markdown stripped, exact character count |
| `Reviewer_<ID>_response.md` | per_reviewer_thread | **canonical response text** — one self-contained file per reviewer; each file IS the paste target for its thread (no aggregate draft, no `PASTE_READY.txt`) |
| `SETUP_METRICS_BLOCK.md` | per_reviewer_thread | canonical — shared setup/metrics text; the copies embedded in reviewer files are derived inclusions (the one sanctioned duplication): edit only the block, then re-propagate to every reviewer file that embeds it |
| `MCP_STRESS_TEST_round<N>.md` | both | canonical — verbatim stress-test transcripts (Phase 6) |
| `wording/<UTC timestamp>/ledger-<ID>.md` | both | canonical — blind-read ledgers of the wording pass (Phase 6.5); findings and dispositions only, no response text |
| `SUPPLEMENTARY_FIG_PDF/` | per_reviewer_thread, optional | derived — venue-compliant figure PDF (Phase 7); no response text |
| `*.html` (+ `.review.json` sidecar) | both, if `RENDER_HTML` | derived — Phase 9 render of each canonical response file |
| `COLLAB_DOC.md` (+ `collab_doc.json`) | both | the collaborator doc (Phase 4 "Collaborator doc"): its board prose is canonical here; every draft and translation section between `<!-- DRAFT:<file> -->` markers is derived, rewritten by `scripts/collab_doc_sync.py`, which also pushes the doc to its HackMD note(s). `collab_doc.json` holds the note ids and the last-pushed hashes, never a token |

## Workflow

### Phase 0: Resume or Initialize

1. If `rebuttal/REBUTTAL_STATE.md` exists → resume from recorded phase
2. Otherwise → create `rebuttal/`, initialize the canonical documents for the active `VENUE_MODE` (Artifacts table) — never the other mode's files
3. Load paper, reviews, venue rules, any user-confirmed evidence

### Phase 1: Validate Inputs and Normalize Reviews

1. Validate venue rules are explicit
2. Normalize all reviewer text into `rebuttal/REVIEWS_RAW.md` (verbatim)
3. Record metadata in `rebuttal/REBUTTAL_STATE.md`
4. If ambiguous, pause and ask

### Phase 2: Atomize and Classify Reviewer Concerns

Create `rebuttal/ISSUE_BOARD.md`.

For each atomic concern:
- `issue_id` (e.g., R1-C2)
- `reviewer`, `round`, `raw_anchor` (short quote)
- `asked_for`: what the raw text literally requests, and nothing more. Name the object (which baselines, which experiment, which analysis) and add a metric or granularity only if the reviewer named one. "Compare with X and Y" → `asked_for: comparison with X, Y; metric not specified`. This field decides what "explicitly asked" covers under Phase 4 "Never expose a weakness".
- `issue_type`: assumptions / theorem_rigor / novelty / empirical_support / baseline_comparison / complexity / practical_significance / clarity / reproducibility / other
- `severity`: critical / major / minor
- `reviewer_stance`: positive / swing / negative / unknown / bad_faith_suspected
  - `bad_faith_suspected` — the review contains verifiable false claims about the paper, hallucinated references, content-free or LLM-generated text, hostile language, or pressure. A merely strict reviewer is `negative`, not this. Triage and reporting: [references/misconduct-reporting.md](references/misconduct-reporting.md). Every card still gets a public answer.
- `reviewer_priority`: standard / pivotal
  - `pivotal` — a reviewer whose response is likely to affect the decision if addressed well: low or borderline rating, addressable concerns, and enough confidence/influence to matter. Phase 3 allocates extra drafting and stress-test budget here.
- `response_mode`: direct_clarification / grounded_evidence / nearest_work_delta / assumption_hierarchy / structural_distinction
  - `structural_distinction` — for "your method reduces to X / is just generic Y / is subsumed by Z" attacks. Pattern: do not agree to the reduction; state the structural feature your parameterization preserves that X/Y/Z does not capture, backed by a concrete mechanism (theorem dependency, derivation step, or empirical consequence). Never use rhetorically without the supporting mechanism.
- `status`: open / answered / deferred / needs_user_input

### Phase 3: Build Strategy Plan

Create `rebuttal/STRATEGY_PLAN.md`.

1. Identify 2-4 **global themes** resolving shared concerns
2. Choose **response mode** per issue
3. Build **character budget** (10-15% opener, 75-80% per-reviewer, 5-10% closing) — applies in `single_document` mode; in `per_reviewer_thread` mode, set per-thread word/char targets instead
4. **Identify pivotal reviewer(s)** — reviewers whose vote or confidence shift would most affect the decision, especially when concerns are addressable rather than ideological. Mark them `reviewer_priority: pivotal` in `ISSUE_BOARD.md`. There may be more than one. Allocate disproportionate drafting + stress-test budget here.
5. **Story: argue what we can win** (user 2026-11-07: 「都是故事上 强调novelty，强调和过去工作的提升，可以吵赢的」). The narrative of every reply leans on the paper's novelty and its improvement over prior work — the arguments we can win. Write each global theme as one of these; pair with "Never expose a weakness" (Phase 4).
6. **Check instance-level complaints by hand** (「单个样本之类的需要手动check下具体咋回事」). When a concern cites a specific sample, example, prompt, video or table cell, open that exact instance and see what actually happened before choosing a response mode; do not answer it from aggregate statistics or from the reviewer's description. Record the finding in the issue card. The same holds for implementation questions ("which parameters are trained", "how is X computed", "what does the checkpoint contain"): answer from the training script, the framework source for any flag whose meaning matters, and the released artifact — never from the paper's own wording, which is what the reviewer is questioning ([references/rhetoric.md](references/rhetoric.md) C14).
7. **Pick the lever per reviewer** (「他给1分不太对，但是不是扳不回来 2分哥，看起来是只要补实验就可以 1分哥，主要是要和他掰扯到毛病挑不出来」). A low score is not final. For each negative-score reviewer, write in `STRATEGY_PLAN.md` which lever moves them:
   - `experiments` — the concerns are missing evidence (e.g. a typical 2): run what they asked for; the reply mostly reports it.
   - `argument` — the concerns attack soundness or claims (e.g. a typical 1): go through every objection and close it — refuted with evidence already in the paper or the sprint, or closed with an approved fix — until nothing is left to fault. No point goes unanswered.
8. **Posting order** (「先一个一个回复，看正分审稿人愿不愿意confirm，他们一般confirm之后就不动了. 然后麻烦的负分先留到最后」). Post replies one reviewer at a time, positive-score reviewers first: once they confirm their score they rarely move again. The difficult negative-score reviewers go last. Record the order in `STRATEGY_PLAN.md`; drafting may run in parallel, posting follows the order (Phase 7).
9. Identify **blocked claims** (ungrounded or unapproved)
10. If unresolved blockers → pause and present to user
  A verdict-bearing manual response MUST begin with
  `Reviewer-Model: <exact-model-id>` — pass the model THIS session is actually
  running as in `executor_model`. Missing, unknown, or same-family identity
  cannot acquit; emit `REVIEW_UNAVAILABLE` rather than guessing. If the executor
  model cannot be named, manual review's cross-family claim is unprovable — say
  so in the report instead of asserting it.


**QUICK_MODE exit**: If `QUICK_MODE = true`, stop here. Present `ISSUE_BOARD.md` + `STRATEGY_PLAN.md` to the user and summarize: how many issues per reviewer, shared vs unique concerns, recommended priorities, and evidence gaps. The user can then decide to continue with full rebuttal (`/rebuttal — quick mode: false`) or write manually.

### Phase 3.5: Evidence Sprint (when AUTO_EXPERIMENT = true)

**Skip entirely if `AUTO_EXPERIMENT` is `false` — instead, pause and present the evidence gaps to the user.**

If the strategy plan identifies issues that require new empirical evidence (tagged `response_mode: grounded_evidence` with `evidence_source: needs_experiment`):

1. Generate a mini experiment plan from the reviewer concerns:
   - What to run (ablation, baseline comparison, scale-up, condition check)
   - Success criterion (what result would satisfy the reviewer)
   - Estimated GPU-hours

2. Invoke `/experiment-bridge` with the mini plan:
   ```
   /experiment-bridge "rebuttal/REBUTTAL_EXPERIMENT_PLAN.md"
   ```

3. Wait for results, then update `ISSUE_BOARD.md`:
   - Tag completed experiments as `user_confirmed_result`
   - Update evidence source for relevant issue cards

4. If experiments fail or are inconclusive:
   - Do NOT fabricate positive results
   - A point estimate in our favor is a win, not an inconclusive result, even when its 95% interval includes 0 ([references/comparison-rules.md](references/comparison-rules.md) says how to write it).
   - The result exposes a weakness, so it stays out of every response file (Phase 4 "Never expose a weakness"); answer the concern on the evidence we have. If the reviewer explicitly asked for this experiment, mark the issue `needs_user_input` and let the user decide whether and how to report it (answered without any concession, "Never concede")

5. Save experiment results to `rebuttal/REBUTTAL_EXPERIMENTS.md` for provenance tracking.

**Time guard**: If estimated GPU-hours exceed rebuttal deadline, skip and flag for manual handling.

### Phase 4: Draft Initial Rebuttal

Author the canonical response file(s) (see Artifacts):

- `single_document` — one `REBUTTAL_DRAFT.md`:
  1. Short opener — thank reviewers + 2-4 global resolutions
  2. Per-reviewer numbered responses — answer → evidence → implication
  3. Short closing — resolved / remaining / acceptance case
  - Material worth keeping but over the strict limit stays inline, marked `[OPTIONAL — cut if over limit]`. There is no separate "rich"/"strict" pair of drafts — the strict paste text is derived.

- `per_reviewer_thread` — one self-contained `Reviewer_<ID>_response.md` per reviewer:
  1. Brief acknowledgment of that reviewer's main thrust
  2. One section per W#/Q# (grouped as `**W1 + Q1**` when one answer covers both): the label, then the reviewer's original text quoted verbatim in a blockquote (copied from the raw review — never paraphrased; ellipsize only overlong passages), then the answer as `**A1:**`, `**A2:**`, ... (answer → evidence → implication)
  3. Optional shared experimental-setup paragraph (see "Reusable setup block" below)
  - Quoted review text counts toward the paste-box character limit — budget for it before drafting.
  - Each file must be readable standalone. No "see Reviewer X's response" references. No global opener. No aggregate draft on top of these files — run metadata (round, stress-test verdicts) goes in `REBUTTAL_STATE.md`. Per-file character counts do not: recount them from the files each time you need to check the limit.

**Rhetoric** — read [references/rhetoric.md](references/rhetoric.md) before drafting (user 2026-11-09: 「主要是学习各种话术. 怎么说服, 反驳」). It holds the answer shape (verdict-first, thanks opener, paragraph length), the persuading and refuting moves, and the anti-patterns the Phase 5 lints check. The reader of every reply is the AC: what is answered with a promise instead of a number is what the meta-review lists as unresolved.

**Reusable setup block (per_reviewer_thread mode).**
If multiple reviewer-thread responses need the same experimental setup or metric definitions, write a canonical `SETUP_METRICS_BLOCK.md`. Reuse it consistently in each reviewer file that needs it. Target ≤ 150 words; expand only with genuinely reviewer-specific additions inline. Change-once-update-everywhere prevents drift across threads.

**Shared evidence across threads (per_reviewer_thread mode).**
When one result or analysis answers concerns from multiple reviewers, it appears at exactly one depth per thread:
1. **Primary thread** — the reviewer whose issue card owns the most direct ask. This file carries the full treatment: protocol sentence, key numbers, honest caveat.
2. **Every other thread** — a 1–2 sentence citation recomposed in *that* reviewer's framing, carrying only the number(s) that answer their specific ask. Write it fresh from the evidence doc; never transplant sentences from another reviewer file.

Self-contained means the reviewer can follow the response without opening another thread — not that every thread repeats the full result. Reviewers and the AC read all threads; near-verbatim repetition reads as boilerplate and burns each thread's character budget. The only sanctioned verbatim duplication across reviewer files is the `SETUP_METRICS_BLOCK.md` inclusion.

**Reviewer-defensive moves:**
- **Never expose a weakness** (user 2026-11-07: 「所有暴露缺点的都不提. 如果 reviewer 明确要了, 那给 user 定」). Nothing in a response file reveals a weakness of our work unless the reviewer explicitly asked for that exact thing. Weaknesses include: a metric or comparison a baseline (or a trivial reference such as a constant predictor) wins; a failed, inconclusive or negative rebuttal experiment; an error we found in our own paper, data or prompts; a caveat or limitation the reviewer did not raise; a model or variant we tried and dropped. Leave it out entirely — no figures AND no qualitative acknowledgment (no "trails", "lower than", "not as strong as", "however", "one limitation is" phrasing): report our own number, anchor comparisons on the metrics we win, and state the claim in positive scope terms ("the judge's validated strength is X"), which requires no reference to the opponent. If the reviewer explicitly asked for it (the unfavorable number itself, the experiment that came out negative, the flaw they named), do not decide alone: mark the issue `needs_user_input`, put the options in `ISSUE_BOARD.md`, and write it only the way the user rules. Conceding is never an option ("Never concede").
- **Never concede** (user 2026-11-07: 「不能有任何让步」). No sentence in a response file, and no edit in a revised PDF, agrees that a criticism of our work is right, retracts or narrows one of our claims, adopts the reviewer's deflating term for it, credits our design to prior work, or admits a limitation, an error or an unfinished part. This holds even when the reviewer is right on a local point, and for the words alone ("we agree", "we accept", "correct", "the reviewer is right", "we concede"), including apologies ("sorry for the misunderstanding", "we apologize", "we regret the confusion"), which concede and also tell the AC the reviewer misread. Answer with what holds: the evidence we win on, stated in positive scope terms. A missing citation is answered with "we will cite X" and nothing more (「漏引的就说会引用就好了」): no admission that it was missing, no credit of our design to it. **Exception — a change the reviewer explicitly requested, answered in the reviewer's own word** (user 2026-11-09: 算「审稿人明确要求的修改，用他的原词回应」). When the review asks for a presentation change in so many words ("Please reconcile these descriptions", "clarify", "make consistent", "add"), the reply may report that change using the reviewer's verb: "Per your comment, we have reconciled the two descriptions … so the two places use the same wording." This answers the request; it is not a concession. It still never says the earlier text was wrong, an error, a mistake, incorrect or inconsistent, and never "we agree"; it quotes the revised text instead (rhetoric C16). Revision promises that add material (a table, a citation, a new result) stay; a promise that retracts or qualifies a claim is a concession and is not made. When the reviewer explicitly asked for a result that goes against us, the user still decides whether it is reported ("Never expose a weakness"), and the reply never frames it as a concession.
- **What "explicitly asked" covers** (user 2026-11-07). Read it off the issue card's `asked_for`, which comes from the raw text, never from a paraphrase. "Compare with X" makes the comparison with X mandatory, but leaves the metric to us. A metric we lose on is "asked for" only when the reviewer named that metric or granularity ("report rank correlation", "does it order the models correctly"). Before telling the user "the reviewer asked for Y", quote the sentence that asks for Y. If no sentence does, the losing number is an ordinary weakness: leave it out without escalating.
- **Choosing what to compare on** — once a comparison is mandatory, follow [references/comparison-rules.md](references/comparison-rules.md): one metric for every baseline in a reply, every win written (interval printed only when it excludes 0), no ties stated, no number that shows the flagship losing, words agree with numbers, and a weak number of ours is placed next to the best other methods reach on the same quantity ("Weak number → the best of the rest is weaker still", user 2026-11-09, on a W2 reply: 「如果说不好, 就写 别人的最好的也不如我们好」).
- **Rulings reach every draft.** When the user rules on an open question, record the ruling in `ISSUE_BOARD.md` (with the draft wording) and `REBUTTAL_STATE.md` right away. Then check every response file already written against it, including files another session drafted, and update them.
- **Limitations items are weaknesses.** When a reviewer lists Limitations (or asks that something "be stated explicitly"), answer each item on the merits exactly like a W#: 1-2 sentences of positive argument per item, grounded in numbers already in the response (framing like "Our position on each:"). Never reply with promise-to-revise phrasing ("will be written into the Limitations section", "becomes an explicit statement in the revised Limitations", "we will state in Limitations") — a promise-to-revise reads as conceding the point instead of defending it. The corresponding paper edit, if the author approves one, is tracked in `REVISION_PLAN.md` only and marked `unpromised`. Revision promises attached to W#/Q# answers ("We will add CIs to the law tables") remain allowed and stay future tense.

Hard rules:
- NEVER invent experiments, numbers, derivations, citations, or links
- NEVER promise what user hasn't approved
- If no strong evidence exists, say less not more

After authoring or changing a canonical draft, regenerate its derived artifacts per the Artifacts table (`single_document`: `PASTE_READY.txt`).

**Collaborator doc** (user 2026-11-09 … 11-11: 「发个 doc 给合作者改」「弄好看点, 分段, 空行」「你不能每次都换啊, 你以后还是要保持 link」「解决了的就删掉」「不要写优点啊, 没意义. 也不要写我们要做的事情」「以后不用更新 doc 了, 就更新这个 md, 你可以写个脚本直接本地 md 同步」「以后就要创建这么一个doc 给合作者」). Every rebuttal gets one, created once the first drafts exist, in the team's language, as `rebuttal/COLLAB_DOC.md` pushed to HackMD:
1. **Layout, in this order:** a header (scores and confidences, which replies are ready, the posting order, what to strip before pasting); a legend of the baseline and arm names the drafts use; *Open decisions* (only what still needs the user; a settled item leaves, its ruling stays in `ISSUE_BOARD.md`); the general response and any AC note; one section per reviewer in posting order with a one-line role ("most likely to move", lever), *Weaknesses* and *Questions* as numbered W#/Q# summaries in the team's language, then the English draft and its translation; experiments in flight; results already in. No strengths and no to-do lists in a reviewer section. Short paragraphs with blank lines between them; numbers in tables.
2. **Drafts are derived.** Each draft or translation is one `<!-- DRAFT:<file> -->` … `<!-- /DRAFT -->` block that `scripts/collab_doc_sync.py <rebuttal_dir> --push` rewrites from the canonical response file (heading with the comment count, one label per PART, `⟦PROMISE⟧` / `⟦NEEDS USER⟧` markers as inline-code chips). After every change to a response file or a translation, rerun it; never edit a draft in the doc or on HackMD. A translation whose `<!-- EN <hash> -->` line is stale stops the push.
3. **One link for the whole rebuttal.** `--create` makes the note once (owner-only; the user widens sharing); later runs update it in place and never re-create it. HackMD rejects an update over 100 KB, so a long doc sets `translation_note` in `collab_doc.json`: the translations move to a second note and the main note keeps each one's heading and a link.
4. **Collaborators edit on HackMD; the local files stay the sources.** The script stops when a note changed since its last push and saves it as `COLLAB_DOC.md.remote.md`: carry board edits into `COLLAB_DOC.md` and draft edits into the response files by hand (a co-author's sentence is never reworded, [references/wording-pass.md](references/wording-pass.md) § 0), then push with `--force`. Comment threads are answered in the canonical files and get a reply on HackMD; § 7 of [references/followup-and-endgame.md](references/followup-and-endgame.md) applies.

Also generate `rebuttal/REVISION_PLAN.md` — the **overall revision checklist**.

This document is the single source of truth for every paper revision promised (explicitly or implicitly) in the rebuttal draft. It exists so the author can track follow-through after the rebuttal is submitted, and so the commitment gate in Phase 5 has a concrete artifact to validate against.

Structure:

1. **Header** — paper title, venue, character limit, rebuttal round.

2. **Overall checklist** — one flat GitHub-style checklist, one atomic paper edit per line, each carrying its `issue_id`, target section, commitment tag, and status:

   ```markdown
   ## Overall Checklist

   - [ ] (R1-C2) Add assumption hierarchy table to §3.1 — commitment: `approved_for_rebuttal` — status: pending
   - [ ] (R2-C1) Clarify novelty delta vs. Smith'24 in §2 related work — commitment: `already_done` — status: verify wording
   - [ ] (R3-C4) Add runtime breakdown figure to Appendix B — commitment: `future_work_only` — status: deferred, note in camera-ready
   ```

3. **Commitment summary** — counts of `already_done` / `approved_for_rebuttal` / `future_work_only`, plus any blocking `needs_user_input` items.

4. **Out-of-scope log** — reviewer concerns that will **not** trigger a paper revision (e.g. `deferred_intentionally`, a point answered by argument with no edit), with a one-line reason each. This keeps the checklist honest: nothing silently disappears.

5. **Unraised errors (internal)** — errors and inconsistencies in the paper that no reviewer raised, including those found while making the promised edits: location, what is wrong, evidence pointer, one line each. The revised PDF does not fix them and no response file mentions them ("Never expose a weakness"); the user decides whether they go into the camera-ready.

Rules for `REVISION_PLAN.md`:
- Every checklist item must map to at least one `issue_id` from `ISSUE_BOARD.md`.
- Every promise in the canonical draft(s) that implies a paper edit must appear as a checklist item — if it is not in the plan, it is a commitment-gate violation.
- Never add items that are not backed by the draft, by user-confirmed evidence, or by a user-approved edit deliberately kept out of the response text (mark these `unpromised` — e.g. Limitations defenses).
- On rerun / follow-up rounds, update checkbox state in place rather than regenerating from scratch.
- **A revised PDF edits only what a reviewer raised** (user 2026-11-07: 「论文不要乱改, 只改 reviewer 提出的. 没提的错误就写到内部文档」). Every change between the submitted version and the revised PDF traces to a checklist item, and through it to an `issue_id`. An error no reviewer raised goes to the Unraised errors section, not into the paper, even when the fix is one word and sits next to an edit being made. Before the revised PDF goes to the user, diff it against the submitted version and match every hunk to an item.

### Phase 5: Safety Validation

Run all lints:
1. **Coverage** — every issue maps to draft anchor
2. **Provenance** — every factual sentence has source
3. **Commitment** — promises are approved AND every paper-edit promise in the draft appears as a checklist item in `REVISION_PLAN.md` (and vice versa — no orphan items in the plan, except items marked `unpromised`: edits the author will make that the response text deliberately does not promise, per the Limitations rule)
4. **Tone** — flag aggressive/submissive/evasive phrases
5. **Consistency** — no contradictions across reviewer replies
6. **Limit** — exact character count on the paste target(s): freshly derived `PASTE_READY.txt`, or each `Reviewer_<ID>_response.md`. Compress if over (redundancy → friendly → opener → wording, never drop critical answers)
7. **Thread-local context** (`per_reviewer_thread` mode only) — each reviewer file must be intelligible without reading any other reviewer file. Flag any "see Reviewer X" references or undefined terms that rely on cross-thread context.
8. **Adversarial design-choice scan** — for each experimental claim, ask: "Could a hostile reviewer find a non-obvious design choice (compute-match, frozen subset, sampling protocol) that I haven't disclosed?" If yes and the choice is a neutral setup fact, add one line to the Setup paragraph; if stating it would expose a weakness, leave it out (Phase 4 "Never expose a weakness"). Narrower than provenance; focused on *design choices* not factual sources.
9. **Cross-thread duplication** (`per_reviewer_thread` mode only) — compare reviewer files pairwise: any sentence of ~15+ words appearing near-verbatim in more than one file, outside the `SETUP_METRICS_BLOCK.md` inclusion, fails. Fix by keeping the full treatment in the primary thread and recomposing the other occurrences per the shared-evidence recipe (Phase 4).
10. **Weakness scan** — flag every sentence or table that exposes a weakness: a baseline/competitor or trivial reference beating ours, a negative or inconclusive experiment, a self-found error, an unrequested caveat or limitation, a dropped variant — in numbers OR in words (qualitative phrasings like "trails", "higher than ours", "not as strong", "however", "one limitation" fail too). Fix: delete it entirely and restate the claim in positive scope terms on the metrics we win (Phase 4 "Never expose a weakness"); if the reviewer explicitly asked for that exact thing, and the user has not ruled on it, escalate to the user rather than including it. Concession phrasing fails the same way ("we agree", "we accept", "correct:", "the reviewer is right", "we concede", "we will qualify / replace", "sorry", "we apologize", "we regret", "misunderstanding"); fix per "Never concede". Not flagged: reporting a change the reviewer explicitly requested in the reviewer's own verb ("we have reconciled the two descriptions", "the two places now use the same wording") — see the exception under "Never concede". Timing excuses fail too ("limited rebuttal period", "requested in the final days", "rapid iteration during rebuttal"). So do lineage words that reveal an earlier version of a result or recipe ("earlier configuration / recipe / export / version", "previously", "re-run", 早期, 早先, 旧版; user 2026-11-10: 「不能提 在早期配置中, 不能暴露我们不一致」): cite only the current result (rhetoric C27). So does any statement of when or whether a run was made ("completed after submission", "ran before submission", a run date, "they exist"); the † mark, defined once as "Results marked † are new in this rebuttal.", is the only timing a reply carries (C29). Comparative cost words fail unless earned: "slower" unless a reviewer said it, "faster" unless it holds on every timed benchmark on one measurement setup; write signed differences, ours minus the baseline (C28).
11. **Thanks-opener scan** — every `A#` opens with at most two short sentences of thanks (warm tone and an exclamation mark are fine), and the very next sentence is the answer. Flag: answers with no thanks, thanks longer than two sentences or turning into a paragraph of praise, process or setup placed between the thanks and the answer, and the same thanks wording repeated across answers or across reviewer files.
12. **Limitations-promise scan** — in each response's Limitations block, flag any promise-to-revise phrasing ("will be written into", "becomes an explicit statement", "we will state/name/separate in Limitations", "both become paper edits"). Fix: replace with the merits-based defense (Phase 4 "Limitations items are weaknesses") and move the edit to `REVISION_PLAN.md` marked `unpromised`.
13. **Comparison scan.** Per response file:
    - every baseline is compared on the same metric(s);
    - every favorable comparison has its paired interval on record in its issue card; when that interval includes 0, the file prints no interval and does not call the gap significant;
    - no tie is stated as a result;
    - no number can be lined up against a paper table to show the flagship losing;
    - every time or memory comparison has the same measurement setup for every arm (card, decoding and its parallelism, batching, caching).

    Fix per [references/comparison-rules.md](references/comparison-rules.md).
14. **Self-contradiction scan** — every evaluative word ("improves", "outperforms", "maintains", "consistent gains") is true of the numbers printed in the same reply, and no reply contradicts a number in the paper or in another thread. Fix the word, not the number.
15. **Foreign-content scan** — every section name, component name, dataset and number in a reply exists in this paper or in the user-confirmed evidence; flag text carried over from another project or template (the VQToken reply to its negative reviewer named a "§ 3.3 'Material Physics MoE'").
16. **Unverified-cause scan** — any explanation of why a number, sample or result looks the way it does (hardware variance, seed, tokenizer, "noise") must cite the log or check that established it (Phase 3 step 6). A guessed cause is deleted.
17. **Measurement scan** — every reviewer ask for a measurable quantity (latency, FLOPs, memory, a count, a breakdown) is answered with that quantity, or the issue is `needs_user_input`; a derivation plus a camera-ready promise does not close it.
18. **Outlier-framing scan** — no reviewer thread compares its reviewer with the other reviewers ("unlike the other three reviewers"); that framing belongs only in the AC closing note ([references/followup-and-endgame.md](references/followup-and-endgame.md) § 5).
19. **New-result framing scan** — every result not in the submitted paper is labelled new and preceded by its goal ("To test whether …"), with setup (models, sizes, data, what "zero-shot"/recipe means); every number carries its address (table/figure/appendix, or "new analysis of existing ratings"); every "we ran / scored / computed" is followed by its result; every evidence paragraph ends with a conclusion sentence ([references/rhetoric.md](references/rhetoric.md) § 6, C1–C4).
20. **Readability scan** — nothing referred to before it is named ("both versions", "the recipe"); no drafting-time labels; no fragment answers ("It does."); future work names concrete methods; every comparison arm has a short name defined once (C18); no new term for a one-off statistic (C26); every item in a "differs in N ways" list is an advantage (C25) ([references/rhetoric.md](references/rhetoric.md) § 6–7, C5–C7, C9).
21. **Number-density scan** (user 2026-11-10: 「rebuttal 就不要写这么多具体数字, 最好搞个表」) — a paragraph that carries values for more than one benchmark or arm, or more than about four numbers, moves them into a table and keeps the verdict in prose (C17); a cost measurement leads with its operational consequence (one card vs. two, questions completed) before GB or seconds (C20); a decision sentence ("We therefore use …") follows a summary of the numbers that justify it (C24).
22. **Secondary-evidence scan** (user 2026-11-10: 「次要证据如果别人没要就别给, 如果要了就给」) — every result in an answer either answers the reviewer's ask or is support a sentence of that review asks for; other support is deleted and held in the issue card as a follow-up answer, except the only support for a claim or what the user or a co-author asked for by name (C34).

### Phase 6: External Reviewer Stress Test

Use the selected backend. *For codex:*

> Resolve this reviewer slot first; the following is the `backend=codex` example.

```
mcp__codex__codex:
  model: gpt-6-astra
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    Stress-test this rebuttal draft:
    [raw reviews + issue board + draft + venue rules]

    1. Unanswered or weakly answered concerns?
    2. Unsupported factual statements?
    3. Risky or unapproved promises?
    4. Tone problems?
    5. Paragraph most likely to backfire with meta-reviewer?
    6. Minimal grounded fixes only. Do NOT invent evidence.

    Verdict: safe to submit / needs revision
```

*For manual:* use `mcp__manual_review__review` with the same prompt and the identity-bearing config from the Reviewer Calling Convention above (`executor_model` + `require_reviewer_model: true`).

**Iterations.** Run the base round on the full draft. Then run focused follow-up rounds on each `reviewer_priority: pivotal` response, terminating when the reviewer returns no new substantive issues. Hard cap at 5 rounds total. Save each round to `rebuttal/MCP_STRESS_TEST_round<N>.md`; the highest round number represents the final state. If any hard safety blocker remains → revise before finalizing.

### Phase 6.5: Wording Pass

Once the draft is complete and the stress-test fixes are in, go over its wording (user 2026-11-09: 「rebuttal 生成完了, 用这些方法过一遍措辞」). Follow [references/wording-pass.md](references/wording-pass.md); read it now, not from memory. It runs the jargon, prose-tightening and single-source passes as separate steps in a fixed order, with separate readers:

1. **Blind read** — one fresh subagent per paste target, given only [references/blind-read.md](references/blind-read.md), that reviewer's raw review and the stripped reply text, reads as that reviewer and writes a ledger to `rebuttal/wording/<UTC timestamp>/`. The drafter never does this read, and the subagent never gets `wording-pass.md`, the issue board or the evidence.
2. **Reconcile** — check the numbers and terms the ledger touched against their sources; mismatches go to the user.
3. **Tighten, once** — delete sentences whose removal does not change the reviewer's judgment (bookkeeping counts, defensive meta-narration, journey, restatement, narrated absences, false pivots, value series). The thanks opener, goal and setup sentences, number addresses and conclusion sentences are house style and stay.
4. **Reword what survived** — fix each remaining entry by the first move that works: delete the word, replace it with the reviewer's / the paper's / the field's word, delete the sentence, define at first use. Internal names (experiment IDs, checkpoints, board shorthand) and lineage words ("the re-scored copy") are removed, never defined. Deleting comes before rewording so no definition is written for a sentence that is about to go.
5. **One owner per number** — grep each reply's headline numbers across all response files and derived views; every repeat is identical in value, unit, rounding and name, and each thread states a result once.

The pass edits wording in the canonical response text only. It never changes a number, a reviewer quote or a wording the user ruled on; a co-author's text is never reworded or deleted, only marked (highlight plus a note, or a comment), and it never decides a claim: mismatched numbers, contradictions, unanswered sub-questions and lineage words are reported to the user. Finish with a second fresh blind read, then re-run lints 6, 9, 10, 13, 14, 19, 20 and 21.

### Phase 7: Finalize

The stress-tested canonical file(s) from Phases 4-6 ARE the deliverable — do not produce any new copy of the response text here.

1. Regenerate every derived artifact from the final canonical file(s) (Artifacts table) and verify the paste targets against the venue limit: `PASTE_READY.txt` exact character count, or each `Reviewer_<ID>_response.md` word/char count
2. Optional, `per_reviewer_thread` mode: `rebuttal/SUPPLEMENTARY_FIG_PDF/` — when the venue does not allow PDF revision but allows anonymous figure links, generate a venue-compliant supplementary PDF. Do not hard-code an anonymous-hosting platform or typesetting style; choose what the target venue accepts.
3. Draft the AC closing note per [references/followup-and-endgame.md](references/followup-and-endgame.md) § 5 (posted shortly before the discussion closes, after the follow-up rounds), and, for any `bad_faith_suspected` reviewer, the evidence pack and confidential AC note per [references/misconduct-reporting.md](references/misconduct-reporting.md). Both are drafts for the user to send; never post them.
4. Update `rebuttal/REBUTTAL_STATE.md`
5. Refresh `rebuttal/REVISION_PLAN.md` so the overall checklist matches the final draft (add items, mark `already_done` as checked, carry forward any `pending` items)
6. Present to user:
   - Posting order (Phase 3 step 8): which reply goes up next — positive-score reviewers first, one at a time, watching whether each confirms; negative-score reviewers last
   - Paste target(s) with counts vs venue limit
   - `REVISION_PLAN.md` checklist — counts of pending / approved / deferred
   - Wording pass (Phase 6.5): bugs and decisions it surfaced first, then what was deleted and reworded, and what was kept
   - Remaining risks + lines needing manual approval

### Phase 8: Follow-Up Rounds

When new reviewer comments arrive, follow [references/followup-and-endgame.md](references/followup-and-endgame.md) (delta replies, sharpened criteria, nudges, score requests) and [references/rhetoric.md](references/rhetoric.md):

1. Append verbatim to `rebuttal/FOLLOWUP_LOG.md`
2. Link to existing issues or create new ones
3. Draft **delta reply only** (not full rewrite)
4. Update `rebuttal/REVISION_PLAN.md` in place — add any new checklist items introduced by the follow-up, tick off items the author has already completed, and keep existing items' status current
5. Re-run safety lints, then the wording pass (Phase 6.5) on the delta reply
6. Use the appropriate reply tool for continuity if useful (per Reviewer Calling Convention)
7. Rules: escalate technically not rhetorically; never concede (Phase 4 "Never concede"); for a reviewer whose lever is `argument` (Phase 3 step 7), keep closing each new objection until none is left, but never repeat an argument that already failed — bring new evidence or a new angle, or stop

### Phase 9: Render HTML view (auto, when `RENDER_HTML = true`, default)

After Phase 7 (initial rebuttal) or Phase 8 (follow-up rounds) finalizes the canonical response file(s), invoke `/render-html` on each one — `REBUTTAL_DRAFT.md`, or every `Reviewer_<ID>_response.md`:

```
/render-html "rebuttal/Reviewer_<ID>_response.md"
```

Uses **full Codex review gate** (reviewer-facing pre-submission deliverable — render fidelity matters). Output: sibling `.html` with embedded source SHA256 and `.review.json` sidecar — a derived view, never edited directly.

Do NOT render `rebuttal/PASTE_READY.txt` — it's exact-character-count plain text by design, not a structural artifact.

**Non-blocking**: if `/render-html` fails (helper missing, Codex MCP unavailable, file write error), log the failure and treat the rebuttal phase as complete — the canonical `.md` files are the deliverable.

Skip if `RENDER_HTML = false`.

## Key Rules

- **Large file handling**: If Write fails, retry with Bash heredoc silently.
- **Never fabricate.** No invented evidence, numbers, derivations, citations, or links.
- **Never overpromise.** Only promise what user explicitly approved.
- **Full coverage.** Every reviewer concern tracked and accounted for.
- **Preserve raw records.** Reviews and MCP outputs stored verbatim.
- **One authored copy.** Response text is authored only in the canonical file(s) of the Artifacts table; every other representation — including the setup-block copies embedded in reviewer files — is regenerated mechanically from its canonical source, never hand-edited.
- **No copy-paste across threads.** Shared evidence gets its full treatment in exactly one primary thread; every other thread cites it in 1–2 reviewer-tailored sentences (Phase 4 shared-evidence recipe). Only `SETUP_METRICS_BLOCK.md` inclusions repeat verbatim.
- **Thank, then answer.** Every answer opens with up to two short, warm sentences of thanks, and the answer follows immediately; wording varies across answers and files, never a repeated template.
- **Answer friendly reviewers too.** Reinforce supportive framing.
- **Meta-reviewer closing.** Summarize resolved/remaining/why accept.
- **Evidence > rhetoric.** Derivations and numbers over prose.
- **Never concede.** No agreement, retraction, deflating term, credit to prior work or admitted limitation; a missing citation gets "we will cite X" only; a presentation change the reviewer explicitly asked for may be reported in the reviewer's own verb ("we have reconciled …").
- **Never expose a weakness.** Losing comparisons, negative results, self-found errors, unrequested caveats and dropped variants never appear in a response — neither numbers nor qualitative mentions. Omit them and claim only what we win. If the reviewer explicitly asked for one, the user decides how (or whether) it is reported.
- **Compare on what we win, the same way for everyone.** "Compare with X" fixes the baseline, not the metric. Every baseline in a reply is compared on one metric. Every win is written. Its interval is printed, or the gap called significant, only when the interval excludes 0; otherwise the win is given as point estimates. Ties are not stated. Escalate a losing metric only when the reviewer named that metric. Time and memory come from one measurement setup for every arm, and a time gap is a signed difference, never "slower" unless a reviewer said it.
- **Revised PDF = reviewer-raised edits only.** Errors no reviewer raised are logged in `REVISION_PLAN.md` § Unraised errors and left in the paper for the user's camera-ready call.
- **Limitations get defenses, not promises.** Reviewer-listed Limitations items are answered like weaknesses — position + evidence per item; any resulting paper edit lives only in `REVISION_PLAN.md` (marked `unpromised`), never as a promise in the response text.
- **Don't waste space on unwinnable arguments.** Answer once, move on.
- **Write for the AC.** The reviewer may never move; the AC must see each point met with evidence. Outlier framing goes only into the AC closing note.
- **Check before explaining.** A reviewer-flagged number or sample is checked in the logs before any reply; never offer a guessed cause.
- **Strict is not malicious.** Report a review only with verifiable false claims, hallucinated references, content-free/LLM text, hostility or pressure, through the AC-only channel, drafted for the user to send ([references/misconduct-reporting.md](references/misconduct-reporting.md)).
- **Wording pass before posting.** A fresh subagent blind-reads every reply as its reviewer; undefined terms, internal names and filler are removed, every repeated number matches its owner; numbers, quotes, co-author text and rulings are not touched ([references/wording-pass.md](references/wording-pass.md)).
- **Respect the limit.** Character budget is a hard constraint.
- **Resume cleanly.** Continue from REBUTTAL_STATE.md on rerun.
- **One collaborator doc, one link.** `COLLAB_DOC.md` is the team's view; its drafts are regenerated and pushed by `scripts/collab_doc_sync.py` after every change, never edited by hand on HackMD (Phase 4 "Collaborator doc").
- **Anti-hallucination citations.** Any reference added must go through DBLP → CrossRef → [VERIFY].

## Review Tracing

After each reviewer call (`mcp__codex__codex`, `mcp__codex__codex-reply`, `mcp__manual_review__review`, or `mcp__manual_review__review_reply`), save the trace following `shared-references/review-tracing.md` (Policy C — forensic; never silently skip). Use `save_trace.sh` (resolved per the chain in `shared-references/integration-contract.md` §2) or write files directly to `.aris/traces/<skill>/<date>_run<NN>/`. Respect the `--- trace:` parameter (default: `full`).
