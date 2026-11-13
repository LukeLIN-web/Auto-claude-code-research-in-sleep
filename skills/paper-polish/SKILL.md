---
name: paper-polish
description: "Polish finished prose with a second AI: a fresh editor subagent runs /paper-prose-tighten (cut only), then /paper-jargon-pass second pass (reword terms), then this skill's references/rewrite.md (active voice with \"we\", cohesion, clarity); the session that owns the text checks every edit (frozen spans byte-identical, numbers unchanged, claim unchanged) before taking it. For paper sections and for rebuttal replies (the rebuttal skill calls it with its own overlay). Use when user says \"润色\", \"过一遍措辞\", \"加强表达和衔接\", \"用 We 主动语态\", \"语言 clarity\", \"让 AI 改一下表达\", \"polish the prose\", \"improve flow\", \"active voice\", or after a section or reply is settled and should read well."
argument-hint: "[paper-dir | section .tex files | reply .md] [— overlay: <file>#<section>] [— frozen: <list or file>] [— ledger: <blind-read ledger>]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, Skill
---

# Paper Polish: cut, reword, rewrite — by a second AI, checked by the owner

Polish: **$ARGUMENTS**

User (2026-11-12): 「我们尽量用 We 这样子的主动语态，你让 AI 给你加强下表达和衔接，以及语言的 clarity」, 「让另一个 AI 润色 … 先 paper prose tighten, 再 paper jargon pass」, 「删和改不要放一个」, 「这一套应该封装为一个单独的 skill, 这样 paper 也能用, 不只是 rebuttal」.

This skill only orchestrates. The rules live in the skills it calls:

| Step | What | Done by | Rules |
|---|---|---|---|
| 1. Blind read | Where does a fresh reader stall? | a fresh subagent (or the caller's ledger) | `/paper-jargon-pass` pass 1, or the caller's blind-read file |
| 2. Reconcile | Do the numbers and terms the ledger touched match their sources? | the owner | `/paper-jargon-pass` second pass, 「改之前先对账」 and B 组 |
| 3. Cut | Which sentences carry no claim? | the editor | `/paper-prose-tighten` (cut only) |
| 4. Reword, then rewrite | Terms the reader stalled on; then active "we" voice, cohesion, clarity on what survived | the same editor | `/paper-jargon-pass` second pass (A/C 组), then [references/rewrite.md](references/rewrite.md) |
| 5. Check | Did any edit move a frozen span, a number or a claim? | the owner | § 5 below |
| 6. Acceptance | Does a second fresh reader still stall? | a second fresh subagent | `/paper-jargon-pass` 验收 4 |

**Roles.** The **owner** is the session that wrote the text or holds its evidence. It never does steps 1, 3, 4 or 6 itself: after days with the evidence it no longer sees its jargon, its filler, or a passive that hides who acted. The **editor** is one fresh subagent per unit (one paper section, or one reply). It is not the drafter, and it is not the blind reader.

**Why this order.** Blind read first: it is the only step that cannot be repeated by someone who has seen the evidence. Cut before reword: a term in a sentence that is about to go needs no definition. Rewrite last: a sentence is rewritten once, with its terms settled and its neighbours final. Cutting and rewriting live in different skills and never run as one mixed read.

## 0. Inputs

- **Target**: paper sections (`sections/*.tex`, read from the compiled PDF for the blind read) or a reply file. One unit per editor.
- **Frozen spans** — copied unchanged by every step, listed by the owner before step 3:
  - quoted text: a reviewer's words, another paper's sentence, quoted revised-paper text;
  - every sentence a co-author wrote or edited in a shared draft (never reworded or deleted; mark it instead — `rebuttal/references/collaboration.md` § 4 has the convention);
  - wording the user ruled on verbatim;
  - in a paper: the abstract and contribution list, unless the user names them as in scope (`/paper-prose-tighten` class 13 reports, never edits, those).
- **Overlay** (optional): a caller's file section whose rules win where they differ from the called skills — for example `rebuttal/references/wording-pass.md` § 3 and § 4.1. Pass the whole section; the editor reads it before the skills.
- **Ledger** (optional): a blind-read ledger the caller already produced. If given, step 1 is skipped.

## 1. Blind read

If no ledger was passed: a fresh subagent runs `/paper-jargon-pass` 第 0 趟 (papers only) and 第一趟, with that skill's isolation (only the PDF text for its section, no files, no grep). Ledger to `paper/review-stage/jargon/<UTC timestamp>/` for papers, or to the caller's directory.

## 2. Reconcile (owner)

Follow `/paper-jargon-pass` 第二趟's first part: numbers first against the result files and tables, B 组 (contradictions, number clashes, count mismatches) straight to the user, never smoothed over. Mark each ledger entry: report / C 组 → step 3 / A 组 term → step 4 / no change. A real mismatch stops the polish of that unit until the user rules.

## 3–4. The editor

Spawn one fresh subagent per unit. Its prompt contains:

1. the target text, with paragraph ids (for a paper, a scratch copy of the section's `.tex`; the editor never edits `paper/` or an Overleaf clone);
2. the frozen-span list;
3. the overlay section, if any;
4. the ledger with the step-2 dispositions;
5. this instruction, verbatim:

> Read the overlay first; it wins where it differs. Then:
> **Step 3 — cut only.** Invoke `/paper-prose-tighten` and follow it on the target. Do not rewrite for style in this step.
> **Step 4 — reword, then rewrite.** Invoke `/paper-jargon-pass` and run only its second pass (查证 + 改写) on the ledger's A 组 / C 组 entries whose sentence is still there; its pass 0 and blind read are already done. Then read `<skills>/paper-polish/references/rewrite.md` and rewrite the surviving sentences: active voice with "we" where the authors acted, cohesion, clarity. The rewrite never cuts a sentence; report a sentence that looks empty.
> If a skill is not in your skill list, read it by path (`<skills>/paper-prose-tighten/SKILL.md`, `<skills>/paper-jargon-pass/SKILL.md`) and follow it the same way.
> Frozen spans are copied character for character. Never change a number, a citation, an address (table / figure / appendix / §), or the claim of a paragraph. Add no term, no hedge, no caveat, no sentence. Do not compile, push, or touch files outside the scratch copy.
> Return: the edited text; a change list with one row per edit (paragraph id, before, after, step 3 class / step 4 term / rewrite § 1–3); a list of what you would change but may not (frozen spans, scope you cannot verify).

Paper-only parts of the called skills that need the real repository (paragraph-map script, compile, short-last-line gate, figure generators, two clones) are run by the owner after step 5, not by the editor.

## 5. Check every edit (owner)

Take the editor's text one paragraph at a time. A paragraph's edits are taken only if:

- every frozen span is byte-identical (diff them);
- the multiset of numbers, citations / `\cite` keys, `\ref` labels and addresses is unchanged, except numbers step 3 deleted under a named `/paper-prose-tighten` class (and, in a paper, still present in a table) — extract and compare, do not eyeball;
- the claim is unchanged: one line per changed paragraph, what it claimed before and after. A strengthened or weakened scope, an added reason, a dropped qualifier, or a qualifier moved so that it scopes another clause rejects the edit;
- the `/paper-prose-tighten` hard stops hold (no null turned into a win, no scoping denominator lost, no protocol difference left unstated);
- no new hedge, caveat, concession or meta-narration (re-run the called skills' greps on the result);
- the unit is not longer than the text the editor was given;
- the overlay's own checks pass (the rebuttal overlay adds: house-style items present, verdict sentence bare, lint 10).

A rejected edit is dropped, not repaired: keep the earlier sentence. Do not hand-merge half of an edited sentence into the old one. Then apply the taken edits to the real files; for a paper, change generated captions in their generator, rebuild, compile, and run the short-last-line gate (`/paper-prose-tighten` class 12). Save the change list, each row marked taken or rejected with the check that rejected it, next to the ledger as `edits-<unit>.md`.

## 6. Acceptance

A second fresh subagent rereads the final text with the step-1 isolation (`/paper-jargon-pass` 验收 4, or the caller's blind-read file). Done when it produces no new load-bearing entry. It only looks for stalls; it does not cut or rewrite.

## Report

In this order: (1) structural findings and bugs from steps 1–2 (contradictions, number clashes) for the user to rule on; (2) what the editor flagged but could not touch; (3) cuts by `/paper-prose-tighten` class, with the kept list; (4) term fixes; (5) rewrites by `rewrite.md` section (voice / cohesion / clarity); (6) rejected edits and why. No "% shorter" headline.

## Never

- The owner cuts, rewords or rewrites itself, or does a blind read.
- One subagent does the blind read and the editing.
- Cutting and rewriting in one step, or rewriting before the terms are fixed.
- Running the polish twice on the same text (both called skills are one-pass); after a rewrite of a section, run it again only on what changed.
- Taking an edit because it reads better, without the § 5 checks.
- Editing a frozen span, including a co-author's passive sentence.
