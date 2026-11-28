---
name: paper-prose-tighten
description: "Cut filler from paper prose while holding every claim constant — bookkeeping counts, defensive meta-narration, narrated absences / 无中生有, false pivots / 错误的转折, value series / 罗列, cross-section duplication, related-work sprawl, wordy phrases where one word does, process vocabulary (\"preregistered\"), one comparison split across sentences and copies of it that disagree, exception clauses (\"all but X\", \"except X\"), claims that survive only behind a pile of caveats, and anything that supports no claim of the paper. Use when user says \"没有支持任何论点\", \"这句支持什么论点\", \"这个放这里干嘛\", \"不应该出现 all but / except\", \"例外从句\", \"论文废话太多\", \"caveat 太多\", \"越讲越乱\", \"别解释了\", \"不要罗列数量\", \"清理废话\", \"无中生有\", \"错误的转折\", \"我要删减文字\", \"不该出现这种工程的术语\", \"related work 太长\", \"能用少词就不用多词\", \"重复也太多了\", \"说一次就行\", \"前后对不上\", \"tighten the prose\", \"cut the filler\", \"too wordy\", or before submission when sections read like an audit log."
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

## The One Test

For every sentence, every number inside it, and every larger unit (a paragraph,
a reported experiment, an example, a method detail, a pointer to a float):

> **Which claim of the paper does it support?**

Name the claim. No claim → delete it. Not soften, not shorten, not move to a
quieter spot in the main text. Delete. (User ruling 2026-11-21:
「如果一个东西没有支持任何论点, 就应该删了」.)

A unit supports a claim when it does one of four things:

- it **states** the claim;
- it is **evidence** for it (a result, a comparison, the reason for a gain, a
  confound ruled out);
- it **defines** what the claim is about (a term, the setup, a protocol constant
  a column uses);
- it **bounds** the claim (a denominator, a scope limit, a result that weighs
  against it).

Nothing else earns a place. That it is true, that it took effort to obtain,
that it is interesting, that a reviewer might ask, and that it was already in
the draft are not claims. The equivalent check from the reader's side: deleting
it changes nothing a reviewer would believe or decide.

The test applies at every size, and the larger the unit the larger the cut. A
paragraph reporting an experiment that no claim rests on goes whole, with its
pointer to the float; the appendix may keep the experiment as a record. The
float itself is then the authors' call: report it, and do not delete it here
(hard stops).

Supporting *something* is not enough: the claim must be one the paper makes (in
the abstract, a contribution, a section's verdict). When a unit would support a
claim the paper never states, the skill does not add that claim. Either an
existing sentence already implies it and takes a few words to say so, or the
unit is listed for the author as "supports no stated claim" and cut.

A number survives when **it is the claim**. A number dies when it is
**evidence that the author did the bookkeeping**. Nobody audits a paper by
reading its prose; they read the tables. Counts belong in tables, in the
artifacts, or nowhere.

In a results section, write down for every number the claim it supports (the
paragraph's verdict, a gain's reason, a confound it rules out, a contribution it
backs). No claim → the number goes; an implied claim → the sentence states it
in a few words, never wider than the evidence. The rule and its edge cases:
`../shared-references/manuscript-craft.md` §2, Experiments ("Every number argues
for a claim").

## The Escalation: Caveat Pressure Means Cut the Claim

A sentence that needs one qualifying clause to be true is a sentence to fix. A
sentence that needs two or three is a sentence the paper is better off without,
and the caveats are the diagnosis rather than the disease. The more you explain,
the messier it gets.

> **If the honest version of a claim takes a pile of caveats, delete the claim.**

This is the escalation of the audit-application rule above, and it fires on
*secondary* claims — a supporting dose curve, a corroborating subset, a "we also
checked" reading — never on a headline. The test is what the paper loses: a
load-bearing claim keeps its caveats because both are load-bearing; a
nice-to-have leaves with its caveats attached, and the section reads straight
through for the first time.

When an author says the explanation itself is the problem, they are exercising
this rule — do not answer it with a better-worded explanation.

## The Fourteen Cut Classes

### 1. Bookkeeping enumerations

Internal-state counts, sub-slice denominators, and pair splits printed to show
the work was done.

| Cut | Why |
|-----|-----|
| `active channels $612 \to 597$, so blurring perturbs the mask without collapsing it` | the reader needs "the mask does not collapse", not the two integers |
| `an exact $64{:}64$ split of the discordant pairs` | the delta already said "tie" |
| `same-image discordant pairs $151{:}97$` | redundant with the reported delta and its interval |
| `A is mostly partial ($37$ of $60$), C complete ($170$ of $190$)` | three parenthetical fractions to support one qualitative sentence |
| `the small-object miss contributes 27 of the 33` | a count of a count |
| `label balance $1204/1203/1204$`, `$903$ each over the four classes` | already in the config table; prose repeats it |

**Rewrite pattern:** keep the *qualitative* fact, drop the arithmetic that
demonstrates it. "blurring perturbs the mask without collapsing it" is the whole
content of the first row.

**Keep** a count when it *is* the finding: a denominator that scopes the claim
(`318 of 450 images exceed the native resolution`), a headline delta, an
interval, a rate the argument turns on.

### 2. Defensive meta-narration

Sentences *about* the paper's own reporting discipline rather than about the
system.

- "We report this rather than claim rotation-invariance."
- "We make none." / "and we claim none."
- "…which is precisely the overstatement this paragraph is guarding against."
- "We report it because a reader is entitled to know that…"
- "This is evaluation hygiene, not a method contribution, and we count it as such."
- "…rather than letting either stand for the other."
- "which we report rather than average away."

These say *"trust us, we were careful."* A reviewer's trust comes from the
protocol section and the tables. Delete the sentence; if it carried a real scope
limit, that limit survives as **one adjective** on the claim (`descriptive`,
`post-hoc`) — not as its own sentence. A *null* is the exception: it gets no
adjective at all (see the hard stop below).

### 3. Alternatives considered and rejected

Narrating the road not taken. "We initially assumed X… Re-running it disproves
that on two counts." "We logged them as reasons rather than running a separate
arm for each." "The saving was quantified on an earlier two-pass variant…
so that ≈41% is not a property of any number reported here."

Keep the conclusion; delete the journey. If the rejected alternative is itself a
contribution (a falsified construction, a negative control that fired), it earns
**one sentence**, not a paragraph.

### 4. Restatement and hedge stacking

The same fact in the topic sentence, in the middle, and in the closing
"therefore" sentence; and hedges layered onto already-hedged claims
("consistent with", "we read as", "in the sense that", "not in the sense that").
Keep one instance, at the position where the reader needs it.

### 5. Narrated absences (无中生有)

Prose whose grammatical subject is something that does not exist:

- "Benchmark X publishes no row for this backbone and has no column for it."
- "X does not report Y for this setting."
- "No official number exists for Z."

A full sentence spent on an empty cell, an experiment nobody ran, a baseline
nobody published. It reads like diligent disclosure — which is why it survives
draft after draft. The deciding test: **can the reader see the gap in the
artifact?** A dash in a cell, a reduced $n$, a row missing from an enumerated
suite — visible, so the absence is load-bearing and lives as one terse legend
clause (`a dash = none published`; `Benchmark X has no baseline arm.`),
never as a narrative sentence. An entity that was never in the table at all —
invisible, delete. The same surface shape gets both verdicts: the two examples
above differ only in whether the table shows the hole being explained.

This class concentrates **in captions**, where authors explain table gaps:
sweep captions for it too, and cut a generated caption (an `AUTO-GENERATED`
header) in its generator script, or the next build resurrects the sentence.

**Keep** an absence statement also when the absence *is* the claim ("no prior
benchmark evaluates X and Y jointly" as a motivation sentence)
or when it states a protocol fact a reviewer would otherwise assume the other
way ("no test-set molecules appear in training").

### 6. False pivots (错误的转折)

A claim delivered as the correction of an alternative nobody proposed: the
sentence erects a reading, negates it, and only then states the claim. The
negated half is the author debating themselves; the positive half is the whole
content.

- "The advantage is also not reducible to the filters the pruner had to
  drop: sorting the same images by the share of the dense model's filters the
  baseline kept, \method leads inside every level of that sparsity." →
  "\method leads at every level of the baseline's sparsity." The
  reviewer had not yet formed the reading being rebutted.
- "X rather than Y" where Y is the author's own invention: delete "rather
  than Y", keep X. "the grid is ordered by two properties of the molecules
  rather than by the dataset" → "the grid is ordered by two properties of
  the molecules."
- "not A but B" → "B".

**Rewrite pattern:** delete everything from the pivot word on ("rather than
…", "not … but", "is not reducible to …") and let the positive claim stand
alone. If the sentence opens with the negation, the rewrite is the positive
claim, stated directly. When the negated half is the only place a protocol or
scope fact is stated (`a held-out annotator, not the benchmark script, scores
each answer`), the fact stays: restate it positively (`scores each answer in
place of the benchmark script`), per (b) below and the protocol hard stop.

**Field notes.**
(a) Sweep headers, titles and captions by eye: sentence-lead negations ("Nor
is the gain fully accounted for by…"), negative `\paragraph` headers, caption
bold titles ("The resolution, not the dataset, sets…") and question-form
section titles do not match a "rather than" grep.
(b) Deleting the "rather than Y" tail is usually scope-safe because the
surviving X carries the scope itself ("a same-hardware anchor", "third-party
reads", "systems as published"). When the negated half is the *only* scope
carrier, restate it positively ("same-weights, cross-protocol comparison")
— the hard stops below still forbid dropping the scope.
(c) **The concessive scope hedge** — `X, although Y`, `X, each a Y`,
`although X grows, Y is bounded` — is a class-6 shape even when Y is real
scope, and it is the highest-yield sub-shape left after the obvious pivots
are gone. It looks like a hard stop, but the passage usually states the same
scope **positively** a sentence or a subsection away, and then the hedge is
class-4 restatement.

**The procedure, in order:** grep the scope's own noun (`hardware`, `forwards`,
`denominator`) across the passage and the neighbouring section. Scope found
stated positively → delete the concessive, nothing is lost. Scope found
nowhere else → move it into the sentence that owns it as a plain assertion,
then delete the concessive. Do not reinstate the concessive as the fix.

**Repo ruling (2026-08-20).** The author's words: 「范围 也删了 … 防止「全都是
⟨property⟩」的过度主张, 不同 ⟨setup⟩ 这些都要删」. Author-facing framing
matters here: do not answer this instruction with a defence of the hard stop.
Run the grep, report where the scope still lands, and cut.

### 7. Cross-section duplication (跨节重复)

Two paragraphs in different sections carrying the same content at different
resolutions. Individually each reads fine; the duplication is only visible from
the paragraph map (`references/procedure.md` step 1), never from reading straight through — by
the time the reader reaches the second copy, the first is 8 pages back and the
author has forgotten writing it.

The recurring shapes, in descending yield:

| Shape | Fix |
|-------|-----|
| An intro **contribution bullet that pre-plays a whole results subsection** — the same sensitivity grid, the same axes, the same per-benchmark ordering | Do not edit: the authors write the contribution list (class 13, last row). Report the overlap and what the bullet could drop. |
| A finding stated in a results **subsection** and again as a **conclusion/analysis bullet** | Keep the results copy; delete the bullet — unless the bullet carries something the subsection does not (see the hard stop below). |
| The method's governing **principle** stated informally in the intro and formally in the method | Intro keeps the hazard in one sentence and cites `\S`; the formal statement, the decomposition, and the concrete quotas live once, in the method. |
| A **scaling / cost / budget** argument in the intro and again in a "Bounded X" method subsection | Same rule: the intro asserts the property, the method derives it. |
| The **motivation** ("full-resolution images are too large to fit") in the intro and again in Settings | Settings keeps only what scopes the *experiment* (which benchmarks exceed the memory limit). |

**Rewrite pattern:** decide which section is the fact's semantic owner —
normally the one that *derives* rather than *asserts* it — and reduce every
other copy to a claim plus a `\S\ref{}`. This is SSOT applied to prose.

**Keep** the second copy when the two are at genuinely different resolutions and
the reader needs both: an intro one-liner and a method derivation are not
duplicates. The test is whether the second copy contains a *number, a
comparison, or a mechanism* the first does not.

### 8. Artifact provenance and hygiene assurance

Sentences whose subject is *how the artifact was produced* rather than what the
system does: which checkpoint was deployed and how it was picked, which split a
curve was flat on, which seed, which stopping rule, what the choice was *not*
made with reference to. They read as reproducibility, which is why they survive
every pass — but reproduction reads the config table, not the prose.

| Cut | Why |
|-----|-----|
| `the released checkpoint is the run's endpoint, fixed without reference to any evaluation signal, so neither pruning level's checkpoint is chosen by benchmark performance` | asserts the absence of cherry-picking; a config table naming the endpoint already carries it |
| `held-out accuracy is flat from step $400$ through $1200$`, in a config-table cell | a second curve nobody plots, on a set nobody else in the paper names |
| `step $1500$, selected by a pre-specified stopping rule inside epoch 2` | the *rule* may be a reproduction fact; `pre-specified` is the assurance — drop that word, keep the rule |
| `on a frozen evaluation subset, accuracy rises across every checkpoint measured` | the subset's identity is bookkeeping; `accuracy rises across the measured checkpoints` is the claim |

**Rewrite pattern:** a checkpoint's *identity* is configuration and belongs in
the config table as a bare value (`step 1200, the run's endpoint`). Everything
about how it was chosen, what it was not chosen by, and what else was flat
where — delete.

**Keep** a provenance fact when a reviewer could otherwise reconstruct a
*different* experiment: the split a headline number is scored on, a train/test
separation, a denominator rule, a protocol the comparison depends on. Those are
hard stops below, not class-8 hits.

**When a reviewer flags two class-8 sentences as disagreeing, delete both.**
Naming the two sets they describe spends sentences defending a supporting
claim.

### 9. Process vocabulary (流程/工程术语)

The words we use to *run* experiments, leaking into the words the paper is
*written* in: `preregistered`, `pre-specified`, `criteria frozen before any
results were read`, `frozen before any test number was read`, `the frozen margin`, `a
frozen evaluation set`, `stopping rule`, `early-kill gate`, `acceptance gate`.

Classes 2 and 8 walk straight past these, because a class-9 hit is an
**adjective on a real result**, not a sentence of its own: the noun it modifies
is load-bearing, the sentence survives the paragraph map intact, and nothing
looks deletable. It is also the one class that says nothing to the reader it
means to reassure — a reviewer cannot check that a margin was fixed before the
results were read, so the word is an assertion about our internal timeline, and asserting
it invites the suspicion it was meant to settle.

| Cut | Keep |
|-----|------|
| `a preregistered two-benchmark ablation` | `a two-benchmark ablation` |
| `With criteria frozen before any new results were read, we re-measured …` | `We re-measured …` |
| `non-inferior at a margin frozen before any results were read` | `non-inferior` — the margin's value lives in the appendix |
| `passes the preregistered non-degradation gate` | `does not degrade` |
| `selected on a dev split before any test number` | `selected on a dev split` |
| `well under the $0.40$ early-kill gate` | `well under $0.40$` |
| `the paper's frozen default configuration` | `the paper's default configuration` |

**Rewrite pattern:** delete the modifier, keep the noun. Unlike class 8 the
sentence almost never dies — an ablation that was preregistered is still an
ablation, and the result it reports is untouched.

**Keep** `frozen` in its *technical* sense, which shares the word and nothing
else: `frozen backbone`, `frozen pruning mask`, `frozen BatchNorm statistics`, `frozen
tokenizer`, `frozen protocol` describe weights and configuration that do not
move. `frozen before …` describes when *we* looked. Only the second is a hit.

**Keep** the object a process word modifies when that object scopes the claim: a
non-inferiority **margin** bounds what "non-inferior" means and stays (its
value in the appendix); only the story of when it was fixed goes.

**Ruling (user 2026-08-20).** 「preregistered 都删了, 论文里就不该出现这种工程的术语. 记住」.

Before retiring a whole verification apparatus (a probe, its null, a negative
control) under this class, run the file-drawer hard stop's test below.

**Sweep note.** Count each term separately (the per-term counts are what you
report), and call GNU grep as `command grep`: in Claude Code's Bash, `grep` is a
function that runs ugrep with `--ignore-files`, so a recursive grep from a
parent directory silently skips every gitignored file. Then sweep the copies outside `sections/`:
figure/table generator strings in `paper/scripts/*.py` and `label` fields in
`paper/data/*.json` render into the PDF too.

### 10. Value series across conditions (罗列)

One quantity's readings at three or more conditions — severity levels,
benchmarks, checkpoints, compression rates — strung through a sentence with
slashes or commas. It is a table row read out loud.

| Cut | Why |
|-----|-----|
| `top-1 accuracy is $94.2$ / $89.5$ / $90.1$ / $78.6\%$ across the four corruption levels` | the same sentence already says it: *falls with severity* |
| `pruning order within a layer does not matter, at $71.2$ / $71.6$ / $72.9$ / $72.3\%$` | "does not matter" **is** the reading; the four numbers only prove we looked |
| `$+0.6$pp on A, $+0.9$ on B, $-1.4$ on C and $+0.2$ on D --- bounded by $1.4$pp` | the bound is the claim; the four values are its raw material |
| `median $4$ / $6$ / $3$ / $3$ on A / B / C / D` | one adjective — "single-digit" — carries all four |
| `$52.1\%$ at base, then $55.0$ / $56.8$ / $56.9\%$ at steps $200$ / $500$ / $1000$` | "rises monotonically, flattening after step 500" is the whole content |
| `$76.4\%$ of the decisive atoms within one bond, $95.1\%$ within three, none more than six` | keep the bound the message-passing depth is compared against, drop the ladder under it |

A series always exists to show a **shape** — monotone fall, flat, one condition
out of line. A reader cannot hold four numbers and does not try: they take the
shape word and skip the digits. So write the shape and delete the digits. **A
series is never load-bearing as a series**; if its shape is not worth one word,
the sentence was not worth keeping either.

**Rewrite pattern:** keep the shape word (`falls with severity`, `does not matter`,
`holds level`, `single-digit`, `rises monotonically`), point at the table or
figure if one carries the values, and keep at most the **one** number the
argument turns on — a bound, or a ceiling the series is measured against.

**Not this class** — two values in contrast (`$41.06\%$ when a kept channel
fires on the object and $12.73\%$ when none does`), a range or IQR (`conversion
rates span $0.21$ to $0.47$`), and a pair whose *near-equality* is the claim
(`keeps a median $27.3\%$ of the dense model's FLOPs against a target budget
of $26.9\%$`). Those are comparisons, not enumerations.

**The appendix is not exempt.** The rule that lets an appendix keep
numbers (`paper-table-craft`, *Result numbers in the prose*) exempts *isolated* numbers that no figure carries —
never a series. Appendices are where this class survives a body-only sweep:
every hit of the ruling that created the class was in one.

**Ruling (user 2026-08-24).** 「严格禁止」. Class 1 walks past these: they are
not counts, denominators or pair splits but *results*, each a number the paper
may report. The defect is the enumeration, not the digit.

### 11. Related-work sprawl (相关工作写太多)

The rule lives in `../shared-references/manuscript-craft.md` (Background /
Related Work): two paragraphs, one per line of prior work. Related work outgrows
it the way the audit log does. Every paper a novelty search turns up earns its
own sentence, every near neighbour earns its own paragraph, and every paragraph
closes on how we differ.

| Cut | Why |
|-----|-----|
| a paragraph for a family the method answers the same way as another (pruners that score weights by magnitude, split off from pruners that score them by gradient) | one line of work; its works join the paragraph whose gap they share |
| `X does A. Y does B. Z does C.`, one sentence per work | one clause per work inside a cluster: `prune by second-order saliency~\cite{x,y,z}` |
| a closing sentence on how our method differs | belongs in the method's Advantages paragraph |

**Rewrite pattern:** name the lines of work the method answers (usually two: the
systems it builds on and the training it changes). For each, write one
paragraph: the line's shared design in a sentence, its variants as cite
clusters with one clause each, and the gap they all share as the last sentence.
Then diff the cite-key set, which must come back empty:

```bash
keys() { grep -o '\\cite[a-z]*{[^}]*}' | sed 's/^[^{]*{//; s/}$//' | tr ',' '\n' | tr -d ' ' | sort -u; }
diff <(git show HEAD:sec/2_related.tex | keys) <(keys < sec/2_related.tex)
```

Every key stays (Hard stops). A work that shrinks to one key in a cluster is
still cited, and concurrent work is still cited and discussed.

**Ruling (user 2026-11-01).** 「一般 related work 两段就行了, 你写的也太多了」.

### 12. Wordy phrases (能用少词就不用多词)

Several words where one word the reader already knows says the same thing.
Drafting from notes, the agent describes a property instead of naming it. Each
cut saves a word or two, so the class is many small edits, not one big one.

| Cut | Write |
|-----|-------|
| `can carry out cross-file and loosely worded completion requests` | `can follow cross-file and vague completion requests` |
| `We refer to the drafter together with the verifier and the test runner it calls as the system` | `We call the drafter, verifier and test runner the system` |
| `It meets the repository's private APIs ... for the first time at deployment` | `It first meets the repository's private APIs ... at deployment` |
| `trains on the public split together with the files collected on ...` | `trains on the public split and the files collected on ...` |
| `none of them in Bench-7's evaluation set` | `none in Bench-7's evaluation set` |
| `calls linting or formatting tools` | `calls lint or format tools` (the method section's name for them) |
| `with the drafter fine-tuned on X, the system succeeds significantly less often than with the frozen drafter` | `fine-tuning on X performs significantly worse than the frozen drafter baseline` |
| `succeeds significantly more often than with it fine-tuned on Y` | `achieves significantly higher success rates than fine-tuning on Y` |
| `The type annotations are what make fine-tuning help` | `The type annotations are the primary driver` |
| `fine-tuned, half and half with The Stack, on the in-house repositories` | `fine-tuned on the in-house repositories mixed 1:1 with The Stack` |
| `fine-tuning the drafter has been reported to lower the success of the whole pipeline` | `naively fine-tuning the drafter often degrades overall pipeline success` |

**Rewrite pattern:** first look for a word the paper already uses (`vague` is
already the paper's word for underspecified requests; `lint and format tools` is the method
section's term), then for the field's usual word or phrase. Swap only when the
short form means the same thing.

**Comparisons take the field's result verbs.** `X performs (significantly)
worse than Y`, `X achieves (significantly) higher success rates than Y`, `X
(significantly) outperforms Y`, never `the system succeeds (significantly)
less / more often with X than with Y`. The thing compared becomes the subject
(`fine-tuning on The Stack alone performs worse than ...`), and the comparator is
named as a baseline, not as a second `with` clause. `more often` stays only for
how often a behavior happens (`imports the named module first more often`), not
for success.

**Not this class** (all from the same draft, all kept):

| Kept | Why |
|------|-----|
| `is not significantly different from` | the project's allowed wording for a null that matters |
| `leaves the verifier in place` | `unchanged` says something else |

Also kept: a qualifier that is the claim or bounds it (`significantly`,
`new repositories from the same crawl`), a term the paper defines
(`lint-guided decoding`), and official benchmark and model names.

**Read every sentence; grep only helps with recall.**

Before keeping a phrase because no single word replaces it, try the field's
standard phrasing.

Cutting words reflows paragraphs; the short last lines a pass leaves are
cleared with cuts from this class in `paper-polish` step 5b.

**Rulings.** User 2026-11-03: 「论文应该能用少词的就不要用多个词, 比如 loose worded
就应该写成 vague」. User 2026-11-11: 「performs worse 是对的, succeeds less often
是不好的写法」.

### 13. One comparison split across sentences, and copies that disagree (同一个比较说好几遍、各处副本对不上)

The same verb against the same baseline, repeated sentence after sentence, each
time with one or two new conditions. This happens when results are added one at
a time as runs finish: each new benchmark gets its own sentence with an `also`.
Class 4 misses it because each sentence states a different fact. Class 12 misses
it because each sentence is short.

| Cut | Write |
|-----|-------|
| `Our method significantly outperforms the drafter alone on Bench-1 and on Bench-2, …` / `On Bench-3 our method also significantly outperforms the drafter alone.` / `Our method also significantly outperforms the drafter alone on Bench-4, and outperforms it on Bench-6.` | `Our method significantly outperforms the drafter alone on Bench-1, Bench-2, Bench-3 and Bench-4, and outperforms it on Bench-6 (Table~\ref{tab:main}).` |
| `on Bench-1, on Bench-2, on Bench-4 and on Bench-5` | `on Bench-1, Bench-2, Bench-4 and Bench-5` (the same repetition at word scale) |

**Rewrite pattern:** write one sentence per baseline. The significant conditions
go in one list. Point-estimate leads (`outperforms`, without `significantly`) follow as a second clause
with `it`, so the baseline is named once. A scope that holds for only some
conditions (the held-out 40 repositories on two of the benchmarks) becomes its own
short sentence after the list; do not nest it inside the list. A different table
is no reason to keep a separate sentence: cite both tables. After merging,
re-read every later `both benchmarks`, `either`, `there` in the paragraph,
because the merge changes what they refer to.

**Keep separate:** a different baseline, or a different metric (success rate
against successes with every line from the drafter). A different metric is a
different claim, even when the verb is the same.

**The inventory doubles as the copy check.** A comparison stated in Results
usually has copies in the intro, the method's advantages, the conclusion and the
abstract. A result added later tends to reach one copy and miss the others. For
each baseline, list every sentence in the paper that compares against it
(`references/procedure.md` step 3): section, verb (`significantly outperforms` / `outperforms` /
`completes significantly more tasks with every line its own`), metric, and
conditions. The Results sentence owns the claim. Every copy is a derived form
(SSOT), so a copy that disagrees with Results is a bug in the copy. Fixing it
does not change what the paper claims.

| Mismatch | Fix |
|----------|-----|
| A copy lists fewer conditions than Results (the conclusion omits Bench-3) | Add the missing ones to the copy. A copy that enumerates must enumerate all of them, or use a summary word that is true for all |
| A copy's verb or metric is stronger than the one in Results (`significantly outperforms` where Results has significance only on every-line-own completions) | Weaken the copy to the Results wording |
| A copy states a condition Results never states (`outperforms it on Bench-7` in the intro and conclusion only) | If the table shows it at the copy's strength (a point-estimate `outperforms` only needs the table), add it to Results. A significance claim with no Results owner goes to `/paper-claim-audit`, not into Results |
| The mismatch is in the abstract or contribution list | Do not edit: the authors write those. Report it |

**Ruling (user 2026-11-03).** 「这重复也太多了 … 明明可以就说一次 <base policy>
单跑」; the copy check answers 「补进结论, 这只是个例子, paper prose tighten
能发现这种错误吗?」.

### 14. Exception clauses (例外从句: `all but X`, `except X`)

A claim about every member of a set, followed by the members it does not hold
for: `leads every open-source row on all but Bench-6`, `outperforms every
baseline except Baseline-C`, `Every row but A and B runs Linter L`, `the test
runs over tasks, except on Bench-9`, `under every teacher but Model-M`,
`every linear layer except the output head`. Whoever writes one has checked the
table and seen the cell where the claim fails, so it reads as accurate. But the
exception is the name the reader remembers. In a caption's bold title the
takeaway becomes the cell the method loses, and the clause is a caveat
(Escalation) that also lists the losing cells.

The exception never goes by itself. Deleting `on all but Bench-6` and keeping
`every` is a false claim. The exception goes together with the `every` it
patches, or the claim is restated so it needs no exception. How depends on what
the exception is:

| The exception is | Rewrite |
|---|---|
| a result cell where a baseline is slightly higher and the test does not resolve it | Drop `every` and the exception together, and state the claim in a form that holds without a hole. The bold and underline marks give the per-column ranking. `significantly outperforms Baseline-A on every benchmark and leads every open-source row on all but Bench-6` → `significantly outperforms Baseline-A on every benchmark and leads the open-source rows`. The first half has no exception and keeps its `every`. |
| a cell where a baseline is significantly higher | The `every` claim is false. Delete that claim (Escalation), or restate it over a group the paper already defines (`on the in-domain benchmarks`) when that group is exactly where it holds. Never invent a group to step around the cell. |
| the complement is a group the paper already names | Name the group. `under every teacher but Model-M` → `under each of the three open models`, when the paper introduced the four as Model-M and three open models. |
| a protocol or configuration fact that differs for a few rows, benchmarks or layers | Give each group its own plain statement. If a table column already gives the value per item, partition by that value (`over paired samples …; over tasks …`) and point at the table. If the rows the rule skips simply lack the thing the rule is about, scope the rule to the rows that have it (`Every row but A and B runs Linter L` → `Every row with a verifier runs Linter L`, when A and B run none). If a positive list already follows, delete the exception (`every linear layer except the output head: the attention and MLP projections …` → `the attention and MLP projections …`, when the next sentence freezes every other weight). |

After the rewrite, check two things. Whatever replaces the `every` must be true of
every member it now covers: the group, the scope or the partition. And the fact
the exception carried must still be stated somewhere. A protocol difference
stated nowhere is a hard stop (below). A result cell the table shows needs no
prose.

**Not this class:** `other than` meaning `different from` (`predicts a class
other than the target`), and a set defined by what it leaves out when that
definition is the column's (`Unseen leaves those tasks out`). Neither says
something about every member and then takes members back.

**Ruling (user 2026-11-16).** 「论文中不应该出现这些 but <Bench>. except xxx,
应该想想怎么删除这些」.

## Hard stops

Deleting text must never upgrade a claim.

- **Never let a deletion turn a null into a win.** State which cells were
  resolved and stop there: by default delete the whole null-labelling clause
  rather than swapping it for `no difference` / `unaffected` / `flat`, which
  asserts the null instead of declining to name it. Which words a null may
  still carry, and when, is the project's ruling (memory `paper-prose-rules`
  §1), not this skill's. `descriptive` and
  `post-hoc` scope a claim rather than label a null, and stay.
- **Never let a null carry a conclusion about what the method needs.** A variant
  that drops a component and is not significantly different from the full recipe
  supports `achieves comparable performance`, nothing more. `does not require X`,
  `X is unnecessary` and `works without X` are capability claims the comparison
  did not test: write the comparison and let the reader draw it. This applies when
  writing the sentence too, not only when cutting (user 2026-11-19「太强了」).
- **Never call a result an orphan because it weighs against a claim.** A result
  that bounds or contradicts a claim the paper makes bears on that claim and
  stays; "supports no claim" means it bears on none, in either direction. Cutting
  the unfavourable half of a comparison under the One Test is cherry-picking.
- **Never delete a denominator that scopes the claim** (full-denominator rules,
  subset sizes that bound generality).
- **Never leave a protocol difference stated nowhere** — different hardware,
  dropped-failure denominator, different budget. This is a stop on the *fact*,
  not on any particular sentence: the concessive clause carrying it is usually
  deletable, because the passage almost always states the same fact positively a
  sentence or two later. Check first (see class 6's "concessive scope hedge"),
  then delete the hedge or restate it positively — never both, never neither.
- **Never delete numbers from tables or captions.** This skill edits *prose*.
  A count moved out of a paragraph is fine precisely because the table keeps it.
  A table or caption that is itself bloated is a different job: hand it to
  `paper-table-craft` / `paper-figure-craft`, which know which rows the body
  cites and which numbers the figure already draws.
- **Never delete a citation or `\cite` key.**
- **Never delete a disclosure that an earlier pre-specified analysis read
  differently** ("an earlier pre-registered subset had shown little effect; the
  full read supersedes it"). It parses as class-3 journey narration, but
  deleting it hides a discordant prior analysis — a prose file-drawer that
  upgrades the surviving claim's apparent robustness. Refer it to the author.
  When the author rules *delete*, or before retiring a verification apparatus
  under class 8 or 9, verify one thing first and say it back: **is any reported
  number scored on the artifact whose history you are erasing?** If none is
  (say, the artifact is training data and every result is benchmark accuracy),
  the deletion retires a discarded *build*. If one is, it is scope, not process,
  and it stays.
- **Never delete a duplicate before checking it is one.** Grep the copy's
  distinguishing noun across the sections first: a result it alone carries
  moves into the owning section instead. Before moving text to the appendix,
  grep the appendix for a pointer back to it (`\S\ref{sec:...}`, "the rule of
  §4"); if one exists, keep a one-sentence version in the body.

Rule of thumb: cut what proves *diligence*; keep what bounds *scope*.

## Procedure

A pass over whole sections or a whole paper follows
[`references/procedure.md`](references/procedure.md): a paragraph map (the only
place classes 7 and 11 and paragraphs over ~250 words show up), the inventory
greps, classify, edit, verify the claim set, compile. Read it before such a
pass. An editor handed a list of lines or a caption applies the classes and hard
stops to those lines directly.

**Scope.** Main text first (`\section` bodies), appendix second. Tables,
captions and figure code belong to `paper-table-craft` / `paper-figure-craft`;
touch them here only to sweep class 5, 6, 8, 9, 12 and 14 leakage, and never to decide
what a caption should contain.

## Reporting

Report as: sections touched, what was cut by class (1–14) or by the One Test
(units that supported no claim, each with one line on what it was), and explicitly
**what was kept and why** — the kept-list is the evidence that tightening did
not become overclaiming. Do not report a "% reduction" as the headline; the
headline is that the argument reads straight through.

## Re-runs

A second pass over text this skill already tightened can still find cuts the
first one missed, so re-running is fine. The bar does not move: a pass that
finds nothing safe to cut says so, and never starts on scope qualifiers to
justify itself.

Classes 7 and 13 need a re-run after any round of section rewriting or a
changed result, because rewriting creates them fresh: tightening §4 to point at
a table leaves the intro bullet that pre-plays §4 untouched, and a result added
to §4 leaves the conclusion's copy of the list one item short. Re-emit the
paragraph map (`references/procedure.md` step 1), diff the one-line summaries,
and re-run the class-13 per-baseline listing (step 3).
