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
  - in a paper: the abstract and contribution list, unless the user names them as in scope (`/paper-prose-tighten` class 13 reports, never edits, those);
  - in a paper: the Conclusion, unless the user names it as in scope; the editor lists what it would change there instead (user 2026-11-16「polish skill 不要改 conclusion」).
- **Overlay** (optional): a caller's file section whose rules win where they differ from the called skills — for example `rebuttal/references/wording-pass.md` § 3 and § 4.1. Pass the whole section; the editor reads it before the skills.
- **Ledger** (optional): a blind-read ledger the caller already produced. If given, step 1 is skipped.
- **Evidence** (user 2026-11-15「不是应该去核对吗」): the result files the text's numbers and scopes come from, and for a paper the table and figure generators and the draft's sources, read-only. The editor checks a fact there before an edit that needs it. Only the blind readers (steps 1 and 6) are kept away from the evidence.
- **Writing rules** (papers; user 2026-11-15): the absolute paths of `research-paper-writing/SKILL.md` with its `references/introduction.md`, `experiments.md`, `figures.md` and `distinguish-prior-work.md`; `paper-table-craft/SKILL.md` and `paper-figure-craft/SKILL.md`; the paper's `CLAUDE.md`, the `CLAUDE.md` of its tables, figures and scripts directories where they exist, and every rule file these point to. The rules stay in those files. The polish never breaks them and fixes every violation it finds: prose by the editor, the rest by the owner (§ 5).

## 1. Blind read

If no ledger was passed: a fresh subagent runs `/paper-jargon-pass` 第 0 趟 (papers only) and 第一趟, with that skill's isolation (only the PDF text for its section, no files, no grep). Ledger to `paper/review-stage/jargon/<UTC timestamp>/` for papers, or to the caller's directory.

## 2. Reconcile (owner)

Follow `/paper-jargon-pass` 第二趟's first part: numbers first against the result files and tables, B 组 (contradictions, number clashes, count mismatches) straight to the user, never smoothed over. Mark each ledger entry: report / C 组 → step 3 / A 组 term → step 4 / no change. A real mismatch stops the polish of that unit until the user rules.

For a paper, also run the `research-paper-writing` checkers once here, before any edit: `scripts/check_draft.py` on the introduction and experiments `.tex`, `scripts/check_figures.py` on the entry `.tex`. A warning is a pointer, not a finding: read what it points at. One that holds in prose joins the ledger for step 3 or 4; one outside prose goes to § 5. One pass is enough (user 2026-11-15「跑脚本 + polish 感觉一次就行了」): § 5 rejects any edit that adds a warning, so nothing is left for a second round.

## 3–4. The editor

Spawn one fresh subagent per unit. Its prompt contains:

1. the target text, with paragraph ids (for a paper, a scratch copy of the section's `.tex`; the editor never edits `paper/` or an Overleaf clone);
2. the frozen-span list;
3. the overlay section, if any;
4. the ledger with the step-2 dispositions;
5. for a paper, the writing rule files under `Writing rules`, paths only;
6. the evidence paths under `Evidence`;
7. this instruction, verbatim:

> Read the overlay first; it wins where it differs. Then:
> **Step 3 — cut only.** Invoke `/paper-prose-tighten` and follow it on the target. Do not rewrite for style in this step.
> **Step 4 — reword, then rewrite.** Invoke `/paper-jargon-pass` and run only its second pass (查证 + 改写) on the ledger's A 组 / C 组 entries whose sentence is still there; its pass 0 and blind read are already done. Then read `<skills>/paper-polish/references/rewrite.md` and rewrite the surviving sentences: active voice with "we" where the authors acted, cohesion, clarity. The rewrite never cuts a sentence; report a sentence that looks empty.
> If a skill is not in your skill list, read it by path (`<skills>/paper-prose-tighten/SKILL.md`, `<skills>/paper-jargon-pass/SKILL.md`) and follow it the same way.
> If the prompt lists files under "Writing rules", read them before step 3; where a project rule file and a general one disagree, the project rule holds. No edit in steps 3 or 4 may break one of these rules. Text that already breaks one is fixed only by an edit its step already allows (a cut under a `/paper-prose-tighten` class, a reword, a rewrite); every other violation, including the ones outside prose (table shading and marks, caption placement, figure type size), goes in your list of what you would change but may not, with the rule (file, section) and the place.
> When an edit needs a fact the text does not state (a scope, a comparator, a training set, a step count), look it up in the files listed under "Evidence" and make the edit if they settle it; name the file and table in the change list. Read those files; never edit them.
> Frozen spans are copied character for character. Never change a number, a citation, an address (table / figure / appendix / §), or the claim of a paragraph. Add no term, no hedge, no caveat, no sentence. Do not compile, push, or touch files outside the scratch copy.
> Return: the edited text; a change list with one row per edit (paragraph id, before, after, step 3 class / step 4 term / rewrite § 1–3); a list of what you would change but may not (frozen spans, a fact the evidence files do not settle, an edit a writing rule forbids, with the rule).

Paper-only parts of the called skills that need the real repository (paragraph-map script, compile, short-last-line gate, figure generators, two clones) are run by the owner after step 5, not by the editor.

## 5. Check every edit (owner)

Take the editor's text one paragraph at a time. A paragraph's edits are taken only if:

- every frozen span is byte-identical (diff them);
- the multiset of numbers, citations / `\cite` keys, `\ref` labels and addresses is unchanged, except numbers step 3 deleted under a named `/paper-prose-tighten` class (and, in a paper, still present in a table) — extract and compare, do not eyeball;
- the claim is unchanged: one line per changed paragraph, what it claimed before and after. A strengthened or weakened scope, an added reason, a dropped qualifier, or a qualifier moved so that it scopes another clause rejects the edit. A scope the text left implicit and the edit now states passes only if the owner finds exactly that scope in the file the change list names;
- the `/paper-prose-tighten` hard stops hold (no null turned into a win, no scoping denominator lost, no protocol difference left unstated);
- no new hedge, caveat, concession or meta-narration (re-run the called skills' greps on the result);
- in a paper, no edit adds a writing-rule warning: run `research-paper-writing/scripts/check_draft.py` (and `check_figures.py` when a caption changed) on the text before and after, and reject an edit that brings in an ERROR or WARN the text did not have;
- the overlay's own checks pass (the rebuttal overlay adds: house-style items present, verdict sentence bare, lint 10).

A rejected edit is dropped, not repaired: keep the earlier sentence. Do not hand-merge half of an edited sentence into the old one. Then apply the taken edits to the real files. For a paper, also fix the writing-rule violations outside prose (table shading and marks, caption placement, figure type size) that the editor listed or a step-2 checker warning showed: yourself, in their generator, unless the fix would change a number, a claim or what a float shows, which goes to the user. Change generated captions in their generator, rebuild, compile, and run the short-last-line gate (`/paper-prose-tighten` class 12). Save the change list, each row marked taken or rejected with the check that rejected it, next to the ledger as `edits-<unit>.md`.

## 6. Acceptance

A second fresh subagent rereads the final text with the step-1 isolation (`/paper-jargon-pass` 验收 4, or the caller's blind-read file). Done when it produces no new load-bearing entry, or after the second acceptance read of the same change, whichever comes first. A reread of fixes counts as a round. After the second read, the owner fixes only real errors (a wrong number, an overclaim, a contradiction), lists the rest for the user, and sends no third reader. Each fresh reader finds something new, so "read until clean" never stops. It only looks for stalls; it does not cut or rewrite.

## Report

In this order: (1) structural findings and bugs from steps 1–2 (contradictions, number clashes) for the user to rule on; (2) what the editor flagged but could not touch; the writing-rule violations outside prose, each with its rule, place and the fix made; (3) cuts by `/paper-prose-tighten` class, with the kept list; (4) term fixes; (5) rewrites by `rewrite.md` section (voice / cohesion / clarity); (6) rejected edits and why; (7) the suggested-experiments table below. No "% shorter" headline.

**Suggested experiments** (user 2026-11-15「最后加一个 返回一个建议实验的表」). The report ends with one table. It has one row per finding from (1) or (2) that needs new evidence, not new wording. Typical cases:

- a claim whose table cell is missing, or rests on fewer episodes or tasks than the table says;
- a gain or speedup credited to one component when two changed between the compared rows;
- a comparison across different training data, pools or protocols when a matched one is possible.

| Finding | Experiment | What it decides | Cost | Status | Zero-cost alternative |
|---|---|---|---|---|---|
| where, in one line | the smallest run that settles it, holding everything else fixed | which sentence stays, changes or goes, under each outcome | GPU-hours and API spend, from a measured per-episode or per-step rate when one exists | already run (point to the result), queued, or new | the rewrite that holds on the evidence already in hand |

A finding that wording alone can fix gets no row. The table only proposes. Nothing is launched; the user picks the rows.

## Never

- The owner cuts, rewords or rewrites itself, or does a blind read.
- One subagent does the blind read and the editing.
- Cutting and rewriting in one step, or rewriting before the terms are fixed.
- Running the polish twice on the same text (both called skills are one-pass); after a rewrite of a section, run it again only on what changed.
- Taking an edit because it reads better, without the § 5 checks.
- Editing a frozen span, including a co-author's passive sentence.
