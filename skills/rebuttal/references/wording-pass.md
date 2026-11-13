# Wording pass: blind read, cut, reword and rewrite, check, one owner per number

Run at Phase 6.5, after the stress-test fixes and before Finalize, and again on every delta reply in Phase 8 (user 2026-11-09: 「rebuttal 生成完了, 用这些方法过一遍措辞」). Steps 3–5 are [`/paper-polish`](../../paper-polish/SKILL.md), the same polish a paper gets: a second AI (the editor) calls `/paper-prose-tighten` (cut), then `/paper-jargon-pass` (reword, then rewrite), and the drafter checks its edits; this file's § 3–5 are the rebuttal overlay passed to it (user 2026-11-12: 「让另一个 AI 润色 … 先 paper prose tighten, 再 paper jargon pass」「这一套应该封装为一个单独的 skill, 这样 paper 也能用」). The steps ask different questions, need different readers, and are **never run as one mixed read**:

| Step | Question | Done by | Origin |
|---|---|---|---|
| 1. Blind read | Can the reviewer parse this word, at this point in the reply? | a fresh subagent that gets only [blind-read.md](blind-read.md), the review and the reply | `docs-jargon-pass`, first pass |
| 2. Reconcile | Do the numbers and terms the ledger touched match their sources? | the drafter, with the evidence | `docs-jargon-pass`, second pass |
| 3. Tighten (cut only) | If this sentence is deleted, does the reviewer's judgment change? | `/paper-polish` editor (a fresh subagent per paste target), overlay § 3 | `paper-polish` → `paper-prose-tighten` |
| 4. Reword, then rewrite | For each term the reader stalled on: delete, replace, or define? Then: do the surviving sentences say "we did", in order, clearly? | the same editor, overlay § 4 | `paper-polish` → `paper-jargon-pass`, then `paper-polish/references/rewrite.md` |
| 5. Check the editor's edits | Did any edit move a frozen span, a number, or the claim? | the drafter | `paper-polish` § 5, plus § 5 here |
| 6. One owner per number | Is this number written once, and identical everywhere it is repeated? | the drafter | `docs-ssot-tighten` |
| 7. Acceptance | Does a second fresh reader still stall? | a second fresh subagent | `docs-jargon-pass` |

**Why this order.** The blind read comes first because it is the only step that cannot be repeated by someone who has seen the evidence. Deleting comes before rewording: a term in a sentence that is about to go needs no definition, and a deletion can remove the sentence a definition was just moved into; for the same reason the voice and cohesion rewrite comes last, inside step 4, and cutting and rewriting live in different skills (user 2026-11-12: 「删和改不要放一个」). The editor is not the drafter: after days with the evidence the drafter no longer hears a stiff sentence, a passive that hides who acted, or a missing link between paragraphs. The drafter checks the editor's edits (step 5), and the number check runs after that so it sees the final text. Tightening runs once over a given text (a second run starts eating scope qualifiers); the acceptance read is not a second tightening — it only looks for stalls.

The pass changes wording only. It does not decide claims: which numbers go in, what is conceded, what is compared are settled by Phases 3–6 and the user's rulings. Everything it finds that is not wording (two numbers that disagree, an answer that contradicts another thread, a claim the evidence does not carry) is **reported, never smoothed over**.

## 0. What is read, what is touched

- **Read**: each paste target as the reviewer will see it — the reviewer's quoted text plus our answers, markdown stripped. Not the status board, not the notes to the group, not the translation.
- **Touched**: the canonical response text only (Artifacts table). Translations, status boards, HTML views and shared-doc mirrors are derived; regenerate or re-sync them after the canonical text changes.
- **Never touched**:
  - the reviewer's quoted text;
  - any sentence a co-author wrote or edited in a shared draft — never reworded, never deleted, never moved, whatever is wrong with it and whatever "keep the latest" seems to allow. **Mark it instead** (user 2026-11-10: 「你就想办法标出来, comment, 或者用不同颜色 指出这里是错的」): highlight the wrong or conflicting phrase and put a short note in a third colour (not the co-author's, not the body colour) at the end of that paragraph, or leave a doc comment. The note states the clash in one line and points to the ruling or number it clashes with ([collaboration.md](collaboration.md) § 4). Where it differs from our version only in wording, it is the version kept; a wrong number or a clear grammar slip in it is the one thing fixed directly ([collaboration.md](collaboration.md) § 2);
  - wording the user ruled on verbatim, and text quoted from the revised paper (fix the paper first, then re-quote);
  - numbers. A wrong number is a bug to report, not a wording fix.

## 1. Step 1 — blind read

**Before the read: one version per answer** (user 2026-11-10: 「保留最新的」). In a shared draft, **our own** superseded versions of an answer are deleted first and only the latest is kept. A co-author's older version or fragment is never deleted, even when it is clearly superseded (user 2026-11-10: 「合作者的永远不删」); the blind reader is simply not given it. A reader given three coexisting versions of A1 spends most of its ledger on their disagreements (first run: 27 entries for one reply, about 8 once the old versions were gone). The older text stays recoverable in the doc history.

One fresh subagent per paste target. Give it exactly: [blind-read.md](blind-read.md), that reviewer's raw review, and the stripped reply text with paragraph ids. Do not give it this file, the issue board, the evidence, or another reviewer's thread. It writes `rebuttal/wording/<UTC timestamp>/ledger-<ReviewerID>.md`.

The drafter never does this read, and never "completes" a ledger from memory: after the evidence has been read the drafter cannot tell where a new reader stalls.

The vocabulary order used in step 4 is the one the blind reader is given: (1) the word the reviewer used, (2) the word the submitted paper uses, (3) the standard term in the field — never a fourth word invented while drafting.

## 2. Step 2 — reconcile

Now the evidence documents, the issue board and the code may be read.

1. **Numbers first.** Check every number the ledger touched against its source (the result file or the paper table). Report-type entries are settled here; a real mismatch stops the pass for that answer until the user rules.
2. **Word against thing.** If a term describes something other than what was run (the reply names the released model where the number comes from retrained weights), that is a factual problem in the reply: report it; rewording alone does not settle which model the claim is about.
3. **Sort the ledger.** Each entry is marked: report to user / idle → step 3 / term → step 4 / no change (with the reason). Entries in co-author text are marked "not touched" and go to the report.

## 3. Step 3 — tighten, cut only (`/paper-prose-tighten`)

**Calling `/paper-polish`.** Run [`/paper-polish`](../../paper-polish/SKILL.md) once per paste target with: target = the stripped reply with paragraph ids; ledger = the step-1 ledger with the step-2 dispositions (so `/paper-polish` skips its own blind read and reconcile); frozen spans = § 0 "Never touched" (the reviewer's quote, quoted paper text, every co-author sentence, wording the user ruled on — copied unchanged, even when passive); overlay = § 3, § 4 and § 5 of this file. The editor also gets that reviewer's raw review; it does not get the issue board, the evidence or another thread. The drafter never does steps 3–4.

**Paper-only parts of `/paper-prose-tighten` are skipped:** the paragraph-map script over `sections/*.tex`, compile, captions and figure generators, the short-last-line gate, the cross-section copy check of class 13 (step 6 does that across threads). The skill's class 11 (related-work sprawl) becomes "secondary evidence nobody asked for" (lint 22).

For each sentence and each number in it: **delete it, and does the reviewer's judgment change?** If not, delete — do not soften or shorten. In a reply the cut classes read as below (this table numbers them for replies: it adds instrument readings and leaves out related-work sprawl):

| # | Class | In a rebuttal | Keep when |
|---|---|---|---|
| 1 | Bookkeeping counts | intermediate counts, subset denominators, split sizes printed to show work | the denominator scopes the claim ("356 of 2,000 videos") or the number is the answer |
| 2 | Defensive meta-narration | "we report this only descriptively", "we do not claim", "to be transparent" | never — and it usually also fails the weakness scan (lint 10) |
| 3 | Journey | "we first tried", "an earlier version", "after re-running" | never; the result stays, the route goes |
| 4 | Restatement and stacked hedges | the same fact at the start, middle and "therefore" of one answer; "consistent with", "we read this as", "in the sense that" on an already hedged claim | one statement, placed where the reviewer needs it — the closing conclusion sentence (C4) is that place |
| 5 | Narrated absence (无中生有) | "X does not report this setting", "there is no official number" | the reviewer can see the gap (a `—` in our table) → one short table note; or the absence is the claim |
| 6 | False pivot (错误的转折) | "not A but B", "rather than A", where nobody proposed A | **A is the reviewer's reading, quoted or paraphrased from the review** — then the pivot is the refutation and stays |
| 7 | Duplication across answers | two answers in one thread give the same result at different resolutions | one owns it; the other keeps one sentence and "(A1)" |
| 8 | Provenance assurances | which checkpoint, how it was picked, what it was not tuned on | the reviewer would otherwise assume a different experiment: what the number was computed on, train/test separation, the protocol a comparison depends on |
| 9 | Process vocabulary | "preregistered", "frozen before reading", "sanity check", "pilot" | the technical sense: frozen backbone, frozen prompts |
| 10 | Value series (罗列) | one quantity at three or more conditions strung into a sentence | write the shape (monotone, flat, one outlier) plus at most one number; the series lives in a table — unless the reviewer asked for exactly these values |
| 11 | Instrument readings | a number that restates a fact already given in the reader's unit (a real-time factor beside "minutes per recording hour"), or that says how a measurement was run rather than what it found: worker or process counts, parallelism degree, the cache hit rate behind a reported speedup, exact token or position counts where a ratio says the same | the comparison's fairness rests on it — then state it in words ("decoded the same way for every method", "on four GPUs"), not as the number |

Step 3 tests **every number inside a kept sentence**, not only whole sentences. A field term that the blind reader cleared (real-time factor, hit rate, tensor-parallel) is cleared as a word; the number it carries still takes the delete test.

**Upgrade rule.** A secondary claim that needs two or three caveats to be true is deleted together with its caveats (「越解释越乱」「别解释了」). Headline answers to a W/Q are never deleted this way; if a headline needs a pile of caveats, that is a strategy problem for the user.

**House style is not filler.** These fail the delete test on a naive reading and stay:

- the thanks opener, up to two short sentences (lint 11);
- the goal sentence before a new result, and its setup (C1, lint 19);
- the address of a number (C2), and the result that follows an action (C3);
- the conclusion sentence that closes an evidence paragraph (C4);
- the superlative-plus-ratio statement of a win (C8);
- the revised text quoted verbatim for a requested presentation change (C16).

A closing request to reconsider the score or rating is not house style: delete it (Phase 4 "Never ask for a score").

**Deleting must not change the claim set.**

- Never delete into a win: when a null or tied statement goes, the whole sentence goes; it is not replaced by "no difference" or "unaffected".
- Never delete the denominator that scopes a claim, or a neutral protocol fact a comparison depends on (lint 8 decides which protocol facts are stated at all).
- Never let a deletion create a concession or expose a weakness; never use the pass to add one.
- Before deleting a "repeat", grep its distinctive noun: a conclusion that appears only once is moved to its owner answer, not deleted.
- One pass. A second pass over the same text finds nothing safe and starts eating scope qualifiers.

## 4. Step 4 — reword, then rewrite (`/paper-jargon-pass`)

Overlay for `/paper-polish` step 4. The editor runs `/paper-jargon-pass`'s **second pass only** (查证 + 改写) on the ledger entries step 2 marked "term" whose sentence is still there. Its pass 0 (LaTeX assembly) does not apply, and its blind read is step 1 here. Also skipped: PDF page order, compile, figures, the two-clone rule, and 「正文不写结果数字」 (a reply carries its numbers; rhetoric C17 decides which go in a table). The skill's ordered moves and its 同物异名 / 悬空指代 rules apply as written; the vocabulary order is § 1's. The rewrite that follows (`/paper-polish`'s `references/rewrite.md`) is in § 4.1.

1. **Try these in order — stop at the first that works:**
   1. **Delete the word** and say the same thing with words already in the reply.
   2. **Replace it** by the vocabulary order of § 1. Then replace it everywhere: every answer, every table head, every thread that uses it.
   3. **Delete the sentence** — a term used once, in a sentence no conclusion rests on.
   4. **Define it at first use**, in one clause, anchored to a term the reviewer already has. Last resort: a definition turns the reviewer's confusion into something they must remember.
2. **Internal names are never defined.** Delete the name and write what it contains: not "the D1 judge" but "a judge trained without any video from that generator family". **Lineage words** are deleted; if the difference they point at changes how the number should be read (other weights, other prompt, other subset), state that difference in one clause. Report every lineage word to the user: it often means two generations of a result sit in one comparison.
3. A term used once is assumed deletable. A term used ten times that the reader still cannot parse is not kept because it is frequent.
4. A definition that arrives later than first use is moved to first use, not duplicated.

### 4.1 Rewrite: active voice, cohesion, clarity ([rewrite.md](../../paper-polish/references/rewrite.md))

After the term fixes, the editor reads `/paper-polish`'s [rewrite.md](../../paper-polish/references/rewrite.md) and rewrites the sentences that survived (user 2026-11-12: 「我们尽量用 We 这样子的主动语态，你让 AI 给你加强下表达和衔接，以及语言的 clarity」): what we did with "we" as the subject and an active verb; known before new; each paragraph's first sentence linked to the question or the paragraph before; connectives that name the relation; one claim per sentence. It only rewrites; a sentence that looks empty is reported, not cut (cutting was step 3). Reply-specific limits ([rhetoric.md](rhetoric.md) C35):
- The sentence after the thanks stays the bare verdict (rhetoric § 1, lint 11): never "We find that all four contrasts are significant", never "We ran …".
- The house-style items of § 3 keep their place and job; their wording may be smoothed, they are not removed.
- Frozen spans are not touched; a co-author's passive sentence stays passive.
- No new hedges, concessions or caveats (lint 10), no new term, no new sentence, and the reply does not get longer (lint 6).

## 5. Step 5 — check the editor's edits

The drafter runs `/paper-polish` § 5 on each paste target (frozen spans byte-identical, numbers and addresses unchanged, one before/after claim line per changed paragraph, no new hedge, not longer; a rejected edit is dropped, not repaired). The reply adds:

- no new hit for the § 7 greps and no new concession or weakness wording (lint 10);
- the house-style items of § 3 are still there, and the sentence after each thanks is still the bare verdict (lint 11);
- the paste target is within the venue limit (lint 6).

Anything the editor flagged but could not touch (a frozen co-author sentence, a scope it could not verify) goes to the report, never into the text. Save the change list as `rebuttal/wording/<UTC timestamp>/edits-<ReviewerID>.md`, each row marked taken or rejected (and the check that rejected it); no reply text beyond the before/after sentences.

## 6. Step 6 — one owner per number

Phase 4 already fixes the depth of shared evidence across threads; this step checks the numbers themselves.

1. **Owner map.** For each headline number: the result file is its source; the primary thread (Phase 4 "Shared evidence across threads") is its owner in the response; the canonical response file is its only authored home.
2. **Signature grep.** Take 3–5 headline numbers per reply, exactly as printed (`3.3%`, `0.95`, `−10.7`), and grep all response files, the setup block and every derived view. For each hit read the context first — **the same string can be two different quantities**, and two different strings can be the same quantity rounded twice.
3. **Each hit is one of:**
   - the owner's statement — stays;
   - a citation in another thread — stays if it is the 1–2 sentence recomposition carrying only the number that answers that reviewer's ask, and the value, unit, rounding and the name of the quantity are identical to the owner's;
   - a copy in one thread that the same thread already gave — replace by "(A1)";
   - a copy in a derived view that differs from the canonical text — the view is stale; regenerate it;
   - a number with no owner anywhere in the evidence — an orphan: report it, do not delete it and do not keep citing it.
4. **Never fix a number in passing.** Two values for one quantity is a bug; the user decides which is right.
5. **Counts of our own material** ("the four experiments above", "all five backbones") go stale with every edit: recount them now, and prefer wording that carries no count when the count is not the point.

## 7. Greps (high recall, classify by hand)

```bash
F="rebuttal/Reviewer_*_response.md"   # or REBUTTAL_DRAFT.md
# internal names and drafting labels: experiment IDs, paths, status tags, TODOs
command grep -nE '\b[A-D][0-9][a-e]?\b|/home/|/shared/|outputs/|ckpt|checkpoint-[0-9]|TODO|TBD|待定|\[[^]]*x\.xx[^]]*\]' $F
# lineage words
command grep -niE 're-?(ran|run|scored|trained|computed|generated)|earlier (run|version)|previous (run|version)|\bv[0-9]\b|the (new|old|second|updated) (run|version|judge|model)' $F
# defensive meta-narration and journey
command grep -niE 'we (do not|don.t) claim|only descriptive|to be (transparent|clear|fair)|for completeness|we note that|it is worth noting|we first (tried|ran)|initially|turned out' $F
# false pivots and concessive hedges
command grep -niE 'rather than|instead of|not (because|due to|merely|simply|just)|is not [^.]{1,40} but|although|even though|while it is true' $F
# narrated absences
command grep -niE 'does not (report|provide|release)|no official|not available|was not (reported|released)' $F
# value series outside tables
command grep -nE '[0-9.]+%? ?/ ?[0-9.]+%? ?/ ?[0-9.]+|([0-9.]+%?, ){3,}' $F | command grep -v '^[^:]*:[0-9]*:\s*|'
# process vocabulary
command grep -niE 'preregister|pre-register|frozen before|sanity check|pilot|ablation we dropped' $F
# passive voice and connective chains (step 4.1): the greps in paper-polish references/rewrite.md § 1–2
```

## 8. Acceptance

- Every load-bearing and local ledger entry has a disposition: word deleted / replaced / sentence deleted / defined / reported / no change (with the reason). Expect about half the entries to end as "no change".
- **A second fresh subagent rereads the final text** with the same isolation as step 1 (again only [blind-read.md](blind-read.md), the review and the new text). The pass is done when it produces no new load-bearing entry.
- For each paragraph that changed, one line: what it claimed before, what it claims now. Any difference is a bug.
- Voice check: grep the § 7 passive pattern; every remaining passive with the authors as the hidden actor is either in a frozen span or turned active.
- Re-run the Phase 5 lints the pass can break: 6 (limit — recount), 9 (cross-thread duplication), 10 (weakness and concession), 13 and 14 (comparison, words agree with numbers), 19, 20 and 23 (voice).
- Derived views regenerated; the replaced terms have no leftovers in any thread, table head or view.
- Report to the user in this order: (1) structural findings; (2) bugs and decisions — mismatched numbers, contradictions, unanswered sub-questions, lineage words, findings in co-author text that was not touched; (3) what was deleted, each with its delete test, and what was reworded. Say what was kept and why: the kept list is the evidence that nothing was over-cut.

## 9. Common misjudgments

| Symptom | Correction |
|---|---|
| The drafter does the blind read | It is void; a fresh subagent with only the review and the reply |
| The blind reader is handed this file, the board or the evidence | It gets blind-read.md, the review and the reply — nothing else |
| A term gets a definition, then its sentence is deleted as filler | Tighten (step 3) before rewording (step 4) |
| The acceptance read is used to cut more sentences | It only looks for stalls; tightening ran once |
| A term is defined two paragraphs later, so it passes | Late definition is recorded; move the definition to first use |
| Every unknown noun is recorded | The threshold is "had to reread", not "unfamiliar" |
| A standard term is rewritten into plain words | Field terms and the reviewer's own terms stay |
| A field term is cleared, so the number it carries stays | Clearing covers the word; the number still takes the delete test (§ 3 class 11) |
| A ratio or speedup is kept without its comparator ("1.6× faster", "4.7× fewer tokens") | Name the comparator in the same clause ("than without the cache", "than the media channel") |
| Only the English is blind-read; the team-language translation is synced string by string | The translation leaks on its own: the lab's shorthand for a benchmark or for "our codebase", and coined renderings of field terms. Give the acceptance reader the translation too and ask it to flag where the two languages say different things |
| An unclear word gets a definition by default | Order is delete word → replace → delete sentence → define |
| A clearer new word is invented | Only the reviewer's, the paper's or the field's word |
| An experiment ID or checkpoint name gets a gloss | Internal names are deleted; write what the thing is |
| A lineage word reads smoothly and passes | Grep for it; ask what differed in the input; report it |
| Filler is rewritten to read better | Filler is deleted, not rewritten |
| The thanks opener or the conclusion sentence is cut as filler | House style; see § 3 |
| "Rather than A" is cut although the reviewer proposed A | That pivot is the refutation; it stays |
| A deleted tie is replaced by "no difference" | Delete the whole sentence |
| Two numbers that disagree are aligned quietly | Report; the user decides |
| A number is replaced across files by string | Same string can be a different quantity; read each hit |
| A co-author's sentence is polished, or an outdated co-author fragment is deleted | Never; highlight the phrase and add a note in a third colour, or comment |
| Only the English reply is changed | Re-sync the translation, the board and the HTML view |
| The drafter tightens or polishes alone, or the editor's edits are taken unchecked | `/paper-polish`: its editor edits, the drafter only checks (its § 5 and § 5 here); its "Never" list covers the rest |
| "We" is pushed into the verdict sentence ("We find that all four contrasts are significant") | The answer after the thanks stays the bare verdict; "we" goes where the authors acted |
| A co-author's passive sentence is turned active | Frozen; report it as a note if at all |

## 10. Lessons from the first run (2026-11-10)

Five replies were blind-read; the user ruled on each reported item in one line. Each ruling below is the general rule it stands for.

**How to report.** List the report-type findings per reviewer as short numbered items, in posting order, each stating the two things that clash and nothing else. The user then rules in a word per item (「删」「说清楚」「改正确」「你改」). A finding that needs a paragraph to state is not yet understood well enough to report.

| # | Finding in the reply | Ruling | Rule |
|---|---|---|---|
| L1 | Two sets carried one name: "event missing" was defined at SA ≤ 2 but the filter kept SA ≥ 3, and the reply's own examples of a missing event sat inside the kept set | 「怎么改?」 → fixed by wording | Name a filtered set by what the filter does ("keeping SA ≥ 3, which excludes every video in which the event is not realized"), not by the property we wish it had ("the videos that realize the event"). Delete an example that lands on the wrong side of our own threshold. State the headline without the threshold if the threshold is only defined later. |
| L2 | "…(mean 2.33), consistent with the policy above", where the policy says such a law receives 1 | fixed by deletion | Do not tie a number to a rule it does not visibly match. Keep the number and the comparison; delete "consistent with". Do not add an explanation that was not checked. |
| L3 | "its 15-configuration leaderboard" — the paper has eight generators, the reply adds two | 「你改」 | A denominator that comes from the lab's result table is an internal name. Recount on the set the reviewer knows (the paper's items plus the new ones) and check that the stated rank still holds there before rewriting. |
| L4 | The conclusion credited the released judge with a transfer shown by retrained held-out judges | 「<released model> 没证据吗?」 | When the evidence comes from retrained weights, look for the released model's own number on the same test before rewording the claim away. If it exists and is favorable, add it with its training overlap stated in one clause, and attribute the held-out number to "the held-out judges". |
| L5 | Text quoted from the revised paper looked ambiguous to the blind reader | 「不确定的事情不要修订」 | A blind-read doubt about quoted paper text is checked against the cited work's own text first. If the source confirms it, nothing changes. Never revise the paper, or the quote, on a doubt alone. |
| L6 | The thanks opener named a comparison the answer does not contain | 「删」 | The thanks sentence may only name what the answer delivers. Thank the reviewer for the topic, not for a specific analysis we are not reporting. |
| L7 | "is off from the human score by 8.1% on average" next to a differently defined 5.5% for the same model and dimension | 「说清楚」 | Every number carries the name of its metric, and two metrics for one model and dimension are told apart in words (mean absolute relative bias over generators vs aggregate relative bias on one generator). When a baseline's output is compared on our scale, say which of its outputs is compared. |
| L8 | "We ran both released checkpoints", then numbers for only one | 「能给吗? 好吗?」 | A baseline that was run but gets no number: give a number only if one exists on the reply's metric and is favorable. Otherwise say in one clause why the comparison is with the other baseline (its output has no counterpart on our scale). The gap is visible to the reviewer, so this narrated absence stays. |
| L9 | A new backbone improves less than its siblings | 「也没事? 比 base 低就行?」 | A variant that beats its own untuned base answers "does the supervision transfer"; it need not beat the other variants. No change, and no added comparison to the siblings. |
| L10 | Two numbers in different answers looked like one quantity (0.80 and 0.92 for "unseen generators") | 「说清楚」 | Give each its table and its unit in the same sentence ("of the same table, also per video-law sample"). |
| L11 | A count in an abandoned fragment disagreed with the latest version (seven vs eight) | 「改正确」, 「保留最新的」, then 「合作者的永远不删」 | In our own superseded text the wrong number goes with the fragment. In a co-author's fragment nothing is removed or corrected: highlight the number and add a note. The first run deleted two co-author fragments under "keep the latest" and had to restore them. |

**Second run (2026-11-11).** After two blind reads and one tighten pass, the collaborator doc still carried a real-time factor next to the minutes-per-hour it implies, a cache hit rate and parallelism degree behind a speedup, worker counts and exact position counts (user: 「这种感觉看不懂啊 没用的信息」). Both blind reads had listed these terms as cleared, and the tighten pass had tested sentences, not the numbers inside kept sentences. Fix: § 3 class 11 and the number-level delete test above. The acceptance read of this run also found a board status that the result files had overtaken (an experiment still marked queued whose result a reply already reported): the board's status column is re-checked against the state file in every wording pass.

**What the pass got wrong, and the fix now in this file.**
- The blind-read rules and the verification rules were first written in one file, and the blind reader was told to read "sections 1 and 2 only". Isolation that depends on the reader not scrolling is not isolation: the blind reader's instructions are a separate file.
- Rewording was first placed before tightening. Deleting comes first.
- The first report mixed wording fixes with strategy questions. Wording fixes are applied and listed last; anything that changes a denominator, adds a result or touches a quoted paper sentence is a question for the user, asked in the short-item form above.
