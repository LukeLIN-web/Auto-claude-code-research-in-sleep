# Rhetoric: persuading and refuting

Read before drafting any response file (Phase 4) and before every follow-up reply (Phase 8).
Everything here operates inside the hard rules of `SKILL.md` — **Never concede**, **Never expose a weakness**, provenance and commitment gates. A move below that would break one of them is not available, however well it worked elsewhere.

User request this file answers (2026-11-09): 「主要是学习各种话术. 怎么说服, 反驳」.

## 0. The reader is the AC

In one thread, two positive reviewers kept borderline ratings after the replies, one of them after being asked to raise it, and the negative reviewer never moved. The paper was accepted on the AC's reading. The meta-review repeated the authors' own framing of the split between the negative reviewer and the others. It also listed, as unresolved, exactly the points the replies had answered with a promise rather than a number.

Consequences for every reply:
- Write so that an AC who skims can see, per point, that the concern was met with evidence. The reviewer may never move; the AC still records what was answered.
- Whatever is answered with a promise instead of a number is what the AC will list as unresolved.
- Moving the reviewer is a bonus; leaving the AC with nothing to hold against the paper is the goal.

## 1. Answer shape

**Default reply pattern per issue:**
- Sentence 1: a short thanks naming what the comment did, then the direct answer to the question as asked — the verdict, the number, or the yes/no ("Thank you for this pivotal comment. All four headline contrasts are significant."). NEVER open with process or setup ("We ran...", "We recomputed...", "New table on...") — that buries the answer; method details come after the verdict.
- Sentence 2-4: grounded evidence
- Last sentence: implication for the paper

**Can / cannot gets a yes or no first** (user 2026-11-12: 「A 应该要回答问题啊, 有个能不能, 你都没说能不能找半天找不到」). When the weakness or question is about capability, whether phrased as a question ("Could the forecaster run at hourly resolution?", "Can the benchmark …?", "Does X hold …?") or as a claim ("… cannot test skill where the model must forecast past its training horizon", "… does not support …"), the sentence right after the thanks starts with the answer itself: "Yes", "Yes, now:", "Yes, for <scope>:", or the scoped form of "not yet". The scope and the evidence come in the same sentence or the next, and the yes says what the reply then shows ("Yes, the benchmark can now test this: extended versions of N cases require the forecaster to run past its training horizon …"; "Our answer is yes for ranking candidate forecasts, which we tested directly; training a forecaster with it is future work."). Failed openers from one thread: an argument the reader has to turn into an answer ("Fixing the initial state constrains which pattern must develop but not how it evolves …"), process ("Inspired by your comment, we ran the comparison you propose …"), setup ("A ranking score has to prefer …, so we ran …"), and a finding about a side question ("In short, giving the initial state makes the task easier but does not change how models compare"). Each was correct, and still the reader could not find whether the answer was yes. The yes goes in the first comment of a split reply, never only in "(continued)". When the honest answer is partial, say yes to the part that holds and name the rest as future work in the same sentence. Do not make the reviewer infer the yes from an experiment description. This is still a verdict, not a concession: "Yes, now" answers a "cannot" without granting that the submitted version was deficient.

**Thanks opener (every answer).** Each `A#` opens by thanking the reviewer, then delivers the verdict right after the thanks (user 2026-11-09「改写 skill」: the warm opener is the house style):
- Up to two short sentences of thanks, warm in tone; an exclamation mark is fine ("Thank you for your keen observation! We appreciate your careful reading."). The sentence right after the thanks is the answer, and may open with "To clarify," — never with process or setup.
- Naming what the comment did adds information and is welcome when it fits ("Thank you for checking Section 4.2 against Table 17."), but generic warm thanks is allowed.
- Vary the wording across answers within a file and across reviewer files. The same thanks sentence repeated at every `A#` reads as a template; keep the warmth, change the words.
- Thank for the observation, not for the verdict. Thanking a reviewer for a concern the answer then refutes ("Thank you for catching this error" when no error exists) concedes a point the evidence does not.
- The file-level acknowledgment at the top of the response covers that reviewer's main thrust; the per-answer openers must not restate it in the same words.
- No flattery paragraphs. Two warm sentences are the ceiling; one thread opened two replies with a whole paragraph of praise for the review, and neither reviewer moved.

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
In one thread, a reviewer asked for scores on a benchmark's subsets. The first reply gave a breakdown the authors chose (by input length); the reviewer had to clarify that they meant the benchmark's official subsets. The second reply gave those, and the reviewer wrote that this addressed all their questions. Read `asked_for` from the raw text; when a benchmark has an official breakdown, the reviewer means that one.

**P2 — Justify a design choice with reasons a reviewer cannot argue with.**
One reply defended a reduced-input setting with three reasons: the efficiency regime the paper targets, the benchmark's standard configuration, and the need to iterate quickly during the rebuttal. The first two carry the answer. The third exposes that the experiment was rushed — drop reasons of that kind ("Never expose a weakness").

**P3 — Turn their praise into the paper's thesis.** When a positive reviewer names a strength, the reply restates it as the paper's contribution with one number behind it, so the AC sees the strength confirmed rather than merely thanked.

**P4 — Close the loop, then stop.** Once a reviewer writes that the concerns are resolved, reply with one short thanks naming what changed. Do not keep feeding them new material.
On asking for a higher score, see [round2-replies.md](round2-replies.md) § 7 Score requests — in one thread it moved nothing.

## 3. Refuting (negative reviewers)

**R1 — Define the regime, then shift the burden.** When the attack is "this has been done" or "compare to stronger baselines", state the regime that makes the work new and invite the reviewer to name a counterexample:
> "To our knowledge, no prior work has formally defined <the regime> … Most existing methods stop at <a weaker operating point> … We welcome references to any method that operates in <the regime> and will include direct comparisons in our revision."

In one thread the AC's meta-review accepted this framing and called the approach novel. Requires that the claim survives `/novelty-check`; if a counterexample exists, this move hands the reviewer a win.

**R2 — Quote their own words back, once.** A reviewer who listed a strength and later attacks the same thing can be shown their sentence:
> "Your Strengths section states: '<their verbatim words>'."

Plain text, once, in a late round, as a pointer for the AC. One thread wrapped it in coloured warning markers, posted hours before the deadline, and got no reply. Loud formatting reads as anger and costs more than it gains.

**R3 — Answer the criterion, not the volume.** When the reviewer has a specific criterion, meet that criterion. In one thread the authors answered "comparisons are insufficient" by counting the experiments in the paper and the rebuttal. The reviewer replied that counting tables or experiments shows nothing about whether the comparisons suffice, and spelled out the real criterion as a number: baselines × benchmarks in one table, against the larger matrix of a paper the reviewer cited. The right reply was that matrix, or — if it cannot be produced — R1. Never count experiments, tables or pages as an argument.

**R4 — Meet a cited standard; do not litigate it.** When the reviewer says "to the standard of paper X", checking X is useful background. Arguing that X is itself weak (counting how few of X's own tables meet the standard) invites the reviewer to state the standard more sharply, which is what happened. Produce what X's table has, on our winning metric, or use R1.

**R5 — State the drop as what we keep, on our metric.** Lead with retention and the efficiency metric the paper defines:
> "<Method> retains <x> % of <benchmark A>'s accuracy and <y> % of <benchmark B>'s … under a <z> % reduction in <cost> … a > <k>× gain in <the paper's efficiency metric>."

Only after the reviewer explicitly named the drop (otherwise the losing benchmark stays out). Even then the user rules on whether the weakest number is printed (`needs_user_input`).

**R6 — Ask for the specific item, then deliver it.** "If there is a specific benchmark or metric you would like to see, please name it and we will add it" puts the next step on the reviewer and shows the AC good faith. It works only if the named item then appears in the next reply; in one thread the authors asked, got a precise answer (another paper's table as the standard), and did not produce it.

**R7 — A scope argument must match what the paper itself evaluates.** In one thread the authors argued that the setting a reviewer raised was a completely different task. The reviewer replied that two of the paper's own benchmarks were in that setting. If the paper's own benchmark list contradicts the scope line, the reviewer turns the paper against the reply. Check the paper's tables before drawing a scope line.

**R8 — Isolating the outlier goes to the AC, not to the outlier.** In one thread's closing note to the AC, the authors wrote that the remaining concerns came from one reviewer of the four, that no methodological flaw had been identified, and that the concerns were about presentation. The AC's meta-review repeated that shape. In the reviewer's own thread, the same move (contrasting that reviewer's comments with the other three reviewers') did not move the reviewer, whose follow-ups only got sharper. Use it only in the AC-facing note ([posting-and-endgame.md](posting-and-endgame.md) § 2 AC closing note), and only with the counts true.

**R10 — A weak number goes next to the best the others reach.** When the reviewer quotes a number of ours that is not high in absolute terms, do not argue that it is high; show that the strongest existing method reaches less on the same quantity, measured with the same protocol (「如果说不好, 就写 别人的最好的也不如我们好」). Conditions: [comparison-rules.md](comparison-rules.md) § Weak number.

**R9 — Structural distinction over denial.** When a reviewer claims the work reduces to / is subsumed by a generic framework, do not deny the reduction. Identify the structural feature our parameterization preserves that the generic framework does not, backed by a concrete mechanism (theorem dependency, derivation step, or empirical consequence) — see `response_mode: structural_distinction` in `SKILL.md`. Never rhetorical without the mechanism.

## 4. Anti-patterns (each one happened in one real thread)

| What was written | What followed | Rule |
|---|---|---|
| A number the reviewer flagged (the text and the table disagreed) explained as a hardware difference between GPU types | The reviewer asked why only that benchmark fluctuated; the authors retracted: the value had been copied from another experiment, and the table was right | Open the logs before answering (Phase 3 step 6). Answer with the verified value and where it comes from. Never offer a guessed cause |
| A missing citation defended by saying prior works also compare models trained on different data | The reviewer answered that this was no reason to leave out a work whose data the paper uses | "We will cite X." Nothing else (「漏引的就说会引用就好了」) |
| "Sorry for the misunderstanding", "We apologize for the omission", "We regret the confusion", "We wholeheartedly agree", "You are correct that …" | Each one concedes; "sorry for the misunderstanding" also tells the AC the reviewer misread | Banned (Never concede). Open with the thanks clause and the verdict |
| A sentence saying the method maintains and even improves performance, next to a table where it scores below the baseline | The table next to the sentence contradicts it | Every evaluative word must agree with the numbers beside it (lint: self-contradiction scan) |
| A reply naming a section and a module that exist only in another project's paper | Text from another project leaked into the reply | Lint: foreign-content scan |
| Reviewer asked for the latency and FLOPs of one component; the reply gave a complexity derivation plus a promise to measure it for the camera-ready | The meta-review listed overhead as unresolved | A measurable ask gets the measurement in the reply |
| Timing excuses: the request came late, the rebuttal period is too short, the run was rushed | Advertises that the work is incomplete | Never expose a weakness. State what is there |
| Several nudge posts to one reviewer within one week, plus posts to all reviewers, most carrying no new content | The reviewer kept the score | [round2-replies.md](round2-replies.md) § 6 Nudges |

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

## 6. Co-author review lessons (2026-11-09)

Co-authors commented on the draft replies in the shared Google Doc (user 2026-11-09: 「你看看 google doc 的改动, 也学一下」). Each lesson below is a comment they left, generalized. Apply them before a co-author has to ask. Lessons C17–C27 are in § 7; drafting moves from text a co-author wrote directly into the doc are in § 9.

**C1 — A new experiment is announced, aimed, set up, then concluded.** Before the first number: say it is new, and what it tests. *"To test whether the per-category conclusions rest on degenerate samples, we recomputed …"* Do not add "(same labels)" or "(no new labels)": what is not new is not volunteered ([collaboration.md](collaboration.md) § 8). Then the setup in one or two sentences — models and sizes, data, what "zero-shot" and the training recipe mean (*"LoRA SFT, rank 16, on the station records of the training years, 2 epochs"*). Then the numbers. Then the conclusion. A number that appears with no stated experiment ("Suddenly it mentions some results. We do not know what experiments these results belong to") is the most common co-author complaint.

**C2 — Every number has an address.** Either a location in the paper (Table / Figure / Appendix / line) or the words "a new analysis of the paper's released labels" (never followed by "(no new labels)", [collaboration.md](collaboration.md) § 8). A reviewer cannot check a number whose source is not stated.

**C3 — No action without its result.** "If we mention we did something, also discuss the results." A sentence like "The model scored all N held-out cases" must be followed by what the scores showed and what that means for the reviewer's question.

**C4 — Close every evidence paragraph with its conclusion.** End on one sentence that states what the numbers demonstrate for the reviewer's concern: *"… demonstrating that the ranking transfers to regions the model never trained on, which is the property an operational forecaster needs."*

**C5 — Name before you refer.** "Both GPT versions" is unreadable until the versions have been named; name them at first mention (*"both GPT versions we tested, gpt-6-astra and gpt-5.5"*). When two items share a number, say so explicitly ("both are 31.5%") so it does not read as a typo.

**C6 — Self-explanatory names.** Labels invented while drafting ("Same recipe") are renamed to what a reader understands at once ("<method> recipe") in the text and in every table.

**C7 — Complete, formal sentences.** No two-word answers ("It does."). Restate the claim as a full sentence: *"The auxiliary supervision also transfers to a backbone from outside the original model family."*

**C8 — Make a win eye-catching: superlative + number + ratio to the runner-up.** Not "X leads" but *"X leads with the largest observation network in the table: the most stations (five times the next largest) and the shortest gap between readings (one eighth of the next shortest)."*

**C9 — Future work is concrete.** Name methods, not intentions: ensemble post-processing, quantile regression on the corrected outputs, fine-tuning with the skill score as the loss, per-region targeted losses. "Using X to train a forecaster is future work" alone reads as hand-waving.

**C10 — Pre-empt the obvious follow-up on an odd-looking number, within the hard rules.** Co-authors asked "larger size makes it worse — do we need to say why?" and "is this value ok when the others are much higher?". Answer such a question in the reply before the reviewer asks it, but only with positive-scope facts that hold: the range every variant lands in, the comparison it still wins (*"all four fine-tuned sizes land in a narrow range, below every closed-source baseline in Table k"*), a neutral setup fact (*"all sizes reused the largest model's hyperparameters without retuning"*). No guessed cause (lint 16), no concession. If no such framing exists, the odd number is an ordinary weakness and leaves the reply ("Never expose a weakness").

**C11 — Generalize from the single instance.** When the reply defends one example the reviewer named (one region), add the check that covers every example the reviewer could name next: *"we removed each of the N regions in turn … for every removal, most models keep their exact rank … all contrasts keep their sign."* Pairs with Phase 3 step 6 (check the named instance by hand first).

**C12 — Do not change what nobody questioned.** A co-author on a proposed title change: "the reviewer does not mention that the title is not reasonable … change title feels unconfident." Unprompted retreats (title, scope, claims) read as lack of confidence; the same rule as "a revised PDF edits only what a reviewer raised".

**C13 — Check that the answer answers the question.** A co-author asked, per answer: "需要确认是否分析回答了审稿人的问题，如果没有，指出来". For each W/Q, list the sub-questions the reviewer asked and mark each answered / partly / not yet (with what is missing). Partial coverage goes to the user, not silently into the post. This is the coverage gate applied at sentence level.

**C14 — Implementation questions are answered from the code and the released artifact, not from the paper's wording.** User 2026-11-09: 「doc 我改了一个, 你学一下」. The reviewer asked whether the input projector is trained, since Section 4.2 says "only LoRA" and Table 17 lists the projector as "trainable". The training flags (`--tuner lora --lora_targets all-linear --freeze_projector false --projector_lr 1e-5`), the training framework's source (with `all-linear`, `freeze_projector false` adds LoRA modules to the projector; `projector_lr` sets the learning rate of the projector's trainable parameters) and the released adapter (LoRA tensors on the backbone and on the projector's linear layers, `modules_to_save` empty) all show the projector is updated **through LoRA**. Before answering "which parameters are trained / how is X computed / what does the checkpoint contain", open the training script, the framework source for any flag whose meaning matters, and the artifact itself; cite what they show.

**C15 — Point to something the reviewer can check.** *"The feature encoder and all base weights stay frozen, so the released checkpoint contains only the LoRA adapters."* One verifiable fact about a public artifact closes a mechanism question better than a restated config. (Stay anonymous: name the artifact, not a link that identifies authors.)

**C16 — For a presentation fix the reviewer asked for: answer, then the revised text verbatim with its location, then every other place that changed, then the consistency sweep.** *"In Section 4.2, we clarify that '…' Besides, Table 17 now describes the projector row as LoRA adapters with their learning rate … In addition, we have checked the rest of the manuscript, including the training details in Appendix F, to make sure the trainable parameters are described the same way."* The sweep sentence pre-empts "and elsewhere?" (C11). When the reviewer's request names the change ("Please reconcile these descriptions"), report it in their verb — "Per your comment, we have reconciled the two descriptions" — which the user ruled is not a concession (2026-11-09); never call the old text wrong or inconsistent. Each location must be true in the revised PDF before posting — diff the revision (lint 3, commitment).

## 7. Co-author review lessons (2026-11-10)

A co-author and the user commented on the draft replies in the shared Google Doc (user 2026-11-10: 「根据comment 改一改 … 更新一下 rebuttal skill . 学习」). Each lesson is one or more of those comments, generalized.

**C17 — Numbers live in a table; the prose carries the verdict.** User: 「rebuttal 就不要写这么多具体数字, 最好搞个表」. Once a reply compares more than one benchmark or more than one arm, put the values in a markdown table (OpenReview renders it) and keep the sentence to the verdict: *"Removing the auxiliary loss lowers accuracy significantly on A, B and C."* Print levels (ours vs. theirs) rather than a Δ row beside them; drop intervals from prose once *significant* is defined in the Conventions. The user confirmed it for every thread (2026-11-10: 「应该放到表格」): per-benchmark cost rows, signed timing differences and scorer comparisons each became a table, with the verdict and *significantly* in the sentence after it and no intervals in the prose. Lint 21 checks this.

**C18 — Name a comparison arm once, then use the name.** Co-author: "give this baseline a name such as '<name>' so that people know what it means when they see '<name>' in the paragraph." Define it in one sentence at first use (*"We call this variant X-only: the same backbone, inputs, schedule and data as our method, with the auxiliary loss removed."*) and use that name in the table and text. A description repeated in place of a name ("X alone", "with the auxiliary loss removed") reads as two different arms. Same rule as C6, for arms instead of drafting labels.

**C19 — A new capability is stated as a diff against the usual pipeline.** Co-author: "use more sentences like 'instead of XXX' or 'rather than XXX'. Let people know what the original inference process is, and compared with it, which steps we remove and which we add." Write the usual process in one sentence and what goes wrong with it, then the replacement step by step: *"The usual way is [one-pass process]; as [the input] grows, that pass [what goes wrong]. Our method replaces that one pass with two steps. Instead of [old step], it [new step]; rather than [old step], it [new step]."* A list of properties ("no step needs …, every pass reads …") makes the reader reconstruct the contrast.

**C20 — Lead a cost measurement with its operational consequence.** Co-author: "highlight the direct outcome — we finish with one card while others need two, many ⟨inputs⟩ cannot be ⟨processed⟩, but we finish all." GB and seconds come second: *"Our method processes every sampled input on one card, whereas the official recipe does not fit on one card: it did not complete [n of N] inputs … The baseline paper's own run of that recipe used two cards."* Check each word against the logs (every sampled input completed, on every benchmark) before writing "every".

**C21 — Where a measurement the reviewer asked for goes against us, give the fewest losing numbers and a verified reason.** Co-author: "it seems to be slower here? if so, write fewer slower results, e.g. only mention one number, and add some discussion why it is slower." Keep the loss on the baseline the reviewer named; drop losses against secondary comparators ("Never expose a weakness"); explain the one kept from a measured breakdown, never a guess (lint 16): *"Our extra time there comes mostly from [stage A] and [stage B]; half of the sampled inputs on that benchmark are small, and one full-resolution pass there takes about two seconds"* (stage medians from the timing ledger). End on what the cost buys. The reply still never uses the word "slower" (C28). Dropping a comparator the user earlier ruled in is reported to the user as an open item.

**C22 — Describe a competitor's mechanism as theirs; never "inserted into ours".** Co-author on *"[a competitor's score] inserted into [our method] adds a second pass on every input"*: "do not mention [our method] here — [that score] is from other work, we do not combine them." State the competitor's cost on its own terms (*"so every scored candidate costs a full forward pass"*), and present a controlled swap as an experiment, not a hybrid method.

**C23 — A controlled comparison names its model, data and what is held fixed.** Co-author: "if we have additional experiments, specify how they are conducted, on what model with what dataset. No need to be long." One sentence: *"Table k compares the two scores directly on the same backbone and all four benchmarks: every row keeps the same inputs, candidates and output head, and only the scoring function changes."* This is C1's setup sentence, required also for paper tables a reply leans on, not only for new runs.

**C24 — Summarize the numbers before the decision they justify.** Co-author on a reply that listed results and then said *"We use one shared head for the four headline benchmarks"*: "add a conclusion to summarize the results … and then this sentence shows our choice based on the conclusion." Pattern: numbers → *"Augmentation alone thus gives our method a significant lead on every benchmark, and the shared head adds to it on two of them."* → *"We therefore use one shared head …"*. Every evidence paragraph and every table ends with a conclusion sentence (C4).

**C25 — Every listed difference must be an advantage.** User on *"no teacher model sits in the loop"* in a list of how our method differs from the closest work: 「好像不是优点?」. In an "X differs in three ways" answer, each item must be something the reviewer would count in our favor; a property that is merely different invites "so what" and dilutes the real differences. Cut it.

**C26 — No new technical term for a one-off statistic.** User on *"median Jaccard 0.37"*: 「不要引用新名词, 简单点」. When a number needs a term the paper and the reply do not otherwise use, say in words what changed (*"changes which channels are kept"*) and keep the number that carries the claim.

**C27 — Never reveal that a result or recipe has an earlier version.** User: 「不能提 在早期配置中, 不能暴露我们不一致」 (on *"In an earlier configuration, …"*), after 「不要暴露我们之前是旧版的」. Words such as *earlier configuration / recipe / export / version*, *previously*, *re-run*, *updated*, 早期, 早先, 旧版 tell the reviewer the paper and the rebuttal disagree somewhere. Cite only the current result; if only an earlier run supports a point, the point goes (or waits for a run on the current setup). A variant that was tried and dropped is a weakness anyway. Lint 10 checks the words.

## 8. User rulings on cost and run wording (2026-11-09 and 11-10)

**C28 — Cost gaps are signed differences; "slower" and "faster" follow the reviewer and the numbers.** User: 「少用更慢，除非审稿人明确指出」, 「不要说 slower」. No reply calls our method slower unless a reviewer has said it is. Give a time gap as a signed paired difference, ours minus the baseline (*"Time, ours − official recipe (s): −x / +y / +z"*), or as two medians with no comparative word (*"X and Y s"*). "Faster" is written only when it holds on every benchmark the reply times, on one measurement setup (comparison-rules: one measurement setup for every arm). When the signed gaps go both ways by a few seconds, say *"within a few seconds of the official recipes"* and lead with memory and one-card feasibility (C20) (user 2026-11-10 「同意」). Lint 10 checks the words.

**C29 — Never tell the reviewer when a run was made.** User on *"we ran them before submission"*: 「不要暴露这些信息给 reviewer」, and on the † convention: 「可以。Results marked † are new in this rebuttal.」. The only timing a reply carries is the † mark, defined once in the Conventions as *"Results marked † are new in this rebuttal."*: never "completed after submission", "ran before submission", "from runs completed after submission", a date, or "they exist". If a sentence's only job is to say when or whether a run was made, delete it and open with the result. Lint 10 checks the words.

## 9. Drafting moves from co-author-written text (2026-11-09/10)

A co-author wrote one reviewer's file opener, A1 and A2 directly in the shared Google Doc. The user kept the co-author's A1 opening paragraph word for word (board, 11-10: 「原文，不改字」). Another co-author left suggestions (run-in labels in bold; "We …" → "Following the suggestions, we …" on work the reviewer asked for). These are the moves worth copying; the two that break hard rules are listed last. User request (2026-11-10): 「根据 google doc 的注释, 更新一下 skill, 学习一下各话术」「就是合作者的 comment」.

**C30 — Restate an abstract weakness as the reader's concrete stake, then say the paper tests exactly that.** *"We understand your question as whether someone who wants to add a new model or new regions to the benchmark next year can trust its skill scores without collecting new station data. … In Appendix X, we test exactly this, and find that the model-level scores stay calibrated when the forecaster, the region, or both are new."* The reviewer wrote "limited evidence for extensibility"; the restatement turns it into a test with a pass condition, and the next sentence reports the pass. Agreeing that the *question* matters (*"We agree this is the right question for a benchmark"*) credits the reviewer without granting the criticism. One sentence of restatement at most; the verdict follows in the next sentence (§ 1).

**C31 — Split the evidence by the reviewer's own cases, one run-in label per case.** The co-author's A1 answered "new models or new regions" with four labelled paragraphs, from the newest evidence to the hardest test: *Two recent forecasters, with new station data (new).* / *A forecaster the benchmark has never seen (App. X.4, Table k).* / *Regions the benchmark has never seen (App. X.6).* / *Everything new at once (App. X.5).* Each label names the case in the reviewer's terms, carries its address (C2) and marks new work "(new)"; a reviewer scanning the labels sees every case covered before reading a number. When a paragraph answers a second sub-question, say so in one clause: *"You also asked about new regions."* (C13). The other co-author suggested bold for such labels (*Scoring policy.*, *Stratified results.*) so they stand out in OpenReview; use one style per file.

**C32 — Work the reviewer asked for is credited to the reviewer and told as steps.** *"Per your comment, we have now included two major SoTA models … We first used each model to produce N forecasts under our original case set …, keeping configurations constant as our previous models. Then, we leveraged our verification pipeline to score each forecast produced by those two new models."* Use it only where the reviewer explicitly asked for the addition (the reviewer's-verb rule in `SKILL.md` "Never concede"); for unrequested analyses it reads as having been told to do them. *First … Then …* gives the setup of C1/C23 in the order it was run.

**C33 — The file opens with a point-by-point promise and an invitation to keep talking.** *"Thank you for your careful review and closely following our work! We appreciate the efforts you invested in reviewing our paper. We have carefully addressed your comment and provide a point-by-point response. We hope it satisfies your expectations and look forward to any of your further thoughts."* The invitation keeps the discussion open, which the AC reads as engagement (§ 0). A single *"We hope our response has addressed your concern."* may close the file's last answer, after its conclusion sentence (C4), never in place of it and not after every answer.

**Not copied (break a hard rule; they stay only as the co-author's own text, under the wording-pass rule that co-author text is not touched):**
- *"… and we should have made our answer easier to find."* concedes a presentation fault the reviewer did not name ("Never concede"). C30's restatement does the same work without it.
- *"We have now incorporated the two models in our manuscript and update all analyses accordingly."* is a revision promise the user had not approved, against the ruling not to change the paper for that reviewer ("Never overpromise"); it went to the board's open decisions ([collaboration.md](collaboration.md) § 2).

## 10. User ruling on secondary evidence (2026-11-10)

**C34 — Secondary evidence goes in only when the reviewer asked for it.** User: 「数字串挪进表格, 次要证据如果别人没要就别给, 如果要了就给.」 For each result in an answer, ask whether it is the answer to the reviewer's ask or support for it. The answer stays. Support stays only when a sentence of this reviewer's review asks for it (quote it, as for `asked_for`): a mechanism analysis behind a head-to-head comparison already given, a breakdown of an aggregate already given, a second metric for a lead already shown, the cost of a variant the reviewer did not raise, a comparison with a baseline the reviewer did not name, a result another reviewer asked for. Two exceptions, both reported to the user: it is the only support for a claim the answer makes, or the user or a co-author asked for it by name. Deleted support is held in the issue card as the follow-up answer if the reviewer asks. What survives and strings several values goes into a table (C17). Lint 22 checks this.

## 11. User ruling on voice (2026-11-12)

**C35 — Active voice, with "we" as the actor.** User: 「我们尽量用 We 这样子的主动语态，你让 AI 给你加强下表达和衔接，以及语言的 clarity」. Draft every action the authors took with "we" as the subject and an active verb: *"We fine-tuned the forecaster on the station records of the training years"*, not *"The forecaster was fine-tuned on …"*; *"We report the per-category results in Table k"*, not *"The per-category results are reported in Table k"*. A method, model, table or result may be the subject instead (*"Our forecaster ranks all ten regions in the observed order"*, *"Table k shows …"*). Impersonal openers go: *"It can be seen that"*, *"It should be noted that"*, *"It is worth noting that"* are deleted and the sentence starts with its subject. Three limits: (1) the sentence after the thanks is still the verdict (§ 1), so "we" does not turn *"All four contrasts are significant."* into *"We find that all four contrasts are significant."*, and never into *"We ran …"*; (2) passive stays where the actor is unknown or irrelevant (*"each image is labelled by three annotators"*), and no actor is invented to avoid it; (3) a co-author's passive sentence is not touched ([collaboration.md](collaboration.md) § 1). Active "we" also carries the cohesion of C1/C32: *"To test this, we … We first … Then, we …"* reads as one line of work, where a string of passives reads as a list of disconnected facts. In the wording pass, `/paper-polish`'s editor subagent applies this through `/paper-jargon-pass` and its [references/rewrite.md](../../paper-polish/references/rewrite.md), after `/paper-prose-tighten` has cut ([wording-pass.md](wording-pass.md) § 3–5); lint 23 checks the voice.

**C36 — An error inherited from a published dataset is attributed to its source, and the reviewer is credited for finding it.** User 2026-11-13: 「你前面认错的一定要谨慎……都是 previous wide-use publication 的错……不是你的错，是领域的历史遗留问题」「少数错误是我们自己造成的 这个后面能不写吗」「就说我们会联系」. The answer (1) says the inherited errors predate our work and come verbatim from widely used, peer-reviewed datasets, cited by number with their venues ([1] … <venue, year>) — check each venue first, never write "peer-reviewed" for an arXiv-only source; (2) says these inaccuracies were rarely noticed and that every work reusing the descriptions inherits them, and credits the reviewer's check for bringing them to light; this answer thanks the reviewer more warmly than the § 1 opener, as someone who helped the field (opener *"Thank you so much for your keen observation! We sincerely appreciate the effort you invested in helping us improve our work."*, one credit clause inside the answer, and a closing *"Thank you again for helping make these shared resources more reliable."*); the extra praise is for data-error answers only, not every reply (user 2026-11-13「不需要每条回复都要夸审稿人. 只是说怎么回复数据错误这部分」); (3) commits to correcting our copy and to contacting the authors of the source datasets where errors were actually found so they can fix them too (a source with no confirmed error may be named in a re-check, never in "contact them to fix these errors": the reviewer can check, and its authors may read the public reply; user 2026-11-13), instead of a list of new internal safeguards; (4) does not volunteer which errors were our own (the no-volunteer rule in `SKILL.md`). The limit: attribute only what really is inherited. When some errors are ours, the reply says "most of them" and stops; it never says "all" or calls an error of ours inherited, because the reviewer has the data and the upstream release to check against, and one disproved attribution costs more than the admission it avoided.

## 12. User ruling on "your measurement is unstable" questions (2026-11-13)

**C37 — Turn low reliability into the benchmark's contribution: novelty first, then a three-row table of human standard, prior SOTA and ours.** User: 「1. 你的 novelty，你是第一个做这个的，而且这个值得探索 2. 尽管现在所有的方法都达不到人类，但是 SOTA 比我们的差……所以我们第一次探索了这几个 metric，同时比现在 SOTA 的 metric 要好，更接近人类的判断」「你的表格放三个 1. 人类的标准 2. SOTA 和人类相似度 3. 我们和人类相似度」「把劣势变成优势」. The answer has four moves:
1. **Why it is worth measuring.** One concrete failure a coarser score would hide (*"A forecast can show a plausible storm track while total rainfall vanishes or appears from nowhere, which a single track score would hide"*), then the novelty claim, hedged with *"to our knowledge"* and tied to a table of the paper (*"is the first … to report how reliably expert forecasters rank models on each category (Table 12)"*). Then turn the weakness into the contribution: the instability can be seen only because we measured it (*"this per-category measurement is what lets us answer the reviewer's question with numbers"*).
2. **No paragraph on why it is unstable.** User: 「再讲为什么不稳……这样肯定不行啊, 这重复劣势了」. A cause paragraph (few cases, twice the sampling error, models close together) restates the weakness at length. Replace it with the level at which the paper's comparison is reliable, as a positive fact with its number (*"Table 9 compares models on these categories through two merged columns, Extremes and Mixed-Phase, whose expert ranking reliability reaches 0.69 and 0.84"*). Give a cause only if the reviewer explicitly asks why, and then use measured causes only (lint 16).
3. **One table with three rows, in this order:** the human standard (reliability projected to the full pool), the best prior evaluator against humans, and ours against humans. Columns = the units the reviewer named, plus the paper's merged columns that contain them. The conclusion sentence first says no automatic evaluator reaches the human standard, so the expert ratings we release are the reference (*"these categories remain an open problem for automatic evaluation, and <benchmark>'s expert ratings are the reference for them"*), then names the columns where ours is closest.
4. **Gate on "ours beats SOTA".** Before writing it, recompute every cell with the fair variant of our model (held out from what it scores; never a checkpoint trained on the scored items). Claim "closest to humans" only for the columns where it holds and name them; never write "better than SOTA" as a blanket claim. Do not drop a column the reviewer named because we lose there; that omission is the first thing the reviewer checks. If the user's requested framing does not hold for every column, write the true version and tell the user which columns break it.
