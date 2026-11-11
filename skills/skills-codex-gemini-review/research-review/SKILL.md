---
name: "research-review"
description: "Get a deep critical review of research from Gemini via gemini-review MCP. Use when user says \"review my research\", \"help me review\", \"get external review\", or wants critical feedback on research ideas, papers, or experimental results."
---

> Override for Codex users who want **Gemini**, not a second Codex agent, to act as the reviewer. Install this package **after** `skills/skills-codex/*`.

# Research Review via `gemini-review` MCP (high-rigor review)

> **Gemini overlay assurance:** `review_independence: cross-family` and `acceptance_status: accepted`.

Get a multi-round critical review of research work from an external LLM with maximum reasoning depth.

## Constants

- **REVIEWER_MODEL = `gemini-review`** — Gemini reviewer invoked through the local `gemini-review` MCP bridge. Set `GEMINI_REVIEW_MODEL` if you need a specific Gemini model override.

## Context: $ARGUMENTS

## Prerequisites

- Install the base Codex-native skills first: copy `skills/skills-codex/*` into `~/.codex/skills/`.
- Then install this overlay package: copy `skills/skills-codex-gemini-review/*` into `~/.codex/skills/` and allow it to overwrite the same skill names.
- Register the local reviewer bridge:
  ```bash
  codex mcp add gemini-review -- python3 ~/.codex/mcp-servers/gemini-review/server.py
  ```
- This gives Codex access to `mcp__gemini-review__review_start`, `mcp__gemini-review__review_reply_start`, and `mcp__gemini-review__review_status`.


## Workflow

### Step 1: Gather Research Context
Before calling the external reviewer, compile a comprehensive briefing:
1. Read project narrative documents (e.g., STORY.md, README.md, paper drafts)
2. Read any memory/notes files for key findings and experiment history
3. Identify: core claims, methodology, key results, known weaknesses
4. For a manuscript, give the entry `.tex` file and the directories that hold its
   figures and tables. Do not write down what each float shows, which argument
   it serves, or where each argument's evidence sits: the reviewer builds that
   map itself (FLOAT AND ARGUMENT MAP block, Step 2).

### Step 2: Initial Review (Round 1)
Send a detailed prompt with high-rigor review:

```
mcp__gemini-review__review_start:
  prompt: |
    [Full research context + specific questions]
    Please act as a senior ML reviewer (NeurIPS/ICML level). Identify:
    1. Logical gaps or unjustified claims
    2. Missing experiments that would strengthen the story
    3. Narrative weaknesses
    4. Whether the contribution is sufficient for a top venue

    === SCOPE LIMITS (these bound what you PROPOSE, never what you look for) ===
    Report anything that is actually wrong here — including a rare-looking case, if
    this repo actually produces it. Then keep the fix in scope:
    1. This is a RESEARCH-WORKFLOW tool, not a security paper. Verification is
       welcome; over-defense is not. Assume a cooperating operator on their own
       machine — a malicious local user is NOT in the threat model.
    2. Do NOT propose SHA / hash / content-fingerprint / digest-binding schemes.
       Reporting a real defect in hashing code that already exists is fine.
    3. NO speculative machinery: do not add feature flags, migration frameworks,
       compat layers, wrappers, pins, or similar mechanisms unless evidence shows
       a current repo defect they fix or an explicit existing invariant they must
       preserve. "Load-bearing", "compatibility", and "not scaffolding" are labels,
       not evidence. Point to the failing path/artifact or invariant, and check the
       proposal's factual premises, such as whether a named package version exists.
    4. NO corner-case obsession: exotic encodings, symlink races, RTL text and
       millisecond races are out of scope unless you can show the case arises here.
    5. Where a rubric or checklist is genuinely needed, do not over-mechanize
       judgement. A clear sentence a human reads beats a scored table nobody
       maintains.
    Exception: code that runs remote commands, starts a network service, or installs
    an MCP server runs on the user's machine with their credentials — trust-boundary
    findings there are in scope and the default is strict.
    Say plainly when something is correct. Do not manufacture findings.
    Be brutally honest. If, after genuinely trying to break it, the work
    holds up and is ready, say so clearly.

    === FLOAT AND ARGUMENT MAP (manuscripts; two required named fields at the end of your reply) ===
    Every figure and every table must serve an argument the paper makes: a
    contribution, a motivation, or a stated advantage of the method. Build the map
    yourself from the manuscript. Output a field named "Float map" with one line per
    figure and per table, main text and appendix, numbered as the compiled PDF
    prints them:
      <Figure/Table N> — what it shows, with its decisive numbers — the argument it
      serves (quote that sentence and give its location) — the sections that cite
      it, or "cited only in its own appendix section".
    Setup and protocol tables serve reproducibility; say so instead of forcing a
    claim onto them.
    The main text must be self-contained: every argument it makes carries at least
    one or two pieces of its evidence in the main text itself. The appendix may add
    evidence (more settings, breakdowns, protocol details); it never holds all of
    it. Output a field named "Argument map" with one line per argument the main text
    makes (a contribution, a motivation, a stated advantage, a result claim, a
    design choice justified by a result):
      <quote the sentence, give its location> — its main-text evidence: a main-text
      figure or table, a number with its comparison in main-text prose, or a
      citation for a claim about prior work (give each location) — its appendix
      evidence, if any.
    Under "Flagged", list with its anchor every float that:
      1. serves no argument (a result no claim rests on);
      2. is cited only in its own appendix section;
      3. does not support the sentence that cites it, e.g. a baseline or an
         undeployed variant holds the decisive cell of the column that sentence
         leans on;
    and every main-text argument that:
      4. has no supporting evidence in the main text: its evidence sits only in the
         appendix (e.g. the sentence rests on "see Appendix C" alone) or nowhere.
    A flagged float or argument is a Critical Weakness only if it would sink the paper.
```

After this start call, immediately save the returned `jobId` and poll `mcp__gemini-review__review_status` with a bounded `waitSeconds` until `done=true`. Treat the completed status payload's `response` as the reviewer output, and save the completed `threadId` for any follow-up round.

### Step 3: Iterative Dialogue (Rounds 2-N)
Use `mcp__gemini-review__review_reply_start` with the saved completed `threadId`, then poll `mcp__gemini-review__review_status` with the returned `jobId` until `done=true` to continue the conversation:

For each round:
1. **Respond** to criticisms with evidence/counterarguments
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
- For a manuscript, the reviewer's float map and argument map, and every float and argument it flagged
- Prioritized TODO list with estimated compute costs
- Paper outline if discussed

Update project memory/notes with key review conclusions.

## Key Rules

- Always ask the Gemini reviewer for strict, high-rigor feedback.
- Send comprehensive context in Round 1 — the external model cannot read your files
- Be honest about weaknesses — hiding them leads to worse feedback
- Focus on ACTIONABLE feedback — "what experiment would fix this?"
- Document the completed `threadId` for potential future resumption
- In a manuscript, every figure and table must serve an argument (user 2026-11-03,
  「每个图表都应该服务论点」), and every main-text argument carries at least one or
  two pieces of its evidence in the main text, never all of it in the appendix
  (user 2026-11-11, 「main 正文应该 self contain」): send the FLOAT AND ARGUMENT MAP
  block, manuscripts only, in the first-round prompt and in every follow-up brief.
  The reviewer builds the map; do not pass on your own map or reading of what a
  float shows or where an argument's evidence sits (reviewer-independence.md).
- The review document should be self-contained (readable without the conversation)

## Prompt Templates

### For initial review:
"I'm going to present a complete ML research project for your critical review. Please act as a senior ML reviewer (NeurIPS/ICML level)..."

### For experiment design:
"Please design the minimal additional experiment package that gives the highest acceptance lift per GPU week. Our compute: [describe]. Be very specific about configurations."

### For paper structure:
"Please turn this into a concrete paper outline with section-by-section claims and figure plan."

### For claims matrix:
"Please give me a results-to-claims matrix: what claim is allowed under each possible outcome of experiments X and Y?"

### For mock review:
"Please write a mock NeurIPS review with: Summary, Strengths, Weaknesses, Questions for Authors, Score, Confidence, and What Would Move Toward Accept."
