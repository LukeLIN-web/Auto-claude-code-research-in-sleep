---
name: paper-claim-audit
description: "Zero-context verification that every number, comparison, and scope claim in the paper matches raw result files — and that every claim about what PRODUCED a number (which weights, which recipe, which arm) and every gloss the paper gives a row, footnote mark or term borrowed from another paper is traceable to its source rather than inferred; that every general method statement (loss, adapter placement, inputs, weights) holds for EVERY configuration the paper reports (each backbone, each protocol), and that no caveat or disclosure contradicts another part of the paper or undermines the configuration it discloses. Uses a fresh cross-model reviewer with NO prior context to prevent confirmation bias. Use when user says \"审查论文数据\", \"check paper claims\", \"verify numbers\", \"论文数字核对\", \"检查表和图有没有事实错误\", \"论文还有哪些 caveat / 奇怪的披露 / 不一致\", or before submission to ensure paper-to-evidence fidelity."
argument-hint: "[paper-directory]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, mcp__codex__codex
---

# Paper Claim Audit: Zero-Context Evidence Verification

> 🔒 **Do not wrap this skill in `/loop`, `/schedule`, or `CronCreate`.** It is
> verdict-bearing — it judges paper-to-evidence fidelity with a deliberately
> zero-context fresh reviewer. Re-firing that verdict on a wall-clock timer adds
> no new signal (it changes only when the *paper or results* change). Schedule
> the *external wait that precedes it* — paper draft ready → then audit
> **once**. See
> [`shared-references/external-cadence.md`](../shared-references/external-cadence.md).

Verify that every claim in the paper matches raw evidence for: **$ARGUMENTS**

## Why This Exists

The executor writes experiments AND writes the paper. It "knows" what the results should be. This creates confirmation bias:
- Rounding 84.7% up to 85.3%
- Reporting best seed instead of average
- Citing metrics from a different experiment config
- Claiming "improves by 15%" when the delta is actually 12.8%

A **fresh reviewer with zero prior context** catches these because it has no expectations — it just compares paper text vs raw files.

## How This Differs From Other Audit Skills

| Skill | Question it answers |
|-------|-------------------|
| `/experiment-audit` | Is the experiment code honest? (fake GT, normalization fraud) |
| `/result-to-claim` | Does the data scientifically support this claim? |
| `/citation-audit` | Is the reference real, and does that paper support being cited here? |
| **`/paper-claim-audit`** | **Does the paper report the data truthfully and precisely — and describe correctly what produced it and what it borrowed?** |

**Mind the seam with `/citation-audit`.** That skill stops at "the reference
exists and the context fits"; this one used to stop at "the number matches".
A sentence that borrows a row from a cited paper and then explains what its
footnote mark means falls between the two: the number is right, the citation
is real, and the explanation can be entirely invented. It is checked here
(failure mode 8) because the gloss is a claim about evidence, and because a
caption is the least-scanned text in a paper — an invented one survives
rounds of both audits.

## Reviewer Persona

Audits use persona **P2 (evidence-anchored, unscored)** from
[`../shared-references/reviewer-personas.md`](../shared-references/reviewer-personas.md):
fixed headings, every finding anchored to a specific location, and **no score or
accept/reject verdict**. A number invites arguing with the number; an anchored
finding is either confirmed or dropped by opening the file it points at.

## Core Principle

**Zero-context, fresh reviewer.** The auditor receives ONLY:
- Paper .tex files (the claims)
- Raw result files (the evidence)

It does NOT receive:
- ❌ EXPERIMENT_LOG.md
- ❌ EXPERIMENT_TRACKER.md
- ❌ AUTO_REVIEW.md
- ❌ NARRATIVE_REPORT.md
- ❌ Any executor summary or interpretation
- ❌ Any prior audit results
- ❌ Any conversation history

This is **stricter than reviewer-independence** — it's zero-context evidence audit.

## Workflow

### Step 1: Collect Files (Executor — Claude)

Locate paper and result files WITHOUT reading or interpreting them.

**Paper files** (claims) — paths shown relative to the shell's working
directory so you can find them with `ls`; when writing them into
`audited_input_hashes`, use paths relative to the paper dir (no `paper/`
prefix) per the "Submission Artifact Emission" section below:
```
paper/main.tex                # → hash key: main.tex
paper/sections/*.tex          # → hash key: sections/*.tex
paper/tables/*.tex (if separate)   # → hash key: tables/*.tex
```

**Result files** (evidence):
```
results/*.json, results/*.jsonl, results/*.csv, results/*.tsv
outputs/*.json, outputs/*.csv
wandb-summary.json (if exists)
**/metrics.json, **/eval_results.json
**/config.yaml, **/args.json (experiment configs)
```

**Source files** (evidence for anything the paper reprints from another
paper — published rows, footnote marks, bin names, split names). Pass the
sources themselves, not our notes about them:
```
docs/reference/**/*.tex     # full text of the benchmarks/systems we quote
```
Without these, failure mode 8 cannot be checked at all: the reviewer has no
way to tell a transcribed gloss from an invented one. A paper that reprints
no external row needs none of these.

**Configuration files, one set per reported configuration** (evidence for
failure mode 12). A paper that runs on more than one backbone, or under more
than one protocol (offline / streaming, audio on / off, with / without an
auxiliary input), has one deployed configuration per cell. For EACH one pass
the training config of every adapter it mounts (yaml / argv) and the `meta.json`
of one product it produced. Passing only the headline backbone's configs is
how a second backbone's different loss goes unseen: its departures table cell
reads "overlap-fraction BCE", nothing numeric to mismatch, and the method
section's CE equation is never set beside it.
```
configs/**/<deployed adapter>.yaml     # per backbone, per adapter
outputs/**/<one product per config>/meta.json
```

**Exclude** (no summaries, no interpretations):
```
EXPERIMENT_LOG.md, EXPERIMENT_TRACKER.md, AUTO_REVIEW*.md
NARRATIVE_REPORT.md, PAPER_PLAN.md, findings.md
Any .md file that is an executor-written summary
Our own .md notes ABOUT a cited paper — pass its .tex, not the note
```

### Step 1b: Prove float = SSOT mechanically first (Executor — Claude)

Only where the paper's tables and figures are **generated** from an SSOT by
scripts (this repo's `paper/scripts/tab_*.py` / `fig_*.py` pattern). Skip when
floats are hand-authored.

Regenerate every float and diff it against what is committed:

- tables → the emitted `.tex` must come back **byte-identical**;
- figures → the PDFs differ in metadata on every rebuild, so compare
  **rendered pixels** (`pypdfium2`, `scale=3`, hash the bitmap), not bytes.

A clean diff retires the whole staleness class — "the float was built from an
older SSOT" — in one command, for every float at once. Restore any float whose
rebuild was metadata-only so the diff you hand on is the real one.

**Then say so in the reviewer prompt**, and point it at what a diff cannot
reach: the *prose* of the captions and the *provenance* of the arms (modes
8–11 below). Without this the reviewer spends its budget re-deriving cells
that a diff already proved, and the caption sentences — the least-scanned text
in the paper — get the leftovers. A byte-identical table is not a correct
table: its caption can still misdescribe what the column is.

### Step 1c: Sweep for errata the paper never received (Executor — Claude)

Result pages get corrected after the paper quotes them. An erratum that says
"the paper's sentence X does not hold" is invisible to a zero-context reviewer
(it reads raw files, not our notes) and to a delta audit (the paper line did
not change). Before launching the reviewer:

```bash
grep -rn -E '稿面|paper|app:|sec:|tab:|fig:' docs/eval_res --include=*.md \
  | grep -E '不成立|要删|勘误|erratum|does not hold|stale|flagged'
```

For each hit, grep the clone for the sentence it names. Still there ⇒ a
confirmed finding of this round, `stale_erratum`, reported without asking the
reviewer. (2026-09-25: the loc-objpair75 result page recorded that the two
arms did NOT share a LoRA init; `app:ranking` still said "from the same
initialization".) Do not pass the erratum text to the reviewer: that would
break zero-context.

### Step 2: Fresh Reviewer Audit (GPT-6-Astra — NEW thread, no reply)

**CRITICAL: Use `mcp__codex__codex` (new thread), NEVER `mcp__codex__codex-reply`.** Every run must be a fresh context.

```
mcp__codex__codex:
  model: gpt-6-astra
  config: {"model_reasoning_effort": "max"}
  prompt: |
    You are a paper-to-evidence auditor. You have ZERO prior context about
    this research. You will receive only paper source files and raw result
    files. Your job is to verify that every number in the paper exactly
    matches the raw evidence.

    Paper files to read:
    [list .tex file paths]

    Result files to read:
    [list .json/.csv/.yaml file paths]

    Source papers we reprint rows or marks from:
    [list .tex file paths, or "none"]

    Floats already proven to match their SSOT mechanically:
    [list, or "none — check the cells too"]

    ## Audit Protocol

    ### A. Extract Every Quantitative Claim
    For each number, percentage, comparison, or scope statement in the paper:
    - Location (section, table, caption, or inline text)
    - Exact claim text
    - The number or comparison being made

    ### B. Trace Each Claim to Evidence
    For each extracted claim, find the supporting raw data:
    - Which result file contains this number?
    - What is the EXACT value in that file?
    - Match status: exact_match / rounding_ok / mismatch

    ### C. Check These Specific Failure Modes

    1. **Number inflation**: Paper says 85.3%, raw file says 84.7%
       Rule: only standard rounding to displayed precision is allowed

    2. **Best-seed cherry-pick**: Paper says "achieves 90.2%" but
       that's the best of 5 seeds; mean is 87.1%
       Rule: check if paper specifies "average" / "best" / "median"

    3. **Config mismatch**: Paper compares Method A vs Baseline B,
       but they used different hyperparameters / datasets / splits
       Rule: verify config files show same settings for compared methods

    4. **Aggregation mismatch**: Paper says "average over 5 seeds"
       but result files show only 3 runs
       Rule: count actual runs vs claimed count

    5. **Delta error**: Paper says "improves by 15%" but
       actual delta is (85.3 - 73.1) / 73.1 = 16.7%
       Rule: verify arithmetic of all relative improvements

    6. **Caption-table mismatch**: Figure caption describes
       something different from what the figure/table actually shows
       Rule: cross-check every caption against its content

    7. **Scope overclaim**: Paper says "consistently outperforms"
       but only tested on 2 datasets
       Rule: check if language matches actual evaluation scope

    8. **Borrowed gloss**: The paper reprints a row, a footnote mark or a
       bin name from someone else's table, and then explains what that mark
       means. Paper's caption: "a = a finetune by the benchmark's authors,
       not released". Source's caption: "an author-finetuned backbone" —
       and nothing more.
       Rule: every word of the gloss must be traceable to the source's own
       sentence. Who trained it, whether it was released, what an acronym
       expands to, which split it is on: if the source does not say it, the
       paper may not either, however plausible the reading. Quote the
       source's defining sentence beside the paper's gloss and diff them.
       This is the one failure mode NEITHER a number audit NOR a citation
       audit covers: the number is right and the reference is real, and the
       invented gloss rides along between them. Check each one even when
       the row's numbers came back exact_match.

    9. **Arm identity**: Claims about what produced a number rather than
       what it is — "the same weights", "both arms carry the answer
       adapter", "with no adapter mounted", "trained on X", "the official
       recipe re-run".
       Rule: resolve these against the arm's own provenance (adapter path,
       config, checkpoint id in the product's metadata), never against its
       accuracy. Two arms can agree on every printed digit and still have
       been produced by different weights.

    10. **Cross-float conflict**: Two floats describe the same underlying
        cell in incompatible ways — a table's caption calls a baseline "an
        official-style whole-clip run on the bare backbone", a figure's
        caption calls the same cell "the same weights as our method".
        Rule: group the claims you extracted by the evidence file each one
        resolves to, then read every description pointing at one file
        together. A per-claim pass cannot see this; only the grouping can.
        Where one sentence covers several cells ("otherwise the same
        weights"), check it against EACH cell it covers — a clause that is
        true of four spokes and false of three is still false.

    11. **Orphan float**: A table or figure that is typeset but never
        referenced, or a \ref to a label that no longer exists.
        Rule: count both directions — every float label against the \ref
        occurrences in the sources, and every \ref against the labels.

    12. **Recipe non-uniformity**: The method section states the recipe in
        general terms ("the selector is trained with cross-entropy against
        the best-covering window", "the only trained parameters are
        rank-16 updates to q, k, v, o", "the answer pass reads the
        transcript outline", "the answer adapter answers the windows"),
        but some reported configuration runs something else: a second
        backbone trained with a different loss, LoRA on extra modules, no
        outline on some benchmarks, base weights instead of the answer
        adapter under one protocol.
        Rule: build a matrix. Rows = every general method statement
        (objective, supervision grid, adapter placement and rank, training
        hardware and optimizer, checkpoint selection, answer-pass inputs,
        answer weights, frame budgets). Columns = every configuration the
        paper reports a number for (each backbone x each protocol /
        benchmark group). Fill each cell from that configuration's own
        config files, not from the prose. Report every cell that differs,
        and for each say:
          (a) is the difference listed in a departures table AND is the
              general statement scoped to exclude it? Listed-but-unscoped
              is still a finding: the method section claims a uniformity
              the paper itself contradicts elsewhere.
          (b) does the claim that the recipe "transfers" / "generalizes" /
              "runs unchanged" survive once these cells are counted?
          (c) is the departure one the paper elsewhere reports as WORSE
              (a second backbone trained with the objective an ablation
              says ranks worse)? That is a self-undermining disclosure.
        A departures table is the least-scanned table in a paper; a cell
        there with no number in it matches nothing and fails nothing unless
        someone sets it beside the method equation.

    13. **Disclosure ledger**: Every sentence that hedges, discloses or
        excepts: "an earlier scan", "retrained", "re-scored copy", "cap
        widened for these questions", "our approximation", "except",
        "with the base weights", "no transcript outline", "at most N%".
        Rule: list them all, then classify each:
          - provenance mix: an ablation or control not run on the deployed
            system (older prompt, older enumeration, retrained adapter,
            different cap) while the prose reads it as a test of the
            deployed system;
          - contradicted: another sentence or caption describes the same
            arm without the exception ("the same windows redrawn" vs "as
            many windows, drawn from a re-scored copy");
          - self-undermining: the disclosure says the deployed choice is
            the worse one, or that a component was switched off where it
            did not help (a config chosen per benchmark on its results);
          - scope gap: an audit or check whose coverage silently excludes
            some benchmarks the paper reports.
        This is the list the author reads to decide what to fix by rerun
        and what to scope in prose; do not collapse it into a verdict.

    14. **Same fact, different words**: One fact stated in several
        places (abstract, intro, method, results, conclusion, appendix,
        captions) with different content: "4.5–16.8%" vs "4.5–16.8
        points", "each of their widths exactly" vs "as many windows",
        "never stacked" vs "stays mounted for the answer pass".
        Rule: for every headline number, every definition of a control
        arm and every system variant, collect all the places that state it
        and diff them.

    ## Output Format (per claim)
    For each claim, report:
    - claim_id: sequential number
    - location: section/table/figure
    - paper_text: exact quote from paper
    - paper_value: the number claimed
    - evidence_file: which raw file
    - evidence_value: the actual number
    - status: exact_match | rounding_ok | ambiguous_mapping |
              missing_evidence | config_mismatch | aggregation_mismatch |
              number_mismatch | scope_overclaim | unsupported_claim |
              source_gloss_unsupported | arm_identity_mismatch |
              cross_float_conflict | orphan_float |
              recipe_nonuniform | disclosure_contradicted |
              disclosure_self_undermining | provenance_mix |
              same_fact_divergent
    - details: explanation if not exact_match. For
      source_gloss_unsupported, quote the source's own defining sentence.

    Overall verdict: PASS | WARN | FAIL
```

### Step 3: Write Report (Executor — Claude)

Parse the reviewer's response and write `PAPER_CLAIM_AUDIT.md`:

```markdown
# Paper Claim Audit Report

**Date**: [today]
**Auditor**: GPT-6-Astra max (fresh zero-context thread)
**Paper**: [paper title from tex]

## Overall Verdict: [PASS | WARN | FAIL]

## Claims Verified: [N total]
- exact_match: [count]
- rounding_ok: [count]
- ambiguous_mapping: [count]
- missing_evidence: [count]
- mismatch: [count]

## Issues Found

### [FAIL/WARN] Claim #N: [description]
- **Location**: Section X / Table Y / Figure Z
- **Paper says**: "..."
- **Evidence shows**: ...
- **Status**: [status]
- **Fix**: [specific correction needed]

## Recipe matrix (failure mode 12)

| Method statement (file:line) | Config A | Config B | ... | Scoped in prose? |
|---|---|---|---|---|

## Disclosure ledger (failure mode 13)

| # | Location | Sentence | Class | Contradicted by / undermines |
|---|---|---|---|---|

## All Claims (detailed)

| # | Location | Paper Value | Evidence Value | Status |
|---|----------|-------------|---------------|--------|
| 1 | Table 2 | 85.3% | 85.28% | rounding_ok |
| 2 | Abstract | "15% improvement" | 12.8% | number_mismatch |
| ... |
```

Also write `PAPER_CLAIM_AUDIT.json` for machine consumption.

### Step 4: Print Summary

```
📋 Paper Claim Audit Complete

  Claims verified: 24
  exact_match:     18
  rounding_ok:      3
  ambiguous:         1
  ⚠️ mismatch:      2

  Overall: ⚠️ WARN

  See PAPER_CLAIM_AUDIT.md for details.
```

## Delta rounds do not replace a whole-paper pass

A delta round audits changed lines. Modes 12–14 and Step 1c find facts that
sit in UNCHANGED lines and go wrong because something else changed: a result
page's erratum, a second backbone's config, a caption elsewhere. Run them
over the whole paper on every round, even when the number audit is
delta-only. (Thirteen rounds, all number-centric and eleven of them delta,
never set the second backbone's "overlap-fraction BCE" cell beside the method
section's cross-entropy equation.)

## When to Run

1. **After `/paper-write`** — first check before improvement loop
2. **After `/auto-paper-improvement-loop`** — recheck if improvement loop changed numbers
3. **Before submission** — final verification

## Integration with Other Skills

### Read by `/auto-paper-improvement-loop` (if exists)

```
if PAPER_CLAIM_AUDIT.json exists:
    read mismatched claims
    fix them as priority items in the improvement round
```

### Advisory, Never Blocking

Same pattern as `/experiment-audit`:
- `PASS` → continue normally
- `WARN` → print warning, continue, flag draft as "check numbers before submission"
- `FAIL` → print alert, continue, but do NOT mark as submission-ready

## Render HTML view (auto, when `RENDER_HTML = true`, default)

After writing `paper/PAPER_CLAIM_AUDIT.md` and `paper/PAPER_CLAIM_AUDIT.json`, invoke `/render-html` on the audit report so the user has a readable HTML view of the verdict + per-claim breakdown:

```
/render-html "paper/PAPER_CLAIM_AUDIT.md" --json "paper/PAPER_CLAIM_AUDIT.json"
```

Uses **full Codex review gate** (audit-class artifact — render-fidelity check matches the skill's existing zero-context cross-model audit invariant). Output lands at `paper/PAPER_CLAIM_AUDIT.html` with embedded source SHA256 and a `.review.json` sidecar carrying the render verdict.

**Non-blocking**: if `/render-html` fails (helper missing, Codex MCP unavailable, file write error), log the failure and treat the skill as complete — the JSON + MD verdict files are the canonical outputs; the HTML view is a convenience for human readers.

Skip if `RENDER_HTML = false` is set in the project's `CLAUDE.md` or passed as `— render html: false`.

## Key Rules

- **Fresh thread EVERY run.** Never use `codex-reply`. Never carry context.
- **Zero executor interpretation.** Only file paths. No summaries.
- **Only raw results.** No EXPERIMENT_LOG, no AUTO_REVIEW, no human summaries.
- **Rounding rule.** Only standard rounding to displayed precision. 84.7% → 84.7% or 85% is OK. 84.7% → 85.3% is NOT OK.
- **Cross-model.** Reviewer must be a different model family from executor.

## Review Tracing

After each `mcp__codex__codex` or `mcp__codex__codex-reply` reviewer call, save the trace following `shared-references/review-tracing.md` (Policy C — forensic; never silently skip). Use `save_trace.sh` (resolved per the chain in `shared-references/integration-contract.md` §2) or write files directly to `.aris/traces/<skill>/<date>_run<NN>/`. Respect the `--- trace:` parameter (default: `full`).

## Submission Artifact Emission

This skill **always** writes `paper/PAPER_CLAIM_AUDIT.json`, regardless of
caller or detector outcome. A detector-negative run (paper has no numeric
claims) emits verdict `NOT_APPLICABLE`; a paper-with-numeric-claims-but-no-
raw-results run emits `BLOCKED`. Silent skip is forbidden — `paper-writing`
Phase 6 and `verify_paper_audits.sh` both rely on this artifact
existing at a predictable path.

The artifact conforms to the schema in `shared-references/assurance-contract.md`:

```json
{
  "audit_skill":      "paper-claim-audit",
  "verdict":          "PASS | WARN | FAIL | NOT_APPLICABLE | BLOCKED | ERROR",
  "reason_code":      "all_numbers_match | rounding_drift | missing_raw_results | ...",
  "summary":          "One-line human-readable verdict summary.",
  "audited_input_hashes": {
    "main.tex":                              "sha256:...",
    "sections/5.evidence.tex":               "sha256:...",
    "/abs/path/to/results/run_2026_04_19.json": "sha256:..."
  },
  "trace_path":       ".aris/traces/paper-claim-audit/<date>_run<NN>/",
  "thread_id":        "<codex mcp thread id>",
  "reviewer_model":   "<resolved — the model that actually ran (target: gpt-6-astra)>",
  "reviewer_reasoning": "<resolved — the effort that actually ran (target: max)>",
  "generated_at":     "<UTC ISO-8601>",
  "details": {
    "total_claims":   <int>,
    "mismatches":     [ ... per-claim issue records ... ],
    "result_files":   [ ... raw files consulted ... ]
  }
}
```

### `audited_input_hashes` scope

Hash the **declared input set** passed into this audit invocation — i.e. the
exact `.tex` files and raw result / config files this run read — not a
repo-wide union and not the reviewer's self-reported subset. If a caller
passed only `main.tex` + a single result file, hash those two files and no
others. The external verifier rehashes these entries; any mismatch flags
`STALE`.

**Path convention** (must match what `verify_paper_audits.sh`
expects): keys are **paths relative to the paper directory** (the arg
passed to the verifier) for in-paper files — so `main.tex`, not
`paper/main.tex` — and **absolute paths** for out-of-paper files such as
external `results/` dirs. The verifier resolves relative entries via
`os.path.join(paper_dir, key)`; prefixing with `paper/` produces
`paper/paper/main.tex` and false-fails as STALE.

### Verdict decision table

| Input state                                           | Verdict          | `reason_code` example |
|-------------------------------------------------------|------------------|-----------------------|
| No numeric claims detected in paper                   | `NOT_APPLICABLE` | `no_numeric_claims`   |
| Numeric claims detected, no raw result files found    | `BLOCKED`        | `no_raw_evidence`     |
| All claims reconcile to raw data                      | `PASS`           | `all_numbers_match`   |
| Minor rounding drift only, no material mismatch       | `WARN`           | `rounding_drift`      |
| Any material mismatch (wrong number, config mismatch) | `FAIL`           | `claim_mismatch`      |
| A gloss of a borrowed row or mark the source does not support | `FAIL`   | `source_gloss_unsupported` |
| Two floats describing one cell incompatibly            | `FAIL`           | `cross_float_conflict` |
| A float typeset but never referenced                   | `WARN`           | `orphan_float`        |
| A general method statement false for a reported configuration | `FAIL`   | `recipe_nonuniform`   |
| A paper sentence a result-page erratum retracted (Step 1c) | `FAIL`       | `stale_erratum`       |
| One fact stated incompatibly in two places             | `FAIL`           | `same_fact_divergent` |
| Disclosures that are only provenance-mix / self-undermining | `WARN`      | `disclosure_ledger`   |
| Reviewer invocation failed (network / malformed)      | `ERROR`          | `reviewer_error`      |

### Thread independence

Every invocation uses a fresh `mcp__codex__codex` thread. Never
`codex-reply`. Do not accept prior audit outputs (PROOF_AUDIT, CITATION_AUDIT,
EXPERIMENT_LOG, AUTO_REVIEW summaries) as input to this audit — the fresh
thread preserves reviewer independence per
`shared-references/reviewer-independence.md`.

### Human-readable sibling

`paper/PAPER_CLAIM_AUDIT.md` is written alongside the JSON for readers.
The JSON is authoritative for `verify_paper_audits.sh`; the Markdown
is for humans. The parent skill (`paper-writing` Phase 6) plus the verifier
decide whether the verdict blocks finalization — this skill itself never
blocks; it only emits.
