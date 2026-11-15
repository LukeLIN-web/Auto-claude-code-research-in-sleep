# Abstract Writing Guide

Fused from Peng Sida's notes (pre-writing questions, the three templates) and the annotation of 55 award papers (statistics, arcs, rules; `corpus/corpus_stats.json`, `corpus-profile.md`).

## Goal
Write a strong abstract by doing three things repeatedly:

1. Think through the abstract logic first.
2. Follow one template (Version 1/2/3 below).
3. Revise the abstract many times.

## Pre-Writing Questions (Important)
Answer these before writing:

1. What technical problem do we solve, and why is there no well-established solution? (important)
2. What is our technical contribution?
3. Why can our method work in essence?
4. What technical advantage and new insight do we provide? (important)
5. What is the main evidence (benchmark, baseline, number)?

## What Award Abstracts Do (55 papers)
| Fact | Value |
|---|---|
| Length | median 174 words (p10–p90: 132–219); median 7 sentences (6–9); one paragraph |
| First sentence | setting/background 32, our method directly 13, the gap 7 |
| Most common arc | **Setting → Gap → Method → Result**, with variants that drop the setting or open with the method |
| Last sentence | a result 21, release of code/data 18, a secondary result 8, a stance 5 |
| Insight sentence | 14/55 (when the method follows from one observation) |
| Stance sentence | 10/55 |
| Numbers | median 1; 90% have ≤ 5–6 |
| Connectors (however/thus/…) | median 0.6 per 100 words, 90% ≤ 1.6 — about one per abstract |

So the default abstract is short, concrete and plain: one gap, one method, one or two results. Insight and stance sentences are added only when the paper has them.

## Versions
### Default — Setting → Gap → Method → Result *(about half of award abstracts)*

1. Setting: what works today, concretely (one sentence).
2. Gap: what fails or is missing, under which condition — and, in the same or the next sentence, why.
3. Method: name it with its category and the one idea that answers the gap (“We present X, a … that …”). Optional: one sentence of mechanism or the insight it rests on.
4. Benefit/evidence: one or two results with benchmark and baseline.
5. Optional last sentence: a secondary capability, a stance, or the release of code/data.

The notes' template for this arc (Challenge -> Contribution):

Introduce the technical challenge, then use one to two sentences to present the technical contribution that solves the challenge.

#### Structure

1. Task.
2. Technical challenge for previous methods.
3. One to two sentences introducing the technical contribution for solving the challenge.
4. Benefits of the technical contribution.
5. Experiment summary.

#### Expert Notes

1. Discuss previous work around the technical challenge that we actually solve.
2. For the contribution sentence(s), usually mention the technical term/name only; do not explain every detailed step.
3. The technical term must be easy to understand; readers should not feel a jump.
4. This ability is very important for writing a good abstract.

Version 1 local cite:

1. `references/examples/abstract/template-a.md`

### Insight-led — Setting → Gap → Insight → Method → Result *(`insight`, `failure` with a clear root cause)*

As the default, with one sentence that states the observation about the problem from which the method follows. Write the observation itself (“The highest frequency a scene can contain is bounded by the sampling rate of its views.”).

The notes' template for this arc (Challenge -> Insight -> Contribution):

Introduce the technical challenge, then use one to two sentences to present the insight for solving the challenge, and then one sentence to present the technical contribution that implements this insight.

#### Structure

1. Task.
2. Technical challenge for previous methods.
3. One sentence introducing the insight for solving the challenge.
4. One to two sentences introducing the technical contribution that implements the insight.
5. Benefits of technical novelty.
6. Experiment summary.

#### Expert Notes

1. Discuss previous work around the technical challenge that we actually solve.
2. Introduce the insight in one clear sentence.
3. For the implementation sentence(s), usually mention the technical term/name only; do not explain every detailed step.
4. The technical term must be easy to understand; do not create a jump in reading.
5. This ability is very important for writing a good abstract.

Version 2 local cite:

1. `references/examples/abstract/template-b.md`

### Direct — Method → (Gap) → Method → Result *(~1/4; `trend`, `capability-gap`, resources)*

1. `We present [Name], a [category] that [does what] from [input].` 2. Prior methods [restriction] → consequence. 3. [Name] instead [key design], allowing [capabilities matching the restriction]. 4. Evidence. 5. Optional transfer/secondary result or release.

### Multiple contributions

Each contribution with its advantage in the same sentence; then evidence.

Version 3: When there are multiple technical contributions, describe each contribution together with its technical advantage.

#### Structure

1. Task.
2. If needed, one contrast sentence about prior methods.
3. Contribution sentence 1 + technical advantage.
4. Contribution sentence 2 + technical advantage.
5. Contribution sentence 3 + technical advantage.
6. Experiment summary.

#### Expert Notes

1. When there are multiple technical contributions, describe each contribution together with its technical advantage.
2. The ability to express "contribution + advantage" in one sentence is very important for writing a good abstract.

Version 3 local cite:

1. `references/examples/abstract/template-c.md`

### By paper type

| Type | Typical arc (coarse) |
|---|---|
| L1 method | Setting → Gap → Method → Result |
| L2 capability | Method → Result (Direct), or Setting → Method → Result |
| L3 scaling | Setting/Question → Method (the study) → Results (the regularity) → Method (recipe) → Result |
| L4 re-examination | Setting → Method (our test) → several Results → Stance |
| L5 mechanism | Setting → Gap/puzzle → Method → Insight (explanation) → Result |
| L6 theory | Setting → Setting of the problem → theorem-level results in words → implication |
| L7 resource | Gap → Resource (scale number) → what it enables → baseline/benchmark result → release |
| L8 measurement | Setting → Method (sensing principle) → Mechanism → Result (prototype) |

## Rules
- About 130–220 words in 6–9 sentences averaging ~20–25 words; one message per sentence, with its reason or evidence inside the sentence. One short sentence for the idea is welcome. Do not split a result from its number or a design from its benefit.
- Each element appears once: do not restate the gap or the benefit in a second sentence.
- Numbers: the headline result(s) and, if essential, one number that defines the scale. No ablation numbers or implementation details.
- At most one logical connector (however, thus, …) in most abstracts; sentence order carries the logic. No dashes (author preference); a colon is fine where it introduces the idea or a list. No sentence ends with “, making …” or a similar participial restatement.
- Every adjective about the method is made concrete in the same sentence.
- Results name the benchmark/baseline or state the scope; wording follows the claim map.
- Include at least one evaluative claim backed by evidence (“outperforms X”, “the first … that …”, “20× faster”); 37 of 55 award abstracts use such a word, and the rest state a comparison in numbers.
- End with the strongest evidence, a concrete secondary result, a stance supported by the results, or the release of code/data — not with generic impact (“opens new avenues”).
- No limitations, costs or losses in the abstract; scope mixed results to where the method wins.

## Example Bank
1. `references/examples/abstract-examples.md`
2. `references/examples/abstract/template-a.md`
3. `references/examples/abstract/template-b.md`
4. `references/examples/abstract/template-c.md`

## Checklist
- [ ] Can a reader identify task, challenge, insight/contribution, and results in one pass?
- [ ] Are all major claims supported by experiments?
- [ ] Are technical names self-contained and readable?
- [ ] Is there any sentence that mixes too many messages?
- [ ] Gap sentence and method sentence match one-to-one.
- [ ] Same claims and strength as the introduction.
- [ ] No hedging on the core idea; no disclaimers.
- [ ] At least one evaluative claim backed by evidence (outperforms, first, faster, …).
- [ ] `python3 scripts/check_draft.py` shows no ERROR and no WARN for connectors, numbers or participial clauses (or each one is justified).
