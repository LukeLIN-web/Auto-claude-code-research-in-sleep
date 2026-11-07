---
name: rebuttal
description: "Workflow 4: Submission rebuttal pipeline. Parses external reviews, enforces coverage and grounding, drafts a safe text-only rebuttal under venue limits, and manages follow-up rounds. Use when user says \"rebuttal\", \"reply to reviewers\", \"ICML rebuttal\", \"OpenReview response\", or wants to answer external reviews safely."
argument-hint: "[paper-path-or-review-bundle]"
allowed-tools: Bash(*), Read, Grep, Glob, Write, Edit, Skill, mcp__antigravity__antigravity, mcp__antigravity__antigravity-reply, mcp__grok__grok, mcp__grok__grok-reply, mcp__claude-review__review, mcp__claude-review__review_reply, mcp__claude-review__review_start, mcp__claude-review__review_reply_start, mcp__claude-review__review_status
---

# Workflow 4: Rebuttal

> **Before each reviewer slot**, follow [Selectable Reviewers](../shared-references/reviewer-backends.md):
> resolve invocation → `.aris/reviewer.json` → Codex default (fresh native reviewer)
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
- ICML-style **text-only rebuttal**
- strict **character limits**
- **multiple reviewers**
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
- **REVIEWER_MODEL = `gpt-6-astra`** — Used via Codex MCP for internal stress-testing.
- **REVIEWER_BACKEND = `codex`** — Default: Codex xhigh stress tester. Use `--reviewer: oracle-pro` only when explicitly requested; if Oracle is unavailable, warn and fall back to Codex xhigh. See `../shared-references/reviewer-routing.md`.
- **MAX_INTERNAL_DRAFT_ROUNDS = 2** — draft → lint → revise.
- **MAX_STRESS_TEST_ROUNDS = 1** — One Codex MCP critique round.
- **MAX_FOLLOWUP_ROUNDS = 3** — per reviewer thread.
- **AUTO_EXPERIMENT = false** — When `true`, automatically invoke `/experiment-bridge` to run supplementary experiments when the strategy plan identifies reviewer concerns that require new empirical evidence. When `false` (default), pause and present the evidence gap to the user for manual handling.
- **QUICK_MODE = false** — When `true`, only run Phase 0-3 (parse reviews, atomize concerns, build strategy). Outputs `ISSUE_BOARD.md` + `STRATEGY_PLAN.md` and stops — no drafting, no stress test. Useful for quickly understanding what reviewers want before deciding how to respond.
- **REBUTTAL_DIR = `rebuttal/`**
- **RENDER_HTML = true** — When `true` (default), Phase 9 renders the canonical `REBUTTAL_DRAFT.md` to HTML. Set `false`, or pass `— render html: false`, to skip.

> Override: `/rebuttal "paper/" — venue: NeurIPS, character limit: 5000`

## Required Inputs

1. **Paper source** — PDF, LaTeX directory, or narrative summary
2. **Raw reviews** — pasted text, markdown, or PDF with reviewer IDs
3. **Venue rules** — venue name, character/word limit, text-only or revised PDF allowed
4. **Current stage** — initial rebuttal or follow-up round

If venue rules or limit are missing, **stop and ask** before drafting.

## Safety Model

Three hard gates — if any fails, do NOT finalize:

1. **Provenance gate** — every factual statement maps to: `paper`, `review`, `user_confirmed_result`, `user_confirmed_derivation`, or `future_work`. No source = blocked.
2. **Commitment gate** — every promise maps to: `already_done`, `approved_for_rebuttal`, or `future_work_only`. Not approved = blocked.
3. **Coverage gate** — every reviewer concern ends in: `answered`, `deferred_intentionally`, or `needs_user_input`. No issue disappears.

## Artifacts

The response text is **authored in exactly one file**: `REBUTTAL_DRAFT.md`. Every other representation is a **derived view** — regenerated mechanically whenever the draft changes, never hand-edited. All edits (internal revise rounds, stress-test fixes, follow-ups) land in the draft. Do not create any response-bearing file outside this table.

| File | Role |
|---|---|
| `REBUTTAL_STATE.md` | canonical — phase, venue rules, round, stress-test verdicts |
| `REVIEWS_RAW.md`, `FOLLOWUP_LOG.md` | canonical — verbatim reviewer text |
| `ISSUE_BOARD.md` | canonical — atomized concerns |
| `STRATEGY_PLAN.md` | canonical — themes, response modes, budgets |
| `REVISION_PLAN.md` | canonical — promised paper edits (checklist) and the internal log of errors no reviewer raised |
| `REBUTTAL_DRAFT.md` | **canonical response text** — the only authored copy; over-limit material inline, marked `[OPTIONAL — cut if over limit]` |
| `PASTE_READY.txt` | derived — `REBUTTAL_DRAFT.md` minus `[OPTIONAL]` blocks, markdown stripped, exact character count |
| `MCP_STRESS_TEST.md` | canonical — verbatim stress-test transcript (Phase 6) |
| `REBUTTAL_DRAFT.html` (+ `.review.json` sidecar) | derived — Phase 9 render, if `RENDER_HTML` |

## Workflow

### Phase 0: Resume or Initialize

1. If `rebuttal/REBUTTAL_STATE.md` exists → resume from recorded phase
2. Otherwise → create `rebuttal/`, initialize the canonical documents (Artifacts table)
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
- `issue_type`: assumptions / theorem_rigor / novelty / empirical_support / baseline_comparison / complexity / practical_significance / clarity / reproducibility / other
- `severity`: critical / major / minor
- `reviewer_stance`: positive / swing / negative / unknown
- `response_mode`: direct_clarification / grounded_evidence / nearest_work_delta / assumption_hierarchy
- `status`: open / answered / deferred / needs_user_input

### Phase 3: Build Strategy Plan

Create `rebuttal/STRATEGY_PLAN.md`.

1. Identify 2-4 **global themes** resolving shared concerns
2. Choose **response mode** per issue
3. Build **character budget** (10-15% opener, 75-80% per-reviewer, 5-10% closing)
4. **Story: argue what we can win** (user 2026-11-07: 「都是故事上 强调novelty，强调和过去工作的提升，可以吵赢的」). Every reply's narrative leans on the paper's novelty and its improvement over prior work; pair with "Never expose a weakness" (Phase 4).
5. **Check instance-level complaints by hand** (「单个样本之类的需要手动check下具体咋回事」). When a concern cites a specific sample, example, prompt, video or table cell, open that exact instance and see what actually happened before choosing a response mode; record the finding in the issue card.
6. **Pick the lever per reviewer** (「他给1分不太对，但是不是扳不回来 2分哥，看起来是只要补实验就可以 1分哥，主要是要和他掰扯到毛病挑不出来」). A low score is not final. Per negative-score reviewer, record in `STRATEGY_PLAN.md`: `experiments` (concerns are missing evidence, e.g. a typical 2: run what they asked for) or `argument` (concerns attack soundness or claims, e.g. a typical 1: close every objection with evidence or an approved fix until nothing is left to fault).
7. **Posting order** (「先一个一个回复，看正分审稿人愿不愿意confirm，他们一般confirm之后就不动了. 然后麻烦的负分先留到最后」). Post replies one reviewer at a time, positive-score reviewers first (once they confirm their score they rarely move again); the difficult negative-score reviewers go last. Record the order in `STRATEGY_PLAN.md`.
8. Identify **blocked claims** (ungrounded or unapproved)
9. If unresolved blockers → pause and present to user

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
   - The result exposes a weakness, so it stays out of the response ("Never expose a weakness" below); answer the concern on the evidence we have. If the reviewer explicitly asked for this experiment, mark the issue `needs_user_input` and let the user decide whether and how to report it (answered without any concession, "Never concede")

5. Save experiment results to `rebuttal/REBUTTAL_EXPERIMENTS.md` for provenance tracking.

**Time guard**: If estimated GPU-hours exceed rebuttal deadline, skip and flag for manual handling.

### Phase 4: Draft Initial Rebuttal

Author the canonical `rebuttal/REBUTTAL_DRAFT.md`.

Structure:
1. **Short opener** — thank reviewers + 2-4 global resolutions
2. **Per-reviewer numbered responses** — answer → evidence → implication
3. **Short closing** — resolved / remaining / acceptance case

Material worth keeping but over the strict limit stays inline, marked `[OPTIONAL — cut if over limit]`. There is no separate "rich"/"strict" pair of drafts — the strict paste text is derived.

Default reply pattern per issue:
- Sentence 1: direct answer
- Sentence 2-4: grounded evidence
- Last sentence: implication for the paper

Heuristics from 5 successful rebuttals:
- Evidence > assertion
- Global narrative first, per-reviewer detail second
- Concrete numbers for counter-intuitive points
- Name closest prior work + exact delta for novelty disputes
- Never concede ("Never concede" below)
- For theory: separate core vs technical assumptions
- Answer friendly reviewers too

Hard rules:
- **Never expose a weakness** (user 2026-11-07: 「所有暴露缺点的都不提. 如果 reviewer 明确要了, 那给 user 定」). Nothing in the response reveals a weakness of our work unless the reviewer explicitly asked for that exact thing: a metric or comparison a baseline (or a trivial reference such as a constant predictor) wins, a failed, inconclusive or negative rebuttal experiment, an error we found in our own paper, data or prompts, a caveat or limitation the reviewer did not raise, a model or variant we tried and dropped. Leave it out entirely — no figures AND no qualitative acknowledgment ("trails", "lower than", "however", "one limitation is"); claim only what we win, in positive scope terms. If the reviewer explicitly asked for it, do not decide alone: mark the issue `needs_user_input` and write it only the way the user rules, including whether to concede at all.
- **Never concede** (user 2026-11-07: 「不能有任何让步」). No sentence in a response file, and no edit in a revised PDF, agrees that a criticism of our work is right, retracts or narrows one of our claims, adopts the reviewer's deflating term for it, credits our design to prior work, or admits a limitation, an error or an unfinished part. This holds even when the reviewer is right on a local point, and for the words alone ("we agree", "we accept", "correct", "the reviewer is right", "we concede"). Answer with what holds: the evidence we win on, stated in positive scope terms. A missing citation is answered with "we will cite X" and nothing more (「漏引的就说会引用就好了」): no admission that it was missing, no credit of our design to it. Revision promises that add material (a table, a citation, a new result) stay; a promise that retracts or qualifies a claim is a concession and is not made. When the reviewer explicitly asked for a result that goes against us, the user still decides whether it is reported ("Never expose a weakness"), and the reply never frames it as a concession.
- NEVER invent experiments, numbers, derivations, citations, or links
- NEVER promise what user hasn't approved
- If no strong evidence exists, say less not more

After authoring or changing the draft, regenerate `rebuttal/PASTE_READY.txt` per the Artifacts table.

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
- Every promise in `REBUTTAL_DRAFT.md` that implies a paper edit must appear as a checklist item — if it is not in the plan, it is a commitment-gate violation.
- Never add items that are not backed by the draft or by user-confirmed evidence.
- On rerun / follow-up rounds, update checkbox state in place rather than regenerating from scratch.
- **A revised PDF edits only what a reviewer raised** (user 2026-11-07: 「论文不要乱改, 只改 reviewer 提出的. 没提的错误就写到内部文档」). Every change between the submitted version and the revised PDF traces to a checklist item, and through it to an `issue_id`. An error no reviewer raised goes to the Unraised errors section, not into the paper, even when the fix is one word and sits next to an edit being made. Before the revised PDF goes to the user, diff it against the submitted version and match every hunk to an item.

### Phase 5: Safety Validation

Run all lints:
1. **Coverage** — every issue maps to draft anchor
2. **Provenance** — every factual sentence has source
3. **Commitment** — promises are approved AND every paper-edit promise in the draft appears as a checklist item in `REVISION_PLAN.md` (and vice versa — no orphan items in the plan)
4. **Tone** — flag aggressive/submissive/evasive phrases
5. **Consistency** — no contradictions across reviewer replies
6. **Limit** — exact character count on the freshly derived `PASTE_READY.txt`. Compress if over (redundancy → friendly → opener → wording, never drop critical answers)
7. **Weakness scan** — flag every sentence or table that exposes a weakness (a baseline or trivial reference beating ours, a negative or inconclusive experiment, a self-found error, an unrequested caveat or limitation, a dropped variant), in numbers OR in words. Fix: delete it and restate the claim on what we win (Phase 4 "Never expose a weakness"); if the reviewer explicitly asked for that exact thing and the user has not ruled on it, escalate to the user. Concession phrasing fails the same way ("we agree", "we accept", "correct:", "the reviewer is right", "we concede", "we will qualify / replace"); fix per "Never concede".

### Phase 6: Codex Reviewer Stress Test

> Resolve this reviewer slot first; the following is the `backend=codex` example.

```
spawn_agent:
  model: gpt-6-astra
  reasoning_effort: xhigh
  message: |
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

Save full response to `rebuttal/MCP_STRESS_TEST.md`. If hard safety blocker → revise before finalizing.

### Phase 7: Finalize

The stress-tested `REBUTTAL_DRAFT.md` from Phases 4-6 IS the deliverable — do not produce any new copy of the response text here.

1. Regenerate `rebuttal/PASTE_READY.txt` from the final draft and verify its exact character count against the venue limit
2. Update `rebuttal/REBUTTAL_STATE.md`
3. Refresh `rebuttal/REVISION_PLAN.md` so the overall checklist matches the final draft (add items, mark `already_done` as checked, carry forward any `pending` items)
4. Present to user:
   - Posting order (Phase 3 step 7): positive-score reviewers first, one at a time, watching whether each confirms; negative-score reviewers last
   - `PASTE_READY.txt` character count vs venue limit
   - `REVISION_PLAN.md` checklist — counts of pending / approved / deferred
   - Remaining risks + lines needing manual approval

### Phase 8: Follow-Up Rounds

When new reviewer comments arrive:

1. Append verbatim to `rebuttal/FOLLOWUP_LOG.md`
2. Link to existing issues or create new ones
3. Draft **delta reply only** (not full rewrite)
4. Update `rebuttal/REVISION_PLAN.md` in place — add any new checklist items introduced by the follow-up, tick off items the author has already completed, and keep existing items' status current
5. Re-run safety lints
6. Use Codex MCP reply for continuity if useful
7. Rules: escalate technically not rhetorically; never concede ("Never concede"); for a reviewer whose lever is `argument` (Phase 3 step 6), keep closing each new objection until none is left, but never repeat an argument that already failed — bring new evidence or a new angle, or stop

### Phase 9: Render HTML view (auto, when `RENDER_HTML = true`, default)

After Phase 7 (initial rebuttal) or Phase 8 (follow-up rounds) finalizes the canonical draft, invoke:

```
/render-html "rebuttal/REBUTTAL_DRAFT.md"
```

Full review gate (reviewer-facing pre-submission deliverable). Output: `REBUTTAL_DRAFT.html` — a derived view, never edited directly. Do NOT render `rebuttal/PASTE_READY.txt` (it's exact-character-count plain text by design).

**Non-blocking**: if `/render-html` fails, log the failure and treat the rebuttal phase as complete — the canonical `REBUTTAL_DRAFT.md` is the deliverable.

Skip if `RENDER_HTML = false`.

## Key Rules

- **Large file handling**: If Write fails, retry with Bash heredoc silently.
- **Never fabricate.** No invented evidence, numbers, derivations, citations, or links.
- **Never overpromise.** Only promise what user explicitly approved.
- **Full coverage.** Every reviewer concern tracked and accounted for.
- **Preserve raw records.** Reviews and MCP outputs stored verbatim.
- **One authored copy.** Response text is authored only in `REBUTTAL_DRAFT.md`; every other representation is regenerated mechanically from it, never hand-edited.
- **Global + per-reviewer structure.** Shared concerns in opener.
- **Answer friendly reviewers too.** Reinforce supportive framing.
- **Meta-reviewer closing.** Summarize resolved/remaining/why accept.
- **Evidence > rhetoric.** Derivations and numbers over prose.
- **Never concede.** No agreement, retraction, deflating term, credit to prior work or admitted limitation; a missing citation gets "we will cite X" only.
- **Never expose a weakness.** Losing comparisons, negative results, self-found errors, unrequested caveats and dropped variants never appear in the response. If the reviewer explicitly asked for one, the user decides how (or whether) it is reported.
- **Revised PDF = reviewer-raised edits only.** Errors no reviewer raised are logged in `REVISION_PLAN.md` § Unraised errors and left in the paper for the user's camera-ready call.
- **Don't waste space on unwinnable arguments.** Answer once, move on.
- **Respect the limit.** Character budget is a hard constraint.
- **Resume cleanly.** Continue from REBUTTAL_STATE.md on rerun.
- **Anti-hallucination citations.** Any reference added must go through DBLP → CrossRef → [VERIFY].

## Review Tracing

After each `spawn_agent` or `send_input` reviewer call, save the trace following `../shared-references/review-tracing.md`. Write files directly to `.aris/traces/rebuttal/<date>_run<NN>/`. Respect the `--- trace:` parameter when present (default: `full`).
