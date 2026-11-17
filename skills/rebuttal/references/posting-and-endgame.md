# Posting and endgame

Read at Phase 7 (posting) and before the closing note (§ 2). Replies to reviewer comments that arrive after round 1 is posted: [round2-replies.md](round2-replies.md).
Rhetoric rules: [rhetoric.md](rhetoric.md). Reports on bad-faith reviews: [misconduct-reporting.md](misconduct-reporting.md).

## 1. Posting order

Post one reviewer at a time, positive-score reviewers first; they usually confirm and then stop moving. Difficult negative-score reviewers go last (Phase 3 step 8, 「先一个一个回复，看正分审稿人愿不愿意confirm，他们一般confirm之后就不动了. 然后麻烦的负分先留到最后」). The board and collaborator doc use the same order from the start, highest score first (user 2026-11-12「下次应该把高分的放前面」); one rebuttal's board led with the 1-score reviewer and could not be reordered once co-authors were editing it.

About 24 h after the round-1 replies are up, post the all-reviewer thank-you ([round2-replies.md](round2-replies.md) § 8), then the individual nudges in the same order, one reviewer per post, one nudge each; a silent positive-score reviewer is left alone, a silent negative-score one is raised with the AC last and, in the last days before the discussion closes, nudged again 24 h after its previous nudge, the last such reviewer with a short confidential AC note posted alongside (§ 6 there).

VQToken fits this: LjpF acknowledged within three days and ended at 5; RRqQ (4) wrote "this fully addresses all my questions" and stayed at 4; the negative reviewer took the whole period.

## 2. Closing note, before the discussion closes

User 2026-11-17:「rebuttal 关闭之前, 要感谢AC和正分reviewer, 你要写个summarize倒是真的」. Every rebuttal ends with a public thank-you that also summarizes the discussion (§ 2a). A separate AC-only note (§ 2b) is added only when a negative-score reviewer still disagrees and no earlier AC note ([misconduct-reporting.md](misconduct-reporting.md), [round2-replies.md](round2-replies.md) § 6) already made that case.

When: in the last 24 h before the discussion closes (ICLR 2027: Nov 18 '26 AoE), after the last reply we expect to send, so nothing of ours follows it. Both are drafts for the user to post; never post them. Record the posting time in `REBUTTAL_STATE.md`.

Where:
- ICLR: official comments on the forum. § 2a readers **everyone**; § 2b readers **Area Chairs (+ SACs/PCs)**, since it compares reviewers. Confirm the readers options in the venue's interface.
- NeurIPS: the "Author Final Remarks" field if the year has it (one field: § 2a first, then § 2b); else AC-only comments.

### 2a. Thank-you and summary (every rebuttal, public)

Title (OpenReview Title field, Title Case, no `**`): `Thank You to the Area Chair and All Reviewers`

Shape (≈ 150–300 words):
1. `Dear Area Chair and Reviewers,`
2. **Bold thanks** to the AC and all reviewers as the discussion closes: their time, guidance and constructive feedback, with an exclamation mark.
3. **Thanks to the positive-score reviewers by ID**, one sentence: for their support and, where they confirmed it, for confirming acceptance. Name only reviewers whose final rating is positive; say nothing about the others here.
4. **Summary.** One sentence that the discussion improved the clarity and rigor of the work; one that we addressed all the concerns (coverage stated with confidence, below) and, only if a revision was uploaded, updated the manuscript accordingly; then 2–4 bullets, each a concern the discussion resolved, in one line with the number or table the thread already gave ("matched fine-tuning baseline: 57.4 vs 57.7 at 0.14 % tokens"). A reviewer-flagged item that was fixed is stated as fixed and checked, without apology or the word "error" ("The Table 4 value flagged by a reviewer now reads 38.22, verified against the evaluation logs; all other entries match the logs."). Then one sentence on the contribution, in the words reviewers used for its strengths.
5. Close: we hope our responses clarified the remaining questions, thanks again, and our commitment to the field, with an exclamation mark.
6. `Best regards,` / `The Authors`

Template (user's model, 2026-11-17; fill the angle brackets, keep the rest):

> Dear Area Chair and Reviewers,
>
> **As the discussion period comes to a close, we would like to express our sincere gratitude to you all for your valuable time, excellent guidance, and constructive feedback!** We are especially grateful to Reviewers <IDs of the positive-score reviewers> for their support <and for confirming acceptance>.
>
> The discussion has significantly helped us improve the clarity and rigor of our work. We have addressed all the concerns with our best efforts <and updated the manuscript accordingly>. In summary:
>
> - <resolved concern 1, one line with its number or table>
> - <resolved concern 2>
> - <resolved concern 3>
>
> We are pleased to have developed <the contribution, in one sentence: what it is and the two or three strengths reviewers recognized>.
>
> We hope our responses have clarified the remaining questions. Thank you again for your hard work, and we are devoted to further contributing to the <field> community!
>
> Best regards,
> The Authors

中文对照：尊敬的领域主席和各位审稿人：**讨论期即将结束，衷心感谢各位宝贵的时间、出色的指导和建设性的意见！** 特别感谢审稿人 <正分审稿人> 的支持<并确认接收>。讨论大大提升了我们工作的清晰度和严谨性。我们已尽全力回应了所有问题<并相应更新了论文>。总结如下：<已解决的问题 1–3>。我们很高兴构建了 <贡献，一句话>。希望我们的回复澄清了余下的问题。再次感谢各位的辛勤付出，我们将继续为 <领域> 社区贡献力量！此致，全体作者

State coverage with confidence (user 2026-11-10: 「要自信, “回答了所有弱点和问题”」): "We have addressed all the concerns", not a hedge such as "addresses the review point by point". It is true once the coverage gate passes (every W/Q has an A#). A stress tester that calls it an overclaim because some sub-question is only partly answered is overruled; the partial answers are reported to the user, not hedged in the note.

### 2b. AC-only note on a remaining disagreement (only when needed)

The one place to frame the whole discussion for the AC. VQToken posted an "Author Final Remarks" note; the AC's meta-review followed its framing (outlier reviewer, novelty, "consensus leaned toward borderline accept"). It does not repeat § 2a's thanks or summary.

Structure (≈ 150–300 words):
1. **Remaining disagreement** — who raised it, what was answered, and why it does not bear on soundness. VQToken: "were raised only by Gyx4 among the four reviewers, do not impede the precise understanding shown by the other three reviewers". Counts must be true; quote, don't characterize ("no methodological flaws were identified" only if no reviewer named one).
2. The positive-score majority, by ID and final rating, only if it is a majority.
3. One warm closing line (no deference line, [round2-replies.md](round2-replies.md) § 7).

### Never in either note

- Anything the public threads did not already contain (no new results only the AC sees).
- Accusations; if a review is reportable, that goes in its own note ([misconduct-reporting.md](misconduct-reporting.md)).
- Promises not tracked in `REVISION_PLAN.md`.
- Concessions or deference lines (SKILL.md "Never concede"; [round2-replies.md](round2-replies.md) § 7).
- In § 2a, any comparison between reviewers.

## 3. After every round

- Update `REVISION_PLAN.md` in place (new items, ticks, statuses).
- Re-run the Phase 5 lints on the new reply.
- Record round, posting time and any reviewer score/acknowledgement in `REBUTTAL_STATE.md`.

## 4. Co-author comments on the shared draft

Moved to [collaboration.md](collaboration.md): ownership of text (§ 1), co-author version vs ours (§ 2), checking against the source (§ 3), marking (§ 4), sync direction (§ 5), comments and suggestions (§ 6), safe edits (§ 7).
