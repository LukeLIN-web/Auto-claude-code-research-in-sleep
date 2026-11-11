---
name: paper-prose-tighten
description: "Cut filler from paper prose while holding every claim constant — bookkeeping counts, defensive meta-narration, narrated absences / 无中生有, false pivots / 错误的转折, value series / 罗列, cross-section duplication, related-work sprawl, wordy phrases where one word does, process vocabulary (\"preregistered\"), one comparison split across sentences and copies of it that disagree, and claims that survive only behind a pile of caveats. Use when user says \"论文废话太多\", \"caveat 太多\", \"越讲越乱\", \"别解释了\", \"不要罗列数量\", \"清理废话\", \"无中生有\", \"错误的转折\", \"我要删减文字\", \"不该出现这种工程的术语\", \"related work 太长\", \"能用少词就不用多词\", \"重复也太多了\", \"说一次就行\", \"前后对不上\", \"tighten the prose\", \"cut the filler\", \"too wordy\", or before submission when sections read like an audit log."
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

The failure it replaces: each review round adds one clarifying clause, every
clause is individually correct and individually cheap, and three rounds later
the paragraph is unreadable in defence of a claim that never earned a paragraph.
When an author says the explanation itself is the problem, they are exercising
this rule — do not answer it with a better-worded explanation.

## The Thirteen Cut Classes

### 1. Bookkeeping enumerations

Internal-state counts, sub-slice denominators, and pair splits printed to show
the work was done.

| Cut | Why |
|-----|-----|
| `abstained blocks $569 \to 551$, so muting perturbs the gate without collapsing it` | the reader needs "the gate does not collapse", not the two integers |
| `an exact $82{:}82$ split of the discordant pairs` | the delta already said "tie" |
| `same-question discordant pairs $166{:}103$` | redundant with the reported delta and its interval |
| `A is mostly partial ($41$ of $70$), C complete ($180$ of $200$)` | three parenthetical fractions to support one qualitative sentence |
| `the within-block miss contributes 32 of the 39` | a count of a count |
| `gold slot balance $1135/1134/1135$`, `$851$ each over A/B/C/D` | already in the config table; prose repeats it |

**Rewrite pattern:** keep the *qualitative* fact, drop the arithmetic that
demonstrates it. "muting perturbs the gate without collapsing it" is the whole
content of the first row.

**Keep** a count when it *is* the finding: a denominator that scopes the claim
(`412 of 500 questions exceed the context limit`), a headline delta, an
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
limit, that limit survives as **one adjective** on the claim (`descriptive`,
`post-hoc`) — not as its own sentence. A *null* is the exception: it gets no
adjective at all (see the hard stop below).

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

This class is **within-paragraph**. Its section-scale twin is class 7, which no
amount of reading one paragraph at a time will surface.

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

Two field notes. This class concentrates **in captions** — that is where
authors explain table gaps — so sweep captions for class 5 even though the rest
of this skill edits prose; and a generated caption (an `AUTO-GENERATED` header)
must be cut in the generator script, or the next build resurrects the sentence.
What a caption is *for* is not this skill's call: `paper-table-craft` and
`paper-figure-craft` own that.

**Keep** an absence statement also when the absence *is* the claim ("no prior
benchmark evaluates X and Y jointly" as a motivation sentence)
or when it states a protocol fact a reviewer would otherwise assume the other
way ("no test-set videos appear in training").

### 6. False pivots (错误的转折)

A claim delivered as the correction of an alternative nobody proposed: the
sentence erects a reading, negates it, and only then states the claim. The
negated half is the author debating themselves; the positive half is the whole
content.

- "The advantage is also not reducible to the material the compressor had to
  drop: sorting the same questions by the share of the clip's audio the
  baseline kept, \method leads inside every level of that coverage." →
  "\method leads at every level of the baseline's audio coverage." The
  reviewer had not yet formed the reading being rebutted.
- "X rather than Y" where Y is the author's own invention: delete "rather
  than Y", keep X. "the map is ordered by two properties of the questions
  rather than by the benchmark" → "the map is ordered by two properties of
  the questions."
- "not A but B" → "B".

**Rewrite pattern:** delete everything from the pivot word on ("rather than
…", "not … but", "is not reducible to …") and let the positive claim stand
alone. If the sentence opens with the negation, the rewrite is the positive
claim, stated directly. No keep cases: you do not know what the reader's
default reading is, so a pivot never earns its place by "correcting" one.

**Field notes (first full pass, 2026-08-05, ~90 cuts).**
(a) The worst pivots are invisible to a "rather than" grep: sentence-lead
negations ("The obvious reading of that pair … is the one the data rejects",
"Nor is the gain fully accounted for by…", "That the shortlist moves is not
by itself evidence…", "Neither length is a swept hyperparameter"), negative
`\paragraph` headers ("…is not doing hidden accuracy work"), caption bold
titles ("The regime, not the benchmark, sets…"), and question-form section
titles ("Is the Lead Bought by What the Montage Discarded?"). Sweep headers,
titles, and captions by eye, not only by grep.
(b) Deleting the "rather than Y" tail is usually scope-safe because the
surviving X carries the scope itself ("a same-stack anchor", "third-party
reads", "systems as published"). When the negated half is the *only* scope
carrier, restate it positively ("same-weights, cross-protocol comparison")
— the hard stops below still forbid dropping the scope.
(c) A negation-first setup often binds a later pronoun ("that explanation",
"It does not") — deleting only the clause dangles the reference. Rewrite the
passage as one positive sentence.
(d) A generator can carry the same pivot in two strings (the LaTeX caption
and a preview/notes block). After editing it, rebuild and re-grep the
rendered `.tex` to confirm the cut landed.
(e) **The concessive scope hedge** — `X, although Y`, `X, each a Y`,
`although X grows, Y is bounded` — is a class-6 shape even when Y is real
scope, and it is the highest-yield sub-shape left after the obvious pivots
are gone. Two examples from one paper: a headline followed by "although
those numbers come from different serving stacks and are not causal method
comparisons", and an $\mathcal{O}(1)$ claim guarded by "although total scan
computation grows linearly with $M$". Both looked like hard stops. Neither
was: the passage already carried the same scope **positively** — "the
informative comparisons are the same-stack anchors" and "that gap is stack
difference" two sentences on; "the whole pipeline costs $M+1$ forwards per
question" one subsection back. So the hedge was pure class-4 restatement
wearing a scope costume.

**The procedure, in order:** grep the scope's own noun (`stack`, `forwards`,
`denominator`) across the passage and the neighbouring section. Scope found
stated positively → delete the concessive, nothing is lost. Scope found
nowhere else → move it into the sentence that owns it as a plain assertion,
then delete the concessive. Do not reinstate the concessive as the fix.

**Repo ruling (2026-08-20).** The author's words: 「范围 也删了 … 防止「全都是
O(1)」的过度主张, 不同 serving stack 这些都要删」. Author-facing framing
matters here: do not answer this instruction with a defence of the hard stop.
Run the grep, report where the scope still lands, and cut.

### 7. Cross-section duplication (跨节重复)

Two paragraphs in different sections carrying the same content at different
resolutions. Individually each reads fine; the duplication is only visible from
the paragraph map (procedure step 1), never from reading straight through — by
the time the reader reaches the second copy, the first is 8 pages back and the
author has forgotten writing it.

The recurring shapes, in descending yield:

| Shape | Fix |
|-------|-----|
| An intro **contribution bullet that pre-plays a whole results subsection** — the same regime map, the same axes, the same per-benchmark ordering | The bullet keeps the *claim* and the two axis names; every reading of the table moves to the subsection. Point at the table, not at the finding. |
| A finding stated in a results **subsection** and again as a **conclusion/analysis bullet** | Keep the results copy; delete the bullet — unless the bullet carries something the subsection does not (see the hard stop below). |
| The method's governing **principle** stated informally in the intro and formally in the method | Intro keeps the hazard in one sentence and cites `\S`; the formal statement, the decomposition, and the concrete quotas live once, in the method. |
| A **scaling / cost / budget** argument in the intro and again in a "Bounded X" method subsection | Same rule: the intro asserts the property, the method derives it. |
| The **motivation** ("clips are too long to fit") in the intro and again in Settings | Settings keeps only what scopes the *experiment* (which benchmarks are over the wall). |

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
| `the deployed checkpoint is the run's endpoint, fixed without reference to any evaluation signal, so neither adapter's checkpoint is chosen by benchmark performance` | asserts the absence of cherry-picking; a config table naming the endpoint already carries it |
| `held-out accuracy is flat from step $300$ through $900$`, in a config-table cell | a second curve nobody plots, on a set nobody else in the paper names |
| `step $2000$, selected by a pre-specified stopping rule inside epoch 1` | the *rule* may be a reproduction fact; `pre-specified` is the assurance — drop that word, keep the rule |
| `on a frozen evaluation subset, accuracy rises across every checkpoint measured` | the subset's identity is bookkeeping; `accuracy rises across the measured checkpoints` is the claim |

**Rewrite pattern:** a checkpoint's *identity* is configuration and belongs in
the config table as a bare value (`step 900, the run's endpoint`). Everything
about how it was chosen, what it was not chosen by, and what else was flat
where — delete.

**Keep** a provenance fact when a reviewer could otherwise reconstruct a
*different* experiment: the split a headline number is scored on, a train/test
separation, a denominator rule, a protocol the comparison depends on. Those are
hard stops below, not class-8 hits.

**Field note (2026-08-20).** This class manufactures apparent contradictions.
Two hygiene sentences written weeks apart — a config-table cell reporting a flat
held-out curve over one range, a results sentence reporting a rising curve over
another — described two different sets, and an external reviewer read them as
the paper contradicting itself. Naming the two sets is the wrong repair: it
spends three sentences to defend a supporting claim. Deleting both dissolves the
contradiction and costs nothing. **When a reviewer flags "these two statements
disagree" and both are class 8, subtract.**

### 9. Process vocabulary (流程/工程术语)

The words we use to *run* experiments, leaking into the words the paper is
*written* in: `preregistered`, `pre-specified`, `criteria frozen before any
readout`, `frozen before any test number was read`, `the frozen margin`, `a
frozen evaluation set`, `stopping rule`, `early-kill gate`, `acceptance gate`.

Classes 2 and 8 walk straight past these, because a class-9 hit is an
**adjective on a real result**, not a sentence of its own: the noun it modifies
is load-bearing, the sentence survives the paragraph map intact, and nothing
looks deletable. It is also the one class that says nothing to the reader it
means to reassure — a reviewer cannot check that a margin was fixed before the
readout, so the word is an assertion about our internal timeline, and asserting
it invites the suspicion it was meant to settle.

| Cut | Keep |
|-----|------|
| `a preregistered two-benchmark ablation` | `a two-benchmark ablation` |
| `With criteria frozen before any new readout, we re-measured …` | `We re-measured …` |
| `non-inferior at a margin frozen before any readout` | `non-inferior` — the margin's value lives in the appendix |
| `passes the preregistered non-degradation gate` | `does not degrade` |
| `selected on a dev split before any test number` | `selected on a dev split` |
| `well under the $0.40$ early-kill gate` | `well under $0.40$` |
| `the paper's frozen default configuration` | `the paper's default configuration` |

**Rewrite pattern:** delete the modifier, keep the noun. Unlike class 8 the
sentence almost never dies — an ablation that was preregistered is still an
ablation, and the result it reports is untouched.

**Keep** `frozen` in its *technical* sense, which shares the word and nothing
else: `frozen backbone`, `frozen scans`, `frozen window enumeration`, `frozen
tokenizer`, `frozen protocol` describe weights and configuration that do not
move. `frozen before …` describes when *we* looked. Only the second is a hit.

**Keep** the object a process word modifies when that object scopes the claim: a
non-inferiority **margin** bounds what "non-inferior" means and stays (value in
the appendix, per the no-numbers-in-body rule); only the story of when it was
fixed goes.

**Field note (2026-08-20 — the ruling that created this class).** The author's
words: 「preregistered 都删了, 论文里就不该出现这种工程的术语. 记住」. Eight
instances of the word and eleven of its relatives left one paper in a single
sweep, and no claim moved.

The same ruling retired an entire *apparatus* of this kind — a training pool's
structural probe, its permutation null, its role-injection negative control and
its acceptance gate — carried redundantly in three places (a config-table row, a
method sentence, an appendix paragraph of numbers), i.e. class 7 stacked on
class 8 stacked on class 9. Deleting all three was safe because **no reported
number was scored on that pool**: the probes defended *training* data, and every
result in the paper is benchmark accuracy, which a training-pool shortcut can
only depress. Run that test before retiring any verification apparatus —
*does a reported number depend on the thing being verified?* — and if the answer
is yes, it is scope, not process, and it stays.

**Sweep note.** Count each term separately (the per-term counts are what you
report), and call GNU grep as `command grep`: in Claude Code's Bash, `grep` is a
function that runs ugrep with `--ignore-files`, so a recursive grep from a
parent directory silently skips every gitignored file. (The 2026-08 note that a
compound `-E` alternation returned zero under ugrep did not reproduce on
2026-10-22; the gitignore skip does.) Then sweep the copies outside `sections/`:
figure/table generator strings in `paper/scripts/*.py` and `label` fields in
`paper/data/*.json` render into the PDF too.

### 10. Value series across conditions (罗列)

One quantity's readings at three or more conditions — distance layers,
benchmarks, checkpoints, compression rates — strung through a sentence with
slashes or commas. It is a table row read out loud.

| Cut | Why |
|-----|-----|
| `the block hit rate is $96.7$ / $90.0$ / $91.3$ / $80.8\%$ across the four distance layers` | the same sentence already says it: *falls with distance* |
| `window choice inside a retained block does not, at $83.0$ / $83.3$ / $85.0$ / $84.4\%$` | "does not" **is** the reading; the four numbers only prove we looked |
| `$+0.8$pp on A, $+0.7$ on B, $-1.6$ on C and $+0.3$ on D --- bounded by $1.6$pp` | the bound is the claim; the four values are its raw material |
| `median $5$ / $5$ / $2$ / $2$ on A / B / C / D` | one adjective — "single-digit" — carries all four |
| `$45.7\%$ at base, then $48.5$ / $50.3$ / $50.4\%$ at steps $100$ / $300$ / $600$` | "rises monotonically, flattening after step 300" is the whole content |
| `$81.3\%$ in a single window, $97.8\%$ within three, none more than eight` | keep the bound the readout budget is compared against, drop the ladder under it |

A series always exists to show a **shape** — monotone fall, flat, one condition
out of line. A reader cannot hold four numbers and does not try: they take the
shape word and skip the digits. So write the shape and delete the digits. **A
series is never load-bearing as a series**; if its shape is not worth one word,
the sentence was not worth keeping either.

**Rewrite pattern:** keep the shape word (`falls with distance`, `does not`,
`holds level`, `single-digit`, `rises monotonically`), point at the table or
figure if one carries the values, and keep at most the **one** number the
argument turns on — a bound, or a ceiling the series is measured against.

**Not this class** — two values in contrast (`$37.18\%$ when a retained window
covers the evidence and $14.29\%$ when none does`), a range or IQR (`conversion
rates span $0.18$ to $0.40$`), and a pair whose *near-equality* is the claim
(`retains a median $30.4\%$ of the deployed windows' seconds against a deployed
coverage of $29.6\%$`). Those are comparisons, not enumerations.

**The appendix is not exempt.** The house rule that lets an appendix keep
numbers (`paper/CLAUDE.md`) exempts *isolated* numbers that no figure carries —
never a series. Appendices are where this class survives a body-only sweep:
every hit of the ruling that created the class was in one.

**Field note (2026-08-24 — the ruling that created this class).** The author
pasted back three consecutive appendix sentences carrying twelve numbers in four
series and wrote 「严格禁止」. Class 1 walks past these: they are not counts,
denominators or pair splits but *results*, each individually a number the paper
is entitled to report. The defect is the enumeration, not the digit.

### 11. Related-work sprawl (相关工作写太多)

The rule lives in `../shared-references/manuscript-craft.md` (Background /
Related Work): two paragraphs, one per line of prior work. Related work outgrows
it the way the audit log does. Every paper a novelty search turns up earns its
own sentence, every near neighbour earns its own paragraph, and every paragraph
closes on how we differ.

| Cut | Why |
|-----|-----|
| a paragraph for a family the method answers the same way as another (executors that take a target position, split off from orchestrated systems) | one line of work; its works join the paragraph whose gap they share |
| `X does A. Y does B. Z does C.`, one sentence per work | one clause per work inside a cluster: `train the executor on other executors' data~\cite{x,y,z}` |
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

**Field note (2026-11-01, the ruling that created this class).** After a
motivation pass added a paragraph for each newly found family, one
draft's related work reached six paragraphs, about 1,800 words and 51 cite keys.
The author wrote 「一般 related work 两段就行了, 你写的也太多了」. The source was
`paper-write`'s "minimum one full page, 3–4 paragraphs", replaced the same day.
The rewrite came to two paragraphs of about 430 words with all 51 keys kept.

### 12. Wordy phrases (能用少词就不用多词)

Several words where one word the reader already knows says the same thing.
Drafting from notes, the agent describes a property instead of naming it. Each
cut saves a word or two, so the class is many small edits, not one big one.

| Cut | Write |
|-----|-------|
| `can carry out long-horizon and loosely worded instructions` | `can follow long-horizon and vague instructions` |
| `We refer to the orchestrator together with the VLA and the tools it calls as the agent` | `We call the orchestrator, VLA and tools the agent` |
| `It meets the orchestrator's subgoals ... for the first time at deployment` | `It first meets the orchestrator's subgoals ... at deployment` |
| `trains on its positive episodes together with those collected on ...` | `trains on its positive episodes and those collected on ...` |
| `none of them in Bench-7's evaluation set` | `none in Bench-7's evaluation set` |
| `calls grasping or placing tools` | `calls grasp or place tools` (the method section's name for them) |

**Rewrite pattern:** first look for a word the paper already uses (`vague` is
already in one benchmark's name; `grasp and place tools` is the method
section's term), then for the field's usual word. Swap only when the short word
means the same thing.

**Not this class** (all from the same draft, all kept):

| Kept | Why |
|------|-----|
| `succeeds significantly less often` | `fails` is a different claim |
| `The VLA's own successful episodes are what make fine-tuning help` | the cleft says *these and nothing else*; dropping `are what` loses that |
| `is not significantly different from` | the project's allowed wording for a null that matters |
| `half and half with DROID` | no single word says it |
| `leaves the orchestrator in place` | `unchanged` says something else |

Also kept: a qualifier that is the claim or bounds it (`significantly`,
`new tasks from the same generator`), a term the paper defines
(`executor self-bootstrapping`), and official benchmark and model names.

**Read every sentence; grep only helps with recall.** A stock list (`in order
to`, `is able to`, `a number of`, `due to the fact`) found nothing in a
4,800-word draft. All six hits came from reading. The step-3 grep lists the
phrases that did turn up, for the next draft.

**Captions too.** One hit was in the Figure 1 caption (`fine-tuned on them
together with DROID`). If captions are generated, change the source in the build
script and rebuild; an edit to the generated `.tex` is overwritten.

**Re-run the short-last-line gate after the pass.** Cutting words reflows the
paragraph, and two of the six edits left a last line under half the column. The
fix is more cuts from this class in the same paragraph (`the VLA and the tools`
→ `VLA and tools`, `20,000 training steps` → `20,000 steps` where the sentence
already says training). Recompile until `paper-compile`'s `check_runts.py`
reads 0.

**Field note (2026-11-03, the ruling that created this class).** On one
abstract's `loosely worded instructions`, the author wrote
「论文应该能用少词的就不要用多个词, 比如 loose worded 就应该写成 vague」. They also
made that edit themselves on Overleaf. After reading every sentence of the
draft, the agent changed six more phrases, and four more to fix short last lines.
The other multi-word phrases carried a claim or had no one-word equivalent.

### 13. One comparison split across sentences, and copies that disagree (同一个比较说好几遍、各处副本对不上)

The same verb against the same baseline, repeated sentence after sentence, each
time with one or two new conditions. This happens when results are added one at
a time as runs finish: each new benchmark gets its own sentence with an `also`.
Class 4 misses it because each sentence states a different fact. Class 12 misses
it because each sentence is short.

| Cut | Write |
|-----|-------|
| `Our method significantly outperforms $\pi_{0.5}$ alone on Bench-1 and on Bench-2, …` / `On Bench-3 our method also significantly outperforms $\pi_{0.5}$ alone.` / `Our method also significantly outperforms $\pi_{0.5}$ alone on Bench-4, and lies clearly above it on Bench-6.` | `Our method significantly outperforms $\pi_{0.5}$ alone on Bench-1, Bench-2, Bench-3 and Bench-4, and lies clearly above it on Bench-6 (Table~\ref{tab:main}).` |
| `on Bench-1, on Bench-2, on Bench-4 and on Bench-5` | `on Bench-1, Bench-2, Bench-4 and Bench-5` (the same repetition at word scale) |

**Rewrite pattern:** write one sentence per baseline. The significant conditions
go in one list. Point-estimate leads (`lies above`) follow as a second clause
with `it`, so the baseline is named once. A scope that holds for only some
conditions (the held-out 87 tasks on two of the benchmarks) becomes its own
short sentence after the list; do not nest it inside the list. A different table
is no reason to keep a separate sentence: cite both tables. After merging,
re-read every later `both benchmarks`, `either`, `there` in the paragraph,
because the merge changes what they refer to.

**Keep separate:** a different baseline, or a different metric (success rate
against successes with every action from the VLA). A different metric is a
different claim, even when the verb is the same.

**The inventory doubles as the copy check.** A comparison stated in Results
usually has copies in the intro, the method's advantages, the conclusion and the
abstract. A result added later tends to reach one copy and miss the others. For
each baseline, list every sentence in the paper that compares against it (step 3
command): section, verb (`significantly outperforms` / `lies above` /
`completes significantly more tasks with every action its own`), metric, and
conditions. The Results sentence owns the claim. Every copy is a derived form
(SSOT), so a copy that disagrees with Results is a bug in the copy. Fixing it
does not change what the paper claims.

| Mismatch | Fix |
|----------|-----|
| A copy lists fewer conditions than Results (the conclusion omits Bench-3) | Add the missing ones to the copy. A copy that enumerates must enumerate all of them, or use a summary word that is true for all |
| A copy's verb or metric is stronger than the one in Results (`significantly outperforms` where Results has significance only on every-action-own completions) | Weaken the copy to the Results wording |
| A copy states a condition Results never states (`lies above it on Bench-7` in the intro and conclusion only) | If the table shows it at the copy's strength (a point-estimate `lies above` only needs the table), add it to Results. A significance claim with no Results owner goes to `/paper-claim-audit`, not into Results |
| The mismatch is in the abstract or contribution list | Do not edit: the authors write those. Report it |

**Field note (2026-11-03, the ruling that created this class).** On one
Main Results section, the author wrote 「这重复也太多了 … 明明可以就说一次
π0.5 单跑」. Merging three sentences into one showed that the conclusion's list
lacked Bench-3. Bench-3 had become significant on 11-01, and that edit
reached the intro and Results but not the conclusion. The author's reply was
「补进结论, 这只是个例子, paper prose tighten 能发现这种错误吗?」. The copy check then found two
more: the intro and method claimed a significant success gain over frame-level
RECAP-style conditioning, while Results (on the 30 s-capped table) is
significant only on every-action-own completions; and the intro and conclusion
said our method lies above $\pi_{0.5}$ alone on Bench-7, which no Results
sentence said.

## Hard stops

Deleting text must never upgrade a claim.

- **Never let a deletion turn a null into a win.** State which cells were
  resolved and stop there: by default delete the whole null-labelling clause
  rather than swapping it for `no difference` / `unaffected` / `flat`, which
  asserts the null instead of declining to name it. Which words a null may
  still carry, and when, is the project's ruling (memory `paper-prose-rules`
  §1), not this skill's. `descriptive` and
  `post-hoc` scope a claim rather than label a null, and stay.
- **Never delete a denominator that scopes the claim** (full-denominator rules,
  subset sizes that bound generality).
- **Never leave a protocol difference stated nowhere** — different stack,
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
  When the author rules *delete* — and on 2026-08-20 one did, for a sentence
  disclosing that a training pool's first construction had leaked and was
  rebuilt — the ruling is theirs, but verify one thing first and say it back:
  **is any reported number scored on the artifact whose history you are
  erasing?** Here nothing was (the pool was training data; every reported result
  was benchmark accuracy, which a training-pool shortcut can only depress), so
  the deletion retired a discarded *build*, not a discarded *reading*. Had one
  number come from that pool, the same deletion would have been the file-drawer
  this stop exists to prevent.
- **Never delete a duplicate before checking it is one.** Two class-7 traps,
  both hit on the first real pass:
  - *The "duplicate" carries a result that exists nowhere else.* A conclusion
    bullet reading "both training stages port to a second backbone" looked like
    a restatement of a whole results subsection — but the subsection covered
    only the *answer* stage, and the bullet's localization-stage result appeared
    in no section and no appendix. **Grep the distinguishing noun** (here the
    evidence-hit metric) across `sections/` before deleting; if it is unique,
    the fix is to move the sentence into the owning section, not to delete it.
  - *The appendix cites the body for what you are moving to the appendix.*
    Before "this belongs in the appendix", grep the appendix for a back-pointer
    (`\S\ref{sec:...}`, "the rule of §4", "the ruling of §5"). An appendix that
    reads "each panel's comparator follows the fair-baseline ruling of §5"
    requires §5 to still state that ruling. Keep a one-sentence version in the
    body and cut only the self-justification around it.

Rule of thumb: cut what proves *diligence*; keep what bounds *scope*.

## Procedure

1. **Map every paragraph before reading for style.** Classes 1–6, 8–10 and 12
   are found by grep; class 13 by the per-baseline listing in step 3; classes 7 and 11 and oversized paragraphs are found only here. Emit one row per
   paragraph — file, line span, word count, and **one line saying what it
   claims**:

   ```bash
   python3 - <<'PY'
   import glob, re
   WORD, SPACE = re.compile(r"[A-Za-z][A-Za-z'\-]*"), re.compile(r"\s+")
   for f in sorted(glob.glob('sections/*.tex')):  # numbered names sort into \input order
       print('=' * 8, f)
       lines = open(f, encoding='utf-8').read().split('\n')
       start = None
       for i, l in enumerate(lines + [''], 1):
           if l.strip() and start is None:
               start = i
           elif not l.strip() and start is not None:
               t = SPACE.sub(' ', ' '.join(lines[start - 1:i - 1])).strip()
               print(f"  L{start}-{i - 1}\t{len(WORD.findall(t)):4d}w\t{t[:70]}")
               start = None
   PY
   ```

   Then read the map, not the paper. Two things fall out that no reading pass
   gives you:
   - **Two rows whose one-line summaries are the same claim** → class 7. This is
     where the largest single cuts are.
   - **Any row over ~250 words** → it is carrying several findings at once.
     Cutting it is not enough; **split it** (see step 5). A 350-word paragraph
     stays unreadable at 250.

   Present the map to the author before editing. It is also the artifact they
   asked for when they say "每一段都在讲啥" — and their pick of which rows to cut
   is worth more than your own ranking.

2. **Scope.** Main text first (`\section` bodies), appendix second. Tables,
   captions and figure code belong to `paper-table-craft` / `paper-figure-craft`;
   touch them here only to sweep class 5, 6, 8, 9 and 12 leakage, and never to decide
   what a caption should contain.

3. **Inventory.** Pull every candidate to a scratch list before editing:

   ```bash
   # numbers-in-prose density, per section
   command grep -o '\$[0-9][0-9,{}.\\]*\$' sections/*.tex | sort | uniq -c | sort -rn | head -40
   # bookkeeping shapes: "N of M", "N:M", "N -> M"
   command grep -nE '[0-9]+ of [0-9]|[0-9]\{?:\}?[0-9]|\\to [0-9]' sections/*.tex
   # class 10 value series: slash-strung readings, and "x on A, y on B, z on C"
   command grep -nE '\$[0-9.]+\$ ?/ ?\$[0-9.]+\$' sections/*.tex | command grep -v '&'
   command grep -nE '(on|at) [A-Z][A-Za-z-]+, \$?[-+0-9]' sections/*.tex | command grep -v '&'
   # class 12 wordy phrases: recall aid only, read every sentence (class 12)
   command grep -niE 'carr(y|ies|ied) out|refer(s|red)? to .* as|for the first time|together with|none of them|loosely worded|in order to' sections/*.tex
   # class 13: every sentence that compares against one baseline, across all sections
   # (run once per baseline noun; read the list for split sentences and for copies that disagree)
   for b in 'alone' 'frozen' 'EXIMO-style' 'zero-shot' 'RECAP'; do
     echo "== $b"; python3 - "$b" <<'PY'
   import glob, re, sys
   for f in sorted(glob.glob('sections/*.tex')):
       for n, line in enumerate(open(f, encoding='utf-8'), 1):
           if line.lstrip().startswith('%'): continue
           for s in re.split(r'(?<=[.;])\s+', line.strip()):
               if sys.argv[1] in s: print(f"{f}:{n}\t{s[:180]}")
   PY
   done
   # meta-narration stems
   command grep -niE 'we (report|claim|make|state|note|stress|log) (this|it|none|them)|rather than (claim|letting|running|averag)|net (it|this|that) away|averag\w* away|entitled to know|guard(ing)? against|we count it as such' sections/*.tex
   # narrated absences: sentences about things that don't exist
   command grep -niE 'publishes no|has no (row|column|entry)|does not (report|publish|evaluate|include|provide)|no official|not (available|reported) (in|for)' sections/*.tex
   # false pivots: negated-alternative claims (high recall — classify by hand;
   # headers, caption titles, and section titles need an eye pass on top)
   command grep -niE 'rather than|instead of|not reducible|, not |; it is|\bnor is|not by itself|not only|is not|are not' sections/*.tex tables/*.tex
   # artifact provenance / hygiene assurance (sweep tables/ too: it hides in config cells)
   command grep -niE 'without reference to|pre-?specified|pre-?registered stopping|deployed checkpoint|the run.s endpoint|held-out (accuracy|acc) is flat|chosen by (benchmark|evaluation)|frozen (evaluation |)subset|seed' sections/*.tex tables/*.tex
   # process vocabulary (class 9) -- count each term separately (class 9's sweep note)
   for t in preregistered pre-registered pre-specified prespecified \
            "criteria frozen" "frozen before" "frozen margin" \
            "frozen evaluation" "stopping rule" "kill gate" "acceptance gate"; do
     n=$(command grep -ric -- "$t" sections/*.tex tables/*.tex 2>/dev/null | awk -F: '{s+=$NF} END{print s+0}')
     [ "$n" != 0 ] && printf '%4s  %s\n' "$n" "$t"
   done
   ```

4. **Classify, don't rewrite yet.** Tag each hit cut / keep / rewrite. The
   temptation is to rewrite a bloated sentence into a slightly less bloated one;
   most hits should be **whole-clause deletions**. On a paper whose claims are
   already settled, expect most hits to be keeps — in practice ~80% of
   absence-pattern hits are load-bearing protocol scope. A low cut count is the
   test working, not failing.

5. **Edit.** Prefer deleting a clause over restructuring a sentence — the fewer
   words that move, the smaller the chance of shifting a claim. The one
   restructuring worth doing is the **paragraph split** step 1 flagged: find the
   findings inside the over-long paragraph, give each its own paragraph with its
   own topic sentence, and cut in the process. Splitting without cutting is
   still a win; the reader can now see where each finding starts.

6. **Verify the claim set is unchanged.** For each edited paragraph, state in
   one line what it claimed before and after. Any difference is a bug, not a
   tightening. Re-check every hard stop above. Then re-grep the labels you
   dropped a `\ref` to — a deleted paragraph can be the only citer of an
   appendix section.

7. **Compile** and report the size change (words or lines per section), plus a
   list of anything you deliberately left because cutting it would have
   loosened a claim.

**Calibrate the estimate.** A per-item cut target set from the map will
overshoot by roughly 2×: load-bearing paragraphs *compress*, they do not delete,
and every "delete this section" item tends to turn into "move one sentence and
delete the rest". A 1,600-word plan landing at ~700 is the normal outcome, not a
failure to execute — say so plainly instead of padding the cut to hit the
estimate.

## Reporting

Report as: sections touched, what was cut by class (1–13), and explicitly
**what was kept and why** — the kept-list is the evidence that tightening did
not become overclaiming. Do not report a "% reduction" as the headline; the
headline is that the argument reads straight through.

## Anti-pattern

Do not run this skill twice on the same text expecting further gain. The second
pass finds nothing safe to cut and starts eating scope qualifiers to justify
itself. One pass, then stop.

The exception is a **class-7 and class-13** pass. Classes 1–6, 8–10 and 12 are sentence-local and
are genuinely exhausted in one run; classes 7 and 13 are not, because they are created fresh
every time a section is rewritten or a result changes — tightening §4 to point at a table leaves the
intro bullet that pre-plays §4 untouched, and a result added to §4 leaves the
conclusion's copy of the list one item short. After any round of section rewriting,
re-emit the paragraph map (step 1) and diff the one-line summaries, and re-run the
class-13 per-baseline listing. Nothing else.
