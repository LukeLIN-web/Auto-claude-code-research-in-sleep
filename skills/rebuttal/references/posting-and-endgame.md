# Posting and endgame

Read at Phase 7 (posting) and before the AC closing note. Replies to reviewer comments that arrive after round 1 is posted: [round2-replies.md](round2-replies.md).
Rhetoric rules: [rhetoric.md](rhetoric.md). Reports on bad-faith reviews: [misconduct-reporting.md](misconduct-reporting.md).

## 1. Posting order

Post one reviewer at a time, positive-score reviewers first; they usually confirm and then stop moving. Difficult negative-score reviewers go last (Phase 3 step 8, 「先一个一个回复，看正分审稿人愿不愿意confirm，他们一般confirm之后就不动了. 然后麻烦的负分先留到最后」). The board and collaborator doc use the same order from the start, highest score first (user 2026-11-12「下次应该把高分的放前面」); one rebuttal's board led with the 1-score reviewer and could not be reordered once co-authors were editing it.

VQToken fits this: LjpF acknowledged within three days and ended at 5; RRqQ (4) wrote "this fully addresses all my questions" and stayed at 4; the negative reviewer took the whole period.

## 2. AC closing note

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

## 3. After every round

- Update `REVISION_PLAN.md` in place (new items, ticks, statuses).
- Re-run the Phase 5 lints on the new reply.
- Record round, posting time and any reviewer score/acknowledgement in `REBUTTAL_STATE.md`.

## 4. Co-author comments on the shared draft

Moved to [collaboration.md](collaboration.md): ownership of text (§ 1), co-author version vs ours (§ 2), checking against the source (§ 3), marking (§ 4), sync direction (§ 5), comments and suggestions (§ 6), safe edits (§ 7).
