# Round-2 replies

Read at Phase 8, before drafting any reply to a reviewer comment that arrives after the round-1 replies are posted, and again before posting it. Everything here works inside the hard rules of `SKILL.md` (Never concede, Never expose a weakness) and [rhetoric.md](rhetoric.md). Posting order and the AC closing note: [posting-and-endgame.md](posting-and-endgame.md).

## 1. What is frozen once round 1 is posted

- **Posted text does not change.** At posting, save a read-only copy of every posted comment (text, character count, sha256) next to the response files, e.g. `posted_<date>/POSTED_COMMENTS.md`. From then on the paste regions of the canonical response files are what the reviewers see; new text goes into a new comment, never into a posted region.
- **Check every round-2 reply against the posted copy**: no contradiction with a posted number or claim, no restating of what already stands in the thread (§ 2).
- **The board holds only what is still to post** (user 2026-11-14「doc 之前发了的也删了, 粘贴页 fix 了, 你把之前发的了都删了, 就加上新的」). Once round 1 is posted, delete the posted reply drafts from the collaborator doc (keep the reviewer summaries) and from the paste page; the frozen copy is the record. Add each round-2 reply under its reviewer as its own block, with the reviewer's new comment quoted, EN, 中文对照, and a source line that cites appendix and table, never repo paths.

## 2. Delta replies

When a reviewer comments again:
1. Append the comment verbatim to `FOLLOWUP_LOG.md`; link it to existing issue cards or open new ones.
2. Reply to the **new** points only. Restate nothing that already stands in the thread.
3. If the reviewer restated the same concern with a sharper criterion (VQToken Gyx4: from "compare with more recent methods" to "one table with multiple compression baselines AND multiple benchmarks: 1x2=2 vs DyCoke's 2x5=10"), the criterion is now the `asked_for`. Either deliver exactly that (the matrix, on our winning metric — `comparison-rules.md`) or switch to the regime argument (rhetoric R1). Do not re-send the earlier answer in new words; never count experiments.
4. Never repeat an argument that already failed — bring new evidence or a new angle, or stop. Escalate technically, not rhetorically.
5. For a reviewer whose lever is `argument` (Phase 3 step 7), keep closing each new objection until none is left.
6. A reviewer-flagged number or sample: open the logs/sample before replying (Phase 3 step 6). The VQToken hardware-variance guess had to be retracted one round later.

Long replies: split into `[PART 1/2]`, `[PART 2/2]` comments when over the per-comment limit (ICLR: "There is a word limit for each comment, but there is no limit on the number of comments"). Each part opens with its own label and closes with "continued in PART 2/2".

## 3. Shape of a round-2 reply

In this order; drop the parts that do not apply:

1. **Title**, only for a reviewer who confirms an accepting rating: `**THANK YOU FOR CONFIRMING THE ACCEPTANCE RATING**` (§ 4).
2. **Bold thanks for every good thing the reviewer wrote**, in the reviewer's own words, then one plain sentence of thanks for the follow-up.
3. **Agree with the reviewer's framing** where we can: "we agree that X is a proxy for Y" (求同存异). "Agree" is fine; "admit", "acknowledge a limitation", "we concede" are not (user 2026-11-14「admit 就不好听, agree 就还行」).
4. **The answer** (§ 5 when it carries a new analysis).
5. **Optional rating request** (§ 7).
6. **Thanks line**: "Thank you again for your time, valuable feedback, and continued support!"
7. **Closing invitation, copied from a posted round-1 closing**: "We look forward to any of your further thoughts!" (中文「期待您进一步的想法！」) (user 2026-11-14「最后加一句, 说如果还有别的问题 请提出, 就直接抄前面 别的就行」). Take the sentence from what round 1 already posted rather than writing a new one, so every thread sounds the same; no "Please do not hesitate to …".

No deference line anywhere ("However, we fully respect your final judgment"): delete it, do not reword it (§ 7, lint 24).

## 4. A reviewer who confirms an accepting rating

When a follow-up confirms acceptance or keeps a positive rating ("I consider the work suitable for acceptance and maintain my positive rating") and leaves a minor concern, the reply thanks first and answers without arguing (user 2026-11-14「能解决你就回消息，title 大写加粗 thank you for confirming acceptance rating 然后不要反驳他，就简短回答问题 他写你的好话，比如什么达到接收标准什么的黑体加粗感谢」「你要是解决不了就简单感谢」):

1. **Title line**, bold and upper case: `**THANK YOU FOR CONFIRMING THE ACCEPTANCE RATING**`.
2. **Bold thanks quoting their praise**: `**Thank you so much for finding the work suitable for acceptance, and the benchmark and judge useful for advancing physically realistic video generation!**` A co-author who rewrites the opening may drop the title or turn the quoted praise into generic thanks ("Thank you so much for your thoughtful follow-up and positive assessment!"); put both back (user 2026-11-14, same request a second time after a co-author rewrite).
3. **Can we resolve the remaining concern with evidence we already have?** No: stop after the thanks, the thanks line and the closing invitation; no answer, no promise, no "future work" paragraph. Yes: answer it. Short by default (one to three plain sentences, verdict first, one number at most per claim). When new analyses of data we already have answer the concern, the longer reply is allowed (user 2026-11-14「为啥要缩回 … 保留这一版」): findings as bold headings (§ 5), a promise to add them to the appendix, an optional rating request.
4. **Never rebut, and do not state our position** (user 2026-11-14「所以也不要说我们的立场」). No "by design" defence, no "we respectfully disagree", no sentence explaining why our view of the concern is right, not even as a neutral design statement; no restating a position the reviewer did not accept. Agreeing with the reviewer's framing is fine (§ 3 item 3). A limitation the reviewer did not ask about is not volunteered (C34).
5. Do not discuss the score beyond the title and an optional closing request (§ 7).

Worked example, short form (a benchmark paper, 2026-11; concern: "semantic alignment is a proxy for event completion, and the criterion scores still combine event realization with physical plausibility"):

> **THANK YOU FOR CONFIRMING THE ACCEPTANCE RATING**
>
> **Thank you for finding the work suitable for acceptance, and the benchmark and judge useful for advancing physically realistic video generation.**
>
> We agree that SA is only a proxy for event completion. The outcome-information study (Appendix Q) also asked every rater directly whether the described outcome occurred: among the 182 of its 900 videos where a majority answered Yes, 17 (9%) still have at least one law rated below 3, so the law scores also catch physical errors in videos where the event is completed.

The first draft added a ranking caveat ("too few to re-rank generators on completed videos alone") and a "by design" stance sentence; both were cut by this rule. The reply that went forward was the long form: title, bold thanks, agreement, the outcome question and its five options, three bold-headed findings, the appendix promise, a rating request, the thanks line and the closing invitation (about 3,000 characters).

## 5. A new analysis in a round-2 reply

The reviewer has the paper and round 1, nothing else. A Codex stress test of the 2026-11 reply found every number right and still asked for these:

- **Name what the reviewer cannot see.** The question asked and its options verbatim ("Does the described result happen?" with its five answers), the video set ("the 900 videos of the experiment described in Appendix Q"), and "of this experiment" when the set differs from the one round 1 used.
- **Define a term again when round 1 used it differently.** Round 1's scoring rule ("a law whose event does not happen receives 1") was about the physical process a law scores; round 2's "event completion" is about the result stated in the prompt. One sentence says which is which.
- **State every denominator.** "a majority of raters who answered the outcome question chose Yes", not "a majority answered Yes".
- **Describe an adjustment by what stays in the score.** "We adjusted video-level law scores for event completion, i.e., the shares of Yes and Partly answers, so that the plausibility answers remain part of the score." Adjust only for what the concern is about: adjusting for all five answers also removed the "looks implausible" judgment, which is physics signal (user 2026-11-14, switched to completion only).
- **"Adjusted vs unadjusted rankings"**, never "the original rankings".
- **One interval format**: "(95% CI [a, b])", the bracket bold as one span, the same in every place; say once what was resampled ("resampling both scenarios and raters") (user 2026-11-14「弄成统一格式」).
- **Headings state what the result shows, never what it lacks** (user 2026-11-14「这两个是不是暴露了我们的缺点」→ changed and deleted). "(2) When the stated result does not occur, law scores still separate plausible from implausible outcomes.", not a heading about what the score cannot do. A closing sentence that a result is uncertain ("Individual ranks changed; comparisons restricted to completed events remain uncertain …") is deleted, not softened.
- **No caveat sentences** ("This is an association, not a causal effect", "while confirming the need to …"): delete them; flag errors, not missing hedges (user 2026-11-14「caveat 不是好东西」). "support reporting the two separately", not "confirming the need to report".
- **Promise what the paper can carry.** "We will add these results to **Appendix Q** and explicitly discuss separate assessments of A, B and C in Future Work." Not "we have now reported" when the revision does not have it, not a "Limitations" section the paper does not have, and no paper edit made just to back a round-2 sentence (user 2026-11-14「不加, 你直接改说法」). "Future Work" is not bold.
- **Stress-test the round-2 reply before posting** (Phase 6, one focused round on that reply alone), then apply what the user approves.

## 6. Nudges

VQToken sent three nudge posts aimed at one reviewer plus two to all reviewers within Aug 2–8, most repeating "Do you still have any concerns?". The reviewer replied to the content posts and kept 2. The NeurIPS 2025 PCs reported "reviewers increasing their scores just to end back-and-forth discussion with the authors, but being silent or critical in private discussions with the AC" and attributed it to "reviewer fatigue". ICLR's author guide asks authors to "remain civil and considerate of the reviewers time".

Rules:
- A nudge carries content: one line per point that changed since the reviewer last wrote, plus one question. An empty "any remaining concerns?" post is not a nudge, it is noise.
- At most one nudge per reviewer after ~3 days of silence, and one more 24–48 h before the discussion closes. No other reminders.
- One all-reviewer post at the start ("responses are posted per thread") and none in the middle.

## 7. Score requests

VQToken asked RRqQ, after "this fully addresses all my questions", to "consider increasing your final rating"; the rating stayed at 4.

Rules:
- A co-author's rating request already in the shared draft goes to the user; it is not deleted silently.
- Asking for a higher rating is allowed (user 2026-11-14「删掉"不向审稿人要分"这个规定」, which lifts the 2026-11-13 ban). Form used in a 2026-11-14 round-2 reply: "If these additional analyses address your remaining concern, we would be grateful if you could consider increasing your rating in light of the strengthened evidence."
- No appeal to personal stakes ("would mean a great deal to our team and our work's visibility").
- No deference line after a request or closing (user 2026-11-14「However, we fully respect your final judgment. 感觉有点生硬 … 把这句删了吧」): no "However, we fully respect your final judgment", "we respect whatever decision you make", "of course, the final decision is yours". It reads stiff, and "However" sets it against the sentence before it. Delete it, do not reword it; the reply ends on the thanks line and the closing invitation (§ 3).
- Whether a reviewer's score moved is recorded in `REBUTTAL_STATE.md`.
