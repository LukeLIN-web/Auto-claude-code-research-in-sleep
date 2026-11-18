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

In this order; drop the parts that do not apply. The closing reply to a reviewer already asked for a higher rating (§ 4) has its own two-sentence shape instead.

1. **Title**, only for a reviewer who confirms an accepting rating: `Thank You for Confirming the Acceptance Rating` (§ 4), in the OpenReview Title field, not in the body.
2. **Bold thanks for every good thing the reviewer wrote**, in the reviewer's own words, then one plain sentence of thanks for the follow-up.
3. **Agree with the reviewer's framing** where we can: "we agree that X is a proxy for Y" (求同存异). "Agree" is fine; "admit", "acknowledge a limitation", "we concede" are not (user 2026-11-14「admit 就不好听, agree 就还行」).
4. **The answer** (§ 5 when it carries a new analysis).
5. **Rating request, followed by an invitation to ask more**, in the same paragraph (pick the request from the forms in § 7; one request per reviewer for the whole discussion, so leave it out once this reviewer has been asked): "If these additional analyses address your remaining concern, we would be grateful if you could consider increasing your rating in light of the strengthened evidence. If you have any further questions, please let us know, and we will address them." (中文「如果您还有其他问题，请告诉我们，我们会进一步解决。」) (user 2026-11-14「应该写在这里 "…恳请您考虑据此提高评分。if you have any further questions. 请进一步让我们知道 我们可以解决."」). To a negative-score reviewer, the request is replaced by "Could you kindly let us know whether our responses have addressed your concerns?" until they write that their concerns are resolved (§ 6 item 6, § 7 form 6). The invitation goes right after the request, not at the very end; without a rating request it still goes before the thanks line. It says we will address the questions, not just that we look forward to thoughts (an earlier "We look forward to any of your further thoughts!" at the end was moved here and reworded).
6. **Thanks line**, last: "Thank you again for your time, valuable feedback, and continued support!"

No deference line anywhere ("However, we fully respect your final judgment"): delete it, do not reword it (§ 7, lint 24).

## 4. A reviewer who confirms an accepting rating

**Already asked for a higher rating (§ 7) and the score did not move: the closing reply.** Post it and nothing more to that reviewer; the next nudge goes to another reviewer (§ 6) (user 2026-11-15「第二轮问了一次, 不加分, 别催了 … 换个人 你两句话感谢他的专业判断，标题里写thank you so much for confirmation of acceptance and professional and insightful suggestions 拍彩虹屁 标题是为了黑体加粗一眼能让AC和其他审稿人看到 … 不要解释了就纯夸 … 不要过长 … 主要意思就让ac看到这里没问题他愿意champion你」). The reply is written for the AC and the other reviewers: the bold title tells them at a glance that this reviewer stands behind acceptance and nothing is open in this thread.

- Title (OpenReview Title field, Title Case, no `**`): `Thank You So Much for Confirming Acceptance and for Your Professional and Insightful Suggestions`
- Body: two sentences of pure praise, thanking their professional judgment. Nothing else: no answer to a point the reviewer still raised, no explanation, no second rating request, no invitation to ask more, no thanks line, no deference line.

> **Thank you so much for confirming that our paper is suitable for acceptance!** We sincerely appreciate your professional judgment and insightful suggestions, which have made our paper much stronger.

中文对照：**非常感谢您确认我们的论文达到接收标准！** 我们由衷感谢您专业的判断和富有洞见的建议，它们让我们的论文更加完善。

**Otherwise** — a follow-up that confirms acceptance or keeps a positive rating ("I consider the work suitable for acceptance and maintain my positive rating") and leaves a minor concern, from a reviewer not yet asked for a higher rating — the reply thanks first and answers without arguing (user 2026-11-14「能解决你就回消息，title 大写加粗 thank you for confirming acceptance rating 然后不要反驳他，就简短回答问题 他写你的好话，比如什么达到接收标准什么的黑体加粗感谢」「你要是解决不了就简单感谢」):

1. **Title**, Title Case, plain text in the OpenReview comment's Title field: `Thank You for Confirming the Acceptance Rating`. OpenReview bolds the title itself, so no `**`; not upper case (reads as shouting; user 2026-11-14「全大写会不会不好看」→「改.」「openreview 标题不需要 **, 自动会加粗.」). The body starts with the bold thanks. The paste page gives the title its own copy button.
2. **Bold thanks quoting their praise**: `**Thank you so much for finding the work suitable for acceptance, and the benchmark and judge useful for advancing physically realistic video generation!**` A co-author who rewrites the opening may drop the title or turn the quoted praise into generic thanks ("Thank you so much for your thoughtful follow-up and positive assessment!"); put both back (user 2026-11-14, same request a second time after a co-author rewrite).
3. **Can we resolve the remaining concern with evidence we already have?** No: stop after the thanks, the invitation to ask more and the thanks line; no answer, no promise, no "future work" paragraph. Yes: answer it. Short by default (one to three plain sentences, verdict first, one number at most per claim). When new analyses of data we already have answer the concern, the longer reply is allowed (user 2026-11-14「为啥要缩回 … 保留这一版」): findings as bold headings (§ 5), a promise to add them to the appendix, an optional rating request.
4. **Never rebut, and do not state our position** (user 2026-11-14「所以也不要说我们的立场」). No "by design" defence, no "we respectfully disagree", no sentence explaining why our view of the concern is right, not even as a neutral design statement; no restating a position the reviewer did not accept. Agreeing with the reviewer's framing is fine (§ 3 item 3). A limitation the reviewer did not ask about is not volunteered (C34).
5. Do not discuss the score beyond the title and an optional closing request (§ 7), which is this reviewer's one request.

**Thanks-only form** — the "No" branch of item 3: the reviewer keeps an accepting rating, lists reservations we have no new evidence for, and asks nothing (user 2026-11-16「回一个感谢」, then「怎么就写了这么点, 她不是有Critical Strengths …吗」「也不要废话太多 太细节」). Four short paragraphs:

1. `Dear Reviewer <ID>,` then the bold thanks quoting the praise in the follow-up itself (e.g. "thorough", "meaningful experiments rather than simply providing explanations") and the kept rating; one plain sentence thanking the follow-up.
2. **One sentence thanking the strengths of the original review** (its Strengths section), in the reviewer's own words, as a list of three or so items. A thanks that covers only the follow-up is too thin. No numbers, no table / figure / appendix addresses, no benchmark-by-benchmark detail: the AC needs to see that the reviewer praised the work, not the evidence again.
3. Professional-judgment thanks, one sentence that the suggestions made the paper stronger, then the invitation to ask more.
4. The thanks line.

Leave out: any mention of the reservations (not even "we respect your reservations", which concedes and is a deference line, lint 24); a praised strength whose restatement brings back a cost or a weak result the reviewer still holds against us (e.g. "honest about cost", "reports null results" when efficiency is a kept reservation); a quantifier from the praise that implies the opposite case ("gains across *most* categories", "addresses *most* concerns"); a list of the reviewer's suggestions by name; the rating request (§ 7: keep the one request for a reply that closes a concern).

> Title: Thank You for Confirming the Acceptance Rating
>
> Dear Reviewer X,
>
> **Thank you so much for finding our rebuttal thorough, for recognizing that we reported meaningful experiments rather than simply providing explanations, and for maintaining your rating in support of acceptance!** We are very grateful for your thoughtful follow-up.
>
> We are also deeply grateful for the strengths you highlighted in your review: our evaluations and the choice of suitable, compatible baselines for comparison, the significant gains at hour scale where bounded per-pass context is genuinely useful, and our informative diagnostic analyses.
>
> We sincerely appreciate your careful and professional judgment throughout the review and discussion process. Your precise suggestions have made our evidence more complete and our paper stronger. If you have any further questions, please let us know, and we will address them.
>
> Thank you again for your time, valuable feedback, and continued support!

Worked example, short form (a benchmark paper, 2026-11; concern: "semantic alignment is a proxy for event completion, and the criterion scores still combine event realization with physical plausibility"):

> Title: Thank You for Confirming the Acceptance Rating
>
> **Thank you for finding the work suitable for acceptance, and the benchmark and judge useful for advancing physically realistic video generation.**
>
> We agree that SA is only a proxy for event completion. The outcome-information study (Appendix Q) also asked every rater directly whether the described outcome occurred: among the 182 of its 900 videos where a majority answered Yes, 17 (9%) still have at least one law rated below 3, so the law scores also catch physical errors in videos where the event is completed.

The first draft added a ranking caveat ("too few to re-rank generators on completed videos alone") and a "by design" stance sentence; both were cut by this rule. The reply that went forward was the long form: title, bold thanks, agreement, the outcome question and its five options, three bold-headed findings, the appendix promise, a rating request with the invitation to ask more, and the thanks line (about 3,000 characters).

## 5. A new analysis in a round-2 reply

The reviewer has the paper and round 1, nothing else. A Codex stress test of the 2026-11 reply found every number right and still asked for these:

- **Name what the reviewer cannot see.** The question asked and its options verbatim ("Does the described result happen?" with its five answers), the video set ("the 900 videos of the experiment described in Appendix Q"), and "of this experiment" when the set differs from the one round 1 used.
- **Define a term again when round 1 used it differently.** Round 1's scoring rule ("a law whose event does not happen receives 1") was about the physical process a law scores; round 2's "event completion" is about the result stated in the prompt. One sentence says which is which.
- **State every denominator.** "a majority of raters who answered the outcome question chose Yes", not "a majority answered Yes".
- **Describe an adjustment by what stays in the score.** "We adjusted video-level law scores for event completion, i.e., the shares of Yes and Partly answers, so that the plausibility answers remain part of the score." Adjust only for what the concern is about: adjusting for all five answers also removed the "looks implausible" judgment, which is physics signal (user 2026-11-14, switched to completion only).
- **"Adjusted vs unadjusted rankings"**, never "the original rankings".
- **One interval format**: "(95% CI [a, b])", the same in every place; say once what was resampled ("resampling both scenarios and raters") (user 2026-11-14「弄成统一格式」).
- **Bold only the title, the thanks, the finding headings and the headline numbers.** Not the data description ("direct outcome judgments collected for all 900 videos"), not the appendix named in a promise ("Appendix Q"), and never an interval: "**0.54 points** (95% CI [0.23, 0.90])", "**Spearman ρ = 0.97** for explicit prompts (95% CI [0.63, 0.98])" (user 2026-11-14「加粗 95% CI [0.23, 0.90] 没必要, **direct outcome judgments …** 没必要, Appendix Q 没必要」, then「they lose the bold too」for the other two intervals). Unbold the same spans in the 中文对照.
- **Headings state what the result shows, never what it lacks** (user 2026-11-14「这两个是不是暴露了我们的缺点」→ changed and deleted). "(2) When the stated result does not occur, law scores still separate plausible from implausible outcomes.", not a heading about what the score cannot do. A closing sentence that a result is uncertain ("Individual ranks changed; comparisons restricted to completed events remain uncertain …") is deleted, not softened.
- **No caveat sentences** ("This is an association, not a causal effect", "while confirming the need to …"): delete them; flag errors, not missing hedges (user 2026-11-14「caveat 不是好东西」). "support reporting the two separately", not "confirming the need to report".
- **Promise what the paper can carry.** "We will add these results to **Appendix Q** and explicitly discuss separate assessments of A, B and C in Future Work." Not "we have now reported" when the revision does not have it, not a "Limitations" section the paper does not have, and no paper edit made just to back a round-2 sentence (user 2026-11-14「不加, 你直接改说法」). "Future Work" is not bold.
- **A method the reviewer asks for that cannot be run in full: give the reason, as facts the AC can check** (user 2026-11-16「也要解释一下啊, <X> 为啥不能完整复现, 理由讲出来」). Say what its public code releases and what it does not, and which components use closed models (with the paper section), then build the closest version on the shared backbone and name, stage by stage, what stands in for each missing or closed component ("in place of the meta-agent"). This is the reason for the substitution, not a caveat sentence, so the no-caveat rule above does not remove it. Read the repository's file tree on the day the reply is written: a session note saying a repository held "only data and metrics" was wrong, as its retrieval and agent code were there.
- **Our complete code release is the contrast** (user 2026-11-16「这也算是我们的优势, 我们会开源完整的代码」). When the requested method's release is partial, the same paragraph states "We will release <our method>'s complete code." right after the reason. This is a promise, so it goes in only when the user has approved it.
- **Stress-test the round-2 reply before posting** (Phase 6, one focused round on that reply alone), then apply what the user approves.

## 6. Nudges

VQToken sent three nudge posts aimed at one reviewer plus two to all reviewers within Aug 2–8, most repeating "Do you still have any concerns?". The reviewer replied to the content posts and kept 2. The NeurIPS 2025 PCs reported "reviewers increasing their scores just to end back-and-forth discussion with the authors, but being silent or critical in private discussions with the AC" and attributed it to "reviewer fatigue". ICLR's author guide asks authors to "remain civil and considerate of the reviewers time". Hence one nudge per reviewer, never a series; the one exception is a negative-score reviewer still silent in the last days before the discussion closes (item 6).

The sequence (user 2026-11-15「你先发个全体message显示你催过了 然后一个一个单独发 催正分的让他们confirm … 一次发一个 半天看一次 如果正分不回复不管他 … 负分不回复 催AC」):

1. **All reviewers first.** The all-reviewer thank-you (§ 8) goes up before any individual nudge. It asks every reviewer for remaining concerns, so it is also the visible record that everyone was nudged. The only other all-reviewer post is a general response posted with round 1, if the rebuttal has one.
2. **Then one reviewer per post**, in the posting order (highest score first, negative-score reviewers last; [posting-and-endgame.md](posting-and-endgame.md) § 1), a few hours apart (user「你等几个小时换一个审稿人问下」). Check the forum about every half day, and answer whatever came in before the next nudge goes up.
3. **One nudge per reviewer.** A reviewer who does not answer it gets no second one, except a negative-score reviewer in the last days before the discussion closes (item 6: another nudge after 24 h of silence).
4. **The nudge to a positive-score reviewer asks them to confirm.** It thanks them for the positive rating in support of acceptance and for their insightful suggestions, says we are committed to resolving all of their concerns, and asks whether any remain. Polite, and no rating request (user「委婉点，问很感谢他们的insightful suggesting我们致力于解决他们所有问题，问他们有没有remaining concerns」「你催的时候写清楚感谢他们正分支持接受」):

   Title (OpenReview Title field, Title Case, no `**`): `Thank You for Supporting the Acceptance of Our Paper`

   > **Thank you so much for your positive rating in support of accepting our paper, and for your insightful suggestions! We are especially grateful that you found <strength 1>, <strength 2>, and <strength 3>.**
   >
   > We are fully committed to resolving all of your concerns. Could you kindly let us know whether you have any remaining concerns? We would be glad to address them.
   >
   > Thank you again for your time and valuable feedback!

   The second bold sentence restates the review's own strengths field (e.g. ICLR's Critical Strengths) in the reviewer's words, woven into one sentence ("you appreciated our X, and found our Y genuinely useful and our Z informative"), without quotation marks (user 2026-11-15「要引用一下他原话的Critical Strengths」, then「不要加引号.」). A bare verdict word such as "good" does not go into "you found our X good" (user「found our evaluations good, 感觉有点尬」); fold it into the verb ("you appreciated our evaluations against …"). Leave out any strength that names a cost, a limitation or a null result, even as praise ("the paper is honest about cost", "honestly reports negative results"): it points the AC at the weakness (Never expose a weakness). No numbers.

   中文对照：**非常感谢您给出支持接收的正面评分，以及富有洞见的建议！我们尤其感谢您认为〈原话 1〉、〈原话 2〉以及〈原话 3〉。** 我们致力于解决您的所有问题。能否请您告诉我们是否还有其他问题？我们很乐意进一步解决。再次感谢您的时间和宝贵意见！

5. **Their answer decides the next post** (user「他们回复没有就使劲夸他们 有的话就赶紧解决到没意见可以提」「如果正分不回复不管他」):
   - *No remaining concerns*: praise them warmly, bold thanks quoting what they wrote (with the § 4 title when they confirm their rating); if no request was made to them yet, the one request follows (§ 7, form 5), then the invitation to ask more and the thanks line.
   - *A concern*: answer it at once (§§ 2–5), and keep answering until nothing is left to raise. The reply that closes it carries the one request if none was made yet.
   - *Kept the score after the request*: the closing reply of § 4, then nothing more to this reviewer.
   - *Silent*: leave them alone in the thread. The positive rating stands; a second nudge only spends goodwill. The AC note of item 6 still asks the AC to prompt them.
6. **A negative-score reviewer is nudged last, briefly: which of their concerns we resolved, then whether that addresses them** (user 2026-11-15「催一个2 分的, 就简短的催下，说明我们解决了他的哪些问题 然后问下他是否address your concern」). No strengths restated and no rating request (user 2026-11-15「别上来就要分, 你就问哪些问题解决了, 要分太露骨了」): to a negative-score reviewer, the nudge and every reply end by asking whether our responses have addressed their concerns (user 2026-11-15「Could you kindly let us know whether our responses have addressed your concerns? 挺好的」), and a rating request comes only after they write that their concerns are resolved (§ 7, form 6).

   Title (OpenReview Title field, Title Case, no `**`): `Thank You for Your Insightful Suggestions`

   > Dear Reviewer <ID>,
   >
   > **Thank you so much for your insightful suggestions!** In our responses, we have addressed each of your concerns:
   >
   > 1. **<The concern, in the review's terms> (W1).** <One sentence: what our reply showed, and the table or section that carries it.>
   > 2. **<…> (W2, Q1).** <…>
   >
   > **Could you kindly let us know whether our responses have addressed your concerns? As the discussion period closes on <date>, we would be grateful to hear from you before then, so that we still have time to address any remaining concern.**
   >
   > Thank you again for your time and valuable feedback!

   - One item per weakness or question, merged where the round-1 reply answered them together, labeled as in the review. Every concern gets an item; leaving one out tells the AC it is still open.
   - **A reviewer who has posted follow-up questions is nudged on those only** (user 2026-11-18「这也不是相关的吧, 你就回他最近一次问的就行」): one item per question in their latest comment(s), restating our answer to it, labeled as they labeled it ("W3 follow-up"); the round-1 weaknesses are not listed again. The opener thanks them for the follow-up questions and says our follow-up responses addressed them.
   - Each item restates the posted reply (§ 1): its conclusion, at most one number, the table or section. No new result and no number the thread does not already show.
   - A result that holds on only some benchmarks is stated by the reply's own conclusion or by one benchmark where it holds, never as a count ("on three of the four") (Never expose a weakness).

   中文对照：**非常感谢您富有洞见的建议！** 我们在回复中逐条回应了您的问题：1. **〈问题〉(W1)。** 〈一句话〉…… **能否请您告诉我们，我们的回复是否解决了您的问题？讨论期将于〈日期〉结束，若您能在此之前回复，我们将非常感激，这样我们仍有时间解决您尚存的任何问题。**再次感谢您的时间和宝贵意见！

   **In the last days before the discussion closes, nudges go to the negative-score reviewers only** (user 2026-11-16, two days before close:「这个阶段的催 主要是你要把负分reviewer抓回来问问题解决没 然后逼他回复，不然他先不回复之后说没解决 … 3 分不要催 好 正分给人家催烦了 现在干低分的 先干2分的，要礼貌」). A negative reviewer who stays silent can tell the AC in the private discussion, after the authors can no longer answer, that the concerns were not resolved; the nudge gets their answer on the record while there is still time to address it. So:
   - Positive-score reviewers get no further post in this window (one more annoys them); their threads stay as they are.
   - Negative-score reviewers go from the highest negative score down (a 2 before a 1), one per post, a few hours apart.
   - **A negative-score reviewer still silent 24 h after its nudge gets another one** (user 2026-11-16「2分如果昨天催了没回, 今天还要催吗. 如果间隔24小时, 你再催一次」). Check the thread at that mark: any reply from the reviewer (a comment, an edited review, a rating change) means no follow-up; answer it instead (§§ 2–5). Otherwise post the same template with <N> in the title recounted on the day of posting; the items stay as in the first nudge. Never two nudges to one reviewer less than 24 h apart. Record each in `REBUTTAL_STATE.md` (item 7) so the next session can measure the 24 h from the last one.
   - The nudge names the date the discussion closes and asks for an answer before it, so that any remaining concern can still be addressed (the template above, that paragraph in bold: user 2026-11-16「这句话黑体加粗」). That is the pressure; the tone stays polite: no "please respond", no "we have not heard from you", no mention of the AC.
   - The title carries the same ask, so it is read even if the body is not (user 2026-11-16「title 以后用这种, Thank You for Your Insightful Suggestions, We aim to Address them ALL before ddl in 2 days, Do you have any remaining concerns?」): `Thank You for Your Insightful Suggestions; We Hope to Address All of Them Before the Discussion Closes in <N> Days. Could You Kindly Let Us Know If Any Concerns Remain?` (<N> counted to the close date on the day of posting). Then「礼貌一点」: no capitals for emphasis ("ALL"), "hope to" rather than "aim to", "Could you kindly let us know" rather than a bare question, the close named as the discussion closing rather than a deadline. It replaces the item-6 title in this window.

   **If it stays silent, write to the AC and ask the AC to prompt the reviewer; outside the last days the reviewer gets no second nudge** (for the last silent negative-score reviewer in the last days, the next paragraph replaces this one) (user 2026-11-15「要是再不回负分不回复就给ac写信, 让ac去催」; earlier「负分不回复 催AC，说为什么其他审稿人都说很好，然后积极engage，就这个负分的意见有问题123，然后不回复」). Silent means no answer by the half-day check after its nudge, with every positive-score reviewer already confirmed or left silent. The note says that the other reviewers rate the paper positively and engaged in the discussion (who confirmed or replied; true counts only), lists the reviewer's points numbered, most serious first (each quotes the review and gives what the submission or our reply contains, and where; "A factual inaccuracy in W<n>" (never "error") only where the submission contradicts the review), states as a fact that the reviewer has not replied to our response or our nudge (with both dates), and asks the AC to encourage the reviewer to respond before the discussion closes. It follows the letter of [misconduct-reporting.md](misconduct-reporting.md) § 4, goes through the channel of § 3 there (readers Area Chairs, never reviewers), and is the one AC note for that reviewer: for a `bad_faith_suspected` reviewer it is the misconduct note itself, not a second letter. Draft it; the user sends it.

   **In the last days, the last silent negative-score reviewer gets the 24 h follow-up nudge and, at the same time, a short confidential note to the AC asking the AC to bring the review into the discussion** (user 2026-11-16「反正剩一个负分的时候可以这样说, 同时给ac写confidential, 说别人觉得很好，他有很多意见，我们仔细解决了，但是他不回复, 问他能不能 bring this review into discussion. 但是 如果没有足够多正分就不能说」). "Last" means every other negative-score reviewer has replied or is already covered by an AC note that has been posted (a misconduct note for that reviewer covers only that reviewer, so this one is a separate note). Post the nudge and the note together; the note does not wait for a further half-day check.

   **One negative-score reviewer per day, reviewer first, then the AC, back to back** (user 2026-11-16, the evening before the last day:「你今天要找ac 催 2分的了，对，现在催，说其他几个审稿人都回复了，还说我们好 … 就这个2分的审稿人不回复 等解决了2分的，明天催1分的」「你先给reviewer发，然后给ac发 可以连续」). This replaces the wait for "last" above when the close is a day or two away:
   - The highest negative score first (a 2 before a 1). On its day: the follow-up nudge in its thread (the 24 h gap does not apply; the title's <N> recounted), then right after it this AC note. The next negative-score reviewer gets the same pair the next day.
   - The note covers only that reviewer: it does not name the other negative-score reviewer (its turn is the next day) and carries no request for other silent reviewers.
   - Point 1 says the other reviewers replied and rate the paper well, in true counts: name who rates positively, and among them who replied in the discussion, quoting a reply verbatim where one says the concerns are addressed. Never "all other reviewers have replied" while one of them has not; the AC sees the forum.
   - Point 2 lists every date we posted to that reviewer: the response and each follow-up, including the one posted just before the note.
   - **Title and wording stay warm** (user 2026-11-16「"Reviewer <ID> has not yet replied to our responses" 也太不礼貌了 … 说说其他几个审稿人都回复了，还说我们好 … 希望能鼓励他讨论, 好 fully address」): the title names the supportive reviewers and asks the AC's help, never states the silence: `Reviewers <A> and <B> Have Confirmed Their Support for Acceptance; Could You Kindly Encourage Reviewer <ID> to Join the Discussion So That We Can Fully Address the Remaining Concerns?` (Title Case, true names only). The silence is one soft sentence ("We have not yet heard back from Reviewer <ID>."), not "has not yet replied to …"; the ask ends "so that we can fully address any remaining concerns".
   - **Body, as the user wrote it on 2026-11-16** (「we truly thank these reviewers actively engage in discussion … However, we want to bring your attention to Reviewer <ID>, who said our work strength at xxxx however, still give us weak reject … We solve all their concerns (W1 to W4), however, no reply … We also find … 100% AI generated by gptzero … We want to respectfully ask to bring this review in to discussion」「更新 skill」), between the opening and the warm closing:
     1. The supportive reviewers (point 1 above), ending "We truly thank these reviewers for actively engaging in the discussion and improving our work with their valuable suggestions."
     2. "However, we would like to bring to your attention the review of Reviewer <ID>." Then the review's own Critical Strengths, quoted verbatim, "yet still rates the paper <r> (<label>)."
     3. "We have addressed all of the reviewer's concerns (W1 to W<n>) in our response of <date> and our follow-up(s) of <dates>. However, we have not yet heard back from Reviewer <ID>."
     4. Only when the user has run an AI-text detector on the review and gives the result: "We also found that <detector> classifies this review as <x>% AI-generated, with <y>% mixed and <z>% human." The detector's output with its name and numbers, never our own verdict ("the review is LLM-generated"); the numbers come from the user, never estimated or re-run by us.
     5. "We want to respectfully ask whether you could bring this review into the discussion, and ask Reviewer <ID> to respond on whether our rebuttal has resolved their concerns." (the user's wording at posting, 2026-11-17: "We want to respectfully ask", no close-date clause; the opening already says "before the discussion closes").
     In item 1 the user wrote "rate the paper as acceptance" for weak-acceptance ratings at posting; use that.
     This supersedes "a request for engagement, not a complaint: no numbered faults" above for this note: the strengths-versus-rating contrast and a detector result are allowed; numbered "inaccuracy" points still belong only to the misconduct note.
   - The note may go before the reviewer's follow-up nudge when the user says so (user 2026-11-16「ac的现在发」, follow-up moved to the next morning); it then names only the follow-ups already posted. Channel as in [misconduct-reporting.md](misconduct-reporting.md) § 3 (Official Comment, readers Area Chairs and above, never reviewers); draft it, the user sends it. It is a request for engagement, not a complaint: no numbered faults in the review and no "inaccuracy" points. In this order:
   1. **The other reviewers rate the paper well**, named by ID, with who confirmed or engaged in the discussion (true counts only). **Only with enough positive scores**: the positive-score reviewers must be a majority of all reviewers. Without that majority, leave this point out; the note opens with point 2.
   2. **The reviewer raised many concerns, and we addressed each of them carefully**: our response (date) and the follow-up nudges (dates). At most the concern labels (W1–W4), no restated results.
   3. **The reviewer has not replied**: one factual sentence with the dates.
   4. **The ask**: whether the AC could bring this review into the discussion before it closes on <date>, plus the request of the next paragraph for any other reviewer still silent.
   5. The warm closing of misconduct-reporting § 4, no signature.

   **The AC is asked to prompt every reviewer who has not replied, positive-score ones included** (user 2026-11-16「ac 就催所有没回的人」). One note to the AC, sent after the half-day check of the last nudge: its close states which reviewers have not replied, with the dates of our response and of each follow-up, and asks the AC to encourage each of them to respond before the discussion closes. Only the reported reviewer carries numbered points; the others get the engagement request alone (for a negative-score reviewer, whether our responses have addressed their concerns), no points. When a note on one reviewer is already drafted, the request goes into its close, not into a second note (one note to the AC). When that note has already been posted, the request goes into the last-days note above. List only reviewers still silent when the note is sent.
7. Record each nudge (time, reviewer), each reply and any score change in `REBUTTAL_STATE.md`, so a resumed session knows who has been nudged and who has been asked for a rating.

## 7. Score requests

VQToken asked RRqQ, after "this fully addresses all my questions", to "consider increasing your final rating"; the rating stayed at 4.

Rules:
- A co-author's rating request already in the shared draft goes to the user; it is not deleted silently.
- Asking for a higher rating is allowed, and is encouraged at the end of a reply that closes the reviewer's concerns (user 2026-11-14「删掉"不向审稿人要分"这个规定」, which lifts the 2026-11-13 ban; then「要求提高分数, 有几种说法…委婉点」).
- Ask politely and indirectly: first ask whether the concerns are now resolved, then ask whether the reviewer would consider a higher rating, as a conditional ("if …, we would be grateful / more than happy …"). Never state that the score should go up, and never name a target score. Pick the form that fits the reviewer, and vary it across threads so the reviewers do not all get the same sentence:
  1. Used in a 2026-11-14 round-2 reply: "If these additional analyses address your remaining concern, we would be grateful if you could consider increasing your rating in light of the strengthened evidence."
  2. The user's wording: "We would be more than happy if you could consider raising your score."
  3. Ask whether the last concern is resolved and whether the rating could go up further (user「让他咨询是否最后的问题解决了，以及是否有可能 further increase rating」): "We hope our responses have resolved your remaining concerns. If so, we would greatly appreciate it if you could consider further increasing your rating."
  4. As a question: "Could you kindly let us know whether our responses have addressed your concerns? If they have, we would be more than happy if you could consider raising your score."
  5. For a reviewer whose rating is already positive: "If you feel the paper has been strengthened by these additions, we would be grateful if you could consider a further increase in your rating."
  6. For a reviewer whose rating is negative, only after they have written that their concerns are resolved; before that, ask whether our responses have addressed their concerns instead (§ 6 item 6; user 2026-11-15「别上来就要分, 你就问哪些问题解决了, 要分太露骨了」): "As we believe all of your concerns have now been addressed, we would be grateful if you could kindly reconsider your rating."
  Each form is followed by the invitation to ask more (§ 3 item 5).
- No appeal to personal stakes ("would mean a great deal to our team and our work's visibility").
- No deference line after a request or closing (user 2026-11-14「However, we fully respect your final judgment. 感觉有点生硬 … 把这句删了吧」): no "However, we fully respect your final judgment", "we respect whatever decision you make", "of course, the final decision is yours". It reads stiff, and "However" sets it against the sentence before it. Delete it, do not reword it; the reply ends on the thanks line (§ 3).
- **One request per reviewer for the whole discussion** (user 2026-11-15「比如第二轮问了一次, 不加分, 别催了 … 换个人」). Once a reviewer has been asked and the score did not move, there is no second request and no further nudge: their next reply gets the closing reply of § 4, and the next post goes to another reviewer.
- Who has been asked, and whether their score moved, is recorded in `REBUTTAL_STATE.md`.

## 8. All-reviewer thank-you, 24 h after round 1

User 2026-11-14:「准备一个给所有reviewer 的信息，感谢他们的review和suggestion来帮助我们提升论文，我们try our best去address他们的concerns，let us know if they have any remaining concerns, 说我们致力于解决他们所有的concern, 一般第一次交后24小时后发」.

About 24 h after the round-1 replies are posted (every thread answered), post one official comment at the top of the forum, readers everyone. It goes up once, as is, in every rebuttal, before any individual nudge (§ 6). It thanks the reviewers for the reviews and suggestions that helped improve the paper, says we tried our best to address their concerns, asks for remaining concerns, and commits to resolving all of them. It names no reviewer, carries no result and adds no deference line (§ 7). Record the posting time in `REBUTTAL_STATE.md`.

Title (OpenReview Title field, Title Case, no `**`): `Thank You to All Reviewers`

> Dear Reviewers,
>
> **Thank you for your thoughtful reviews and constructive suggestions, which have helped us improve our paper!**
>
> We have tried our best to address each of your concerns in our point-by-point responses. If you have any remaining concerns or further questions, please let us know. We are fully committed to resolving all of your concerns.
>
> Thank you again for your time and valuable feedback!
>
> Best regards,
> The Authors

中文对照：各位审稿人：**感谢各位细致的审稿意见和建设性的建议，帮助我们提升了论文！** 我们已在逐条回复中尽力回应了各位的每一个问题。如果您还有任何问题，请告诉我们。我们会尽全力解决您的所有问题。再次感谢各位的时间和宝贵意见！此致，全体作者
