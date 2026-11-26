---
name: research-review
description: Get a deep critical review of research from a selected reviewer (Codex by default, Gemini, Grok, Claude Code, or manual). Use when user says "review my research", "help me review", "get external review", or wants critical feedback on research ideas, papers, or experimental results.
argument-hint: "[topic-or-scope]"
allowed-tools: Bash(*), Read, Grep, Glob, Write, Edit, mcp__codex__codex, mcp__codex__codex-reply, mcp__manual_review__review, mcp__manual_review__review_reply, mcp__antigravity__antigravity, mcp__antigravity__antigravity-reply, mcp__grok__grok, mcp__grok__grok-reply, mcp__claude-review__review, mcp__claude-review__review_reply, mcp__claude-review__review_start, mcp__claude-review__review_reply_start, mcp__claude-review__review_status
---

# Research Review via External Reviewer Backend (max reasoning)

Get a multi-round critical review of research work from the selected external reviewer backend with maximum reasoning depth.

## Constants

- REVIEWER_MODEL = `gpt-6-astra`, reasoning effort `max` (deep-audit tier; capability fallback per `reviewer-routing.md`, never below `xhigh`). Must be an OpenAI model (e.g., `gpt-6-astra`, `gpt-6.1-sol`).
- **REVIEWER_BACKEND = `codex`** — With no `— reviewer:` argument and no project
  `.aris/reviewer.json` this is the route (`reviewer_route.py --project <root>
  --host claude-code --tier deep` prints the same), so there is nothing to
  resolve. A selected Gemini/Antigravity, Grok or Claude Code route takes its
  first and reply calls, model and effort from
  [reviewer-backends.md](../shared-references/reviewer-backends.md), manual and
  Oracle from `reviewer-routing.md`, with the same prompt files and cwd; a
  selected route that is unavailable does not fall back silently.
- **REVIEWER_PERSONA = `P1`** — The frame the reviewer is asked to adopt, from
  [`../shared-references/reviewer-personas.md`](../shared-references/reviewer-personas.md).
  `P1` (Gatekeeper: reject-by-default, scored, plus a rewrite strategy) is the
  default because this skill answers "is this submittable?". Override with
  `— persona: P2` for an unscored, six-heading, evidence-anchored review when
  the deliverable is a verifiable fix list rather than a verdict. It sets the
  logic thread; a manuscript's structure thread always runs P4.
- **REVIEW_INPUT = `source`** — What a manuscript's reviewer may read. `source`
  (default): the LaTeX source directory and, if one is supplied, the compiled
  PDF. `pdf`: the compiled PDF and nothing else, as a conference reviewer sees
  the submission; see *PDF-only mode*. Override with `— input: pdf`; a project's
  own instructions may fix the mode, and then every call follows it.

## Two reports for a manuscript

A manuscript gets two reviewer threads and two reports, one on logic and one on
structure (user 2026-11-16: 「一个看逻辑, 一个看结构」). Start both in Round 1,
in parallel, as fresh threads over the same brief and files; each keeps its own
threadId, rounds and trace, and neither is shown the other's output:

- **Logic thread** — REVIEWER_PERSONA: are the claims new, supported and
  consistent.
- **Structure thread** — P4 (`reviewer-personas.md` §8) + FLOAT AND ARGUMENT
  MAP: what each section is for, where content sits, how long each part runs,
  whether every float serves an argument, and which passages support none.

An idea or project context has no sections: it gets the logic thread only.

**Report each thread as it lands** (user 2026-11-16: 「先汇报出来的, 这样节约时间」).
The threads finish at different times. When one returns, spot-check its anchors,
save its trace, write its report, and give the user its findings at once. Do not
hold one thread's results until the other returns. The thread still running is
named as running, never summarized ahead of its reply.

## PDF-only mode

With REVIEW_INPUT = `pdf` the reviewer judges the paper a conference reviewer
would receive: no source, no comments left in the `.tex`, no result files, no
project notes. It applies to both threads of a manuscript and to every round.

1. **Review directory.** Compile the manuscript, then put the PDF alone in a
   new, empty directory outside the project tree. For the structure thread,
   copy `manuscript-craft.md` into the same directory and give that copy as
   `[SECTION POLICY]` (`--section-policy`). Write the brief and the prompt
   files into it as well. The reviewer's cwd is this directory, read-only.
2. **Brief.** It names the venue, the PDF, and the submission status (which
   pages are frozen, if any), and says that the PDF is the whole submission and
   that nothing outside this directory may be read. It lists no source file,
   no figure or table directory, and no path into the project.
3. **Anchors.** The reviewer anchors each finding to a page, a section, a
   figure or table number as printed, and a quoted sentence; it cannot give a
   file and line. The executor maps each anchor to the source during the
   spot-check. The anchor rule and its four cases are unchanged.
4. **Checkers.** Step 1's mechanical checkers still run on the source; the
   executor runs them, and their output is never sent to the reviewer.
5. **Scope check.** When a thread returns, read its trace for any file it
   opened outside the review directory. A finding that rests on such a file is
   dropped as an anchor that does not hold (case 2), and the trace's `scope`
   field and the report record what was read. A read-only sandbox does not
   confine reads to the cwd, so this check is what enforces the mode.
6. **Trace and report.** Record `review_input: pdf` in the trace, and state in
   each report's first paragraph that the reviewer saw only the PDF.

A finding that the PDF cannot settle (for example, whether two tables share a
set of episodes) arrives as `No direct evidence found in the manuscript.` and is
handled as case 3: the paper should say it, or the executor confirms from the
source that it already does and drops the finding.

## Passages that expose a weakness

Some findings are anchored on a passage in which the manuscript itself hands the
reader the weakness. Whether the reviewer flags one or the executor notices it
while spot-checking anchors, it is reported and put to the user under the rule of
`/paper-claim-audit` (*Disclosure ledger: delete what stands alone, ask about
the rest*), which owns it: the same ledger rows under their own heading in the
logic report, the stand-alone ones deleted and listed, the rest asked. A row or
cell the reviewer picked out of a table where the method is mostly higher is not
such a passage: the finding is dropped under `reviewer-personas.md` §4, case 4.

## Persona

The logic thread gets the persona template of `reviewer-personas.md` (§2 for
P1, §3 for P2) exactly as written, with only its bracketed fields filled:
`scripts/build_prompts.py` (Step 2) copies it. Never paraphrase or restate it —
the reject-by-default framing and the evidence-anchor clause are what make the
output actionable rather than flattering.

The anchor rule (`reviewer-personas.md` §4) applies to every round, including the
spot-check that drops a finding whose anchor does not hold up. Do not restate it
here — it has one owner.

At idea/project stage the artifact is not a manuscript: send P1's
**proposal-stage variant** (§2), which anchors findings to the supplied context
files and lifts the ban on citing outside literature, since prior-work coverage
is what the review is for at that stage. Name it in the prompt: `--logic-only
--input "Variant: proposal-stage (reviewer-personas.md §2)"`.

## Context: $ARGUMENTS

## Workflow

### Step 1: Gather Research Context
Before calling the reviewer:
1. For a manuscript, give the entry `.tex` file and the directories that hold its
   figures and tables (in *PDF-only mode*, the PDF alone). Do not write down what each float shows, which argument
   it serves, or where each argument's evidence sits: the reviewer builds that
   map itself ([`review-float-map.md`](../shared-references/review-float-map.md)).
2. For a manuscript, run the mechanical checkers of the `research-paper-writing` skill before the
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
Write the brief to `RESEARCH_REVIEW_REQUEST.md` (in *PDF-only mode*, into the
review directory). It carries what the templates do not: the specific questions
and the primary artifact / raw-result paths the reviewer should inspect, and for
an idea or project the context itself. Then build the prompt files:

```bash
python3 <this skill's dir>/scripts/build_prompts.py --out <prompt dir> \
  --brief <absolute path to RESEARCH_REVIEW_REQUEST.md> --venue "<VENUE>" \
  --input "Manuscript: <absolute path> (<what it is, e.g. the compiled PDF; the whole submission>)"
# add --persona P2, --section-policy <the copy> (PDF-only mode), --logic-only (an idea or project)
```

It writes `logic_prompt.txt` (REVIEWER_PERSONA) and `structure_prompt.txt` (P4,
then the FLOAT AND ARGUMENT MAP block of `review-float-map.md`). Each template is
copied unchanged from its fence in shared-references with only its bracketed
fields filled, and the script stops if one is left. Send each file, unedited, as
its thread's whole prompt, both fresh threads in the same turn:

```
mcp__codex__codex:
  model: REVIEWER_MODEL
  config: {"model_reasoning_effort": "max"}
  sandbox: read-only
  cwd: <review cwd>
  prompt: |
    Your complete prompt is <absolute path to logic_prompt.txt>. Read it and
    follow it exactly as written.
```

The structure thread is the same call on `structure_prompt.txt`. When the
`codex` MCP server is not connected in this session, run the bridge's own
`codex exec` command with each file on stdin, and `codex exec resume` for
follow-up rounds: [`references/codex-exec.md`](references/codex-exec.md). Check
successful completion and actual file coverage before interpreting a response.

### Step 3: Iterative Dialogue (Rounds 2-N)
A manuscript's logic and structure threads continue separately, each with its
own threadId. Every round follows `reviewer-personas.md` §5: re-submit the
current files and have the reviewer re-check each prior criticism against them
and rule SUSTAINED / OVERRULED / PARTIALLY SUSTAINED. Do not argue the point in
prose — an account of what you changed, or of why the criticism was wrong, is
exactly what `shared-references/reviewer-independence.md` forbids passing to a
reviewer. Write the updated brief, such as `RESEARCH_REVIEW_ROUND_2.md`, rerun
the script with `--round 2 --brief <its absolute path>` (the structure thread's
prompt carries the FLOAT AND ARGUMENT MAP block again), and send:

```text
mcp__codex__codex-reply:
  threadId: [saved reviewer threadId from Step 2]
  # replies inherit the thread's model and effort
  prompt: |
    Your complete prompt is <absolute path to logic_prompt_round2.txt>. Read it
    and follow it exactly as written.
```

### Step 4: Document Everything
Write a **logic report** and, for a manuscript, a **structure report**, each
self-contained and each written when its own thread returns (see *Two reports
for a manuscript*). Both go in one directory per reviewed draft, beside the raw
files: the brief, the prompt files, each thread's raw reply and the checker
output. Each report opens with one paragraph: thread
id, reviewer model and effort as run, how it was called (MCP tool or `codex
exec`), what the reviewer was given, and the score and verdict. Then, each under
its own heading, the logic report has:
- what the reviewer credits
- the major issues and, apart from them, the other suggestions: each with its anchor, whether the anchor holds, and what to do
- the findings an experiment can address: the experiment and the claim or table cell it would settle; say so when there are none
- the passages that expose a weakness, each with the question to the user (see *Passages that expose a weakness*)

and the structure report has:
- the section map and every structure issue whose anchor holds, with its move
- the float map and argument map, and every float and argument flagged
- under its own heading, every passage and every row or column of a table that supports no argument (flag 6): the quote or its name, its location, one line on what it is, and the proposal (for a row or column whose numbers favor the method, the sentence to add; otherwise delete it, or put it to the user, with the reason)
- under its own heading, every variant that extends the method (another round, more steps, more data) and is neither better nor settled (flag 7): its location, its numbers against the method's, whether a main-text sentence rests on it, and the proposal, which is to hide it (`review-float-map.md`, Acting)
- the checker warnings of Step 1 that hold after reading the text they point at, under their own heading, apart from the reviewer's points

Both reports also list the findings dropped (an anchor that does not hold,
`reviewer-personas.md` §4 case 4, or a point the user has already ruled on), each
with its reason, and, when an earlier draft was reviewed, what changed against
that report. The user's rulings on a report are appended to it under their own
heading with the date; a follow-up round is appended to the same report.

With `— composed: <canonical-report-path>` (`/idea-discovery` passes it), fold
the conclusions into that report and cite the trace path instead of writing a
report of your own; without the directive, never infer composed mode
([`output-composition.md`](../shared-references/output-composition.md)).

## Key Rules

- Be honest about weaknesses — hiding them leads to worse feedback
- Focus on ACTIONABLE feedback — "what experiment would fix this?"
- A manuscript's structure thread carries the FLOAT AND ARGUMENT MAP block in every round, and the reviewer builds the map; the rulings behind it (user 2026-11-03, 2026-11-11, 2026-11-19) are owned by [`review-float-map.md`](../shared-references/review-float-map.md)
- Document the threadId for potential future resumption
- The review document should be self-contained (readable without the conversation)

## Review Tracing

After each reviewer call, save the trace following `shared-references/review-tracing.md` (Policy C — forensic; never silently skip). Record the selected route/session/cwd, requested and reported models, actual effort, raw response, completion and scope, verdict, independence and acceptance per `reviewer-backends.md`. Use `save_trace.sh` (resolved per the chain in `shared-references/integration-contract.md` §2) or write files directly to `.aris/traces/<skill>/<date>_run<NN>/`. Respect the `--- trace:` parameter (default: `full`).
