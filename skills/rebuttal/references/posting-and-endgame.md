# Posting and endgame

Read at Phase 7 (posting) and before the closing note (§ 2). Replies to reviewer comments that arrive after round 1 is posted: [round2-replies.md](round2-replies.md).
Rhetoric rules: [rhetoric.md](rhetoric.md). Reports on bad-faith reviews: [misconduct-reporting.md](misconduct-reporting.md).

## 1. Posting order

Post one reviewer at a time, positive-score reviewers first; they usually confirm and then stop moving. Difficult negative-score reviewers go last (Phase 3 step 8, 「先一个一个回复，看正分审稿人愿不愿意confirm，他们一般confirm之后就不动了. 然后麻烦的负分先留到最后」). The board and collaborator doc use the same order from the start, highest score first (user 2026-11-12「下次应该把高分的放前面」).

About 24 h after the round-1 replies are up, post the all-reviewer thank-you ([round2-replies.md](round2-replies.md) § 8), then the individual nudges in the same order, one reviewer per post, one nudge each; a silent positive-score reviewer is left alone, a silent negative-score one is raised with the AC last and, in the last days before the discussion closes, nudged again 24 h after its previous nudge, the last such reviewer with a short confidential AC note posted alongside (§ 6 there).

## 2. Closing note, before the discussion closes

User 2026-11-17:「rebuttal 关闭之前, 要感谢AC和正分reviewer, 你要写个summarize倒是真的」. Every rebuttal ends with a public thank-you that also summarizes the discussion (§ 2a), a separate thank-you in the thread of each positive-score or score-raising reviewer (§ 2c), plus a confidential closing message to the AC (§ 2b) whenever some reviewer has not confirmed a positive rating.

When: in the last 24 h before the discussion closes (ICLR 2027: Nov 18 '26 AoE), after the last reply we expect to send, so nothing of ours follows it. All are drafts for the user to post; never post them. Record the posting time in `REBUTTAL_STATE.md`.

Where:
- ICLR: official comments on the forum. § 2a and § 2c readers **everyone**; § 2b readers **Area Chairs (+ SACs/PCs)**, since it compares reviewers. Confirm the readers options in the venue's interface.
- NeurIPS: the "Author Final Remarks" field if the year has it (one field: § 2a first, then § 2b); else AC-only comments.

### 2a. Thank-you and summary (every rebuttal, public)

Title (OpenReview Title field, Title Case, no `**`): `Thank You to the Area Chair and All Reviewers`

Shape (≈ 150–300 words):
1. `Dear Area Chair and Reviewers,`
2. **Bold thanks** to the AC and all reviewers as the discussion closes: their time, guidance and constructive feedback, with an exclamation mark.
3. **Summary.** One sentence that the discussion improved the clarity and rigor of the work; one that we addressed all the concerns (coverage stated with confidence, below) and, only if a revision was uploaded, updated the manuscript accordingly; then 2–4 bullets, each a concern the discussion resolved, in one line with the number or table the thread already gave ("matched fine-tuning baseline: <ours> vs <theirs> at <budget>"). A reviewer-flagged item that was fixed is stated as fixed and checked, without apology or the word "error" ("The Table <n> value flagged by a reviewer now reads <v>, verified against the evaluation logs; all other entries match the logs."). Then one sentence on the contribution, in the words reviewers used for its strengths.
4. Close: we hope our responses clarified the remaining questions, thanks again, and our commitment to the field, with an exclamation mark.
5. `Best regards,` / `The Authors`

No reviewer is named here; each one is thanked in their own thread (§ 2c).

Template (user's model, 2026-11-17; fill the angle brackets, keep the rest):

> Dear Area Chair and Reviewers,
>
> **As the discussion period comes to a close, we would like to express our sincere gratitude to you all for your valuable time, excellent guidance, and constructive feedback!**
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

中文对照：尊敬的领域主席和各位审稿人：**讨论期即将结束，衷心感谢各位宝贵的时间、出色的指导和建设性的意见！**讨论大大提升了我们工作的清晰度和严谨性。我们已尽全力回应了所有问题<并相应更新了论文>。总结如下：<已解决的问题 1–3>。我们很高兴构建了 <贡献，一句话>。希望我们的回复澄清了余下的问题。再次感谢各位的辛勤付出，我们将继续为 <领域> 社区贡献力量！此致，全体作者

State coverage with confidence (user 2026-11-10: 「要自信, “回答了所有弱点和问题”」): "We have addressed all the concerns", not a hedge such as "addresses the review point by point". It is true once the coverage gate passes (every W/Q has an A#). A stress tester that calls it an overclaim because some sub-question is only partly answered is overruled; the partial answers are reported to the user, not hedged in the note.

### 2b. Confidential closing message to the AC

User 2026-11-17:「AC confidential message: 先写感谢AC，然后黑体一大堆 写有哪些问题，然后我们rebuttal的进度是啥样，哪些reviewer support我们，然后剩下的reviewer你要说清楚 不回复 还是 有问题 有错误啥的，我们做了一堆觉得尽可能解决了但是他们不回复。或者他们有问题，事实错误还是啥 然后你要给ac说不赞成反对意见也要说清楚为啥不赞成，然后我们做了啥 最后再感谢一次」.

The one place to frame the whole discussion for the AC, readers Area Chairs (+ SACs/PCs). Draft it whenever at least one reviewer has not confirmed a positive rating; if every reviewer is a confirmed positive, § 2a is enough. It does not replace the per-reviewer AC notes already sent ([round2-replies.md](round2-replies.md) § 6, [misconduct-reporting.md](misconduct-reporting.md)); it closes them, citing their dates instead of repeating them.

**No rating tag after a reviewer's ID in anything sent to the AC** (user 2026-11-19「以后给ac的 不要 有(rating ， 这次就报错了」). Write `Reviewer <ID>`, never `Reviewer <ID> (rating 2)`, `(2: Weak Reject)` or `(<rating>, confidence <c>)`; this holds for this message, the per-reviewer AC notes ([round2-replies.md](round2-replies.md) § 6) and the misconduct note ([misconduct-reporting.md](misconduct-reporting.md) § 4). The AC reads every rating in the forum, and a tag copied from the draft is false the moment the reviewer changes the score. A rating appears in only two places: a raise ("raised the rating from <a> to <b>"), and the complaint sentence of the engagement note that sets the review's own strengths against its score ("yet still rates the paper <r> (<label>)", [round2-replies.md](round2-replies.md) § 6). A kept score is not stated, and a reviewer's "maintain a Weak Accept"-style sentence is not quoted (user 2026-11-19「不好听不要」); quote what the reviewer wrote about the paper or the rebuttal instead. Right before the user posts any AC note, reload the forum and check every "has not responded" and every score in the draft against it; if a reviewer has replied since the draft, that paragraph is rewritten first.

Structure, in this order:
1. **Thank the AC**, one or two warm sentences, for handling the submission and guiding the discussion.
2. **The concerns raised, in bold.** One line per concern, the concern itself in bold as a lead-in, then in plain text what we did and the number or table the thread gave ("**Baseline under matched fine-tuning.** We added it (Reviewer A, W1): <ours> vs <theirs> at <budget>."). Group concerns several reviewers share into one line naming all of them. A reviewer-flagged item that was fixed is stated as fixed and checked, never as an error.
3. **Where the rebuttal stands**, in a few sentences: every weakness and question answered (coverage stated with confidence, § 2a), what was added in the discussion (new analyses, a revision if one was uploaded), and how many follow-up rounds took place.
4. **Who supports the paper**: each positive-score reviewer by ID, with a verbatim quote where one confirmed acceptance or wrote that the concerns are addressed. Counts must be true; the AC sees the forum.
5. **Each remaining reviewer, said plainly which case it is**, one short paragraph each:
   - *No reply*: what we did for them (the concerns answered, the analyses added), then that they have not replied, with every date we posted to them ("Reviewer <ID> has not responded to our response of <date> or our follow-ups of <dates>."). We believe the concerns are resolved as far as possible.
   - *Replied, a concern still open*: the concern in their words, what we did, and why we believe it is answered.
   - *A factual error in the review*: the reviewer's verbatim words, what the submission says and where (section, table, line). Stated as fact, never as an accusation.
6. **Where we disagree with an opposing view, say so and why**: the view (quoted), the reason we do not agree (evidence in the paper or the thread, or support from another reviewer, quoted), and what we did about it anyway. Quote, don't characterize ("no methodological flaws were identified" only if no reviewer named one); e.g. that the remaining concerns were raised by one reviewer of four, stated only when the forum shows it.
7. **Thank the AC again**, one warm closing line (no deference line, [round2-replies.md](round2-replies.md) § 7; no signature, [misconduct-reporting.md](misconduct-reporting.md) § 4).

Title (OpenReview Title field, Title Case, no `**`, no submission prefix): `Summary of the Discussion for the Area Chair`

```
Dear Area Chair,

Thank you so much for handling our submission and for guiding the
discussion! <one more sentence of thanks, optional>

The reviews raised the following concerns, all of which we have
addressed:
- **<Concern 1>.** <What we did, with the number or table> (Reviewers <A>, <C>).
- **<Concern 2>.** <...> (Reviewer <B>).
- **<Concern 3>.** <...>

Our responses answer every weakness and question. During the discussion
we added <new analyses> <and uploaded a revision with ...>.

Reviewers <A> and <B> support acceptance;
Reviewer <A> wrote: "<verbatim confirmation>".

Reviewer <C> has not responded to our response of <date> or
our follow-ups of <dates>. We addressed each of the reviewer's concerns:
<one line>. <Or: Reviewer <D>'s W<k> states "<verbatim>"; the submission
reports <fact> in <Section / Table>.>

We respectfully disagree with <the opposing view, quoted>, because
<reason, with evidence or another reviewer's verbatim support>.
Nevertheless, we <what we did>.

Thank you again for your time and efforts in handling our submission!
```

**Shape from the user's reference notes (user 2026-11-18「给你个参考」「更新一下skill」); it supersedes the title, salutation, order and closing of the structure and template above.** The structure's content stays (every concern answered, who supports, each remaining reviewer's case, a stated disagreement where one exists), laid out as:

1. Title (Title Case, no `**`), thanks first, then what the note is: `Thank You for Your Careful Oversight: Final Confidential Summary of Reviewer Assessments and Completed Evidence`. With a meta-review already out: `Final Confidential Rebuttal Summary - Thank You for Your Guidance; Completed Evidence Addressing the Metareview's Central Concern for Your Consideration`.
2. `Dear Area Chair <ID>, SAC, and PC,` (the AC's ID when the forum shows it; otherwise `Dear Area Chair, SAC, and PC,`).
3. **Bold thanks** for the AC's careful oversight and the time devoted to the submission; one sentence of gratitude to all reviewers for strengthening the paper; one sentence that, as the discussion concludes, this is a concise confidential summary of the reviewer record and the completed evidence.
4. **Reviewer assessments.** One bullet per reviewer, bold lead-in `Reviewer <ID>` (no rating tag, see above): a confirmation quoted verbatim where one was posted ("stated: \"…\""), a raised score as "raised the recommendation from <a> to <b>", a proposal we carried out ("proposed …; we ran this experiment in full"). A reviewer who did not reply: its own strengths quoted, what we completed with the dates, each invitation to identify a remaining concern with its date, any earlier AC note by date; then "No response followed." / "No further concern was raised."
5. **No articulated remaining concern**, when no reviewer named one after our last answers: "The discussion record therefore contains no articulated remaining concern. We respectfully ask that the pre-rebuttal objections not be treated as continuing unresolved concerns unless they are supported by the completed post-rebuttal record."
6. **Evidence directly resolving the central concerns** (or "…the metareview's central concerns"): the concerns grouped into two to four numbered central concerns, each a bold claim sentence naming the reviewers who raised it, then the completed evidence with the numbers and appendices the threads gave. Smaller points go in one **Additional evidence** paragraph, the reviewer in brackets after each.
7. **Taken together**: one sentence that the evidence resolves the central concerns and that the positive assessments of the supporting reviewers confirm it, then warm thanks to those reviewers by ID.
8. **The ask, in bold**: that the complete evidence and the reviewer assessments be considered in the final decision, and the hope that resolving the central concerns supports acceptance; thanks again.
9. `Sincerely,` / `Authors of Submission <N>` (this note is signed, unlike the per-reviewer AC notes).

Post it in the last two hours before the discussion closes (user 2026-11-18「等到最后两小时」), after every other post, as an Official Comment with readers Program Chairs, Senior Area Chairs and Area Chairs. Under the venue's comment limit (OpenReview 5,000 characters): cut the Additional evidence paragraph before any central concern.

**A reviewer whose unchanged score contradicts its own post-rebuttal statements** (it wrote that its evaluation increased, or confirmed points, then left the score) gets a separate confidential request in the same window, modelled on the user's second reference. Title: `Confidential Request for Area Chair Attention - Inconsistency Between Reviewer <ID>'s Post-Rebuttal Statements, Absence of Any Articulated Remaining Concern, and Unchanged Rating`. Body: thanks to the AC and all reviewers; the reviewer's positive acknowledgments quoted verbatim; every later question and our answer to it, with dates; our explicit invitations to name a remaining concern, with dates, and that none was named; that the unchanged score is not reconciled with these statements; the request that the unchanged score be weighed against the completed record and that the pre-rebuttal objections not be treated as unresolved unless the post-rebuttal record supports them; thanks for an independent, fair assessment. Only for a reviewer that actually posted such statements; a reviewer that never replied is covered by item 4 of the summary.

### 2c. A thank-you in each supporting reviewer's thread

User 2026-11-17:「然后感谢reviewer的话，你给每个reviewer下单独感谢就行，主要是正分的或者提分的」. Reviewers are thanked one by one, each in their own thread, not by name in § 2a. Who gets one: every reviewer with a positive final rating and every reviewer who raised the score. A negative-score reviewer who stayed silent gets none (their thread ends with the nudges, [round2-replies.md](round2-replies.md) § 6); one who engaged without raising is left to the user's call.

Posted in the same last-24 h window as § 2a, readers everyone. Shape (≈ 60–120 words), wording varied across reviewers:
1. `Dear Reviewer <ID>,`
2. **Bold thanks** for their time and support as the discussion closes, with an exclamation mark; for a score raise, thank them for raising it.
3. One sentence naming what their review improved, concretely (the suggestion or check, quoted or named: "your suggestion to report the matched fine-tuning baseline", "the Figure 2 clarification").
4. One closing line of thanks.
5. `Best regards,` / `The Authors`

No result, no new claim, no rating request, no deference line. Title (Title Case, no `**`): `Thank You for Your Support and Insightful Suggestions` (a raise: `Thank You for Raising Your Rating and for Your Insightful Suggestions`). It does not reuse the wording of an earlier closing reply in the same thread ([round2-replies.md](round2-replies.md) § 4).

### Never in any closing note

- Anything the public threads did not already contain (no new results only the AC sees).
- Accusations (a factual error in a review, stated with the reviewer's words and the paper's location, is not one); if a review is reportable, that goes in its own note ([misconduct-reporting.md](misconduct-reporting.md)).
- Promises not tracked in `REVISION_PLAN.md`.
- Concessions or deference lines (a stated disagreement in § 2b, "We respectfully disagree … because …", is neither) (SKILL.md "Never concede"; [round2-replies.md](round2-replies.md) § 7).
- In § 2a and § 2c, any comparison between reviewers.

## 3. After every round

- Update `REVISION_PLAN.md` in place (new items, ticks, statuses).
- Re-run the Phase 5 lints on the new reply.
- Record round, posting time and any reviewer score/acknowledgement in `REBUTTAL_STATE.md`.

## 4. Co-author comments on the shared draft

Moved to [collaboration.md](collaboration.md): ownership of text (§ 1), co-author version vs ours (§ 2), checking against the source (§ 3), marking (§ 4), sync direction (§ 5), comments and suggestions (§ 6), safe edits (§ 7).
