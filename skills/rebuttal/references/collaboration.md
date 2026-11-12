# Collaboration: co-authors on the shared draft

Read this whenever a co-author has touched the shared draft (the collaborator doc of `SKILL.md` Phase 4, or a Google Doc board): before syncing the doc and the canonical files in either direction, before marking anything a co-author wrote, and before answering their comments. The writing lessons drawn from co-author text live in [rhetoric.md](rhetoric.md) § 6–9; this file is about who owns which text and what to do with it.

## 1. Who owns which text

Every sentence in the shared draft has one owner, and the owner decides what may be done to it.

| Owner | What | What we may do |
|---|---|---|
| Us | our drafts, translations, board prose, our notes and highlights | Update in place whenever it is stale, without asking; delete a resolved note and its highlight at once (user 2026-11-10「你写的就直接更新, 合作者的 就 append 注」) |
| A co-author | any sentence they wrote or edited, usually in their own colour | Never reword, delete or move it (2026-11-09「恢复合作者原文的，以后合作者改了你就不要改」, 2026-11-10「合作者的永远不删」). Mark it (§ 4); add to it only by appending after their text in body colour, never woven in (2026-11-09「只 append 不改合作者的话」) |
| The user | text the user typed into the doc, and every ruling | Same as a co-author's text |

Two exceptions let us change a co-author's sentence: the user names the spot and the new wording (「你直接改成 …」), or the co-author agrees to a listed set of fixes (「她说她的 4 处你可以改正确」). Change exactly those, put the changed sentence in our colour, and log the consent with its date.

"Keep the latest" applies to our own superseded versions only; a co-author's older version stays in the doc (it is simply not given to the blind reader, [wording-pass.md](wording-pass.md) § 1).

## 2. Their version or ours: wording or substance

When a co-author's version of a passage differs from ours, sort each difference (user 2026-11-12「一些无关紧要的措辞就用她的, 需要讨论的就在 doc 上注」):

| Kind | Examples | What to do |
|---|---|---|
| Wording only | a different thanks opener, another order of the same facts, an equivalent description, a warmer closing | **Use theirs.** Sync it into the canonical file verbatim and drop our version. Withdraw any note of ours that only suggested style ("reads awkwardly", "250 said twice", "including … lists all of them") |
| Placeholder | `[X] pt`, `Table [N]`, `Appendix [L]` | Fill it in the canonical file from the primary source (§ 3). Their doc text keeps the bracket; a note lists the values |
| Clear slip | "we have make", a wrong word ("pivot" for "pivotal"), "your comment … addressed them" | Not changed by us. One short note lists the fix for them; the canonical file takes their text verbatim and is re-synced once they fix it |
| Substance | a concession, a revision promise the user has not approved, an overclaim (calling a model "SoTA" that the human study rated well below another), a number or fact that disagrees with its source, a conflict with a ruling, a comment pushed over the limit | Highlight and note (§ 4), and list it under the board's open decisions. The canonical file keeps the approved text until the group decides |

A paragraph that carries any substance item waits as a whole: do not sync its wording-only parts piecemeal, or the canonical file ends up with half of a paragraph whose other half is still under discussion. Say in the report which paragraphs wait and why.

## 3. Check against the source, not against our board

Before marking a co-author's sentence wrong, check it against the primary source: the revised paper build (figure and table numbers, appendix letters and captions from the `.aux`, figure commits), the results files, the review text. Never against our own board or notes, which may be the stale copy.

Lesson (2026-11-12): a co-author's A2 described the redrawn figure ("We removed the ring of direct nouns … The caption and the sentence in Section 3.1 … have been updated"). We first reported it as wrong because our own to-do line on the board still described an earlier design of the same figure. The revision build and the figure's commit history showed their description was right and our line was stale. When this happens, update our text, mark nothing in theirs, and tell the user plainly which earlier statement was wrong.

## 4. Marking a co-author's text

- Highlight the exact phrase (yellow) and put one short note in a third colour (red; neither the co-author's colour nor body text) at the end of that paragraph, or leave a doc comment (user 2026-11-10「你就想办法标出来, comment, 或者用不同颜色 指出这里是错的」).
- Date the note and keep it to what is wrong and what it clashes with: 【注（11-12）：…】. Point to the ruling or the number; propose a fix only for substance and slips, never for style (§ 2).
- Notes are ours: update them when facts change, delete them with their highlight once resolved, and strip them from anything pasted.
- Mirror the note's facts in the notes section of the canonical response file, so the next session sees the open point without opening the doc.

## 5. Sync direction

- **Co-author text: doc → canonical, verbatim.** Never the reverse. Normalize only markup (escapes, chips), not words.
- **Our text: canonical → doc.** Where co-authors edit the doc, change our spans in place with targeted edits; never rebuild the doc wholesale from local files, which erases their text.
- **Translations are ours.** When a co-author's English changes, retranslate it in the canonical file and the doc; keep placeholders as the English has them.
- After any sync, regenerate the derived views (collaborator doc, HTML board) and re-measure the comment lengths (lint 6). If a render gate refuses a file another session edited (internal names, paths), fix the offending line in our notes and say so.
- Diff every draft paragraph in the doc against the canonical files before editing. A passage synced late can sit stale in the doc while the files have moved on.

## 6. Comments and suggestions

- Read every comment thread, open suggestion and direct edit before touching the doc. Each needs its own read: the Drive text export (`read_file_content` with comments) carries threads but not suggestions; suggestions come from the Docs API (`read_doc`: `suggestions[]` and the `suggested*Ids` on text runs). Direct edits show up only as a diff against the canonical files.
- In the status report, list co-author comments that are still unanswered, especially those that @-mention the user, with their date and what they ask.
- A comment whose anchor text is gone (the co-author deleted it after commenting) is reported as such; do not guess where it belonged.
- The Docs API cannot accept or reject suggestions or resolve threads. Keystroke-fragment suggestions ("Di", "Diff", "Differ" … from one aborted edit) are listed for the user to reject in the web UI.
- Reply to each comment with exactly what changed, quoting the new wording ("Replaced 'It does.' with '…'"), and whether the mirrors (translation, response file) were updated. If the connector cannot post replies, hand the user one line per thread to paste.
- A co-author's edit that conflicts with a user ruling (a revision promise against a ruling not to change the paper for that reviewer, a reply pushed over the character limit) is never applied silently: it goes to the open decisions.
- Record each group decision with its date ("Decided (11-09): the title stays unchanged") in the doc, `ISSUE_BOARD.md` and `REBUTTAL_STATE.md`, and carry it to every reply it touches.
- Edit commented text inside its anchor where the change allows; rewriting the whole anchored span detaches the thread, so say so in the reply list when that cannot be avoided.
- A co-author's worry about the character limit is answered with measured counts per comment, markers stripped (lint 6). When an edit pushes a comment over the limit, re-split at a W/Q boundary.
- Generalize recurring comments, and the moves in text co-authors write themselves, into [rhetoric.md](rhetoric.md) § 6–9.

## 7. Editing the doc safely

- Read the whole doc before the first edit and after every write; send every positional batch guarded by the revision id of the latest read. A rejected batch means someone is typing: read again and rebuild, never drop the guard.
- Apply edits from the highest index down so earlier positions stay valid within one batch.
- Read the result back and check text, colour and highlight before reporting.
