---
name: paper-polish
description: "Polish finished prose with a second AI: a fresh editor subagent runs /paper-prose-tighten (cut only), then /paper-jargon-pass second pass (reword terms), then this skill's references/rewrite.md (active voice with \"we\", cohesion, clarity); the session that owns the text checks every edit (frozen spans byte-identical, numbers unchanged, claim unchanged) before taking it. For paper sections and for rebuttal replies (the rebuttal skill calls it with its own overlay). Use when user says \"润色\", \"过一遍措辞\", \"加强表达和衔接\", \"用 We 主动语态\", \"语言 clarity\", \"让 AI 改一下表达\", \"polish the prose\", \"improve flow\", \"active voice\", or after a section or reply is settled and should read well."
argument-hint: "[paper-dir | section .tex files | reply .md] [— overlay: <file>#<section>] [— frozen: <list or file>] [— ledger: <blind-read ledger>]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, Skill, SendMessage
---

# Paper Polish: cut, reword, rewrite — by a second AI, checked by the owner

Polish: **$ARGUMENTS**

User (2026-11-12): 「我们尽量用 We 这样子的主动语态，你让 AI 给你加强下表达和衔接，以及语言的 clarity」, 「让另一个 AI 润色 … 先 paper prose tighten, 再 paper jargon pass」, 「删和改不要放一个」, 「这一套应该封装为一个单独的 skill, 这样 paper 也能用, 不只是 rebuttal」.

This skill only orchestrates. The rules live in the skills it calls:

| Step | What | Done by | Rules |
|---|---|---|---|
| 1. Blind read | Where does a fresh reader stall? | fresh subagents in parallel, one per share of the scope (or the caller's ledger) | `/paper-jargon-pass` pass 1, or the caller's blind-read file |
| 2. Reconcile | Do the numbers and terms the ledger touched match their sources? | the owner | `/paper-jargon-pass` second pass, 「改之前先对账」 and B 组 |
| 3. Cut | Which sentences carry no claim? | the editor | `/paper-prose-tighten` (cut only) |
| 4. Reword, then rewrite | Terms the reader stalled on; then active "we" voice, cohesion, clarity on what survived | the same editor | `/paper-jargon-pass` second pass (A 组), then [references/rewrite.md](references/rewrite.md) |
| 5. Check | Did any edit move a frozen span, a number or a claim? | the owner | § 5 below |
| 5b. Short last lines | Which paragraphs now end in a line under half the column? | the same editor, again | § 5b below |

**Roles.** The **owner** is the session that wrote the text or holds its evidence. It never does steps 1, 3, 4 or 5b itself: after days with the evidence it no longer sees its jargon, its filler, or a passive that hides who acted. The **editor** is one fresh subagent per unit (one part of a paper section, or one reply). It is not the drafter, and it is not a blind reader.

**Why this order.** Blind read first: it is the only step that cannot be repeated by someone who has seen the evidence. Cut before reword: a term in a sentence that is about to go needs no definition. Rewrite last: a sentence is rewritten once, with its terms settled and its neighbours final. Cutting and rewriting live in different skills and never run as one mixed read.

## Scripts

In `scripts/`, run with `python3`. The owner's mechanical work runs from these, not from code written anew each run. All only read, except `apply_edits.py --write`.

| Script | Step | What it does |
|---|---|---|
| `polish_scope.py <clone> <base>` | 0 | Prose lines changed since commit BASE (git blame), with author, in reading order |
| `blind_pack.py <clone> <pdf> <aux> <scope.tsv> <outdir>` | 1 | Page text, figure canvases, one `in_scope-<k>.txt` per reader with ids, `ids.tsv` |
| `check_edits.py <orig> <edited> --scope <lines>` | 5, 5b | The mechanical checks of § 5; prints only the paragraphs that need a look |
| `apply_edits.py <base> <edited> <target> [--reject <lines>] [--write]` | 5, 5b | Per-paragraph merge of the taken edits onto the real file |

Each script's docstring has its options.

## 0. Inputs

- **Target**: paper sections (`sections/*.tex`, read from the compiled PDF for the blind read) or a reply file. For a paper, the scope is `scripts/polish_scope.py` against the commit the previous polish finished on, with the frozen rows deleted. Text is polished once; after it changes, only what changed is polished again.
- **Frozen spans** — copied unchanged by every step, listed by the owner before step 3:
  - quoted text: a reviewer's words, another paper's sentence, quoted revised-paper text;
  - every sentence a co-author wrote or edited in a shared draft (never reworded or deleted; mark it instead — `rebuttal/references/collaboration.md` § 4 has the convention);
  - wording the user ruled on verbatim;
  - in a paper: the abstract and contribution list, unless the user names them as in scope (`/paper-prose-tighten` class 13 reports, never edits, those);
  - in a paper: the Conclusion, unless the user names it as in scope; the editor lists what it would change there instead (user 2026-11-16「polish skill 不要改 conclusion」).
- **Page count is not the polish's job** (user 2026-11-16「skill 里可以写明 polish 不处理页数」). The polish neither checks nor reports the page limit. It merges no floats, moves nothing to an appendix, and shrinks no figure to save space. Page tightening is a separate pass (`/paper-float-compact`). Short last lines are not a page fix: step 5b clears them because each one is a rule violation in its own paragraph. The same holds for every revision between polishes (user 2026-11-01「不用每次都改页数, 收紧页数可以最后一天再改.」): adding a figure, a table or a sentence never gives way to the page limit, squeezes no float and cuts no sentence to win a page back, and does not report an overflow or offer ways to fix it. The compile check covers only that the paper builds and its references and float numbers resolve. Page tightening is done once, on the last day before the deadline, with `/paper-float-compact`.
- **Overlay** (optional): a caller's file section whose rules win where they differ from the called skills — for example `rebuttal/references/wording-pass.md` § 3 and § 4.1. Pass the whole section; the editor reads it before the skills.
- **Ledger** (optional): a blind-read ledger the caller already produced. If given, step 1 is skipped.
- **Evidence** (user 2026-11-15「不是应该去核对吗」): the result files the text's numbers and scopes come from, and for a paper the table and figure generators and the draft's sources, read-only. The editor checks a fact there before an edit that needs it. Only the blind readers (step 1) are kept away from the evidence.
- **Writing rules** (papers; user 2026-11-15): the absolute paths of the rule files that can govern the unit's text. The polish never breaks them and fixes every violation it finds: prose by the editor, the rest by the owner (§ 5). Per unit:
  - always: `research-paper-writing/SKILL.md`, the paper's `CLAUDE.md`, and the prose rule files that `CLAUDE.md` points to;
  - by section: `research-paper-writing/references/introduction.md` for the introduction, `experiments.md` for experiments and appendix results, `distinguish-prior-work.md` for the introduction and related work;
  - by float: `paper-table-craft/SKILL.md` and the tables directory's `CLAUDE.md` when the unit holds a table caption; `paper-figure-craft/SKILL.md`, `research-paper-writing/references/figures.md` and the figures directory's `CLAUDE.md` when it holds a figure caption.

  A rule file that cannot apply to the unit's text is left out: no edit to the unit can break it, and every editor reads its whole list before it starts. A build or scripts `CLAUDE.md` is the owner's; the editor builds nothing but its scratch copy, with the command the owner gives.

## 1. Blind read

The readers are spawned in interactive sessions too (user 2026-11-27).

If no ledger was passed: for a paper, the owner runs `/paper-jargon-pass` 第 0 趟 (zero reading), compiles, and runs `scripts/blind_pack.py` on the scope; it splits the scope into shares by that skill's 第一趟 rule for parallel readers. Spawn one reader per share in one message, each running 第一趟 with that skill's isolation on `pdf_pages.txt`, `figure_canvases.txt` and its own `in_scope-<k>.txt`, and writing `ledger-<k>.md` to `review-stage/jargon/<UTC timestamp>/` in the paper directory, or to the caller's directory. This is a Tier-2 static fan-out ([`fan-out-pattern.md`](../shared-references/fan-out-pattern.md)): the readers only list stalls, the owner merges them, and without the Agent tool the readers run one after another. The editors of § 3–4 fan out the same way.

While the readers run, the owner does the work that does not need the ledger: the numbers check of the in-scope sentences (step 2), the step-2 checkers, the unit split and the editor briefs.

## 2. Reconcile (owner)

Merge the readers' ledgers as `/paper-jargon-pass` 第一趟 says, then follow its 第二趟 「改之前先对账」 and B 组 paragraphs. Mark each ledger entry: report / C 组 → step 3 / A 组 term → step 4 / no change. A real mismatch stops the polish of that unit until the user rules.

For a paper, also run the `research-paper-writing` checkers once here, before any edit: `research-paper-writing/scripts/check_draft.py` on the introduction and experiments `.tex`, `research-paper-writing/scripts/check_figures.py` on the entry `.tex`. A warning is a pointer, not a finding: read what it points at. One that holds in prose joins the ledger for step 3 or 4; one outside prose goes to § 5. One pass is enough (user 2026-11-15「跑脚本 + polish 感觉一次就行了」): § 5 rejects any edit that adds a warning, so nothing is left for a second round.

## 3–4. The editor

Spawn one fresh subagent per unit, all in one message. A unit is at most about one printed page of in-scope text, cut at a section, subsection or paragraph heading: the slowest editor sets the step's wall time. Record each editor's agent id; step 5b sends it more work. Its prompt contains:

1. the target text, with paragraph ids (for a paper, a scratch copy of the unit's `.tex`; the editor never edits the paper directory or an Overleaf clone);
2. the frozen-span list;
3. the overlay section, if any;
4. the ledger files that hold the unit's ids (`ids.tsv` names the reader of each), with the step-2 dispositions;
5. for a paper, the unit's writing rule files (§ 0), paths only;
6. the evidence paths under `Evidence`;
7. for a paper, the command that compiles a scratch copy of the whole paper into an output directory beside the copy, and the path of `paper-compile/scripts/check_runts.py`, both for step 5b;
8. this instruction, verbatim:

> Read the overlay first; it wins where it differs. Then:
> **Step 3 — cut only.** Invoke `/paper-prose-tighten` and apply its classes to the target directly; its `references/procedure.md` (paragraph map, paragraph split, compile) is the owner's, not yours. Also dispose of the ledger's C 组 entries as `/paper-jargon-pass` 第二趟 says (delete or demote). Do not rewrite for style in this step.
> **Step 4 — reword, then rewrite.** Invoke `/paper-jargon-pass` and run only its second pass (查证 + 改写) on the ledger's A 组 entries whose sentence is still there; its pass 0 and blind read are already done. Then read `<skills>/paper-polish/references/rewrite.md` and rewrite the surviving sentences: active voice with "we" where the authors acted, cohesion, clarity, and merging neighbouring sentences that share a subject or predicate (its § 4). The rewrite never cuts a sentence; report a sentence that looks empty.
> If a skill is not in your skill list, read it by path (`<skills>/paper-prose-tighten/SKILL.md`, `<skills>/paper-jargon-pass/SKILL.md`) and follow it the same way.
> If the prompt lists files under "Writing rules", read them before step 3; where a project rule file and a general one disagree, the project rule holds. No edit in steps 3 or 4 may break one of these rules. Text that already breaks one is fixed only by an edit its step already allows (a cut under a `/paper-prose-tighten` class, a reword, a rewrite); every other violation, including the ones outside prose (table shading and marks, caption placement, figure type size), goes in your list of what you would change but may not, with the rule (file, section) and the place.
> When an edit needs a fact the text does not state (a scope, a comparator, a training set, a step count), look it up in the files listed under "Evidence" and make the edit if they settle it; name the file and table in the change list. Read those files; never edit them.
> Keep one line per original line: a line whose whole text you cut becomes exactly `%CUT`, a split sentence stays on its line, sentences merged under `rewrite.md` § 4 go on the first of their lines and each other one becomes `%CUT`, and you add no line.
> Frozen spans are copied character for character. Never change a number, a citation, an address (table / figure / appendix / §), or the claim of a paragraph; a number that goes with a sentence cut under a step-3 class is a cut, not a change. Add no term, no hedge, no caveat, and no sentence that says something the paragraph did not. Three moves are allowed: splitting a sentence in two on its line, merging neighbouring sentences of one paragraph that share a subject or predicate with every case they stated kept (prefer this to a split: a paragraph should not gain sentences), and stating a premise the text left implicit when an evidence file states it (name the file in the change list). Do not push, and do not touch files outside your scratch directory. Compile nothing before step 5b, and then only your scratch copy.
> Return: the edited text; a change list with one row per edit (paragraph id, before, after, step 3 class / step 4 term / rewrite § 1–4); a list of what you would change but may not (frozen spans, a fact the evidence files do not settle, an edit a writing rule forbids, with the rule), each with the text you would write.
> **Step 5b — short last lines, only when the owner sends them.** The owner names a scratch copy of the whole paper with your taken edits applied. Clear the runts in your list there by the gate in `<skills>/paper-polish/SKILL.md` § 5b, compiling with the command given; a runt the gate sends to the user goes in your list of what you would change but may not. Return the change list as before.

The split and premise moves and the 5b substitutions are user rulings (2026-11-16): 「允许一句话在同一行里拆成两句，也允许把原文隐含的前提写出来」, 「可以替换」. The merge move is a ruling of 2026-11-20: 「尽量合并话语, 不然话语越来越长」.

Paper-only parts of the called skills that need the real repository (paragraph-map script, the build of the real paper, figure generators) are run by the owner after step 5, not by the editor.

## 5. Check every edit (owner)

Run `scripts/check_edits.py <orig> <edited> --scope <in-scope lines> --terms <file> --check-draft <research-paper-writing/scripts/check_draft.py>` on each file of the unit. The terms file lists the frozen names and the significance and scope words whose counts must not change. The script does the extraction and comparison in the list below and prints only the paragraphs that need a look; the claim line is the owner's. Take the editor's text one paragraph at a time. A paragraph's edits are taken only if:

- every frozen span is byte-identical (diff them);
- the multiset of numbers, citations / `\cite` keys, `\ref` labels and addresses is unchanged, except numbers step 3 deleted under a named `/paper-prose-tighten` class (and, in a paper, still present in a table) — extract and compare, do not eyeball;
- the claim is unchanged: one line per changed paragraph, what it claimed before and after. A strengthened or weakened scope, an added reason, a dropped qualifier, or a qualifier moved so that it scopes another clause rejects the edit. A scope or premise the text left implicit and the edit now states passes only if the owner finds exactly that scope or premise in the file the change list names;
- the `/paper-prose-tighten` Hard stops hold;
- no new hedge, caveat, concession or meta-narration (re-run the called skills' greps on the result);
- in a paper, no edit adds a writing-rule warning: `check_draft.py` (and `check_figures.py` when a caption changed) on the text before and after; reject an edit that brings in an ERROR or WARN the text did not have;
- the overlay's own checks pass (the rebuttal overlay adds: house-style items present, verdict sentence bare, lint 10).

Every in-scope heading ends at seven words or fewer (`rewrite.md` § 3; user 2026-11-18「标题太长是不可接受的」). `check_edits.py` lists each longer one, edited or not. A heading still over seven words goes back to its editor with step 5b's runts, or to the user when it is frozen.

A rejected edit is dropped, not repaired: keep the earlier sentence. Do not hand-merge half of an edited sentence into the old one. Pull, then apply the taken edits with `scripts/apply_edits.py <orig> <edited> <real file> --reject <rejected lines> --write`. Other sessions may have changed the real file since the scratch copy was made, so it works per paragraph. A paragraph where they changed a line the editor also changed keeps their version: its edits are dropped, and its sentences go in the report as changed during the polish and not polished (the next polish's scope picks them up). A paragraph where they changed only other lines gets the edits, and the owner runs the § 5 checks again on the merged paragraph. Never merge by hand. For a paper, also fix the writing-rule violations outside prose (table shading and marks, caption placement, figure type size) that the editor listed or a step-2 checker warning showed: yourself, in their generator, unless the fix would change a number, a claim or what a float shows, which goes to the user. Change generated captions in their generator, rebuild, compile, and run `check_runts.py` for step 5b. Save the change list, each row marked taken or rejected with the check that rejected it, next to the ledger as `edits-<unit>.md`.

## 5b. Short last lines (papers)

**The gate.** A paragraph may not end in a line shorter than half its column (a runt). `paper-compile/scripts/check_runts.py` on the compiled PDF lists them. Run it after every pass that edits paper prose, since a cut or a reword reflows the paragraph, and clear each runt inside its own paragraph by shortening: a cut under `/paper-prose-tighten` class 12, a shorter word or phrase for a longer one (`the agent` → `one`), or a reorder inside the sentence. Never a longer sentence, `\looseness` or spacing. Recompile until `check_runts.py` lists none of them. A runt in a frozen span, or one that only a claim-changing cut would clear, goes to the user.

**In the polish.** Other sessions keep pushing while the polish runs, so the runt list is taken from the head, not from the commit with step 5's edits. Pull, compile and run `check_runts.py`. Each runt it reports goes back to the editor whose unit holds its paragraph: `SendMessage` to that editor's agent id, with the runts and a fresh scratch copy of the whole paper at that head. Make one copy per editor: a paragraph's line breaks depend only on its own text, so the editors run in parallel. That head's files are the base for `check_edits.py` and `apply_edits.py` on the runt cuts. A runt in a paragraph outside every unit goes to the editor with the smallest unit; this includes runts in paragraphs the polish did not touch, since drafting leaves them for the polish to clear (paper `CLAUDE.md`). The editor compiles its copy until its runts are gone (the instruction's step 5b). Check its cuts with § 5 and apply them the same way: `apply_edits.py` drops a cut whose paragraph another session changed in the meantime. Then compile the result and run `check_runts.py` once more. Revert a cut whose paragraph now ends in a runt it did not have before. A runt that is still there after this round is listed for the user, not sent round again.

## 6. No acceptance read

The polish ends after step 5b with the report. It sends no acceptance blind read after the edits, in any round (user 2026-11-16「polish 去掉 acceptance blind read , 一次都不做.」): step 1 is the only blind read, and the § 5 checks gate every edit. The rebuttal wording pass, which calls the polish, adds none either (user 2026-11-26「rebuttal 也去掉」).

## Report

In this order: (1) structural findings and bugs from steps 1–2 (contradictions, number clashes) for the user to rule on; (2) what the editor flagged but could not touch; the writing-rule violations outside prose, each with its rule, place and the fix made; (3) cuts by `/paper-prose-tighten` class, with the kept list; (4) term fixes; (5) rewrites by `rewrite.md` section (voice / cohesion / clarity / merge); (6) rejected edits and why, and runts left for the user; (7) the suggested-experiments table below. No "% shorter" headline. Each item of (1) and (2) quotes its sentence and gives the replacement text (one per option when the user must choose), so the user answers with a pick, not with "how would you change it?". A caption that names fewer results than the text (one significant cell, one benchmark, where the text names more) is not a finding: a caption states only the most important one (user 2026-11-22「以后不要汇报了，caption本来就应该只说最重要的」). A caption that contradicts the text, or claims a significance or scope its evidence does not support, is a finding.

**Suggested experiments** (user 2026-11-15「最后加一个 返回一个建议实验的表」). The report ends with one table. It has one row per finding from (1) or (2) that needs new evidence, not new wording. Typical cases:

- a claim whose table cell is missing, or rests on fewer episodes or tasks than the table says;
- a gain or speedup credited to one component when two changed between the compared rows;
- a comparison across different training data, pools or protocols when a matched one is possible.

| Finding | Experiment | What it decides | Cost | Status | Zero-cost alternative |
|---|---|---|---|---|---|
| where, in one line | the smallest run that settles it, holding everything else fixed | which sentence stays, changes or goes, under each outcome | GPU-hours and API spend, from a measured per-episode or per-step rate when one exists | already run (point to the result), queued, or new | the rewrite that holds on the evidence already in hand |

A finding that wording alone can fix gets no row. The table only proposes. Nothing is launched; the user picks the rows.
