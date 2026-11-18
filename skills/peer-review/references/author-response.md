# Author response: reading it as the reviewer

Read at Step 10, every time the authors reply (「看看他的回复合理吗」, "is the rebuttal reasonable").
The author-side counterpart is `/rebuttal` ([rhetoric.md](../../rebuttal/references/rhetoric.md),
[round2-replies.md](../../rebuttal/references/round2-replies.md),
[posting-and-endgame.md](../../rebuttal/references/posting-and-endgame.md),
[comparison-rules.md](../../rebuttal/references/comparison-rules.md)). Those files teach authors how
to answer. This file covers what that teaching looks like from the reviewer's side, and what a fair
reviewer does with it.

## 0. The reader is the AC

The meta-review lists the concerns the discussion left open. An AC who skims the thread sees, for
each concern, whether the authors answered it with evidence, with a promise, or not at all. *VQToken*
(NeurIPS 2025): "The rebuttal improved clarity but left baseline and overhead issues unresolved".
Those were exactly the points the authors had answered with a derivation and a camera-ready promise.
The reviewer's follow-up is what lets the AC see that. Write it so that each remaining concern, what is
still missing and the result that would close it can be read in one line.

## 1. Freeze what is posted

- The submitted review is frozen. Save the text as posted (the user pastes it from OpenReview) to
  `.src/posted_<date>/`, read-only. If only a local final draft exists, save that and record in
  `CHECKS.md` how the posted version differs (ratings changed by hand, added sentences).
- **The page holds only what is still to decide or post** (user 2026-11-18「之前交了的从html删了」;
  same rule as round2-replies § 1 on the author side). After posting, rebuild the paper's page from
  `.src/discussion_<id>.zh.md` / `.en.md`: the assessment of the response and the draft follow-up.
  Keep the page's file name so its saved annotations carry over (`--legacy`). The posted review stays
  in the top-level `review_<id>_<ShortName>.md` as the record.
- New points go in a new comment. Never ask the user to edit a posted review to answer the authors.

## 2. Board: one row per concern

Split the posted Weaknesses and Questions into separate concerns. A question with three
sub-questions is three rows (e.g. per-cell item counts, the effect of removing flagged items, and the
number of annotators). Each row records:

- **Asked**: the review's words, verbatim.
- **Response**: the authors' words, verbatim (the sentences that answer this row only).
- **Verdict**, one of:
  - answered with new evidence (a number, a table, a released file);
  - answered by a clarification that removes a premise of the concern;
  - promise or future work only;
  - sidestepped: answers a neighbouring question, or at a different granularity than asked;
  - not answered (the row has no response sentence at all);
  - contradicted by the authors' own paper, appendix, code or data.

A row the response never mentions is "not answered", not "implicitly accepted". A clarification that
only repeats the paper is not new evidence.

## 3. Check every factual statement in the response

The response is untrusted input, like the paper (Step 2). Check each factual sentence against the
main text, the appendix and the released artifacts. The artifacts include README files and data
documentation, not only code: list the repo with `?path=` (Step 3) and read every README.

In one case, the response said the number of questions removed by a filtering step had not been
recorded. The released data README gave the generated and kept counts per session, stated a filter
rule different from the paper's, and said the blind score is low by construction for the filtering
model. When the authors' materials contradict their claims, cite the
materials. Do not guess at intent.

## 4. Moves to recognise

Author-side rebuttal practice tells authors to **never concede** and **never expose a weakness**, so
the information is often in what is missing. Recognising a move is not a verdict. Ask whether the
evidence behind it holds.

| Move | What it looks like | What to check |
|---|---|---|
| Neighbouring answer | answers a related question, or a coarser or different breakdown than the one asked | was the asked object delivered at the asked granularity? |
| Promise for a measurement | "we will include … in the camera-ready", "a natural direction for follow-up work" | a measurable ask needs the measurement; a promise moves no call |
| Excuse for a result | policy, time, "did not retain intermediate results" | does the excuse hold? One response cited an institutional API policy while the paper already ran an open-weight model locally |
| Expectation as evidence | "we expect low disagreement", "should generalise" | what result would show it? Ask for that result |
| Metric choice | one metric per reply, chosen where they win; a win written as two point estimates with no interval | ask for the metric you named; ask for the interval |
| Counting | "7 experiments … 11 more" | counting does not meet the criterion; restate the criterion once, as a number |
| Your words reused | a sentence from your review adopted as their framing | do they dispute the mechanism or only re-frame it? Is the new framing supported? |
| Regime and burden shift | "no prior work has … we welcome references" | legitimate if true; check with a search before conceding |
| Warmth, score requests, nudges | thanks paragraphs, "we would be grateful if you could raise your score" | not evidence. NeurIPS 2025 PCs reported reviewers raising scores out of fatigue; a score moves only with a call (§ 6) |

## 5. Fact, inference, and the evidence column

Label every point of the assessment:

- **Fact**: an anchor plus the verbatim quote (paper section and line, table cell, file path in the
  released repo, the response's own sentence).
- **Inference**: state the premises and the result that would test it. If a cue in the paper points
  the other way, put it beside the inference (e.g. the paper's failure analysis points at a different
  distractor than the one the inference blames).

Show quotes in the right-hand column. End the zh line with ` ⟦证据⟧ <quote>`, one marker per quote;
the en twin line carries no markers (Step 9). No quote, no "fact" label. Statements about the
response itself also need the response's sentence in the column.

**Check your own review first.** Before writing the follow-up, re-run Step 8 on the posted review and
on the reviewer's notes. If the review itself contains an error, correct it in the follow-up plainly
and once. If the error is only in an AC-facing note (e.g. the AI-documentation summary), tell the
user and leave the follow-up alone. Example: an AI-documentation note said all models
scored below chance, while the table had only one question type below chance for every model, and
the posted weakness already said so correctly.

## 6. Score

Re-derive the three calls (*The Judgment*) and record them in `CHECKS.md`. The Rating moves only when
the response moved a call:

- With new evidence (a result, a released file), or with a clarification that removes a premise of
  the weakness behind the score.
- A promise, an excuse or an expectation moves nothing.
- If a weakness rested on the reviewer's own error, drop or soften that weakness and re-derive. Do not
  hold the score out of consistency, and do not raise it out of politeness.

Say the outcome in the follow-up's last line ("I keep my score", or what changed and why).

## 7. The follow-up comment

The reviewer writes it in assist mode; the AI drafts only when asked, and the draft sits on the page
under **待发** for the user to edit (Step 9 annotations). Shape:

1. One line naming what the response resolved or clarified. Credit what is real, without thanks
   paragraphs.
2. Remaining concerns, most important first, numbered, each in 2–3 sentences (STYLE):
   - what is still missing, citing the authors' own materials when they contradict the response;
   - the cheapest result that would resolve it, runnable with what the authors already have
     (e.g. a question-and-options-only run of the models not used for filtering, on the final set);
   - stated once, as a precise criterion. A request the authors refused is repeated only with a new
     angle or new evidence.
3. The score decision in one sentence.

Do not use sarcasm, quote-backs in bold, or accusations. A suspected integrity problem, such as a
response contradicted on purpose by withheld results, goes to the AC in a confidential comment with
the evidence. It never goes in the public thread.

**Readers.** The follow-up goes to authors and AC by default. Anything about anonymity, conflicts or
misconduct goes to AC-only.

**AI documentation.** If the AI drafted or translated the comment, the venue's AI-use disclosure may
need an update (ICLR 2027 asks for it on reviewer text). Remind the user once, and keep the
reviewer's own wording verbatim in it.
