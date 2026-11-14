# Follow-up rounds and endgame

Read at Phase 7 (posting) and Phase 8 (every new reviewer comment).
Rhetoric rules: [rhetoric.md](rhetoric.md). Reports on bad-faith reviews: [misconduct-reporting.md](misconduct-reporting.md).

## 1. Posting order

Post one reviewer at a time, positive-score reviewers first; they usually confirm and then stop moving. Difficult negative-score reviewers go last (Phase 3 step 8, 「先一个一个回复，看正分审稿人愿不愿意confirm，他们一般confirm之后就不动了. 然后麻烦的负分先留到最后」). The board and collaborator doc use the same order from the start, highest score first (user 2026-11-12「下次应该把高分的放前面」); one rebuttal's board led with the 1-score reviewer and could not be reordered once co-authors were editing it.

VQToken fits this: LjpF acknowledged within three days and ended at 5; RRqQ (4) wrote "this fully addresses all my questions" and stayed at 4; the negative reviewer took the whole period.

## 2. Delta replies

When a reviewer comments again:
1. Append the comment verbatim to `FOLLOWUP_LOG.md`; link it to existing issue cards or open new ones.
2. Reply to the **new** points only. Restate nothing that already stands in the thread.
3. If the reviewer restated the same concern with a sharper criterion (VQToken Gyx4: from "compare with more recent methods" to "one table with multiple compression baselines AND multiple benchmarks: 1x2=2 vs DyCoke's 2x5=10"), the criterion is now the `asked_for`. Either deliver exactly that (the matrix, on our winning metric — `comparison-rules.md`) or switch to the regime argument (rhetoric R1). Do not re-send the earlier answer in new words; never count experiments.
4. Never repeat an argument that already failed — bring new evidence or a new angle, or stop. Escalate technically, not rhetorically.
5. For a reviewer whose lever is `argument` (Phase 3 step 7), keep closing each new objection until none is left.
6. A reviewer-flagged number or sample: open the logs/sample before replying (Phase 3 step 6). The VQToken hardware-variance guess had to be retracted one round later.

Long replies: split into `[PART 1/2]`, `[PART 2/2]` comments when over the per-comment limit (ICLR: "There is a word limit for each comment, but there is no limit on the number of comments"). Each part opens with its own label and closes with "continued in PART 2/2".

## 2a. A reviewer who confirms an accepting rating

When a follow-up confirms acceptance or keeps a positive rating ("I consider the work suitable for acceptance and maintain my positive rating") and leaves a minor concern, the reply is short and only thanks and answers (user 2026-11-14「能解决你就回消息，title 大写加粗 thank you for confirming acceptance rating 然后不要反驳他，就简短回答问题 他写你的好话，比如什么达到接收标准什么的黑体加粗感谢」「你要是解决不了就简单感谢」):

1. **Title line**, bold and upper case: `**THANK YOU FOR CONFIRMING THE ACCEPTANCE RATING**`.
2. **Bold thanks for every good thing the reviewer wrote**, in the reviewer's own terms: `**Thank you for finding the work suitable for acceptance, and the benchmark and judge useful for advancing physically realistic video generation.**`
3. **Can we resolve the remaining concern with evidence we already have?** Yes: answer it in one to three plain sentences, the verdict first, one number at most per claim. No: stop after the thanks; no answer, no promise, no "future work" paragraph.
4. **Never rebut, and do not state our position** (user 2026-11-14「所以也不要说我们的立场」). No "by design" defence, no "we respectfully disagree", no sentence explaining why our view of the concern is right, not even as a neutral design statement; no restating a position the reviewer did not accept; agreeing with the reviewer's framing ("We agree that SA is only a proxy for event completion") is fine. A limitation the reviewer did not ask about is not volunteered (C34).
5. Never mention the score beyond the title; never ask for anything (§ 4).

Worked example (a benchmark paper, 2026-11; concern: "semantic alignment is a proxy for event completion, and the criterion scores still combine event realization with physical plausibility"):

> **THANK YOU FOR CONFIRMING THE ACCEPTANCE RATING**
>
> **Thank you for finding the work suitable for acceptance, and the benchmark and judge useful for advancing physically realistic video generation.**
>
> We agree that SA is only a proxy for event completion. The outcome-information study (Appendix Q) also asked every rater directly whether the described outcome occurred: among the 182 of its 900 videos where a majority answered Yes, 17 (9%) still have at least one law rated below 3, so the law scores also catch physical errors in videos where the event is completed.

The first draft of this reply added a ranking caveat ("too few to re-rank generators on completed videos alone") and a "by design" stance sentence; both were cut by this rule.

## 3. Nudges

VQToken sent three nudge posts aimed at one reviewer plus two to all reviewers within Aug 2–8, most repeating "Do you still have any concerns?". The reviewer replied to the content posts and kept 2. The NeurIPS 2025 PCs reported "reviewers increasing their scores just to end back-and-forth discussion with the authors, but being silent or critical in private discussions with the AC" and attributed it to "reviewer fatigue". ICLR's author guide asks authors to "remain civil and considerate of the reviewers time".

Rules:
- A nudge carries content: one line per point that changed since the reviewer last wrote, plus one question. An empty "any remaining concerns?" post is not a nudge, it is noise.
- At most one nudge per reviewer after ~3 days of silence, and one more 24–48 h before the discussion closes. No other reminders.
- One all-reviewer post at the start ("responses are posted per thread") and none in the middle.

## 4. Score requests

VQToken asked RRqQ, after "this fully addresses all my questions", to "consider increasing your final rating"; the rating stayed at 4.

Rules (user 2026-11-13「不要和他们要分」):
- Never ask a reviewer for a score, in any round: no "we hope the reviewer will reassess the soundness rating", no "we would be grateful if the reviewer would reconsider the score", no conditional "if the additions change your assessment …", no separate post about the score. A closing sentence may hope the answers address the concerns ("We hope these experiments address the reviewer's concerns."), nothing about the rating.
- No appeal to personal stakes ("would mean a great deal to our team and our work's visibility").
- No deference line after a request or closing (user 2026-11-14「However, we fully respect your final judgment. 感觉有点生硬 … 把这句删了吧」): no "However, we fully respect your final judgment", "we respect whatever decision you make", "of course, the final decision is yours". It reads stiff, and "However" sets it against the sentence before it. Delete it, do not reword it; the reply ends on the thanks.
- A co-author's text that already carries a score request is not deleted silently: ask the user. On 2026-11-14 the user kept a co-author's conditional request in a round-2 reply to a reviewer who had confirmed acceptance ("If these additional analyses address your remaining concern, we would be grateful if you could consider increasing your rating in light of the strengthened evidence.").
- Whether a reviewer's score moved is recorded in `REBUTTAL_STATE.md`, never raised in the thread.

## 5. AC closing note

The one place to frame the whole discussion for the AC. VQToken posted an "Author Final Remarks" note; the AC's meta-review followed its framing (outlier reviewer, novelty, "consensus leaned toward borderline accept").

Where:
- NeurIPS: the "Author Final Remarks" field if the year has it; else the AC-only comment.
- ICLR: an official comment on the forum shortly before the discussion closes (ICLR 2027: Nov 18 '26 AoE). Readers: **Area Chairs (+ SACs/PCs)** when it compares reviewers or names an outlier; **public** only if it compares no reviewer. Confirm the readers options in the venue's interface.

Structure (≈ 250–400 words):
1. One line of thanks naming the reviewers who engaged.
2. **What the discussion established** — 2–4 bullets, each a resolved concern with its number ("matched fine-tuning baseline: 57.4 vs 57.7 at 0.14 % tokens").
3. **Reviewer-flagged items, closed** — each in one sentence, stated as fixed and checked, without apology or the word "error" (VQToken: "A single table value flagged by BtRV was traced to a neighboring-column transcription typo … no other discrepancies were found" — drop "typo" under Never concede: "The Table 4 value flagged by BtRV now reads 38.22, verified against the evaluation logs; all other entries match the logs.").
4. **Remaining disagreement**, if any — who raised it, what was answered, and why it does not bear on soundness. VQToken: "were raised only by Gyx4 among the four reviewers, do not impede the precise understanding shown by the other three reviewers". Counts must be true; quote, don't characterize ("no methodological flaws were identified" only if no reviewer named one).
5. Three-line summary of the contribution (problem, method, evidence).

State coverage with confidence (user 2026-11-10: 「要自信, “回答了所有弱点和问题”」): *"Our response answered every weakness and question"*, not a hedge such as "addresses the review point by point". It is true once the coverage gate passes (every W/Q has an A#). A stress tester that calls it an overclaim because some sub-question is only partly answered is overruled; the partial answers are reported to the user, not hedged in the note.

Never in the closing note:
- Anything the public threads did not already contain (no new results only the AC sees).
- Accusations; if a review is reportable, that goes in its own note ([misconduct-reporting.md](misconduct-reporting.md)).
- Promises not tracked in `REVISION_PLAN.md`.

## 6. After every round

- Update `REVISION_PLAN.md` in place (new items, ticks, statuses).
- Re-run the Phase 5 lints on the new reply.
- Record round, posting time and any reviewer score/acknowledgement in `REBUTTAL_STATE.md`.

## 7. Co-author comments on the shared draft

Moved to [collaboration.md](collaboration.md): ownership of text (§ 1), co-author version vs ours (§ 2), checking against the source (§ 3), marking (§ 4), sync direction (§ 5), comments and suggestions (§ 6), safe edits (§ 7).
