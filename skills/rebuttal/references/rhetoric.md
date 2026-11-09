# Rhetoric: persuading and refuting

Read before drafting any response file (Phase 4) and before every follow-up reply (Phase 8).
Everything here operates inside the hard rules of `SKILL.md` — **Never concede**, **Never expose a weakness**, provenance and commitment gates. A move below that would break one of them is not available, however well it worked elsewhere.

User request this file answers (2026-11-09): 「主要是学习各种话术. 怎么说服, 反驳」.
Worked example used throughout: [case-vqtoken-neurips2025.md](case-vqtoken-neurips2025.md) (quotes marked *VQToken*).

## 0. The reader is the AC

In the VQToken thread the final ratings were 2 / 4 / 5 / 4: BtRV wrote "I will keep my score at Borderline Accept", RRqQ stayed at 4 after being asked to raise it, and the negative reviewer ended at 2. The paper was accepted on the AC's reading. The meta-review repeated the authors' own framing: *"One reviewer rejected the paper citing weak baselines and unclear motivation, while others found the approach promising and novel in practice."* It also listed exactly the points the replies had left soft: *"The rebuttal improved clarity but left baseline and overhead issues unresolved."*

Consequences for every reply:
- Write so that an AC who skims can see, per point, that the concern was met with evidence. The reviewer may never move; the AC still records what was answered.
- Whatever is answered with a promise instead of a number is what the AC will list as unresolved.
- Moving the reviewer is a bonus; leaving the AC with nothing to hold against the paper is the goal.

## 1. Answer shape

**Default reply pattern per issue:**
- Sentence 1: a short thanks naming what the comment did, then the direct answer to the question as asked — the verdict, the number, or the yes/no ("Thank you for this pivotal comment. All four headline contrasts are significant."). NEVER open with process or setup ("We ran...", "We recomputed...", "New table on...") — that buries the answer; method details come after the verdict.
- Sentence 2-4: grounded evidence
- Last sentence: implication for the paper

**Thanks opener (every answer).** Each `A#` opens by thanking the reviewer, then delivers the verdict immediately — the thanks is a lead-in, never a delay:
- Keep it to one clause or one short sentence (≤ 10 words), and put the direct answer in the same sentence or the next one. If the verdict has slipped past sentence two, the opener is too long.
- Name what the comment did, so the thanks carries information: `Thank you for this pivotal comment` / `for pushing on the judge's validated scope` / `for this precise question about per-law support` / `for checking the artifacts directly`. Generic praise with no object ("Thank you for the insightful comment") is filler when it appears more than once.
- Vary the wording across answers within a file and across reviewer files. The same thanks sentence repeated at every `A#` reads as a template and devalues all of them; treat it under the same no-verbatim-reuse rule as shared evidence.
- Thank for the observation, not for the verdict. Thanking a reviewer for a concern the answer then refutes ("Thank you for catching this error" when no error exists) concedes a point the evidence does not.
- The file-level acknowledgment at the top of the response covers that reviewer's main thrust; the per-answer openers must not restate it in the same words.
- No flattery stacks. *VQToken* opened two replies with "deeply grateful … exceptionally thorough and professional review … invaluable … instrumental"; neither reviewer moved. One specific clause beats four adjectives.

**Paragraph length (readability).** No paragraph over 4-5 sentences in the reviewer-facing text. When a response to one W/Q runs longer, insert blank lines at argument boundaries — typical seams: concession/claim | mechanism or evidence | concrete example | scope statement or revision promise. Split with line breaks only; never reword while splitting. Long walls of text read as evasive and reviewers skim past the numbers buried mid-paragraph.

**Content heuristics (from successful rebuttals):**
- Evidence > assertion
- Global narrative first, per-reviewer detail second (single_document mode only)
- Concrete numbers for counter-intuitive points
- Name closest prior work + exact delta for novelty disputes
- For theory: separate core vs technical assumptions
- Answer friendly reviewers too
- **Pre-registered calibration phrasing.** When a threshold or hold-out was fixed before generated samples were inspected, say so explicitly with a phrase like "set on hold-out before any generated sample was inspected." Defuses cherry-pick attacks at near-zero word cost. Only use when actually true.
- **Surface non-obvious design choices upfront.** If the experimental setup has a non-obvious design choice (compute-matched ≠ epoch-matched, atypical seed protocol, restricted parameter subset, etc.), name it concretely with numbers where they clarify the design choice. Pre-empts adversarial reverse engineering. This covers neutral setup facts a reader needs to read the number; a caveat that would expose a weakness falls under "Never expose a weakness" and is not volunteered.

## 2. Persuading (positive and swing reviewers)

**P1 — Hand over the exact object at the granularity they named, on the first try.**
*VQToken*: RRqQ asked for "specific numerical scores for its various subsets" of LongVideoBench. The first reply gave max-frames buckets (16/32/64); RRqQ had to clarify they meant the official S2E/S2O/S2A/O2E/O2I subsets. The second reply gave those, and RRqQ wrote "this fully addresses all my questions." Read `asked_for` from the raw text; when a benchmark has an official breakdown, the reviewer means that one.

**P2 — Justify a design choice with reasons a reviewer cannot argue with.**
*VQToken* defended an 8-frame setting with three reasons: the efficiency regime the paper targets, "the standard configuration provided by LongVideoBench and VLMEvalKit", and "rapid iteration during rebuttal". The first two carry the answer. The third exposes that the experiment was rushed — drop reasons of that kind ("Never expose a weakness").

**P3 — Turn their praise into the paper's thesis.** When a positive reviewer names a strength, the reply restates it as the paper's contribution with one number behind it, so the AC sees the strength confirmed rather than merely thanked.

**P4 — Close the loop, then stop.** Once a reviewer writes that the concerns are resolved, reply with one short thanks naming what changed. Do not keep feeding them new material.
On asking for a higher score, see [followup-and-endgame.md](followup-and-endgame.md) § Score requests — in VQToken it moved nothing.

## 3. Refuting (negative reviewers)

**R1 — Define the regime, then shift the burden.** When the attack is "this has been done" or "compare to stronger baselines", state the regime that makes the work new and invite the reviewer to name a counterexample:
> "To our knowledge, no prior work has formally defined extreme token reduction … Most existing methods cap out at 30 %–80 % reduction … We welcome references to any methods exceeding 99 % reduction and will include direct comparisons in our revision." (*VQToken*)

The AC's meta-review accepted the framing ("Using discrete VQ codebooks for token reduction in video LLMs is novel"). Requires that the claim survives `/novelty-check`; if a counterexample exists, this move hands the reviewer a win.

**R2 — Quote their own words back, once.** A reviewer who listed a strength and later attacks the same thing can be shown their sentence:
> "Your Strengths section states: 'Experiments and ablation are relatively extensive.'"

Plain text, once, in a late round, as a pointer for the AC. *VQToken* wrapped it in four 🟥 markers (posted hours before the deadline; no reply). Loud formatting reads as anger and costs more than it gains.

**R3 — Answer the criterion, not the volume.** When the reviewer has a specific criterion, meet that criterion. *VQToken* answered "comparisons are insufficient" by counting ("7 experiments … 11 more … totaling 18"). The reviewer replied: *"Counting how many tables include multiple benchmarks OR multiple baselines, or how many other experiments were done, does not demonstrate …"* and spelled out the real criterion (compression baselines × benchmarks in one table: "1x2=2 numbers … Compare this to Dycoke's Table 1 … 2x5=10"). The right reply was that matrix, or — if it cannot be produced — R1. Never count experiments, tables or pages as an argument.

**R4 — Meet a cited standard; do not litigate it.** When the reviewer says "to the standard of paper X", checking X is useful background. Arguing that X is itself weak ("They compare multiple benchmarks in only 2 of their 6 tables") invites the reviewer to state the standard more sharply, which is what happened. Produce what X's table has, on our winning metric, or use R1.

**R5 — State the drop as what we keep, on our metric.** Lead with retention and the efficiency metric the paper defines:
> "VQToken retains 99.5 % of NextQA's accuracy, 98.1 % of ActivityNet-QA's … under a 99.86 % reduction in token count … a > 300× increase in TokDense." (*VQToken*)

Only after the reviewer explicitly named the drop (otherwise the losing benchmark stays out). Even then the user rules on whether the weakest number is printed (`needs_user_input`).

**R6 — Ask for the specific item, then deliver it.** "If there is a specific benchmark or metric you would like to see, please name it and we will add it" puts the next step on the reviewer and shows the AC good faith. It works only if the named item then appears in the next reply; *VQToken* asked, got a precise answer (DyCoke Table 1 standard), and did not produce it.

**R7 — A scope argument must match what the paper itself evaluates.** *VQToken* argued long-video understanding is "another important, yet completely different, task". The reviewer replied that "2 of 5 benchmarks they conduct the experiments on the paper are long videos". If the paper's own benchmark list contradicts the scope line, the reviewer turns the paper against the reply. Check the paper's tables before drawing a scope line.

**R8 — Isolating the outlier goes to the AC, not to the outlier.** In the closing note to the AC, *VQToken* wrote that the remaining concerns "were raised only by Gyx4 among the four reviewers", that "no methodological flaws were identified", and that they "are presentation-oriented". The AC's meta-review repeated that shape. In the reviewer's own thread, the same move ("Unlike the other three reviewers, Reviewer Gyx4's comments center on paper organization, writing style …") did not move the reviewer, whose follow-ups only got sharper. Use it only in the AC-facing note ([followup-and-endgame.md](followup-and-endgame.md) § AC closing note), and only with the counts true.

**R10 — A weak number goes next to the best the others reach.** When the reviewer quotes a number of ours that is not high in absolute terms, do not argue that it is high; show that the strongest existing method reaches less on the same quantity, measured with the same protocol (「如果说不好, 就写 别人的最好的也不如我们好」). Conditions: [comparison-rules.md](comparison-rules.md) § Weak number.

**R9 — Structural distinction over denial.** When a reviewer claims the work reduces to / is subsumed by a generic framework, do not deny the reduction. Identify the structural feature our parameterization preserves that the generic framework does not, backed by a concrete mechanism (theorem dependency, derivation step, or empirical consequence) — see `response_mode: structural_distinction` in `SKILL.md`. Never rhetorical without the mechanism.

## 4. Anti-patterns (each one happened in VQToken)

| What was written | What followed | Rule |
|---|---|---|
| A flagged number (39.3 vs 38.2) explained as "subtle hardware-driven variations between GPU architectures" | Reviewer: "Why did only the metrics of this benchmark fluctuate …?" Authors retracted: a value "copied from a different experiment"; the correct number was the one in the table | Open the logs before answering (Phase 3 step 6). Answer with the verified value and where it comes from. Never offer a guessed cause |
| Missing citation defended with "many prior video‐LLM works compare models trained under different … data regimes" | Reviewer: "this cannot be the reason to 'hide' LLaVA-Video without any citing" | "We will cite X." Nothing else (「漏引的就说会引用就好了」) |
| "Sorry for the misunderstanding", "We apologize for the omission", "We regret the confusion", "We wholeheartedly agree", "You are correct that …" | Each one concedes; "sorry for the misunderstanding" also tells the AC the reviewer misread | Banned (Never concede). Open with the thanks clause and the verdict |
| "7 B VQToken 78.59 vs 7 B LLaVA-OV 81.40 … These results confirm that VQToken not only maintains but improves performance" | The table next to the sentence contradicts it | Every evaluative word must agree with the numbers beside it (lint: self-contradiction scan) |
| "§ 3.3 'Material Physics MoE'" in a video-token paper | Text from another project leaked into the reply | Lint: foreign-content scan |
| Reviewer asked for k-means latency/FLOPs; reply gave a complexity derivation plus "we will include actual latency measurements … in the camera-ready" | Meta-review: "left … overhead issues unresolved" | A measurable ask gets the measurement in the reply |
| "requested during the final two days", "the limited rebuttal period prevents us", "rapid iteration during rebuttal" | Advertises that the work is incomplete | Never expose a weakness. State what is there |
| Three nudge posts aimed at one reviewer plus two to all reviewers, Aug 2–8, most carrying no new content | Reviewer kept 2 | [followup-and-endgame.md](followup-and-endgame.md) § Nudges |

## 5. Phrase bank

All lines are compatible with Never concede / Never expose a weakness. Fill brackets from evidence only.

Verdict-first openers
- "Thank you for pressing on [X]. [Verdict in one clause]: [number]."
- "Thank you for checking [table/sample] directly. The value is [v] ([log/run id])."

Novelty / "done before"
- "To our knowledge, no prior work [does X under regime Y]. The closest, [Z], [does W]; the difference is [mechanism]. We would welcome a pointer to any method that [operates under Y] and will compare against it directly."

"Compare with stronger baselines"
- "[Baseline A] and [B] at matched token budget on [benchmarks]: ours [a] vs [b] vs [c]." (one metric for every baseline — `comparison-rules.md`)

"Reduces to generic X"
- "[X] fixes [component]; our formulation keeps [structural feature], which is what [Theorem/Eq./Table] depends on."

Missing citation
- "We will cite [X]."

Reviewer-flagged number (after checking logs, and after the user's ruling)
- "Thank you for checking this cell. The value from [log] is [v]; Table [n] reports [v]."

Scope
- "The validated strength of [method] is [X], shown on [benchmarks/numbers]."

Ask for specifics
- "If there is a particular [benchmark/metric/baseline] you would like to see, please name it and we will add it to this thread."

Quote-back (once, late)
- "Your review lists as a strength: '[verbatim]'. The added [table] extends exactly that."

## 6. Co-author review lessons (Bench-P ICLR 2027 board, 2026-11-09)

Co-authors commented on the draft replies in the shared Google Doc (user 2026-11-09: 「你看看 google doc 的改动, 也学一下」). Each lesson below is a comment they left, generalized. All of them were applied to that draft; apply them before a co-author has to ask.

**C1 — A new experiment is announced, aimed, set up, then concluded.** Before the first number: say it is new, and what it tests. *"To test whether the per-domain and per-law conclusions rest on videos in which the event is missing (new experiment, same labels), we recomputed …"* Then the setup in one or two sentences — models and sizes, data, what "zero-shot" and the training recipe mean (*"LoRA SFT, rank 32, on 9,758 per-law human scores from the 7 non-Veo generators, 1 epoch"*). Then the numbers. Then the conclusion. A number that appears with no stated experiment ("Suddenly it mentions some results. We do not know what experiments these results belong to") is the most common co-author complaint.

**C2 — Every number has an address.** Either a location in the paper (Table / Figure / Appendix / line) or the words "a new analysis of the paper's human ratings (no new labels)". A reviewer cannot check a number whose source is not stated.

**C3 — No action without its result.** "If we mention we did something, also discuss the results." A sentence like "Judge-P-9B scored all 500 videos" must be followed by what the scores showed and what that means for the reviewer's question.

**C4 — Close every evidence paragraph with its conclusion.** End on one sentence that states what the numbers demonstrate for the reviewer's concern: *"… demonstrating that Judge-P-9B's preference for physical correctness transfers to generators it never trained on, which is the property a reward model needs."*

**C5 — Name before you refer.** "Both GPT versions" is unreadable until the versions have been named; name them at first mention (*"both GPT versions we tested, gpt-6-astra and gpt-5.5"*). When two items share a number, say so explicitly ("both are 29.0%") so it does not read as a typo.

**C6 — Self-explanatory names.** Labels invented while drafting ("Same recipe") are renamed to what a reader understands at once ("Judge-P recipe") in the text and in every table.

**C7 — Complete, formal sentences.** No two-word answers ("It does."). Restate the claim as a full sentence: *"The physics supervision also transfers to a backbone from outside the Qwen family."*

**C8 — Make a win eye-catching: superlative + number + ratio to the runner-up.** Not "Bench-P leads" but *"Bench-P leads with the largest human study in the table: the most annotators (459, seven times WorldModelBench's 65, the next largest) and the lowest workload per annotator (12.6 videos, one tenth of the next lowest, 128)."*

**C9 — Future work is concrete.** Name methods, not intentions: best-of-N / rejection sampling, DPO on judge-ranked preference pairs, RL fine-tuning (GRPO-style) with the judge score as reward, per-law targeted rewards. "Training a generator with X as the reward is future work" alone reads as hand-waving.

**C10 — Pre-empt the obvious follow-up on an odd-looking number, within the hard rules.** Co-authors asked "larger size makes it worse — do we need to say why?" and "is 19.9 ok when others are 30+?". Answer such a question in the reply before the reviewer asks it, but only with positive-scope facts that hold: the range every variant lands in, the comparison it still wins (*"all four fine-tuned sizes land at 3.3% to 8.6%, below every closed judge in Table 5"*), a neutral setup fact (*"all sizes reused the 9B hyperparameters without retuning"*). No guessed cause (lint 16), no concession. If no such framing exists, the odd number is an ordinary weakness and leaves the reply ("Never expose a weakness").

**C11 — Generalize from the single instance.** When the reply defends one example the reviewer named (scenario 153), add the check that covers every example the reviewer could name next: *"we removed each of the 250 scenarios in turn … for every removal, 6 of 8 generators keep their exact rank … all Table 23 contrasts keep their sign."* Pairs with Phase 3 step 6 (check the named instance by hand first).

**C12 — Do not change what nobody questioned.** A co-author on a proposed title change: "the reviewer does not mention that the title is not reasonable … change title feels unconfident." Unprompted retreats (title, scope, claims) read as lack of confidence; the same rule as "a revised PDF edits only what a reviewer raised".

**C13 — Check that the answer answers the question.** A co-author asked, per answer: "需要确认是否分析回答了审稿人的问题，如果没有，指出来". For each W/Q, list the sub-questions the reviewer asked and mark each answered / partly / not yet (with what is missing). Partial coverage goes to the user, not silently into the post. This is the coverage gate applied at sentence level.

**C14 — Implementation questions are answered from the code and the released artifact, not from the paper's wording.** User edit of the R5 W1 reply (2026-11-09: 「doc 我改了一个, 你学一下」). The reviewer asked whether the vision–language aligner is trained, since Section 3.5 says "only LoRA" and Table 24 lists the aligner as "trainable". The earlier draft read Table 24 literally ("the aligner is updated alongside the LoRA parameters"), which was imprecise. The training flags (`--train_type lora --target_modules all-linear --freeze_aligner false --aligner_lr 2e-6`), the ms-swift source (with `all-linear`, `freeze_aligner false` adds LoRA modules to the aligner; `aligner_lr` sets the learning rate of the aligner's trainable parameters) and the released adapter (LoRA tensors on the language model and on `visual.merger.linear_fc1/fc2`, `modules_to_save` empty) all show the aligner is updated **through LoRA**. Before answering "which parameters are trained / how is X computed / what does the checkpoint contain", open the training script, the framework source for any flag whose meaning matters, and the artifact itself; cite what they show.

**C15 — Point to something the reviewer can check.** *"The vision encoder and all base weights stay frozen, so the released checkpoint contains only the LoRA adapters."* One verifiable fact about a public artifact closes a mechanism question better than a restated config. (Stay anonymous: name the artifact, not a link that identifies authors.)

**C16 — For a presentation fix the reviewer asked for: answer, then the revised text verbatim with its location, then every other place that changed, then the consistency sweep.** *"In Section 3.5, we clarify that '…' Besides, Table 24 now describes the aligner row as LoRA adapters with their learning rate … In addition, we have checked the rest of the manuscript, including the training details in Appendix H, to make sure the trainable parameters are described the same way."* The sweep sentence pre-empts "and elsewhere?" (C11). Each location must be true in the revised PDF before posting — diff the revision (lint 3, commitment).
