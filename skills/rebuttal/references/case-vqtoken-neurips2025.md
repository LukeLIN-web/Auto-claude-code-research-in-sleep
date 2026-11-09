# Case: VQToken, NeurIPS 2025 (Submission 3333) — accepted as poster

Source: https://openreview.net/forum?id=X8oEu4Gs3W (thread saved by the user on 2026-11-09 to `juyi/tmp/demorebuttal.txt`).
Paper: *VQToken: Neural Discrete Token Representation Learning for Extreme Token Reduction in Video Large Language Models*.
Use: worked example for [rhetoric.md](rhetoric.md) and [followup-and-endgame.md](followup-and-endgame.md). It shows moves to copy and moves to avoid; several of its replies break this skill's rules (concessions, apologies, exposed weaknesses) and are quoted here only as warnings.

## Reviewers and outcome

| Reviewer | Final rating / conf. | Main ask | How it ended |
|---|---|---|---|
| Gyx4 | 2 Reject / 3 | Motivation of VQ-attention and hashing; comparisons vs recent pruning methods at similar token counts; clarity | Two sharper follow-ups; final: "still lacks sufficient baseline comparisons on multiple benchmarks" |
| BtRV | 4 Borderline accept / 4 | Large drops on long-video benchmarks; ablations only on NextQA; matched-data baseline; LLaVA-Video uncited | Caught a wrong table value; "I will keep my score at Borderline Accept" |
| LjpF | 5 Accept / 4 | Scaling beyond 0.5 B; adaptive ratio; NextQA-MC details | Acknowledged after one reply |
| RRqQ | 4 Borderline accept / 4 | k-means overhead (FLOPs, latency); token-count scaling; LongVideoBench subsets | "this fully addresses all my questions"; stayed at 4 after a score request |

Decision: Accept (poster). Meta-review (e): *"One reviewer rejected the paper citing weak baselines and unclear motivation, while others found the approach promising and novel in practice. The rebuttal improved clarity but left baseline and overhead issues unresolved. Overall, consensus leaned toward borderline accept and the AC agrees with them."*

## What worked

1. **Regime framing + burden shift** (to Gyx4): "To our knowledge, no prior work has formally defined extreme token reduction … We welcome references to any methods exceeding 99 % reduction and will include direct comparisons." The meta-review calls the approach novel. → rhetoric R1.
2. **Exact granularity on the second try** (to RRqQ): official LongVideoBench subsets S2E/S2O/… → "fully addresses all my questions". → rhetoric P1.
3. **Retention framing on the paper's own metric** (to BtRV): "retains 99.5 % … 98.1 % … under a 99.86 % reduction in token count … > 300× increase in TokDense." → rhetoric R5.
4. **Matched baseline delivered** (to BtRV): LLaVA-OV fine-tuned one epoch on the same data, reported next to ours.
5. **Closing note to the AC** ("Author Final Remarks"): named the three engaged reviewers, listed what was resolved, isolated the remaining concerns as "raised only by Gyx4 among the four reviewers" and "presentation-oriented". The meta-review reproduces this structure. → followup § 5, rhetoric R8.

## What failed

1. **Guessed cause for a wrong number.** BtRV: text says 39.3, Table 4 says 38.2. Reply: "subtle hardware-driven variations between GPU architectures … RTX 4090 versus the A100". BtRV: "Why did only the metrics of this benchmark fluctuate, and with a relatively large amplitude …?" Reply: "You are correct … the values had been inadvertently copied from a different experiment … the correct accuracy is 38.22 %." One wrong guess cost a second round and a public admission. → check logs first.
2. **Excuse for a missing citation.** "Many prior video‐LLM works compare models trained under different schedules or data regimes" → BtRV: "this cannot be the reason to 'hide' LLaVA-Video without any citing or refering as the paper uses their data." → "We will cite X."
3. **Counting instead of meeting the criterion.** "our original submission already includes 7 experiments … we added 11 more" → Gyx4: "Counting how many tables include multiple benchmarks OR multiple baselines … does not demonstrate the original submission already did sufficient comparisons … (1x2=2 numbers …) Compare this … to Dycoke's Table 1 … (2x5=10)". → rhetoric R3.
4. **Arguing against the reviewer's cited standard** ("[DyCoke] compare multiple benchmarks in only 2 of their 6 tables") instead of meeting it. → rhetoric R4.
5. **Scope line contradicted by the paper**: "completely different task" vs "2 of 5 benchmarks … are long videos". → rhetoric R7.
6. **Promise instead of a measurement** for k-means overhead; the meta-review lists overhead as unresolved.
7. **Overclaim against its own table**: 7 B result 78.59 vs 81.40 described as "not only maintains but improves performance".
8. **Foreign text**: "§ 3.3 'Material Physics MoE'" in the reply to Gyx4.
9. **Outlier framing inside the outlier's thread** ("Unlike the other three reviewers, Reviewer Gyx4's comments center on paper organization, writing style …") and a 🟥-highlighted quote-back; no movement.
10. **Nudges without content** and a separate score-request post to RRqQ; no rating moved.
11. **Apology/concession openers** throughout: "Sorry for the misunderstanding", "We apologize for the omission", "We regret the confusion", "We wholeheartedly agree". Banned here (Never concede).

## Reviewer behaviour worth recognising

Gyx4 is a strict, good-faith reviewer: specific, re-reads, states the criterion numerically. Such a reviewer is not reportable ([misconduct-reporting.md](misconduct-reporting.md) § 1); the only levers are meeting the stated criterion or a regime argument the AC accepts.
