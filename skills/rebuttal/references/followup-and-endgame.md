# Follow-up rounds and endgame

Read at Phase 7 (posting) and Phase 8 (every new reviewer comment).
Rhetoric rules: [rhetoric.md](rhetoric.md). Reports on bad-faith reviews: [misconduct-reporting.md](misconduct-reporting.md).

## 1. Posting order

Post one reviewer at a time, positive-score reviewers first; they usually confirm and then stop moving. Difficult negative-score reviewers go last (Phase 3 step 8, 「先一个一个回复，看正分审稿人愿不愿意confirm，他们一般confirm之后就不动了. 然后麻烦的负分先留到最后」).

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

## 3. Nudges

VQToken sent three nudge posts aimed at one reviewer plus two to all reviewers within Aug 2–8, most repeating "Do you still have any concerns?". The reviewer replied to the content posts and kept 2. The NeurIPS 2025 PCs reported "reviewers increasing their scores just to end back-and-forth discussion with the authors, but being silent or critical in private discussions with the AC" and attributed it to "reviewer fatigue". ICLR's author guide asks authors to "remain civil and considerate of the reviewers time".

Rules:
- A nudge carries content: one line per point that changed since the reviewer last wrote, plus one question. An empty "any remaining concerns?" post is not a nudge, it is noise.
- At most one nudge per reviewer after ~3 days of silence, and one more 24–48 h before the discussion closes. No other reminders.
- One all-reviewer post at the start ("responses are posted per thread") and none in the middle.

## 4. Score requests

VQToken asked RRqQ, after "this fully addresses all my questions", to "consider increasing your final rating"; the rating stayed at 4.

Rules:
- Never ask a reviewer who has not written that their concerns are resolved.
- After such a statement, at most one sentence, once, conditional, in the same reply that thanks them: "If the additions change your assessment, we would be grateful if the rating could reflect it." Never a separate post titled for the score; never repeated.
- No appeal to personal stakes ("would mean a great deal to our team and our work's visibility").

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

When the draft lives in a shared doc (the collaborator doc on HackMD, `SKILL.md` Phase 4; earlier rebuttals used a Google Doc) and co-authors comment or suggest:
- Read every comment, open suggestion and direct edit before touching the doc; never rebuild it wholesale from the local files, which would erase their text.
- Each source needs its own read. The Drive text export (`read_file_content` with comments) carries comment threads but not suggestions; read suggestions from the Docs API (`read_doc`: `suggestions[]`, and the `suggested*Ids` on text runs for their anchors). Direct edits show up only as a diff of the doc against the canonical files; text a co-author wrote is often the richest lesson (`rhetoric.md` § 9).
- Reply to each comment with exactly what changed, quoting the new wording ("Replaced 'It does.' with '…'"), and whether mirrors (e.g. the Chinese version, `Reviewer_<ID>_response.md`) were updated.
- A co-author's edit that conflicts with a user ruling (e.g. a revision promise — "We will add both models to the revised paper" — against a ruling not to change the paper for that reviewer, or a reply pushed over the character limit) is not applied silently: list it under the board's open-decision section for the user.
- Record each group decision with its date ("Decided (11-09): the title stays unchanged") in the doc, `ISSUE_BOARD.md` and `REBUTTAL_STATE.md`, and propagate it to every reply it touches ("Rulings reach every draft").
- Before editing, diff every draft paragraph in the doc against the canonical files (normalize markdown escapes and chips). A passage synced late can sit stale in the doc while the files have moved on; in one run the doc's copy of one answer still carried "In an earlier configuration" after the files had replaced it, and the user caught it.
- Edit commented text inside its anchor where the change allows (insert around it, change words within it). Rewriting the whole anchored span detaches the thread from the text; when the request requires that, say so in the reply list.
- If the doc connector cannot reply in threads, hand the user one line per thread (what changed, quoting the new wording) to paste.
- A co-author's worry about the character limit is answered with measured counts per comment, markers stripped (lint 6). When an edit pushes a comment over the limit, re-split at a W/Q boundary and update the comment counts the board shows.
- Generalize recurring comments, and the moves in text co-authors write themselves, into `rhetoric.md` § 6–9 so the next draft needs fewer of them.
