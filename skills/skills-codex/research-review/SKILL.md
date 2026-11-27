---
name: "research-review"
description: "Get a deep critical review of research from a fresh Codex agent or a selected Gemini, Grok, or Claude Code reviewer. Use when user says \"review my research\", \"help me review\", \"get external review\", or wants critical feedback on research ideas, papers, or experimental results."
---

# Research Review with a Selectable Reviewer

> **Codex assurance:** the fresh base reviewer is same-family. Record
> `review_independence: same-family` and `acceptance_status: provisional` in
> traces and deliverables. A selected reviewer can record cross-family accepted
> only after a completed, in-scope positive review with actual different model
> families; an unavailable reviewer is BLOCKED, never a fabricated PASS.

Get a multi-round critical review of research work from an external LLM with maximum reasoning depth.

## Constants

- REVIEWER_MODEL = `gpt-6-astra` — Model used via a secondary Codex agent, reasoning effort `max` (deep-audit tier; capability fallback per `reviewer-routing.md`, never below `xhigh`). Must be an OpenAI model (e.g., `gpt-6-astra`, `gpt-6.1-sol`)
- **REVIEWER_BACKEND = `codex`** — Default: a fresh Codex reviewer at the deep-audit tier (`max`). Resolve `— reviewer:`, project `.aris/reviewer.json`, then this default using `reviewer_route.py` (`--host codex --tier deep`), per [reviewer-backends.md](../shared-references/reviewer-backends.md). Gemini/Antigravity, Grok, and Claude Code use that contract at every call below; legacy `oracle-pro` rules remain in `reviewer-routing.md`.

## Context: $ARGUMENTS

## Prerequisites

- The selected review tool must be available. Native Codex uses authorized `spawn_agent` and `send_input`; MCP routes use their own first/reply tools.
- If the selected reviewer is unavailable, record `REVIEW_UNAVAILABLE`. The executor reviewing itself does not satisfy the fresh-reviewer requirement.

## Workflow

### Step 1: Gather Research Context
Before calling the reviewer:
1. For a manuscript, give the entry `.tex` file and the directories that hold its
   figures and tables. Do not write down what each float shows, which argument
   it serves, or where each argument's evidence sits: the reviewer builds that
   map itself (FLOAT AND ARGUMENT MAP block, Step 2).
2. For a manuscript, run the mechanical checkers of the `research-paper-writing` skill before the
   reviewer is called, and keep their output:
   ```bash
   W=<skills dir>/research-paper-writing/scripts
   python3 $W/check_draft.py <introduction .tex> <experiments .tex>
   python3 $W/check_figures.py --layout two <entry .tex>     # --layout one for a one-column venue
   ```
   `check_draft.py` compares the introduction with award papers (logical connectors per 100 words,
   sentence length, runs of short sentences) and flags experiments sentences with more than two numbers;
   `check_figures.py` flags long captions and long first caption sentences, table captions below the
   tabular, and ranking tables with no shaded row. These are counts, not
   judgements: do not send them to the reviewer, and do not treat one as a finding until the sentence
   or caption it points at has been read.

### Step 2: Initial Review (Round 1)
Save the resolved route and its session id/cwd. Send the following substantive
prompt through the selected first-call tool, with primary artifact paths inside
the review workspace. The native Codex example uses max reasoning:

```
spawn_agent:
  model: REVIEWER_MODEL
  reasoning_effort: max
  message: |
    [Original research question, author claims, specific questions, and primary
    artifact/raw-result paths. Read those files to check the claims yourself.]
    Please act as a senior ML reviewer (NeurIPS/ICML level). Start from the
    assumption that the work is broken somewhere — your job is to find where.
    Be adversarial. Trust nothing the author tells you — verify everything
    yourself. Identify:
    1. Logical gaps or unjustified claims
    2. Missing experiments that would strengthen the story
    3. Narrative weaknesses
    4. Whether the contribution is sufficient for a top venue

    Be brutally honest. If, after genuinely trying to break it, the work
    holds up and is ready, say so clearly.
```

A manuscript gets two reviewer threads and two reports, one on logic (above) and
one on structure (below) (user 2026-11-16: 「一个看逻辑, 一个看结构」). Start the
structure thread in the same turn as a second fresh agent over the same files;
each keeps its own agent id, rounds and trace, and neither is shown the other's
output. An idea or project context gets the logic thread only. Fill
`[SECTION POLICY]` with the absolute path of
`../shared-references/manuscript-craft.md`, never a summary of it.

**Report each thread as it lands** (user 2026-11-16: 「先汇报出来的, 这样节约时间」).
When one thread returns, spot-check its anchors, save its trace, write its report,
and give the user its findings at once; do not hold them until the other thread
returns. The thread still running is named as running, never summarized ahead of
its reply.

```
spawn_agent:
  model: REVIEWER_MODEL
  reasoning_effort: max
  message: |
    [Primary manuscript paths: entry .tex file, figure and table directories.]
    Trust nothing the author tells you — verify everything yourself.

    [Role]
    You are a senior reviewer for [VENUE]. Read the manuscript for its structure
    only: what each section is for, whether each piece of content sits in the
    section that owns it, the order it comes in, and whether the space each part
    takes matches what it carries. A separate reviewer judges the claims, the
    evidence and the novelty: do not judge whether a result convinces, whether a
    baseline is missing, or how new the work is.

    [Section policy]
    Judge each section against §2 of [SECTION POLICY] and against [VENUE]'s own
    instructions; the venue wins where they differ.

    [What to check]
    1. Role. Each section does its own job and only that job. Flag content in the
       wrong section: a result argued in the Method, method detail first given in
       the Experiments, related-work discussion in the Introduction, a new result
       or qualifier in the Conclusion.
    2. Length. The space a part takes matches its weight. A summary part (the
       abstract, the introduction's contribution paragraph, the conclusion) states
       the claim; it does not re-list the benchmarks, settings or numbers the body
       already reports. A side point given a paragraph, or the main result given a
       clause, is flagged too.
    3. Order. Sections and paragraphs follow the argument, and each paragraph opens
       with the point it makes.
    4. Repetition. The same content at the same level of detail in two places,
       beyond the intended cascade (section opening -> introduction -> abstract,
       each a stricter summary of the one below).

    [Evidence rule]
    Every issue carries an anchor: the section and paragraph (quote its first
    words), or the figure or table number. An issue you cannot anchor is dropped.

    [Output]
    - "Section map": one line per section and subsection, in order: its job in
      one phrase — what it actually holds — its length in paragraphs — ok or
      flagged.
    - "Structure issues": each flagged item, the one that costs a reader most
      first: its anchor, which of checks 1-4 it fails, and the move (cut, compress
      to what length, move to which section, or reorder). Report only what is
      there; write "No structure issues found." when nothing survives.
    No score, no verdict, and no prose outside these fields and the fields any
    block appended below requires.

    === FLOAT AND ARGUMENT MAP (manuscripts; two required named fields at the end of your reply) ===
    Every figure and every table must serve an argument the paper makes: a
    contribution, a motivation, or a stated advantage of the method. Build the map
    yourself from the manuscript. Output a field named "Float map" with one line per
    figure and per table, main text and appendix, numbered as the compiled PDF
    prints them:
      <Figure/Table N> — what it shows, with its decisive numbers — the argument it
      serves (quote that sentence and give its location) — the sections that cite
      it.
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
      2. does not support the sentence that cites it, e.g. a baseline or an
         undeployed variant holds the decisive cell of the column that sentence
         leans on;
    and every main-text argument that:
      3. has no supporting evidence in the main text: its evidence sits only in the
         appendix (e.g. the sentence rests on "see Appendix C" alone) or nowhere.
    and every float or passage in the wrong medium (a figure before a table, a
    table before prose):
      4. a table whose conclusion is a shape a figure would show: a trend over an
         ordered variable, a ranking or gap among a few arms, a distribution, a
         breakdown into parts, a trade-off between two quantities;
      5. a prose passage, main text or appendix, that walks through values,
         settings or parallel items one by one where a table or figure would hold
         them.
    and every passage or part of a float, main text or appendix, that supports
    no argument:
      6. a sentence, a number, a paragraph, a reported experiment, or a part of a
         table (a row or a column) that
         states no argument the paper makes, is not evidence for one, does not
         define what one is about (a term, the setup, a protocol constant) and
         does not bound one (a denominator, a scope limit, a result that weighs
         against it). A row or column is evidence only if a sentence, in the
         prose or in the caption's opening, reads it. Quote it or name it, give
         its location and say in one line what it is.
    and every reported variant that extends the method and does not improve it:
      7. a row, a series or a paragraph for a variant that gives the method more
         of what it already uses (another round, more training steps, more data,
         a larger model, a longer schedule) whose result is not better than the
         method's and is not settled either way by the paper's own test. It
         supports no argument and shows a reader where the method stops
         improving. Name it, give its location and its numbers against the
         method's, and say whether any sentence of the main text rests on it.
    and every printed number a reader cannot trace:
      8. a number in a table cell, a caption or a sentence whose origin the
         paper does not give, or whose form is noisier than what it says: a
         setting solved from another quantity and printed as the solved value
         ("the top 31.4%", picked so that two sets come out the same size); a
         threshold or fraction the authors chose, with no reason or citation
         beside it; a count pair "N of M" in a table cell; more digits than
         the neighbouring numbers carry. Quote it, give its location and say
         which kind it is.
    An appendix float or section needs no citation from the main text or from
    another appendix section: one cited only where it sits is fine. Do not flag
    it and do not ask for a pointer to it.
    A flagged float or argument is a Critical Weakness only if it would sink the paper.
```

### Step 3: Iterative Dialogue (Rounds 2-N)
Use the selected continuation tool with the saved session id. Preserve its
model and cwd; a manuscript's logic and structure threads continue separately,
each with its own id. For native Codex this is `send_input`:

```text
send_input:
  target: [saved reviewer id from Step 2]
  message: |
    Please continue the review using the revised materials below.

    Revised files:
    - /absolute/path/to/file1
    - /absolute/path/to/file2

    Focus on unresolved weaknesses and whether the revision actually fixed them.
```

Each round asks the reviewer to re-check each prior criticism against the
revised files and rule SUSTAINED / OVERRULED / PARTIALLY SUSTAINED. Do not argue
the point in prose: an account of what you changed, or of why the criticism was
wrong, is what `../shared-references/reviewer-independence.md` forbids passing to
a reviewer.

### Step 4: Document Everything
Write a **logic report** and, for a manuscript, a **structure report**, each
self-contained and each written when its own thread returns. Both go in one
directory per reviewed draft, beside the raw files: the brief, the prompt files,
each thread's raw reply and the checker output. Each report opens with one
paragraph: reviewer session id, model and effort as run, what the reviewer was
given, and the score and verdict. Then, each under its own heading, the logic
report has:
- what the reviewer credits
- the major issues and, apart from them, the other suggestions: each with its anchor, whether the anchor holds, and what to do
- the findings an experiment can address: the experiment and the claim or table cell it would settle; say so when there are none

and the structure report has:
- the section map and every structure issue whose anchor holds, with its move
- the float map and argument map, and every float and argument flagged
- under its own heading, every passage and every row or column of a table that supports no argument (flag 6): the quote or its name, its location, one line on what it is, and the proposal (for a row or column whose numbers favor the method, the sentence to add; otherwise delete it, or put it to the user, with the reason)
- under its own heading, every variant that extends the method (another round, more steps, more data) and is neither better nor settled (flag 7): its location, its numbers against the method's, whether a main-text sentence rests on it, and the proposal, which is to hide it (`review-float-map.md`, Acting)
- under its own heading, every printed number a reader cannot trace (flag 8): the quote, its location and its kind (a solved value, a chosen setting with no reason, an `N of M` cell, extra digits).
- the checker warnings of Step 1 that hold after reading the text they point at, under their own heading, apart from the reviewer's points

Both reports also list the findings dropped (an anchor that does not hold, or a
point the user has already ruled on), each with its reason, and, when an earlier
draft was reviewed, what changed against that report. The user's rulings on a
report are appended to it under their own heading with the date; a follow-up
round is appended to the same report.

With `— composed: <canonical-report-path>` (`/idea-discovery` passes it), fold
the conclusions into that report and cite the trace path instead of writing a
report of your own; without the directive, never infer composed mode, and
`— standalone` always wins
([`output-composition.md`](../shared-references/output-composition.md)).

### Step 5: Review Tracing

Save a trace for every reviewer call following `../shared-references/review-tracing.md`. Record the resolved route, session id/cwd, requested and actual reported model/effort, prompt, raw response, decisions, and action items. Check successful completion and required file coverage before assigning a verdict. Record model-family independence and acceptance using `reviewer-backends.md`; agreement alone does not establish cross-family acceptance.

## Key Rules

- Provide comprehensive context and primary files in Round 1; require artifact-grounded verification. An unreadable file is missing evidence.
- Be honest about weaknesses — hiding them leads to worse feedback
- Focus on ACTIONABLE feedback — "what experiment would fix this?"
- Document the agent id for potential future resumption
- In a manuscript, every figure and table must serve an argument (user 2026-11-03,
  「每个图表都应该服务论点」), and every main-text argument carries at least one or
  two pieces of its evidence in the main text, never all of it in the appendix
  (user 2026-11-11, 「main 正文应该 self contain」), and evidence takes a figure before a table, a table before prose (user 2026-11-19, `manuscript-craft.md` §4): send the FLOAT AND ARGUMENT MAP
  block in the structure thread's first-round prompt and in every follow-up brief.
  The reviewer builds the map; do not pass on your own map or reading of what a
  float shows or where an argument's evidence sits (reviewer-independence.md).
- The review document should be self-contained (readable without the conversation)
