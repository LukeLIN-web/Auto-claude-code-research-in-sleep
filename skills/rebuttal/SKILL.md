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

## Constants

- **VENUE = `ICML`** — Default venue. Override if needed.
- **RESPONSE_MODE = `TEXT_ONLY`** — v1 default.
- **REVIEWER_MODEL = `gpt-6-astra`** — Default model for the Codex backend. Used for internal stress-testing.
- **REVIEWER_BACKEND = `codex`** — Default: Codex MCP (xhigh). Override with `— reviewer: oracle-pro` for Oracle MCP; other backends, including manual review, per `shared-references/reviewer-routing.md`.
- **MAX_INTERNAL_DRAFT_ROUNDS = 2** — draft → lint → revise.
- **VENUE_MODE = `single_document`** — `single_document` for one shared author response, or `per_reviewer_thread` when each reviewer thread renders independently. Confirm the venue/interface before drafting if unclear. Affects Phase 4/7 output shape.
- **STRESS_TEST_ROUNDS_BASE = 1** — One external reviewer critique round on the full response set. Add one focused round for `reviewer_priority: pivotal` responses. Hard cap at 2 (Phase 6 "Iterations").
- **MAX_FOLLOWUP_ROUNDS = 3** — per reviewer thread.
- **REBUTTAL_DIR = `rebuttal/`**

> Override: `/rebuttal "paper/" — venue: NeurIPS, character limit: 5000`

## Reviewer Calling Convention

For `codex`, use `mcp__codex__codex` for new review threads and `mcp__codex__codex-reply` for follow-up rounds (reuse threadId). Other backends: the note at the top of this file.

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
| [references/rhetoric.md](references/rhetoric.md) | Phase 4, Phase 8 | 话术: answer shape, thanks opener, persuading moves (P1–P4), refuting moves (R1–R10), anti-patterns, phrase bank, co-author and user-edit lessons (C1–C27), user rulings on cost and run wording (C28–C29), drafting moves from co-author text (C30–C33), secondary evidence only when asked (C34), active voice with "we" (C35), inherited dataset errors attributed to their source (C36), "unstable measurement" turned into the contribution with a human / prior SOTA / ours table (C37) |
| [references/comparison-rules.md](references/comparison-rules.md) | Phase 4, Phase 5 lint 13 | minimum evidence, one metric per reply, one measurement setup for every arm, intervals, ties, weak number vs best of the rest, words agree with numbers |
| [references/wording-pass.md](references/wording-pass.md) | Phase 6.5 | wording pass on the finished draft, for the drafter: order of the steps, reconcile, tighten filler, reword (delete → replace → define) and rewrite for voice and cohesion — the overlay passed to `/paper-polish`, whose editor subagent runs `/paper-prose-tighten` (cut) then `/paper-jargon-pass` (reword, rewrite) — the drafter's checks on its edits, one owner per number; what is never touched; acceptance; user rulings L1–L11 on reported findings |
| [references/lints.md](references/lints.md) | Phase 5, and wherever a later step names a lint by number | lints 8–26: design choices, cross-thread duplication, weakness and concession, thanks opener, Limitations promises, comparison, self-contradiction, foreign content, unverified causes, measurements, outlier framing, new-result framing, readability, number density, secondary evidence, voice, deference lines, Conventions line, AC-note rating tags |
| [references/blind-read.md](references/blind-read.md) | Phase 6.5 blind read and acceptance read, Phase 8 blind read before posting — handed to the blind-read subagent, which gets no other method file | who the reader is, the three signals to record, ledger format |
| [references/posting-and-endgame.md](references/posting-and-endgame.md) | Phase 7, before the closing note | posting order, the closing note before the discussion closes (public thank-you to the AC and reviewers with a summary of the discussion, § 2a; a separate thank-you in the thread of each positive-score or score-raising reviewer, § 2c; confidential closing message to the AC whenever some reviewer has not confirmed a positive rating: thanks, the concerns in bold with what we did, where the rebuttal stands, who supports us, each remaining reviewer as no reply / open concern / factual error, why we disagree with an opposing view, thanks again, § 2b), after every round |
| [references/round2-replies.md](references/round2-replies.md) | Phase 8 (every reviewer comment after round 1 is posted) | what is frozen once round 1 is posted, delta replies, shape of a round-2 reply (title, bold thanks, agree, answer, rating request + invitation to ask more, thanks), replies to a reviewer who confirms acceptance (incl. the two-sentence closing reply once a rating request did not move the score, and the thanks-only reply that thanks the original review's strengths in one sentence when reservations remain and nothing can answer them), a new analysis in a round-2 reply (definitions, denominators, adjustment, CI format, headings, no caveats, promises), nudges (all-reviewer first, then one reviewer per post, one each; silent positive left alone, silent negative → AC, and in the last days another nudge after 24 h plus, for the last silent negative one, a short AC note at the same time), score requests (one per reviewer), the all-reviewer thank-you posted 24 h after round 1 (§ 8) |
| [references/collaboration.md](references/collaboration.md) | Phase 4 collaborator doc, whenever a co-author has touched the shared draft | the collaborator doc: layout, derived drafts, one link, HackMD sync (§ 9); who owns which text, co-author version vs ours (wording → theirs, substance → note), check against the source not our board, marking, sync direction, comments and suggestions, safe doc edits |
| [references/revised-pdf.md](references/revised-pdf.md) | Phase 4, before any edit to the paper for a revised PDF | only reviewer-raised edits; a small revision (appendices pruned to what a reply cites, by commenting out); paper and replies do not repeat; a requested baseline in a submitted table; internal evidence against a printed sentence waits for camera-ready |
| [references/misconduct-reporting.md](references/misconduct-reporting.md) | Phase 2 (`bad_faith_suspected`), on user request | strict vs malicious triage, evidence pack, channel and timing, note to the AC, what never to do |

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
| `*.html` | both, optional | derived — an HTML view of a canonical response file; regenerate it whenever that file changes |
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
6. **Check instance-level complaints by hand** (「单个样本之类的需要手动check下具体咋回事」). When a concern cites a specific sample, example, input or table cell, open that exact instance and see what actually happened before choosing a response mode; do not answer it from aggregate statistics or from the reviewer's description. Record the finding in the issue card. The same holds for implementation questions ("which parameters are trained", "how is X computed", "what does the checkpoint contain"): answer from the training script, the framework source for any flag whose meaning matters, and the released artifact — never from the paper's own wording, which is what the reviewer is questioning ([references/rhetoric.md](references/rhetoric.md) C14).
7. **Pick the lever per reviewer** (「他给1分不太对，但是不是扳不回来 2分哥，看起来是只要补实验就可以 1分哥，主要是要和他掰扯到毛病挑不出来」). A low score is not final. For each negative-score reviewer, write in `STRATEGY_PLAN.md` which lever moves them:
   - `experiments` — the concerns are missing evidence (e.g. a typical 2): run what they asked for; the reply mostly reports it.
   - `argument` — the concerns attack soundness or claims (e.g. a typical 1): go through every objection and close it — refuted with evidence already in the paper or in user-confirmed new results, or closed with an approved fix — until nothing is left to fault. No point goes unanswered.
8. **Posting order** (「先一个一个回复，看正分审稿人愿不愿意confirm，他们一般confirm之后就不动了. 然后麻烦的负分先留到最后」). Post replies one reviewer at a time, positive-score reviewers first: once they confirm their score they rarely move again. The difficult negative-score reviewers go last. Record the order in `STRATEGY_PLAN.md`; drafting may run in parallel, posting follows the order (Phase 7). **Every board, doc and HTML view lists the reviewers in this same order from its first version: highest score first, lowest last** (user 2026-11-12「下次应该把高分的放前面, 你先让正分confirm」). Do not lead with the lowest-scoring or most confident reviewer.
9. Identify **blocked claims** (ungrounded or unapproved)
10. If unresolved blockers or evidence gaps (a concern that needs a new experiment) → pause and present them to the user

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
- **Significance is defined once, in a Conventions line** (user 2026-11-13「开头定义一下 convention … 不要在正文中说不然很奇怪」). When a reply reports three or more significance statements or intervals, or a reply already defines one, its opening carries `**Conventions.** *Significant* means that the 95% bootstrap interval of a difference, resampled over <unit>, excludes zero.` (state the true resampling unit; add the draw count or a correction such as Holm only if the reply relies on it). The body then says "significant(ly)" and never repeats "the 95% … interval excludes zero"; bracketed intervals in tables may stay. If the opener is a co-author's text, the Conventions line is its own paragraph after it, in our colour.
- **Never expose a weakness** (user 2026-11-07: 「所有暴露缺点的都不提. 如果 reviewer 明确要了, 那给 user 定」). Nothing in a response file reveals a weakness of our work unless the reviewer explicitly asked for that exact thing. Weaknesses include: a metric or comparison a baseline (or a trivial reference such as a constant predictor) wins; a failed, inconclusive or negative rebuttal experiment; an error we found in our own paper, data or prompts; a caveat or limitation the reviewer did not raise; a model or variant we tried and dropped. Leave it out entirely — no figures AND no qualitative acknowledgment (no "trails", "lower than", "not as strong as", "however", "one limitation is" phrasing): report our own number, anchor comparisons on the metrics we win, and state the claim in positive scope terms ("the model's validated strength is X"), which requires no reference to the opponent. If the reviewer explicitly asked for it (the unfavorable number itself, the experiment that came out negative, the flaw they named), do not decide alone: mark the issue `needs_user_input`, put the options in `ISSUE_BOARD.md`, and write it only the way the user rules. Conceding is never an option ("Never concede").
- **Never concede** (user 2026-11-07: 「不能有任何让步」). No sentence in a response file, and no edit in a revised PDF, agrees that a criticism of our work is right, retracts or narrows one of our claims, adopts the reviewer's deflating term for it, credits our design to prior work, or admits a limitation, an error or an unfinished part. This holds even when the reviewer is right on a local point, and for the words alone ("we agree", "we accept", "correct", "the reviewer is right", "we concede"), including apologies ("sorry for the misunderstanding", "we apologize", "we regret the confusion"), which concede and also tell the AC the reviewer misread. Answer with what holds: the evidence we win on, stated in positive scope terms. A missing citation is answered with "we will cite X" and nothing more (「漏引的就说会引用就好了」): no admission that it was missing, no credit of our design to it. **Exception — a change the reviewer explicitly requested, answered in the reviewer's own word** (user 2026-11-09: 算「审稿人明确要求的修改，用他的原词回应」). When the review asks for a presentation change in so many words ("Please reconcile these descriptions", "clarify", "make consistent", "add"), the reply may report that change using the reviewer's verb: "Per your comment, we have reconciled the two descriptions … so the two places use the same wording." This answers the request; it is not a concession. It still never says the earlier text was wrong, an error, a mistake, incorrect or inconsistent, and never "we agree"; it quotes the revised text instead (rhetoric C16). Revision promises that add material (a table, a citation, a new result) stay; a promise that retracts or qualifies a claim is a concession and is not made. When the reviewer explicitly asked for a result that goes against us, the user still decides whether it is reported ("Never expose a weakness"), and the reply never frames it as a concession.
- **What "explicitly asked" covers** (user 2026-11-07). Read it off the issue card's `asked_for`, which comes from the raw text, never from a paraphrase. "Compare with X" makes the comparison with X mandatory, but leaves the metric to us. A metric we lose on is "asked for" only when the reviewer named that metric or granularity ("report rank correlation", "does it order the models correctly"). Before telling the user "the reviewer asked for Y", quote the sentence that asks for Y. If no sentence does, the losing number is an ordinary weakness: leave it out without escalating.
- **Choosing what to compare on** — once a comparison is mandatory, follow [references/comparison-rules.md](references/comparison-rules.md): one metric for every baseline in a reply, every win written (interval printed only when it excludes 0), no ties stated, no number that shows the flagship losing, words agree with numbers, and a weak number of ours is placed next to the best other methods reach on the same quantity ("Weak number → the best of the rest is weaker still", user 2026-11-09: 「如果说不好, 就写 别人的最好的也不如我们好」).
- **Rulings reach every draft.** When the user rules on an open question, record the ruling in `ISSUE_BOARD.md` (with the draft wording) and `REBUTTAL_STATE.md` right away. Then check every response file already written against it, including files another session drafted, and update them.
- **Limitations items are weaknesses.** When a reviewer lists Limitations (or asks that something "be stated explicitly"), answer each item on the merits exactly like a W#: 1-2 sentences of positive argument per item, grounded in numbers already in the response (framing like "Our position on each:"). Never reply with promise-to-revise phrasing ("will be written into the Limitations section", "becomes an explicit statement in the revised Limitations", "we will state in Limitations") — a promise-to-revise reads as conceding the point instead of defending it. The corresponding paper edit, if the author approves one, is tracked in `REVISION_PLAN.md` only and marked `unpromised`. Revision promises attached to W#/Q# answers ("We will add CIs to the per-region tables") remain allowed and stay future tense.

Hard rules:
- NEVER invent experiments, numbers, derivations, citations, or links
- NEVER promise what user hasn't approved
- If no strong evidence exists, say less not more

After authoring or changing a canonical draft, regenerate its derived artifacts per the Artifacts table (`single_document`: `PASTE_READY.txt`).

**Collaborator doc.** Every rebuttal gets one once the first drafts exist: `rebuttal/COLLAB_DOC.md`, in the team's language, pushed to HackMD by `scripts/collab_doc_sync.py`. Before creating or changing it, read [references/collaboration.md](references/collaboration.md) § 9 (layout, derived drafts, one link, co-author edits on HackMD).

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
- Before any edit to the paper for a revised PDF, read [references/revised-pdf.md](references/revised-pdf.md).

### Phase 5: Safety Validation

Run all lints:
1. **Coverage** — every issue maps to draft anchor
2. **Provenance** — every factual sentence has source
3. **Commitment** — promises are approved AND every paper-edit promise in the draft appears as a checklist item in `REVISION_PLAN.md` (and vice versa — no orphan items in the plan, except items marked `unpromised`: edits the author will make that the response text deliberately does not promise, per the Limitations rule)
4. **Tone** — flag aggressive/submissive/evasive phrases
5. **Consistency** — no contradictions across reviewer replies
6. **Limit** — exact character count on the paste target(s): freshly derived `PASTE_READY.txt`, or each `Reviewer_<ID>_response.md`. Compress if over (redundancy → friendly → opener → wording, never drop critical answers)
7. **Thread-local context** (`per_reviewer_thread` mode only) — each reviewer file must be intelligible without reading any other reviewer file. Flag any "see Reviewer X" references or undefined terms that rely on cross-thread context.

Lints 8–26 are in [references/lints.md](references/lints.md): read it now and run them all.

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

*For the Codex CLI:* one background session per reviewer file, so `per_reviewer_thread` files are tested in parallel. Each session is a one-shot review: its request carries the scope and, in round 2, the round-1 fixes.

```
codex exec -m gpt-6-astra -c model_reasoning_effort=xhigh -s read-only -C <repo root> --skip-git-repo-check \
  -o <trace dir>/<NNN>-<ID>.response.md - < <trace dir>/<NNN>-<ID>.request.md > <trace dir>/<NNN>-<ID>.log 2>&1 &
```

The prompt goes on stdin (`-`): with the prompt as an argument and stdin left open, `codex exec` stops at "Reading additional input from stdin" until it is killed. `<trace dir>` is the Review Tracing run directory (`.aris/traces/rebuttal/<date>_run<NN>/`), so the request, response and log files are the trace.

**Iterations.** Run the base round on the full draft. Then run one focused round on the `reviewer_priority: pivotal` responses, skipped when the base round raised no substantive issue in them. Hard cap at 2 rounds total (user ruling 2026-11-14: at most two review rounds per change, in every repository): tell the second round it is the last, limit it to the first round's fixes, and have it give each must-fix item as a replacement sentence; apply those and stop. Save each round to `rebuttal/MCP_STRESS_TEST_round<N>.md`; the highest round number represents the final state. If a hard safety blocker remains after round 2, report it to the user instead of running a third round.

### Phase 6.5: Wording Pass

Once the draft is complete and the stress-test fixes are in, run the wording pass of [references/wording-pass.md](references/wording-pass.md) (user 2026-11-09: 「rebuttal 生成完了, 用这些方法过一遍措辞」); read it now, not from memory. It changes wording only: everything else it finds goes to the user.

### Phase 7: Finalize

The stress-tested canonical file(s) from Phases 4-6 ARE the deliverable — do not produce any new copy of the response text here.

1. Regenerate every derived artifact from the final canonical file(s) (Artifacts table) and verify the paste targets against the venue limit: `PASTE_READY.txt` exact character count, or each `Reviewer_<ID>_response.md` word/char count
2. Optional, `per_reviewer_thread` mode: `rebuttal/SUPPLEMENTARY_FIG_PDF/` — when the venue does not allow PDF revision but allows anonymous figure links, generate a venue-compliant supplementary PDF. Do not hard-code an anonymous-hosting platform or typesetting style; choose what the target venue accepts.
3. Draft the closing note per [references/posting-and-endgame.md](references/posting-and-endgame.md) § 2 (posted in the last 24 h before the discussion closes, after the follow-up rounds): always the public thank-you to the AC and reviewers with a summary of the discussion (§ 2a) and a thank-you in the thread of each positive-score or score-raising reviewer (§ 2c), plus the confidential closing message to the AC whenever some reviewer has not confirmed a positive rating (§ 2b), and, for any `bad_faith_suspected` reviewer, the evidence pack and confidential AC note per [references/misconduct-reporting.md](references/misconduct-reporting.md) (sent last, once the positive-score reviewers are secured, § 3 there). Both are drafts for the user to send; never post them. Also hand the user the all-reviewer thank-you ([references/round2-replies.md](references/round2-replies.md) § 8, fixed text), to post about 24 h after the round-1 replies are up.
4. Update `rebuttal/REBUTTAL_STATE.md`
5. Refresh `rebuttal/REVISION_PLAN.md` so the overall checklist matches the final draft (add items, mark `already_done` as checked, carry forward any `pending` items)
6. Present to user:
   - Posting order (Phase 3 step 8): which reply goes up next — positive-score reviewers first, one at a time, watching whether each confirms; negative-score reviewers last
   - Paste target(s) with counts vs venue limit
   - `REVISION_PLAN.md` checklist — counts of pending / approved / deferred
   - Wording pass (Phase 6.5): bugs and decisions it surfaced first, then what was deleted and reworded, and what was kept
   - Remaining risks + lines needing manual approval

### Phase 8: Follow-Up Rounds

When new reviewer comments arrive, follow [references/round2-replies.md](references/round2-replies.md) (frozen round-1 text, delta replies, reply shape, new analyses, nudges, score requests) and [references/rhetoric.md](references/rhetoric.md):

1. Append verbatim to `rebuttal/FOLLOWUP_LOG.md`
2. Link to existing issues or create new ones
3. Draft **delta reply only** (not full rewrite)
4. Update `rebuttal/REVISION_PLAN.md` in place — add any new checklist items introduced by the follow-up, tick off items the author has already completed, and keep existing items' status current
5. Re-run safety lints, then one fresh blind read of the delta reply before posting ([references/round2-replies.md](references/round2-replies.md) § 2 item 7); no full wording pass
6. Use the appropriate reply tool for continuity if useful (per Reviewer Calling Convention)
7. Before writing each reply, reread [references/round2-replies.md](references/round2-replies.md) § 3–§ 8; never write it from memory
8. Rules: escalate technically not rhetorically; never concede (Phase 4 "Never concede"); for a reviewer whose lever is `argument` (Phase 3 step 7), keep closing each new objection until none is left, but never repeat an argument that already failed — bring new evidence or a new angle, or stop

## Key Rules

- **Never fabricate.** No invented evidence, numbers, derivations, citations, or links.
- **Never overpromise.** Only promise what user explicitly approved.
- **Full coverage.** Every reviewer concern tracked and accounted for.
- **Preserve raw records.** Reviews and MCP outputs stored verbatim.
- **Answer friendly reviewers too.** Reinforce supportive framing.
- **Closing note.** Before the discussion closes, thank the AC and summarize what the discussion resolved and why accept (posting-and-endgame § 2a), thank each positive-score or score-raising reviewer in their own thread (§ 2c); the remaining reviewers (no reply, open concern, factual error) and why we disagree go only to the AC (§ 2b).
- **Evidence > rhetoric.** Derivations and numbers over prose.
- **Don't waste space on unwinnable arguments.** Answer once, move on.
- **Write for the AC.** The reviewer may never move; the AC must see each point met with evidence. Outlier framing goes only into the AC-only closing note (posting-and-endgame § 2b).
- **Respect the limit.** Character budget is a hard constraint.
- **Resume cleanly.** Continue from REBUTTAL_STATE.md on rerun.
- **Every other drafting rule is stated once, where it applies**: Phase 4 defensive moves (never concede, never expose a weakness), the Phase 5 lints, the Phase 6.5 wording pass, and the reference files.
- **Anti-hallucination citations.** Any reference added must go through DBLP → CrossRef → [VERIFY].

## Review Tracing

After each reviewer call, save the trace following `shared-references/review-tracing.md` (Policy C — forensic; never silently skip). Use `save_trace.sh` (resolved per the chain in `shared-references/integration-contract.md` §2) or write files directly to `.aris/traces/<skill>/<date>_run<NN>/`. Respect the `--- trace:` parameter (default: `full`).
