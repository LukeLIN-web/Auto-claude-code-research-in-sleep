---
name: "novelty-check"
description: "Verify research idea novelty against recent literature, and read the idea and its closest prior work for 实用、好用、成功率高 (practical, easy to use, high success rate). Use when user says \"查新\", \"novelty check\", \"有没有人做过\", \"check novelty\", or wants to verify a research idea is novel before implementing."
---

> Override for Codex users who want **Gemini**, not a second Codex agent, to act as the reviewer. Install this package **after** `skills/skills-codex/*`.

# Novelty Check Skill

> **Gemini overlay assurance:** `review_independence: cross-family` and `acceptance_status: accepted`.

Check whether a proposed method/idea has already been done in the literature: **$ARGUMENTS**

## Constants

- **REVIEWER_MODEL = `gemini-review`** — Gemini reviewer invoked through the local `gemini-review` MCP bridge. Set `GEMINI_REVIEW_MODEL` if you need a specific Gemini model override.

## Instructions

Given a method description, systematically verify its novelty:

### Phase A: Extract Key Claims
1. Read the user's method description
2. Identify 3-5 core technical claims that carry the claimed delta:
   - What is the method?
   - What problem does it solve?
   - What is the mechanism?
   - What makes it different from obvious baselines?
3. Freeze the **core delta** before any search: the one or two design choices
   that define the method, i.e. what it does differently at training or
   deployment (what is trained, on which data, with which labels or inputs,
   which components run at deployment). Write it as one sentence. The score is
   judged on this sentence, and it is not redefined after a paper turns up.
4. Write down what the idea must deliver in practice (the user's top priority:
   实用、好用、成功率高 — practical, easy to use, high success rate):
   - which success rate it must beat, against which **simplest strong
     baseline** (e.g. the underlying policy run alone, the best off-the-shelf
     method on that benchmark), under the same protocol;
   - what it needs at deployment on a new task (per-task exploration or
     tuning, demos, CAD / digital twin, privileged simulator state, a closed
     frontier API at inference, training compute);
   - what one episode costs (wall-clock, API spend).
5. Fix the prior-art cutoff from the target venue's concurrent-work rule.
   Take the venue and its cutoff from the project (its CLAUDE.md or memory)
   when it names them; otherwise read the venue's call for papers or reviewer
   guidelines (e.g. CVPR 2027: work first public after 2026-09-15 is
   concurrent). Write down the venue, the cutoff date and the rule's own
   wording for the boundary. If no venue is known, say so in the report and
   treat every paper as prior work until the user names one. Take the
   neighbour scope from the project the same way (e.g. robotics and
   embodied work only, not phone-GUI, web, math, code or text-only
   agents); a paper outside it is neither prior nor concurrent work.

### Phase B: Multi-Source Literature Search
For EACH core claim, search using ALL available sources:

1. **Web Search** (via `WebSearch`):
   - Search arXiv, Google Scholar, Semantic Scholar
   - Use specific technical terms from the claim
   - Try at least 3 different query formulations per claim
   - Include year filters for 2024-2026

2. **Known paper databases**: Check against:
   - ICLR 2025/2026, NeurIPS 2025/2026, ICML 2025/2026
   - CoRL 2025/2026, RSS 2025/2026, ICRA 2025/2026, IROS 2025/2026
   - Recent arXiv preprints (2025-2026)

3. **Read abstracts**: For each potentially overlapping paper, WebFetch its abstract and related work section

4. **Practicality read** (实用 / 好用 / 成功率高): for each paper that makes the
   Closest Prior Work table, read its results and setup sections (not just
   the abstract) and record, only from what the paper states (write "not
   reported" otherwise, never estimate):
   - **成功率高 / high success** — headline success and setting; margin over
     the simplest strong baseline under the same protocol, or "not compared";
     a system whose added orchestrator / tools do worse than its own base
     policy alone fails this axis.
   - **好用 / easy to use** — what a new task needs: per-task exploration,
     prompt tuning or demos; CAD or a digital twin; privileged simulator
     state (ground-truth poses, segmentation, rendered depth); a closed
     frontier API at inference; training data and compute; released code
     and weights.
   - **实用 / practical** — wall-clock and API cost per episode; real-robot
     evidence; unseen tasks / scenes / perturbations.
   Give each axis Yes / Partial / No with one reason and its source (table
   or section). The axis a close paper fails on is often where the proposed
   method can win.

5. **Date every overlapping paper** against the Phase-A cutoff. The date is
   when the overlapping content first went public: arXiv v1's date, which
   `verify_papers.py` (the anti-hallucination check below, run on every
   listed paper anyway) prints as `arxiv_v1_date`, or the date of the later
   version where that content first appears; for a paper not on arXiv,
   its first public date. Never guess the day from the arXiv id's month. Tag
   it **Prior** (public before the cutoff) or **Concurrent** (inside the
   venue's concurrent window). Keep searching up to today: concurrent work is
   still reported, cited and discussed.

### Phase C: Cross-Model Verification
Call REVIEWER_MODEL via `mcp__gemini-review__review_start` with high-rigor review:
```
mcp__gemini-review__review_start:
  prompt: |
    [Full novelty briefing + prior work list + specific novelty questions]
```

After this start call, immediately save the returned `jobId` and poll `mcp__gemini-review__review_status` with a bounded `waitSeconds` until `done=true`. Treat the completed status payload's `response` as the reviewer output, and save the completed `threadId` for any follow-up round.
Prompt should include:
- The proposed method description and the frozen core-delta sentence
- All papers found in Phase B, each with its first-public date and its
  Prior / Concurrent tag, plus the target venue, its cutoff, the rule's
  wording and the neighbour scope
- Ask: "Is this method novel? What is the closest prior work? What is the delta?"
- The Phase-A practicality targets and the Phase-B practicality read, and ask:
  "Is the proposed method practical, easy to use, and high-success compared
  with the closest work and with the simplest strong baseline? Correct any
  practicality cell you can check against the paper. What is the single
  biggest obstacle to it being practical, easy to use, or high-success?"
- The NOVELTY VERDICT LIMITS block below, verbatim — the reviewer judges under it

### The verdict limits

Copy this block **verbatim** into the reviewer's briefing; the report in
Phase D is judged under it too.

```
=== NOVELTY VERDICT LIMITS (these bound how you judge, never how widely you search) ===
Search exhaustively; judge calibrated. Two failures waste months equally:
passing an idea a published paper already contains, and killing a viable idea
because the territory has neighbors.
1. Proximity is information, not a verdict. Someone working nearby goes in the
   report; it is not by itself a reason to reject.
2. ABANDON has exactly one qualification: a specific prior paper, public
   before the target venue's concurrent-work cutoff, already contains this
   result — name that paper and its first-public date. No named prior paper,
   no ABANDON.
3. Crowded-but-deltaed is PROCEED: state the delta over prior work in one
   sentence a reviewer could verify. A thin delta, meaning a named prior paper
   contains the core delta in a narrower form, is PROCEED WITH CAUTION: say
   what would make it carry, not why it should die. CAUTION is not a safe
   middle: if you cannot name that paper, the verdict is PROCEED.
4. Concurrent work, public inside the venue's concurrent window, is never a
   veto and never lowers the score, even when its contribution is identical
   to this idea. That is a race — report it as work the paper must cite and
   discuss, and let the user decide whether to run it.
5. A direct attack on a central problem is legitimate novelty when nobody has
   executed it well. "This area is hot" does not mean "this area is taken."
6. This check is an early gate, never the last one — more triage, pilots, or
   external review still stand between any idea and a paper, whatever order
   this run uses. A wrongly passed idea dies cheaply at one of them; a wrongly
   killed idea is never seen again. When torn between two verdicts, choose the
   more permissive one.
7. Judge the frozen core delta, not each component. A prior paper lowers the
   score only when it contains the core delta. A paper that shares components,
   the paradigm, the benchmark or the evaluation setting but lacks the core
   delta costs no novelty. List it under "Shares components" in one line,
   with no deduction. "Every component has a prior" is true of almost every
   method, so it is never by itself a reason to call the delta thin.
8. A difference that changes what the system does at training or deployment
   (what is trained, on which data, with which labels or inputs, which
   components run at deployment) is a method difference. Only a difference in
   where it runs (sim or real, robot, benchmark, task set, scale) is a setting
   difference. Do not relabel method differences as setting differences.
9. Evidence gaps are not novelty: whether the current experiments isolate a
   component, or whether the data exercises it. Report them under "Evidence
   the paper needs". They never lower the score.
Score on the core delta:
   8-10  no prior paper contains the core delta (neighbours sharing
         components are normal)                                  -> PROCEED
   6-7   a prior paper contains part of the core delta; the rest is new
                                                                  -> PROCEED
   4-5   a prior paper contains the core delta in a narrower form (per task
         instead of pooled, one modality); the delta is that extension
                                                     -> PROCEED WITH CAUTION
   1-3   a prior paper contains the core delta and differs only in setting
                                      -> ABANDON candidate; name the paper
Say plainly when an idea clears the check. Do not manufacture overlap.
```

### Phase D: Novelty Report
Output a structured report:

```markdown
## Novelty Check Report

### Proposed Method
[1-2 sentence description]

### Core Delta (frozen in Phase A)
[one sentence]

### Target Venue and Cutoff
[venue] — prior work is public before [date]; [the rule's wording, source]

### Core Claims
1. [Claim 1] — Closest prior: [paper] — What stays unknown or different: [delta] — Concurrent: [paper], if any
2. [Claim 2] — Closest prior: [paper] — What stays unknown or different: [delta] — Concurrent: [paper], if any
...

### Closest Prior Work
Only papers that contain all, part, or a narrower form of the core delta.
| Paper | First public | Venue | Core delta: all / part / narrower | Overlap | Key Difference |
|-------|--------------|-------|-----------------------------------|---------|----------------|

### Shares Components (no deduction; whether to cite is the user's call)
- [paper, first public]: [the component it shares; the core-delta piece it lacks]

### Concurrent Work (cite and discuss; costs no novelty)
| Paper | First public | Overlap | Compare where possible |
|-------|--------------|---------|------------------------|

### Overall Novelty Assessment
- Score: X/10 on the core delta (scale in the verdict limits)
- Recommendation: PROCEED / PROCEED WITH CAUTION / ABANDON (per the verdict
  limits: crowded-but-deltaed ground is PROCEED; ABANDON must name a prior
  paper)
- Key differentiator: [what makes this unique over prior work, if anything]
- Risk: [what a reviewer would cite as prior work; what the venue rule still
  asks for concurrent work]

### Practicality (实用 / 好用 / 成功率高)
| Work | 成功率高 (vs simplest strong baseline) | 好用 (what a new task needs) | 实用 (cost, real robot, unseen) |
|------|------|------|------|
| [closest paper] | Yes/Partial/No — reason, source | ... | ... |
| **Proposed method** | ... | ... | ... |

- Verdict for the proposed method: PRACTICAL / NEEDS WORK / IMPRACTICAL,
  with the single biggest obstacle
- Where the neighbors fall short, and which of those gaps the proposed
  method can close with same-protocol numbers

### Evidence the Paper Needs (not novelty)
[experiments that would show the core delta is what helps; data that does not
yet exercise it]

### Suggested Positioning
[State the method by its core delta in one sentence a reviewer could verify.
Prior work goes in related work with the piece each lacks; frame the method as
an extension of a paper only when that paper contains the core delta. Name
concurrent work as concurrent]
```

### Important Rules
- **实用、好用、成功率高 matters most** (user ruling 2026-10-14: "实用、好用、
  成功率高最重要。我们必须要做实用、好用、成功率高的方法"). Novelty is a gate,
  not the goal: a novel idea that loses to the simplest strong baseline, or
  only works with per-task exploration, a digital twin, privileged simulator
  state, or minutes per episode, is reported as such in the Practicality
  section, however clean its delta. Practicality does not change the novelty
  verdict rules (ABANDON still needs a named paper); it is its own verdict.
- **Score the core delta, not the parts** (user ruling 2026-10-22: "感觉每次都
  分数太低"). Reports kept saying no prior paper did the whole thing and still
  scored 4-6, because "every component has a prior" read as a thin delta and
  papers lacking the defining mechanism were counted as deductions. The
  core-delta sentence is frozen before the search so it cannot be bent around
  a paper found later; a paper that contains it still costs the score.
- **Prior art ends at the target venue's concurrent-work cutoff** (user
  ruling 2026-10-14). Only prior work can make an idea not novel. Concurrent
  work may contain exactly the same contribution; that costs no novelty, but
  the paper still cites and discusses it, and compares where possible.
- Making a known but impractical method practical is a legitimate delta when
  shown with same-protocol numbers: success no lower, a named dependency
  removed, measured seconds or dollars saved per episode.
- Two failures waste months equally: a false novelty claim, and a viable idea
  abandoned because the territory has neighbors. Be brutally honest in both
  directions — and when an idea clears the check, say so plainly.
- Novelty can live in the combination or in a positive finding (X works) even
  when every individual claim rates LOW — judge the idea, not each claim in
  isolation.
- "Applying X to Y" earns novelty by what had to change in the method to work
  in Y, or by a positive finding the application reveals. Judge that, not the
  template.
- Check both the method AND the experimental setting for novelty
- **"We find X works" may be written; "we find X does not work" never is**
  (user ruling 2026-10-22: "「我们发现 X 有用」 可以写, 永远不写 我们发现 X
  没用"). A negative finding is never offered as the contribution; a failure
  mode is only motivation. Report what remains as the method's delta, and do
  not recommend downgrading a method contribution to a finding (user ruling
  2026-10-22: "不行, 你就作为新方法,").
- Always check the most recent 6 months of arXiv, up to today and past the
  cutoff — the field moves fast
- **Anti-hallucination for Closest Prior Work.** Every paper in the prior-work and concurrent-work tables must pass pre-search verification via `verify_papers.py` (canonical name resolved per [`shared-references/integration-contract.md`](../shared-references/integration-contract.md) §2; 3-layer arXiv / CrossRef / Semantic Scholar fallback inside the helper itself). Policy D1 (primary + degraded-output fallback): if the helper is unresolved **or** its invocation fails, tag candidate entries `[UNVERIFIED]` and surface the uncertainty rather than dropping them. Never fabricate arXiv IDs, DOIs, or titles from memory. Full protocol in [`shared-references/citation-discipline.md`](../shared-references/citation-discipline.md) § Pre-Search Verification Protocol.

