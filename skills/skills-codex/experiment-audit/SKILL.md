---
name: experiment-audit
description: "Audit experiment integrity before claiming results. Uses fresh-agent GPT-6-Astra review (same-family provisional in the base Codex mirror) to check for fake ground truth, score normalization fraud, phantom results, insufficient scope, and a moved evaluation boundary. Use when user says \"审计实验\", \"check experiment integrity\", \"audit results\", \"实验诚实度\", or after experiments complete before writing claims."
argument-hint: "[experiment-dir-or-results-path]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, mcp__antigravity__antigravity, mcp__antigravity__antigravity-reply, mcp__grok__grok, mcp__grok__grok-reply, mcp__claude-review__review, mcp__claude-review__review_reply, mcp__claude-review__review_start, mcp__claude-review__review_reply_start, mcp__claude-review__review_status
---

# Experiment Audit: Fresh-Agent Integrity Verification

> **Before each reviewer slot**, follow [Selectable Reviewers](../shared-references/reviewer-backends.md):
> resolve invocation → `.aris/reviewer.json` → Codex default (fresh native reviewer)
> with `reviewer_route.py` through the canonical helper resolver, preserving this
> slot's tier, fresh contexts, source/image inputs and deterministic gates.
> Codex examples/pins below apply only to `backend=codex`; other routes use their
> own first-call/reply contract. Save the route and actual returned identity;
> unavailable selections are `REVIEW_UNAVAILABLE`. Classify acceptance from actual
> families/completion/scope. Forward invocation reviewer/model/effort overrides
> to reviewer-bearing children. Generation workers are unchanged.


> **Codex assurance:** base semantic audit results record
> `review_independence: same-family` and `acceptance_status: provisional`.
> Deterministic evidence checks may be accepted; unavailable reviewer calls emit
> BLOCKED/ERROR rather than a provisional PASS.

Audit experiment integrity for: **$ARGUMENTS**

## Why This Exists

LLM agents can produce fraudulent experimental results through:
1. **Fake ground truth** — creating synthetic "reference" from model outputs, then reporting high agreement as performance
2. **Score normalization** — dividing metrics by the model's own max to get 0.99+
3. **Phantom results** — claiming numbers from files that don't exist or functions never called
4. **Insufficient scope** — reporting 2-scene pilots as "comprehensive evaluation"
5. **Moved evaluation boundary** — editing the scoring code or test data after results exist, switching benchmark or split mid-project, subsampling without saying so, or reporting only the best of several runs

These are NOT intentional deception — they are failure modes of optimizing agents that lack integrity constraints. This skill adds that constraint.

## Core Principle

**The executor (Codex) collects file paths. A fresh Codex reviewer reads code and judges integrity. The executor does NOT participate in integrity judgment; this base route is same-family/provisional.**

This follows `shared-references/reviewer-independence.md` and `shared-references/experiment-integrity.md`.

## Constants

- **REVIEWER_BACKEND = `codex`** — Default: Codex reviewer agent (`spawn_agent`, max — deep-audit tier). Override with `— reviewer: oracle-pro` for GPT-5.5 Pro via Oracle MCP. See `shared-references/reviewer-routing.md`.

## Workflow

### Step 1: Collect Artifacts (Executor — Codex)

Locate and list these files WITHOUT reading or summarizing their content:

```
Scan project directory for:
1. Evaluation scripts:    *eval*.py, *metric*.py, *test*.py, *benchmark*.py
2. Result files:          *.json, *.csv in results/, outputs/, logs/
3. Ground truth paths:    look in eval scripts for data loading (dataset paths, GT references)
4. Experiment tracker:    EXPERIMENT_TRACKER.md, EXPERIMENT_LOG.md
5. Paper claims:          NARRATIVE_REPORT.md, paper/sections/*.tex, PAPER_PLAN.md
6. Config files:          *.yaml, *.toml, *.json configs with metric definitions
7. Plan:                  EXPERIMENT_PLAN.md (benchmark, split and metric fixed before the runs)
```

**DO NOT summarize, interpret, or explain any file content.** Only collect paths.

### Step 2: Send to Reviewer (GPT-6-Astra via Codex MCP)

Pass ONLY file paths and the audit checklist to the reviewer. The reviewer reads everything directly.

> Resolve this reviewer slot first; the following is the `backend=codex` example.

```text
spawn_agent:
  model: gpt-6-astra
  reasoning_effort: max
  message: |
    You are an experiment integrity auditor. Start from the assumption that the
    evaluation is compromised somewhere — your job is to find where. Be
    adversarial. Trust nothing the author tells you — verify everything
    yourself. Read ALL files listed below and check for the following fraud
    patterns.

    Files to read:
    - Evaluation scripts: [list paths]
    - Result files: [list paths]
    - Experiment tracker: [list paths]
    - Paper claims: [list paths]
    - Config files: [list paths]
    - Plan: [path]
    The project's git history is readable: use git log -p on the evaluation
    and data paths.

    ## Audit Checklist

    ### A. Ground Truth Provenance
    For each evaluation script:
    1. Where does "ground truth" / "reference" / "target" come from?
    2. Is it loaded from the DATASET, or generated/derived from MODEL OUTPUTS?
    3. If derived: is it explicitly labeled as proxy evaluation?
    4. Are official eval scripts used when available for this benchmark?
    FAIL if: GT is derived from model outputs without explicit proxy labeling.

    ### B. Score Normalization
    For each metric computation:
    1. Is any metric divided by max/min/mean of the model's OWN output?
    2. Are raw scores reported alongside any normalized scores?
    3. Are any scores suspiciously close to 1.0 or 100%?
    FAIL if: Normalization denominator comes from prediction statistics.

    ### C. Result File Existence
    For each claim in the paper/narrative:
    1. Does the referenced result file actually exist?
    2. Does the claimed metric key exist in that file?
    3. Does the claimed NUMBER match what's in the file?
    4. Is the experiment tracker status DONE (not TODO/IN_PROGRESS)?
    FAIL if: Claimed results reference nonexistent files or mismatched numbers.

    ### D. Dead Code Detection
    For each metric function defined in eval scripts:
    1. Is it actually CALLED in any evaluation pipeline?
    2. Does its output appear in any result file?
    WARN if: Metric functions exist but are never called.

    ### E. Scope Assessment
    1. How many scenes/datasets/configurations were actually tested?
    2. How many seeds/runs per configuration?
    3. Does the paper use words like "comprehensive", "extensive", "robust"?
    4. Is the actual scope sufficient for those claims?
    WARN if: Scope language exceeds actual evidence.

    ### F. Evaluation Type Classification
    Classify each evaluation as:
    - real_gt: uses dataset-provided ground truth
    - synthetic_proxy: uses model-generated reference
    - self_supervised_proxy: no GT by design
    - simulation_only: simulated environment
    - human_eval: human judges

    ### G. Evaluation Boundary
    For each reported number:
    1. Is the scoring code the benchmark's official code, unmodified? Did the
       executor change scoring code, judge prompt or test data after results
       existed?
    2. Same benchmark, split and metric as the plan? Was any switched or dropped
       without the paper saying so?
    3. Was the test data subsampled, filtered or partly made by the executor
       without the paper saying so?
    4. Do the tracker and logs show more seeds or configurations than are
       reported, with only the best kept?
    5. Can training or model-selection code read the test answers?
    FAIL if: scoring code or test data changed after results existed, or test
    answers are readable by training or selection code, and the paper does not
    say so.
    WARN if: an undisclosed switch, subsample or selection (items 2-4).

    ## Output Format

    For each check (A-G), report:
    - Status: PASS | WARN | FAIL
    - Evidence: exact file:line references
    - Details: what specifically was found

    Overall verdict: PASS | WARN | FAIL
    
    Be thorough. Read every eval script line by line.
```

### Step 3: Parse and Write Report (Executor — Codex)

Parse the reviewer's response and write `EXPERIMENT_AUDIT.md`:

```markdown
# Experiment Audit Report

**Date**: [today]
**Auditor**: [actual selected model and effort; fresh read-only session;
actual family comparison and completion status]
**Project**: [project name]

## Overall Verdict: [PASS | WARN | FAIL]

## Integrity Status: [pass | warn | fail]

## Checks

### A. Ground Truth Provenance: [PASS|WARN|FAIL]
[details + file:line evidence]

### B. Score Normalization: [PASS|WARN|FAIL]
[details]

### C. Result File Existence: [PASS|WARN|FAIL]
[details]

### D. Dead Code Detection: [PASS|WARN|FAIL]
[details]

### E. Scope Assessment: [PASS|WARN|FAIL]
[details]

### F. Evaluation Type: [real_gt | synthetic_proxy | ...]
[classification + evidence]

### G. Evaluation Boundary: [PASS|WARN|FAIL]
[details + file:line or commit evidence]

## Action Items
- [specific fixes if WARN or FAIL]

## Claim Impact
- Claim 1: [supported | needs qualifier | unsupported]
- Claim 2: ...
```

Also write `EXPERIMENT_AUDIT.json` for machine consumption:

```json
{
  "audit_skill": "experiment-audit",
  "verdict": "WARN",
  "reason_code": "scope_exceeds_evidence",
  "summary": "Two-scene evaluation supports a qualified claim only.",
  "audited_input_hashes": {"results/eval.json": "sha256:<hash>"},
  "trace_path": ".aris/traces/experiment-audit/2026-04-10_run01/",
  "agent_id": "agent_019f...",
  "verdict_id": "agent_019f...",
  "executor_model": "codex-gpt-6-astra",
  "executor_family": "openai",
  "reviewer_model": "gpt-6-astra",
  "reviewer_family": "openai",
  "reviewer_reasoning": "max",
  "review_independence": "<actual family comparison>",
  "acceptance_status": "<actual acceptance status>",
  "generated_at": "2026-04-10T00:00:00Z",
  "date": "2026-04-10",
  "auditor": "gpt-6-astra-max",
  "overall_verdict": "warn",
  "integrity_status": "warn",
  "checks": {
    "gt_provenance": {"status": "pass", "details": "..."},
    "score_normalization": {"status": "warn", "details": "..."},
    "result_existence": {"status": "pass", "details": "..."},
    "dead_code": {"status": "pass", "details": "..."},
    "scope": {"status": "warn", "details": "..."},
    "eval_boundary": {"status": "pass", "details": "..."},
    "eval_type": "real_gt"
  },
  "claims": [
    {"id": "C1", "impact": "supported"},
    {"id": "C2", "impact": "needs_qualifier"}
  ]
}
```

### Step 4: Print Summary

```
🔬 Experiment Audit Complete

  GT Provenance:      ✅ PASS — real dataset GT used
  Score Normalization: ⚠️ WARN — boundary metric uses self-reference
  Result Existence:    ✅ PASS — all files exist, numbers match
  Dead Code:           ✅ PASS — all metric functions called
  Scope:               ⚠️ WARN — 2 scenes, paper says "comprehensive"
  Eval Boundary:       ✅ PASS — official scorer, unchanged since the first result

  Overall: ⚠️ WARN
  
  See EXPERIMENT_AUDIT.md for details.
```

## Integration with Other Skills

### Automatic in /research-pipeline (advisory, never blocks)

When integrated into the pipeline, this skill runs automatically after `/experiment-bridge` and before `/auto-review-loop`:

```
/experiment-bridge → results ready
    ↓
/experiment-audit (automatic, advisory)
    ├── PASS  → continue normally
    ├── WARN  → print ⚠️ warning, continue, tag claims as [INTEGRITY: WARN]
    └── FAIL  → print 🔴 alert, continue; claims resting on the failed check are unsupported
    ↓
/auto-review-loop → proceeds with integrity tags visible to reviewer
```

**Never halts the pipeline.** On FAIL the pipeline continues, but the claims resting on the failed check are unsupported until fixed and re-audited.

### Read by /result-to-claim (if exists)

`/result-to-claim` Step 3.5 reads `EXPERIMENT_AUDIT.json`; how a FAIL changes the verdict is defined there.

## Key Rules

- **Reviewer independence**: executor collects paths, reviewer judges. Period.
- **Never halt the pipeline**: a FAIL makes the claims resting on it unsupported; it does not stop the other work.
- **File-as-switch**: no EXPERIMENT_AUDIT.md = skill was never run = zero impact on existing behavior.
- **Review class**: base Codex is same-family provisional; a completed positive selected review may claim cross-family accepted only with known different model families.
- **Honest about limits**: the audit catches common patterns, not all possible fraud. It is a safety net, not a guarantee.

## Acknowledgements

Motivated by community-reported integrity issues (#57, #131) where executor agents created fake ground truth and self-normalized scores.

## Review Tracing

After each reviewer agent call, save the trace following `shared-references/review-tracing.md` (Policy C — forensic; never silently skip). Use `save_trace.sh` (resolved per the chain in `shared-references/integration-contract.md` §2) or write files directly to `.aris/traces/<skill>/<date>_run<NN>/`. Respect the `--- trace:` parameter (default: `full`).
