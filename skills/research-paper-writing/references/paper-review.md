# Paper Review (Paper Rview)

## Goal

Use an adversarial, reviewer-style checklist to detect reject risks early and revise the paper before submission.

## Core Principle

Pursue perfectionism in paper quality: assume reviewers will probe every weak point and proactively fix them.

## Critical Rule (Do Not Violate)

Every major claim, especially in Abstract and Introduction, must be:

1. technically correct,
2. explicitly supported by experimental evidence, and
3. supported in the main text itself: at least one or two pieces of its evidence sit in the main text, never all of them in the appendix (the self-contained rule in `SKILL.md`).

If a claim is not supported, either add evidence or weaken/remove the claim.

## What Usually Gets a Paper Accepted

1. Sufficient contribution (for example: novel task, novel pipeline, novel module, novel design choices, new experimental findings, or new insight).
2. Better empirical performance than prior methods under fair comparisons.
3. Sufficient comparison experiments and ablation studies.

## Common Rejection Dimensions

| Rejection Dimension          | Typical Failure Signals                                                                                                                                                                                                                                                                    |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1. Insufficient contribution | 1.1 Targeted failure cases are too common.<br /> 1.2 Proposed technique is already well explored; expected gains are predictable/well-known.<br /> 1.3 The technique is straightforward.                                                                                                     |
| 2. Unclear writing           | 2.1 Missing technical details; work is not reproducible.<br />2.2 A method module lacks clear motivation.                                                                                                                                                                                  |
| 3. Weak empirical effect     | 3.1 Improvement over prior methods is only marginal.<br /> 3.2 Even if better than previous methods, absolute performance is still not strong enough.                                                                                                                                      |
| 4. Incomplete evaluation     | 4.1 Missing ablation studies.<br />4.2 Missing important baselines or important evaluation metrics.<br /> 4.3 Datasets are too simple to prove the method truly works.                                                                                                                    |
| 5. Problematic method design | 5.1 Experimental setting is unrealistic.<br />5.2 Method has technical flaws and appears unreasonable.<br />5.3 Method is not robust and needs per-scenario hyperparameter tuning. <br /> 5.4 New design introduces stronger limitations than its benefits, leading to negative net value. |

## End-of-Paper Self-Review Question List

Add this checklist near the end of the draft while revising.
Use each question to trigger concrete edits before submission.

### 1. Contribution

1. What new knowledge does this paper give to readers?
2. Are we solving a truly meaningful failure case, not a trivial/common one?
3. Is the technical idea genuinely non-obvious beyond well-explored practice?
4. Is our gain surprising or insightful rather than a predictable improvement?
5. Is there at least one clear novelty type (task/pipeline/module/design finding/insight)?
6. Does the Abstract name the ingredient that separates the method from the generic recipe it resembles (its training signal or labels), or can a reader take it for that recipe?
7. Are the contribution items independent, and does an empirical item claim only the factors its controls isolate ("better than alternative recipes" is not "X is the primary driver")?

Questions 6–7 follow `../../shared-references/manuscript-craft.md` §2 (Abstract, Introduction). Ask the questions that decide whether a reviewer understands the contribution (Contribution 6, Experimental Strength 5–6) before the prose questions.

### 2. Writing Clarity

1. Can a knowledgeable reader reproduce the method from the paper?
2. Did we provide enough technical detail for each key module?
3. Is the motivation of every module explicit and logically connected to a challenge?
4. Are terms and notation consistent across sections?
5. Does each paragraph carry one clear message with smooth transitions?
6. Does the Introduction run one chain (problem, why the obvious fix fails, why the ingredient may work, method, validation), with a second motivation entering as what a component makes possible?
7. Does every universal qualifier in the Abstract, Introduction and contribution list ("all new data", "only W changes", "without demonstrations") hold for every stage of the system, with its reference point stated?

Questions 6–7 follow `../../shared-references/manuscript-craft.md` §2 (Introduction).

### 3. Experimental Strength

1. Are improvements over strong baselines meaningful, not just statistically tiny?
2. Is absolute performance competitive enough for the target venue?
3. Are gains consistent across multiple datasets/settings/metrics?
4. Do we report both strengths and failure cases honestly?
5. Which comparison does each headline number belong to? Is the full system's gain over the bare baseline framed as the whole system's, and does the comparison that changes only the core component say so? (Their order is the authors' call: ask, do not flag.)
6. Is every number placed beside a property ("without a privileged signal") obtained in that setting, and if the best number needs the signal, are both given with their settings?
7. Is every failure breakdown used as motivation, not as proof that one component is to blame?

Questions 5–7 follow `../../shared-references/manuscript-craft.md` §2 (Abstract, Introduction).

### 4. Evaluation Completeness

1. Do we include ablations for all key design choices?
2. Are all strong/recent baselines included under fair settings?
3. Are evaluation metrics standard and sufficient for this task?
4. Are datasets/scenarios challenging enough to validate real effectiveness?
5. Are comparison and ablation protocols clearly documented?
6. Does each results paragraph give one verdict per group of benchmarks, one or two numbers and a reason from the paper's own evidence, or does it walk the table benchmark by benchmark, or an ablation variant by variant with a pair of numbers each?
7. Can a reader tell from every cell of a results table how its model was trained? A row whose training differs by column without a mark lets a reviewer read in-domain results as transfer.
8. Does every transfer claim, and every instance a claim names ("with two models"), have main-text evidence produced that way?
9. Does the main Setup define only what the main text uses, with every term of a main-text sentence or float defined in the main text?
10. Does each main gain carry its reason from a measurement in the paper (failure kinds, which kind of task gains most), written beside the gain? A section that only reports comparisons reads to a reviewer as lacking insight, and one where most sentences share one frame as text generated from a results script.

Questions 6–10 follow `../../shared-references/manuscript-craft.md` §2 (Experiments); `experiments.md` (E2, E3, Writing Rules 4 and 8–9, Readability rules 11–13) shows the fix for each.

### 5. Method Design Soundness

1. Is the experimental setting realistic for practical use?
2. Does the method have hidden technical defects or unreasonable assumptions?
3. Is the method robust without heavy per-case hyperparameter retuning?
4. Do benefits outweigh added complexity and new limitations?
5. Could reviewers reasonably argue that the net benefit is negative?
6. Does the Method describe the configuration the main rows actually run? A component the Abstract or Introduction highlights that the tables use only as a variant reads as an overclaim.
7. Does every filter or exclusion in the method's equations state its reason beside the equation: by construction, by citation, or by an ablation with a significant difference?
8. Can a reader tell from the Method alone, before the first results table, whether one trained model serves every benchmark or each domain has its own?

Questions 6–8 follow `../../shared-references/manuscript-craft.md` §2 (Method); `method.md`, "Configuration, Filters and Training Unit", shows the fix for each.

## Adversarial Writing Workflow

1. Read the paper as a skeptical reviewer.
2. Answer every question above with explicit evidence from the paper.
3. Mark each item as `pass`, `needs revision`, or `needs new experiment`.
4. Revise claims, writing, experiments, or method scope accordingly.
5. Repeat until no major rejection risk remains.
