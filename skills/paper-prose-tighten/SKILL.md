---
name: paper-prose-tighten
description: "Cut filler from paper prose: bookkeeping-count enumerations (\"abstained blocks 569 → 551\", \"32 of the 39\", \"discordant pairs 166:103\"), defensive meta-narration (\"we report this rather than claim X\", \"a reader is entitled to know\"), and self-referential audit trail that no reviewer reads. Use when user says \"论文废话太多\", \"不要罗列数量\", \"清理废话\", \"tighten the prose\", \"cut the filler\", \"too wordy\", or before submission when sections read like an audit log instead of an argument."
argument-hint: "[paper-directory-or-section-files]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob
---

# Paper Prose Tighten: Cut the Audit Log Out of the Argument

Tighten the prose of: **$ARGUMENTS**

## Why This Exists

Papers written by an agent that also ran the experiments drift toward a
characteristic failure: **the prose becomes the audit trail.** Every number the
agent verified gets printed, every scope limit it reasoned about gets a
sentence, every alternative reading it considered and rejected gets disclosed.
Each addition is individually defensible — that is exactly why the drift is
invisible from inside. The result is technically accurate prose that a reviewer
cannot read, in which the actual claim is buried under its own provenance.

This is not the same failure as overclaiming, and the fix is not the same fix.
This skill deletes text while holding the claim constant; it never settles what
the claim should be. Run it **after** the claims are settled, never as a
substitute for settling them.

**Composition with `/paper-claim-audit`.** The two are orthogonal, not opposed:
that audit fixes text that is *wrong* (inflated numbers, cherry-picked seeds,
mismatched configs, bad delta arithmetic, captions that disagree with their
table), this one deletes text that is *empty*. Its one scope-facing failure mode
— language must match the evaluation actually run — is a hard stop here too, so
run the audit first and tighten after.

The real hazard is in how audit findings get **applied**. A `WARN` closed by
bolting on one more disclosure sentence manufactures exactly the bloat this skill
removes. Close a finding by **correcting the number, the comparison, or the
claim verb**; reach for a new sentence only when no existing sentence can carry
the correction. If the only thing a proposed edit would change is the precision
of a disclosure's wording, it is not an edit worth making.

## How This Differs From Other Skills

| Skill | Question it answers |
|-------|-------------------|
| `/paper-claim-audit` | Do the numbers in the text match the raw files? |
| `/result-to-claim` | Does the data support this claim at all? |
| `/auto-paper-improvement-loop` | What would an external reviewer complain about? |
| **`/paper-prose-tighten`** | **Which sentences carry no claim and can be deleted outright?** |

## The One Test

For every sentence, and for every number inside a sentence:

> **Does deleting it change what a reviewer would believe or decide?**

If no → delete it. Not soften, not shorten. Delete.

A number survives when **it is the claim**. A number dies when it is
**evidence that the author did the bookkeeping**. Nobody audits a paper by
reading its prose; they read the tables. Counts belong in tables, in the
artifacts, or nowhere.

## The Four Cut Classes

### 1. Bookkeeping enumerations

Internal-state counts, sub-slice denominators, and pair splits printed to show
the work was done.

| Cut | Why |
|-----|-----|
| `abstained blocks $569 \to 551$, so muting perturbs the gate without collapsing it` | the reader needs "the gate does not collapse", not the two integers |
| `an exact $82{:}82$ split of the discordant pairs` | the delta already said "tie" |
| `same-question discordant pairs $166{:}103$` | redundant with the reported delta and its interval |
| `TraceAV is mostly partial ($79$ of $133$), OmniVideoBench complete ($262$ of $307$)` | three parenthetical fractions to support one qualitative sentence |
| `the within-block miss contributes 32 of the 39` | a count of a count |
| `gold slot balance $1135/1134/1135$`, `$851$ each over A/B/C/D` | already in the config table; prose repeats it |

**Rewrite pattern:** keep the *qualitative* fact, drop the arithmetic that
demonstrates it. "muting perturbs the gate without collapsing it" is the whole
content of the first row.

**Keep** a count when it *is* the finding: a denominator that scopes the claim
(`801 of 1,062 questions exceed the whole-clip limit`), a headline delta, an
interval, a rate the argument turns on.

### 2. Defensive meta-narration

Sentences *about* the paper's own reporting discipline rather than about the
system.

- "We report this rather than claim frame-invariance."
- "We make none." / "and we claim none."
- "…which is precisely the overstatement this paragraph is guarding against."
- "We report it because a reader is entitled to know that…"
- "This is evaluation hygiene, not a method contribution, and we count it as such."
- "…rather than letting either stand for the other."
- "which we report rather than average away."

These say *"trust us, we were careful."* A reviewer's trust comes from the
protocol section and the tables. Delete the sentence; if it carried a real scope
limit, that limit survives as **one adjective** on the claim
(`descriptive`, `not significant`, `directional`) — not as its own sentence.

### 3. Alternatives considered and rejected

Narrating the road not taken. "We initially assumed X… Re-running it disproves
that on two counts." "We logged them as reasons rather than running a separate
arm for each." "The saving was quantified on an earlier three-stage variant…
so that ≈58% is not a property of any number reported here."

Keep the conclusion; delete the journey. If the rejected alternative is itself a
contribution (a falsified construction, a negative control that fired), it earns
**one sentence**, not a paragraph.

### 4. Restatement and hedge stacking

The same fact in the topic sentence, in the middle, and in the closing
"therefore" sentence; and hedges layered onto already-hedged claims
("consistent with", "we read as", "in the sense that", "not in the sense that").
Keep one instance, at the position where the reader needs it.

## What NOT To Cut

Deleting text must never upgrade a claim. Hard stops:

- **Never delete a significance qualifier** to make a null read as a win.
  `not significant`, `directional`, `descriptive`, `post-hoc` stay.
- **Never delete a denominator that scopes the claim** (full-denominator rules,
  subset sizes that bound generality).
- **Never delete a protocol difference** that makes a comparison unfair
  (different stack, dropped-failure denominator, different budget).
- **Never delete numbers from tables or captions.** This skill edits *prose*.
  A count moved out of a paragraph is fine precisely because the table keeps it.
- **Never delete a citation or `\cite` key.**

Rule of thumb: cut what proves *diligence*; keep what bounds *scope*.

## Procedure

1. **Scope.** Main text first (`\section` bodies), appendix second. Skip tables,
   captions, and figure code unless the caption itself narrates.

2. **Inventory.** Pull every candidate to a scratch list before editing:

   ```bash
   # numbers-in-prose density, per section
   grep -o '\$[0-9][0-9,{}.\\]*\$' sections/*.tex | sort | uniq -c | sort -rn | head -40
   # bookkeeping shapes: "N of M", "N:M", "N -> M"
   grep -nE '[0-9]+ of [0-9]|[0-9]\{?:\}?[0-9]|\\to [0-9]' sections/*.tex
   # meta-narration stems
   grep -niE 'we (report|claim|make|state|note|stress|log) (this|it|none|them)|rather than (claim|letting|running|averag)|entitled to know|guard(ing)? against|we count it as such' sections/*.tex
   ```

3. **Classify, don't rewrite yet.** Tag each hit cut / keep / rewrite. The
   temptation is to rewrite a bloated sentence into a slightly less bloated one;
   most hits should be **whole-clause deletions**.

4. **Edit.** Prefer deleting a clause over restructuring a sentence — the fewer
   words that move, the smaller the chance of shifting a claim.

5. **Verify the claim set is unchanged.** For each edited paragraph, state in
   one line what it claimed before and after. Any difference is a bug, not a
   tightening. Re-check every hard stop above.

6. **Compile** and report the size change (words or lines per section), plus a
   list of anything you deliberately left because cutting it would have
   loosened a claim.

## Reporting

Report as: sections touched, what was cut by class (1–4), and explicitly
**what was kept and why** — the kept-list is the evidence that tightening did
not become overclaiming. Do not report a "% reduction" as the headline; the
headline is that the argument reads straight through.

## Anti-pattern

Do not run this skill twice on the same text expecting further gain. The second
pass finds nothing safe to cut and starts eating scope qualifiers to justify
itself. One pass, then stop.
