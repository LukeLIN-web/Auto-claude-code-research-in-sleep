---
name: rebuttal
description: "Workflow 4: Submission rebuttal pipeline. Parses external reviews, enforces coverage and grounding, drafts a safe text-only rebuttal under venue limits, and manages follow-up rounds. Use when user says \"rebuttal\", \"reply to reviewers\", \"ICML rebuttal\", \"OpenReview response\", or wants to answer external reviews safely."
argument-hint: "[paper-path-or-review-bundle]"
allowed-tools: Bash(*), Read, Grep, Glob, Write, Edit, Skill, mcp__codex__codex, mcp__codex__codex-reply, mcp__manual_review__review, mcp__manual_review__review_reply
---

# Workflow 4: Rebuttal

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
- **REVIEWER_MODEL = `gpt-5.6-sol`** — Default model for the Codex backend. Used for internal stress-testing. Manual backend uses whatever model the user chooses.
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
    config: {"model_reasoning_effort": "xhigh"}
  Save the returned `threadId`.
  Use `mcp__manual_review__review_reply` for follow-up rounds with:
    threadId: [saved manual-review threadId]
    prompt: [follow-up prompt]
    config: {"model_reasoning_effort": "xhigh"}

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

## Artifacts

The response text is **authored in exactly one place** — the canonical file(s) for the active `VENUE_MODE`. Every other representation is a **derived view**: regenerated mechanically from its source whenever the source changes, and never hand-edited. All edits (internal revise rounds, stress-test fixes, follow-ups) land in the canonical file. Do not create any response-bearing file outside this table.

The rule covers **measurements** of the response, not only its text. Character counts, word counts and per-file lengths are derived facts that own no file: measure them at the moment a decision depends on them, and let the number die with the check. A count written into any document is wrong as soon as the response is edited, and whoever reads it next — including you on resume — will take it for fact.

| File | Mode | Role |
|---|---|---|
| `REBUTTAL_STATE.md` | both | canonical — phase, venue rules, round, stress-test verdicts. Never record anything measurable from the response files (character or word counts, per-file lengths) |
| `REVIEWS_RAW.md`, `FOLLOWUP_LOG.md` | both | canonical — verbatim reviewer text |
| `ISSUE_BOARD.md` | both | canonical — atomized concerns |
| `STRATEGY_PLAN.md` | both | canonical — themes, response modes, budgets |
| `REVISION_PLAN.md` | both | canonical — promised paper edits (checklist) |
| `REBUTTAL_DRAFT.md` | single_document | **canonical response text** — the only authored copy; over-limit material inline, marked `[OPTIONAL — cut if over limit]` |
| `PASTE_READY.txt` | single_document | derived — `REBUTTAL_DRAFT.md` minus `[OPTIONAL]` blocks, markdown stripped, exact character count |
| `Reviewer_<ID>_response.md` | per_reviewer_thread | **canonical response text** — one self-contained file per reviewer; each file IS the paste target for its thread (no aggregate draft, no `PASTE_READY.txt`) |
| `SETUP_METRICS_BLOCK.md` | per_reviewer_thread | canonical — shared setup/metrics text; the copies embedded in reviewer files are derived inclusions (the one sanctioned duplication): edit only the block, then re-propagate to every reviewer file that embeds it |
| `MCP_STRESS_TEST_round<N>.md` | both | canonical — verbatim stress-test transcripts (Phase 6) |
| `SUPPLEMENTARY_FIG_PDF/` | per_reviewer_thread, optional | derived — venue-compliant figure PDF (Phase 7); no response text |
| `*.html` (+ `.review.json` sidecar) | both, if `RENDER_HTML` | derived — Phase 9 render of each canonical response file |

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
- `issue_type`: assumptions / theorem_rigor / novelty / empirical_support / baseline_comparison / complexity / practical_significance / clarity / reproducibility / other
- `severity`: critical / major / minor
- `reviewer_stance`: positive / swing / negative / unknown
- `reviewer_priority`: standard / pivotal
  - `pivotal` — a reviewer whose response is likely to affect the decision if addressed well: low or borderline rating, addressable concerns, and enough confidence/influence to matter. Phase 3 allocates extra drafting and stress-test budget here.
- `response_mode`: direct_clarification / grounded_evidence / nearest_work_delta / assumption_hierarchy / narrow_concession / future_work_boundary / structural_distinction
  - `structural_distinction` — for "your method reduces to X / is just generic Y / is subsumed by Z" attacks. Pattern: agree on the local reduction; show the structural feature your parameterization preserves that X/Y/Z does not capture, backed by a concrete mechanism (theorem dependency, derivation step, or empirical consequence). Never use rhetorically without the supporting mechanism.
- `status`: open / answered / deferred / needs_user_input

### Phase 3: Build Strategy Plan

Create `rebuttal/STRATEGY_PLAN.md`.

1. Identify 2-4 **global themes** resolving shared concerns
2. Choose **response mode** per issue
3. Build **character budget** (10-15% opener, 75-80% per-reviewer, 5-10% closing) — applies in `single_document` mode; in `per_reviewer_thread` mode, set per-thread word/char targets instead
4. **Identify pivotal reviewer(s)** — reviewers whose vote or confidence shift would most affect the decision, especially when concerns are addressable rather than ideological. Mark them `reviewer_priority: pivotal` in `ISSUE_BOARD.md`. There may be more than one. Allocate disproportionate drafting + stress-test budget here.
5. Identify **blocked claims** (ungrounded or unapproved)
6. If unresolved blockers → pause and present to user

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
   - Switch response mode to `narrow_concession` or `future_work_boundary`
   - Do NOT fabricate positive results

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

Default reply pattern per issue:
- Sentence 1: the direct answer to the question as asked — the verdict, the number, or the yes/no ("All four headline contrasts are significant", "Both are robust to the reference"). NEVER open with process or setup ("We ran...", "We recomputed...", "New table on...") — that buries the answer; method details come after the verdict.
- Sentence 2-4: grounded evidence
- Last sentence: implication for the paper

**Paragraph length (readability).** No paragraph over 4-5 sentences in the reviewer-facing text. When a response to one W/Q runs longer, insert blank lines at argument boundaries — typical seams: concession/claim | mechanism or evidence | concrete example | scope statement or revision promise. Split with line breaks only; never reword while splitting. Long walls of text read as evasive and reviewers skim past the numbers buried mid-paragraph.

**Reusable setup block (per_reviewer_thread mode).**
If multiple reviewer-thread responses need the same experimental setup or metric definitions, write a canonical `SETUP_METRICS_BLOCK.md`. Reuse it consistently in each reviewer file that needs it. Target ≤ 150 words; expand only with genuinely reviewer-specific additions inline. Change-once-update-everywhere prevents drift across threads.

**Shared evidence across threads (per_reviewer_thread mode).**
When one result or analysis answers concerns from multiple reviewers, it appears at exactly one depth per thread:
1. **Primary thread** — the reviewer whose issue card owns the most direct ask. This file carries the full treatment: protocol sentence, key numbers, honest caveat.
2. **Every other thread** — a 1–2 sentence citation recomposed in *that* reviewer's framing, carrying only the number(s) that answer their specific ask. Write it fresh from the evidence doc; never transplant sentences from another reviewer file.

Self-contained means the reviewer can follow the response without opening another thread — not that every thread repeats the full result. Reviewers and the AC read all threads; near-verbatim repetition reads as boilerplate and burns each thread's character budget. The only sanctioned verbatim duplication across reviewer files is the `SETUP_METRICS_BLOCK.md` inclusion.

Heuristics from successful rebuttals (content):
- Evidence > assertion
- Global narrative first, per-reviewer detail second (single_document mode only)
- Concrete numbers for counter-intuitive points
- Name closest prior work + exact delta for novelty disputes
- Concede narrowly when reviewer is right
- For theory: separate core vs technical assumptions
- Answer friendly reviewers too

**Reviewer-defensive moves:**
- **Minimum sufficient evidence per concern.** Usually one numerical anchor: the metric that maps directly to *that reviewer's* specific ask. Cut metrics other reviewers care about — bloat dilutes the answer.
- **Favorable-comparison selection.** A response quotes a head-to-head number only where our method wins it. If a baseline beats us on a metric, the losing comparison stays out of every response file entirely — no figures AND no qualitative acknowledgment (no "trails", "lower than", "not as strong as" phrasing): report our own number, anchor the comparison on the metrics we win, and state the claim in positive scope terms ("the judge's validated strength is X"), which requires no reference to the opponent. If a reviewer explicitly demands the unfavorable number itself, pause and surface the conflict to the user instead of volunteering it. (`narrow_concession` remains available for the reviewer's substantive points — never for baseline head-to-heads.)
- **Pre-registered calibration phrasing.** When a threshold or hold-out was fixed before generated samples were inspected, say so explicitly with a phrase like "set on hold-out before any generated sample was inspected." Defuses cherry-pick attacks at near-zero word cost. Only use when actually true.
- **Surface non-obvious design choices upfront.** If the experimental setup has a non-obvious caveat (compute-matched ≠ epoch-matched, atypical seed protocol, restricted parameter subset, etc.), name it concretely with numbers where they clarify the design choice. Pre-empts adversarial reverse engineering.
- **Structural distinction over denial.** When a reviewer claims your work reduces to / is subsumed by a generic framework, do not deny the reduction. Identify the structural feature your parameterization preserves that the generic framework does not — see `response_mode: structural_distinction`.
- **Concede without surrendering the claim.** When the reviewer is partly right, explicitly accept the local point, then state what remains true and why it still supports the paper's contribution. Pair the concession with the preserved theorem, mechanism, empirical result, or scope condition.
- **Limitations items are weaknesses.** When a reviewer lists Limitations (or asks that something "be stated explicitly"), answer each item on the merits exactly like a W#: 1-2 sentences of positive argument per item, grounded in numbers already in the response (framing like "Our position on each:"). Never reply with promise-to-revise phrasing ("will be written into the Limitations section", "becomes an explicit statement in the revised Limitations", "we will state in Limitations") — a promise-to-revise reads as conceding the point instead of defending it. The corresponding paper edit, if the author approves one, is tracked in `REVISION_PLAN.md` only and marked `unpromised`. Revision promises attached to W#/Q# answers ("We will add CIs to the law tables") remain allowed and stay future tense.

Hard rules:
- NEVER invent experiments, numbers, derivations, citations, or links
- NEVER promise what user hasn't approved
- If no strong evidence exists, say less not more

After authoring or changing a canonical draft, regenerate its derived artifacts per the Artifacts table (`single_document`: `PASTE_READY.txt`).

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

4. **Out-of-scope log** — reviewer concerns that will **not** trigger a paper revision (e.g. `deferred_intentionally`, `narrow_concession` with no edit), with a one-line reason each. This keeps the checklist honest: nothing silently disappears.

Rules for `REVISION_PLAN.md`:
- Every checklist item must map to at least one `issue_id` from `ISSUE_BOARD.md`.
- Every promise in the canonical draft(s) that implies a paper edit must appear as a checklist item — if it is not in the plan, it is a commitment-gate violation.
- Never add items that are not backed by the draft, by user-confirmed evidence, or by a user-approved edit deliberately kept out of the response text (mark these `unpromised` — e.g. Limitations defenses).
- On rerun / follow-up rounds, update checkbox state in place rather than regenerating from scratch.

### Phase 5: Safety Validation

Run all lints:
1. **Coverage** — every issue maps to draft anchor
2. **Provenance** — every factual sentence has source
3. **Commitment** — promises are approved AND every paper-edit promise in the draft appears as a checklist item in `REVISION_PLAN.md` (and vice versa — no orphan items in the plan, except items marked `unpromised`: edits the author will make that the response text deliberately does not promise, per the Limitations rule)
4. **Tone** — flag aggressive/submissive/evasive phrases
5. **Consistency** — no contradictions across reviewer replies
6. **Limit** — exact character count on the paste target(s): freshly derived `PASTE_READY.txt`, or each `Reviewer_<ID>_response.md`. Compress if over (redundancy → friendly → opener → wording, never drop critical answers)
7. **Thread-local context** (`per_reviewer_thread` mode only) — each reviewer file must be intelligible without reading any other reviewer file. Flag any "see Reviewer X" references or undefined terms that rely on cross-thread context.
8. **Adversarial design-choice scan** — for each experimental claim, ask: "Could a hostile reviewer find a non-obvious design choice (compute-match, frozen subset, sampling protocol) that I haven't disclosed?" If yes, add a one-line caveat in the Setup paragraph. Narrower than provenance; focused on *design choices* not factual sources.
9. **Cross-thread duplication** (`per_reviewer_thread` mode only) — compare reviewer files pairwise: any sentence of ~15+ words appearing near-verbatim in more than one file, outside the `SETUP_METRICS_BLOCK.md` inclusion, fails. Fix by keeping the full treatment in the primary thread and recomposing the other occurrences per the shared-evidence recipe (Phase 4).
10. **Losing-comparison scan** — flag every sentence or table where a baseline/competitor beats ours, in numbers OR in words (qualitative phrasings like "trails", "higher than ours", "not as strong" fail too). Fix: delete the losing comparison entirely and restate the claim in positive scope terms on the metrics we win (Phase 4 favorable-comparison selection); if a reviewer explicitly demanded that exact number, escalate to the user rather than including it.
11. **Limitations-promise scan** — in each response's Limitations block, flag any promise-to-revise phrasing ("will be written into", "becomes an explicit statement", "we will state/name/separate in Limitations", "both become paper edits"). Fix: replace with the merits-based defense (Phase 4 "Limitations items are weaknesses") and move the edit to `REVISION_PLAN.md` marked `unpromised`.

### Phase 6: External Reviewer Stress Test

Use the selected backend. *For codex:*

```
mcp__codex__codex:
  model: gpt-5.6-sol
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

*For manual:* use `mcp__manual_review__review` with the same prompt and `config: {"model_reasoning_effort": "xhigh"}`.

**Iterations.** Run the base round on the full draft. Then run focused follow-up rounds on each `reviewer_priority: pivotal` response, terminating when the reviewer returns no new substantive issues. Hard cap at 5 rounds total. Save each round to `rebuttal/MCP_STRESS_TEST_round<N>.md`; the highest round number represents the final state. If any hard safety blocker remains → revise before finalizing.

### Phase 7: Finalize

The stress-tested canonical file(s) from Phases 4-6 ARE the deliverable — do not produce any new copy of the response text here.

1. Regenerate every derived artifact from the final canonical file(s) (Artifacts table) and verify the paste targets against the venue limit: `PASTE_READY.txt` exact character count, or each `Reviewer_<ID>_response.md` word/char count
2. Optional, `per_reviewer_thread` mode: `rebuttal/SUPPLEMENTARY_FIG_PDF/` — when the venue does not allow PDF revision but allows anonymous figure links, generate a venue-compliant supplementary PDF. Do not hard-code an anonymous-hosting platform or typesetting style; choose what the target venue accepts.
3. Update `rebuttal/REBUTTAL_STATE.md`
4. Refresh `rebuttal/REVISION_PLAN.md` so the overall checklist matches the final draft (add items, mark `already_done` as checked, carry forward any `pending` items)
5. Present to user:
   - Paste target(s) with counts vs venue limit
   - `REVISION_PLAN.md` checklist — counts of pending / approved / deferred
   - Remaining risks + lines needing manual approval

### Phase 8: Follow-Up Rounds

When new reviewer comments arrive:

1. Append verbatim to `rebuttal/FOLLOWUP_LOG.md`
2. Link to existing issues or create new ones
3. Draft **delta reply only** (not full rewrite)
4. Update `rebuttal/REVISION_PLAN.md` in place — add any new checklist items introduced by the follow-up, tick off items the author has already completed, and keep existing items' status current
5. Re-run safety lints
6. Use the appropriate reply tool for continuity if useful (per Reviewer Calling Convention)
7. Rules: escalate technically not rhetorically; concede if reviewer is correct; stop arguing if reviewer is immovable and no new evidence exists

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
- **Answer friendly reviewers too.** Reinforce supportive framing.
- **Meta-reviewer closing.** Summarize resolved/remaining/why accept.
- **Evidence > rhetoric.** Derivations and numbers over prose.
- **Concede selectively.** Narrow honest concessions > broad denials.
- **Never volunteer losing comparisons.** A comparison a baseline wins never appears in a response — neither its numbers nor any qualitative mention that the baseline is ahead. Omit it and claim only the metrics we win.
- **Limitations get defenses, not promises.** Reviewer-listed Limitations items are answered like weaknesses — position + evidence per item; any resulting paper edit lives only in `REVISION_PLAN.md` (marked `unpromised`), never as a promise in the response text.
- **Don't waste space on unwinnable arguments.** Answer once, move on.
- **Respect the limit.** Character budget is a hard constraint.
- **Resume cleanly.** Continue from REBUTTAL_STATE.md on rerun.
- **Anti-hallucination citations.** Any reference added must go through DBLP → CrossRef → [VERIFY].

## Review Tracing

After each reviewer call (`mcp__codex__codex`, `mcp__codex__codex-reply`, `mcp__manual_review__review`, or `mcp__manual_review__review_reply`), save the trace following `shared-references/review-tracing.md` (Policy C — forensic; never silently skip). Use `save_trace.sh` (resolved per the chain in `shared-references/integration-contract.md` §2) or write files directly to `.aris/traces/<skill>/<date>_run<NN>/`. Respect the `--- trace:` parameter (default: `full`).
