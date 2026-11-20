---
name: research-review
description: Get a deep critical review of research from a selected reviewer (Codex by default, Gemini, Grok, Claude Code, or manual). Use when user says "review my research", "help me review", "get external review", or wants critical feedback on research ideas, papers, or experimental results.
argument-hint: "[topic-or-scope]"
allowed-tools: Bash(*), Read, Grep, Glob, Write, Edit, mcp__codex__codex, mcp__codex__codex-reply, mcp__manual_review__review, mcp__manual_review__review_reply, mcp__antigravity__antigravity, mcp__antigravity__antigravity-reply, mcp__grok__grok, mcp__grok__grok-reply, mcp__claude-review__review, mcp__claude-review__review_reply, mcp__claude-review__review_start, mcp__claude-review__review_reply_start, mcp__claude-review__review_status
---

# Research Review via External Reviewer Backend (max reasoning)

> 🔒 **Do not wrap this skill in `/loop`, `/schedule`, or `CronCreate`.** It is
> verdict-bearing — it produces a cross-model review verdict, multi-round with
> reviewer thread continuity. An external timer re-fires the verdict on
> wall-clock time and breaks the reviewer's round-to-round memory: zero new
> signal, full token cost. Schedule the *external wait that precedes it* (work
> ready → then review once), not the verdict. See
> [`shared-references/external-cadence.md`](../shared-references/external-cadence.md).

Get a multi-round critical review of research work from the selected external reviewer backend with maximum reasoning depth.

## Constants

- REVIEWER_MODEL = `gpt-6-astra` — Default model for the Codex backend, reasoning effort `max` (deep-audit tier). Must be an OpenAI model (e.g., `gpt-6-astra`, `gpt-6.1-sol`). Manual backend uses a model the user chooses — it must be a recognized model from a different family (OpenAI, Anthropic, Google, DeepSeek, Moonshot/Kimi, Qwen).
- **REVIEWER_BACKEND = `codex`** — Default: Codex MCP (max). Resolve `— reviewer:`, project `.aris/reviewer.json`, then this default using `reviewer_route.py` (`--host claude-code --tier deep`), per [reviewer-backends.md](../shared-references/reviewer-backends.md). Gemini/Antigravity, Grok, and Claude Code use that contract at every call below. Legacy Oracle/manual contracts remain in `reviewer-routing.md`; unavailable selected routes do not silently fall back.
- **REVIEWER_PERSONA = `P1`** — The frame the reviewer is asked to adopt, from
  [`../shared-references/reviewer-personas.md`](../shared-references/reviewer-personas.md).
  `P1` (Gatekeeper: reject-by-default, scored, plus a rewrite strategy) is the
  default because this skill answers "is this submittable?". Override with
  `— persona: P2` for an unscored, six-heading, evidence-anchored review when
  the deliverable is a verifiable fix list rather than a verdict. It sets the
  logic thread; a manuscript's structure thread always runs P4.

## Two reports for a manuscript

A manuscript gets two reviewer threads and two reports, one on logic and one on
structure (user 2026-11-16: 「一个看逻辑, 一个看结构」). Start both in Round 1,
in parallel, as fresh threads over the same brief and files; each keeps its own
threadId, rounds and trace, and neither is shown the other's output:

- **Logic thread** — REVIEWER_PERSONA + SCOPE LIMITS: are the claims new,
  supported and consistent.
- **Structure thread** — P4 (`reviewer-personas.md` §8) + FLOAT AND ARGUMENT
  MAP: what each section is for, where content sits, how long each part runs,
  and whether every float serves an argument.

An idea or project context has no sections: it gets the logic thread only.

**Report each thread as it lands** (user 2026-11-16: 「先汇报出来的, 这样节约时间」).
The threads finish at different times. When one returns, spot-check its anchors,
save its trace, write its report, and give the user its findings at once. Do not
hold one thread's results until the other returns. The thread still running is
named as running, never summarized ahead of its reply.

## Passages that expose a weakness

Some findings are anchored on a passage in which the manuscript itself hands the
reader the weakness. Whether the reviewer flags one or the executor notices it
while spot-checking anchors, it is reported and put to the user under the rule of
`/paper-claim-audit` (*Disclosure ledger: delete what stands alone, ask about
the rest*), which owns it: the same ledger rows under their own heading in the
logic report, the stand-alone ones deleted and listed, the rest asked.

## Persona

Send the persona template **verbatim** from `reviewer-personas.md` (§2 for P1,
§3 for P2), with `[VENUE]` and the manuscript/context fields filled in. Do not
paraphrase it — the reject-by-default framing and the evidence-anchor clause are
what make the output actionable rather than flattering.

The anchor rule (`reviewer-personas.md` §4) applies to every round, including the
spot-check that drops a finding whose anchor does not hold up. Do not restate it
here — it has one owner.

At idea/project stage the artifact is not a manuscript: send P1's
**proposal-stage variant** (§2), which anchors findings to the supplied context
files and lifts the ban on citing outside literature, since prior-work coverage
is what the review is for at that stage.

Follow-up rounds obey `reviewer-personas.md` §5: **no prose rebuttal** — the
reviewer re-reads the current files and rules SUSTAINED / OVERRULED / PARTIALLY
SUSTAINED itself.

## Reviewer Calling Convention

When calling the reviewer, branch on REVIEWER_BACKEND:

**If REVIEWER_BACKEND ∈ {antigravity, grok, claude-code}:**
  Use the selected first/reply protocol in `reviewer-backends.md`, with the
  same review prompt, explicit cwd containing the primary files, and resolved
  provider-specific model/effort. Save route, cwd and session id for continuation.
  A Claude Code bridge may run DeepSeek; derive family from its reported model.

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

Content fidelity: the manual reviewer should see the same substantive review
brief Codex would read. If the manual UI supports file upload / attachment,
reuse the same brief file; otherwise paste the brief contents inline because
remote web UIs cannot read your local filesystem paths. Review tracing applies
equally to both backends.

## Context: $ARGUMENTS

## Prerequisites

- The selected MCP must be available. For the default **Codex MCP Server**:
  ```bash
  claude mcp add codex -s user -- python3 "$HOME/aris_repo/mcp-servers/codex-exec/server.py"   # your ARIS clone's path
  ```
- This gives Claude Code access to `mcp__codex__codex` and `mcp__codex__codex-reply` tools

## Workflow

### Step 1: Gather Research Context
Before calling the external reviewer, compile a comprehensive briefing:
1. Read project narrative documents (e.g., STORY.md, README.md, paper drafts)
2. Read any memory/notes files for key findings and experiment history
3. Identify: core claims, methodology, key results, known weaknesses
4. For a manuscript, give the entry `.tex` file and the directories that hold its
   figures and tables. Do not write down what each float shows, which argument
   it serves, or where each argument's evidence sits: the reviewer builds that
   map itself ([`review-float-map.md`](../shared-references/review-float-map.md)).
5. For a manuscript, run the mechanical checkers of the `research-paper-writing` skill before the
   reviewer is called, and keep their output:
   ```bash
   W=<skills dir>/research-paper-writing/scripts
   python3 $W/check_draft.py --abstract <abstract .tex> <introduction .tex> <experiments .tex>
   python3 $W/check_figures.py --layout two <entry .tex>     # --layout one for a one-column venue
   ```
   `check_draft.py` compares the abstract and introduction with award papers (logical connectors per 100 words,
   sentence length, runs of short sentences), flags an abstract with no number, three sentences of one paragraph
   in the "outperforms" frame and "slightly" in either, and flags experiments sentences with more than two numbers;
   `check_figures.py` flags long captions and long first caption sentences, table captions below the
   tabular, and ranking tables with no shaded row. These are counts, not
   judgements: do not send them to the reviewer, and do not treat one as a finding until the sentence
   or caption it points at has been read.

### Step 2: Initial Review (Round 1)
Send a detailed prompt with max reasoning, using the selected backend. For
the `codex` backend, keep the MCP payload short: write the full briefing to
`RESEARCH_REVIEW_REQUEST.md`, then point Codex at that file.

*For codex backend:*

```
mcp__codex__codex:
  model: gpt-6-astra
  config: {"model_reasoning_effort": "max"}
  prompt: |
    Read the review brief at <absolute path to RESEARCH_REVIEW_REQUEST.md>.
    Executor notes are not evidence beyond the files they cite, so verify the
    referenced artifacts before judging. Trust nothing the author tells you —
    verify everything yourself.

    [REVIEWER_PERSONA template, verbatim from shared-references/reviewer-personas.md]

    [SCOPE LIMITS block, verbatim from shared-references/review-scope-limits.md]
```

For a manuscript, start the structure thread in the same turn, as a second
fresh call:

```
mcp__codex__codex:
  model: gpt-6-astra
  config: {"model_reasoning_effort": "max"}
  prompt: |
    Read the review brief at <absolute path to RESEARCH_REVIEW_REQUEST.md>.
    Trust nothing the author tells you — verify everything yourself.

    [P4 template, verbatim from shared-references/reviewer-personas.md §8, with
    [SECTION POLICY] = the absolute path of shared-references/manuscript-craft.md]

    [FLOAT AND ARGUMENT MAP block, verbatim from shared-references/review-float-map.md]
```

For Antigravity, Grok, or Claude Code, send the same prompt through its selected
first-call tool; do not copy Codex's `config` into another tool. Check successful
completion and actual file coverage before interpreting the response.

The persona template already carries the role, the reject-by-default stance, the
review dimensions (originality / rigor / claim-evidence consistency), the anchor
requirement, and the output contract — do not restate the role in your own words.
The review brief carries the substance: full research context, the specific
questions, and the primary artifact / raw-result paths the reviewer should
inspect.

*For manual backend:* use `mcp__manual_review__review` with the same persona
template and brief contents. If the manual-review UI supports attachments, attach
`RESEARCH_REVIEW_REQUEST.md`; otherwise paste the brief inline. Save the
returned `threadId`.

### Step 3: Iterative Dialogue (Rounds 2-N)
For `codex` backend: use `mcp__codex__codex-reply` with the returned `threadId`.
For `manual` backend: use `mcp__manual_review__review_reply` with the same `threadId`.
For Antigravity, Grok, or Claude Code: use the saved route's continuation protocol
in `reviewer-backends.md`; keep its model/cwd and repeat Claude cwd/tools.
Use the appropriate tool to continue the conversation; a manuscript's logic and
structure threads continue separately, each with its own threadId. For Codex follow-up
rounds, write an updated brief such as `RESEARCH_REVIEW_ROUND_2.md` and send
only the path:

```text
mcp__codex__codex-reply:
  threadId: [saved reviewer threadId from Step 2]
  # replies inherit the thread's model/effort (gpt-6-astra max)
  prompt: |
    Read the updated review brief at <absolute path to
    RESEARCH_REVIEW_ROUND_2.md>.
    Focus on unresolved weaknesses and whether the revision actually fixed them.
```

For manual follow-up rounds, attach that same updated brief if possible;
otherwise paste it inline.

For each round:
1. **Re-submit the updated artifact** and ask the reviewer to re-check each
   prior criticism against the current files and rule SUSTAINED / OVERRULED /
   PARTIALLY SUSTAINED. Do not argue the point in prose — an account of what you
   changed, or of why the criticism was wrong, is exactly what
   `shared-references/reviewer-independence.md` forbids passing to a reviewer.
2. **Ask targeted follow-ups** on the most actionable points
3. **Request specific deliverables**: experiment designs, paper outlines, claims matrices

Key follow-up patterns:
- "If we reframe X as Y, does that change your assessment?"
- "What's the minimum experiment to satisfy concern Z?"
- "Please design the minimal additional experiment package (highest acceptance lift per GPU week)"
- "Please write a mock NeurIPS/ICML review with scores"
- "Give me a results-to-claims matrix for possible experimental outcomes"

### Step 4: Convergence
Stop iterating when:
- Both sides agree on the core claims and their evidence requirements
- A concrete experiment plan is established
- The narrative structure is settled

### Step 5: Document Everything
Save the full interaction and conclusions to a review document in the project root:
- Round-by-round summary of criticisms and responses
- Final consensus on claims, narrative, and experiments
- Claims matrix (what claims are allowed under each possible outcome)
- Prioritized TODO list with estimated compute costs
- Paper outline if discussed
- For a manuscript, the passages that expose a weakness, each with the question to the user (see *Passages that expose a weakness*)

For a manuscript that document is the **logic report**, and the structure thread
gets its own **structure report** beside it, each self-contained and each written
when its own thread returns (see *Two reports for a manuscript*):
- the section map and every structure issue whose anchor holds, with its move
- the float map and argument map, and every float and argument flagged
- the checker warnings of Step 1 that hold after reading the text they point at, under their own heading, apart from the reviewer's points

Update project memory/notes with key review conclusions.

> **Composed mode** — if invoked with `— composed: <canonical-report-path>` (an
> orchestrator like `/idea-discovery` passes this), do **not** write a standalone review
> `.md` in the project root. The raw conversation is already persisted to `.aris/traces/…`
> (see *Review Tracing* below — that audit copy is kept in every mode); fold the review
> *conclusions* (consensus, claims matrix, prioritized TODOs, and a manuscript's
> structure issues under their own heading) into the orchestrator's
> canonical report and cite the trace path there. **Default (no `— composed:` directive):
> behave exactly as above — write the standalone review document.** Never infer composed
> mode from a report file merely existing. Full rules:
> [`shared-references/output-composition.md`](../shared-references/output-composition.md).

## Key Rules

- For the default Codex route, pin `model: gpt-6-astra` + `config: {"model_reasoning_effort": "max"}` (deep-audit tier; capability fallback per `reviewer-routing.md`, never below `xhigh`). Other selected routes use their resolved model/effort.
- For `manual`, use the identity-bearing config above. Tool fields belong to their own provider contracts; do not copy a payload between bridges.
- Put comprehensive context in the review brief. Codex can read local files
  when you pass an absolute path; manual reviewers usually cannot, so attach or
  paste the same brief there.
- Be honest about weaknesses — hiding them leads to worse feedback
- Focus on ACTIONABLE feedback — "what experiment would fix this?"
- Every weakness must carry an evidence anchor; spot-check anchors before acting, and drop findings whose anchor does not check out
- In a manuscript, every figure and table must serve an argument (user 2026-11-03), and every main-text argument carries at least one or two pieces of its evidence in the main text, never all of it in the appendix (user 2026-11-11), and evidence takes a figure before a table, a table before prose (user 2026-11-19, `manuscript-craft.md` §4): send the FLOAT AND ARGUMENT MAP block of `shared-references/review-float-map.md` in the structure thread's first-round prompt and every follow-up brief; the reviewer builds the map
- Document the threadId for potential future resumption
- The review document should be self-contained (readable without the conversation)

## Prompt Templates

### For initial review:
Use the REVIEWER_PERSONA template verbatim (`../shared-references/reviewer-personas.md` §2 for P1, §3 for P2), then append the project context. The follow-up templates below are additive — they run inside the same thread after the persona review lands.

### For experiment design:
"Please design the minimal additional experiment package that gives the highest acceptance lift per GPU week. Our compute: [describe]. Be very specific about configurations."

### For paper structure:
"Please turn this into a concrete paper outline with section-by-section claims and figure plan."

### For claims matrix:
"Please give me a results-to-claims matrix: what claim is allowed under each possible outcome of experiments X and Y?"

### For mock review:
"Please write a mock NeurIPS review with: Summary, Strengths, Weaknesses, Questions for Authors, Score, Confidence, and What Would Move Toward Accept."

## Review Tracing

After each reviewer call, save the trace following `shared-references/review-tracing.md` (Policy C — forensic; never silently skip). Record the selected route/session/cwd, requested and reported models, actual effort, raw response, completion and scope, verdict, independence and acceptance per `reviewer-backends.md`. Use `save_trace.sh` (resolved per the chain in `shared-references/integration-contract.md` §2) or write files directly to `.aris/traces/<skill>/<date>_run<NN>/`. Respect the `--- trace:` parameter (default: `full`).
  A verdict-bearing manual response MUST begin with
  `Reviewer-Model: <exact-model-id>` — pass the model THIS session is actually
  running as in `executor_model`. Missing, unknown, or same-family identity
  cannot acquit; emit `REVIEW_UNAVAILABLE` rather than guessing. If the executor
  model cannot be named, manual review's cross-family claim is unprovable — say
  so in the report instead of asserting it.
