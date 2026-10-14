---
name: novelty-check
description: Verify research idea novelty against recent literature, and read the idea and its closest prior work for 实用、好用、成功率高 (practical, easy to use, high success rate). Use when user says "查新", "novelty check", "有没有人做过", "check novelty", or wants to verify a research idea is novel before implementing.
argument-hint: "[method-or-idea-description]"
allowed-tools: WebSearch, WebFetch, Grep, Read, Glob, mcp__codex__codex
---

# Novelty Check Skill

Check whether a proposed method/idea has already been done in the literature: **$ARGUMENTS**

## Constants

- REVIEWER_MODEL = `gpt-6-astra` — Model used via Codex MCP. Must be an OpenAI model (e.g., `gpt-6-astra`, `o3`, `gpt-4o`)

## Instructions

Given a method description, systematically verify its novelty:

### Phase A: Extract Key Claims
1. Read the user's method description
2. Identify 3-5 core technical claims that carry the claimed delta:
   - What is the method?
   - What problem does it solve?
   - What is the mechanism?
   - What makes it different from obvious baselines?
3. Write down what the idea must deliver in practice (the user's top priority:
   实用、好用、成功率高 — practical, easy to use, high success rate):
   - which success rate it must beat, against which **simplest strong
     baseline** (e.g. the underlying policy run alone, the best off-the-shelf
     method on that benchmark), under the same protocol;
   - what it needs at deployment on a new task (per-task exploration or
     tuning, demos, CAD / digital twin, privileged simulator state, a closed
     frontier API at inference, training compute);
   - what one episode costs (wall-clock, API spend).

### Phase B: Multi-Source Literature Search
For EACH core claim, search using ALL available sources:

1. **Web Search** (via `WebSearch`):
   - Search arXiv, Google Scholar, Semantic Scholar
   - Use specific technical terms from the claim
   - Try at least 3 different query formulations per claim
   - Include year filters for 2024-2026

2. **Known paper databases**: Check against:
   - ICLR 2025/2026, NeurIPS 2025, ICML 2025/2026
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

### Phase C: Cross-Model Verification
Call REVIEWER_MODEL via Codex MCP (`mcp__codex__codex`) with xhigh reasoning.
When the method description plus the Phase-B paper list is more than a short
note, avoid pasting it inline into the MCP prompt. Write a dossier file such as
`NOVELTY_DOSSIER.md` (or a project-local equivalent) containing the method
description, core claims, candidate papers, and the exact questions below, then
send only the file path:
```
mcp__codex__codex:
  model: gpt-6-astra
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    Read the novelty dossier at <absolute path to NOVELTY_DOSSIER.md> and
    follow all instructions in it.
```
Dossier contents should include:
- The proposed method description
- All papers found in Phase B
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
2. ABANDON has exactly one qualification: a specific published paper already
   contains this result — name that paper. No named paper, no ABANDON.
3. Crowded-but-deltaed is PROCEED: state the delta in one sentence a reviewer
   could verify. Thin or contested delta is PROCEED WITH CAUTION — say what
   would make it carry, not why it should die. CAUTION is not a safe middle:
   if you cannot name the specific thing that makes the delta thin, the
   verdict is PROCEED.
4. Concurrent or competing work is not a veto. That is a race — report it and
   let the user decide whether to run it.
5. A direct attack on a central problem is legitimate novelty when nobody has
   executed it well. "This area is hot" does not mean "this area is taken."
6. This check is an early gate, never the last one — more triage, pilots, or
   external review still stand between any idea and a paper, whatever order
   this run uses. A wrongly passed idea dies cheaply at one of them; a wrongly
   killed idea is never seen again. When torn between two verdicts, choose the
   more permissive one.
Say plainly when an idea clears the check. Do not manufacture overlap.
```

### Phase D: Novelty Report
Output a structured report:

```markdown
## Novelty Check Report

### Proposed Method
[1-2 sentence description]

### Core Claims
1. [Claim 1] — Closest: [paper] — What stays unknown or different: [delta]
2. [Claim 2] — Closest: [paper] — What stays unknown or different: [delta]
...

### Closest Prior Work
| Paper | Year | Venue | Overlap | Key Difference |
|-------|------|-------|---------|----------------|

### Overall Novelty Assessment
- Score: X/10 (anchor: 5/10 = has clear neighbors but a defensible delta worth
  a pilot; reserve 1-3 for results a named published paper already contains)
- Recommendation: PROCEED / PROCEED WITH CAUTION / ABANDON (per the verdict
  limits: crowded-but-deltaed ground is PROCEED; ABANDON must name the paper)
- Key differentiator: [what makes this unique, if anything]
- Risk: [what a reviewer would cite as prior work]

### Practicality (实用 / 好用 / 成功率高)
| Work | 成功率高 (vs simplest strong baseline) | 好用 (what a new task needs) | 实用 (cost, real robot, unseen) |
|------|------|------|------|
| [closest paper] | Yes/Partial/No — reason, source | ... | ... |
| **Proposed method** | ... | ... | ... |

- Verdict for the proposed method: PRACTICAL / NEEDS WORK / IMPRACTICAL,
  with the single biggest obstacle
- Where the neighbors fall short, and which of those gaps the proposed
  method can close with same-protocol numbers

### Suggested Positioning
[State the delta honestly in one sentence a reviewer could verify]
```

### Important Rules
- **实用、好用、成功率高 matters most** (user ruling 2026-10-14: "实用、好用、
  成功率高最重要。我们必须要做实用、好用、成功率高的方法"). Novelty is a gate,
  not the goal: a novel idea that loses to the simplest strong baseline, or
  only works with per-task exploration, a digital twin, privileged simulator
  state, or minutes per episode, is reported as such in the Practicality
  section, however clean its delta. Practicality does not change the novelty
  verdict rules (ABANDON still needs a named paper); it is its own verdict.
- Making a known but impractical method practical is a legitimate delta when
  shown with same-protocol numbers: success no lower, a named dependency
  removed, measured seconds or dollars saved per episode.
- Two failures waste months equally: a false novelty claim, and a viable idea
  abandoned because the territory has neighbors. Be brutally honest in both
  directions — and when an idea clears the check, say so plainly.
- Novelty can live in the combination or the finding even when every
  individual claim rates LOW — judge the idea, not each claim in isolation.
  Known parts arranged to reveal something unknown are novel.
- "Applying X to Y" earns novelty by what the application reveals — a
  non-obvious interaction, failure mode, or insight. Judge the revelation, not
  the template.
- Check both the method AND the experimental setting for novelty
- If the method is not novel but the FINDING would be, say so explicitly
- Always check the most recent 6 months of arXiv — the field moves fast
- **Anti-hallucination for Closest Prior Work.** Every paper in the prior-work table must pass pre-search verification via `verify_papers.py` (canonical name resolved per [`shared-references/integration-contract.md`](../shared-references/integration-contract.md) §2; 3-layer arXiv / CrossRef / Semantic Scholar fallback inside the helper itself). Policy D1 (primary + degraded-output fallback): if the helper is unresolved **or** its invocation fails, tag candidate entries `[UNVERIFIED]` and surface the uncertainty rather than dropping them. Never fabricate arXiv IDs, DOIs, or titles from memory. Full protocol in [`shared-references/citation-discipline.md`](../shared-references/citation-discipline.md) § Pre-Search Verification Protocol.

## Review Tracing

After each `mcp__codex__codex` or `mcp__codex__codex-reply` reviewer call, save the trace following `shared-references/review-tracing.md` (Policy C — forensic; never silently skip). Use `save_trace.sh` (resolved per the chain in `shared-references/integration-contract.md` §2) or write files directly to `.aris/traces/<skill>/<date>_run<NN>/`. Respect the `--- trace:` parameter (default: `full`).
