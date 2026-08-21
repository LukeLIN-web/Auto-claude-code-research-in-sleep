---
name: paper-prose-tighten
description: "Cut filler from paper prose: bookkeeping-count enumerations (\"abstained blocks 569 → 551\", \"32 of the 39\", \"discordant pairs 166:103\"), defensive meta-narration (\"we report this rather than claim X\", \"a reader is entitled to know\"), narrated absences / 无中生有 (\"Video-Odyssey publishes no row for this backbone and has no column\"), false pivots / 错误的转折 (\"X rather than Y\", \"the advantage is not reducible to Z\" — delete the negated alternative, state the claim directly), cross-section duplication / 跨节重复 (an intro contribution bullet that pre-plays a whole results subsection; the same result in a subsection and again in the conclusion bullets), artifact-provenance assurance (\"the deployed checkpoint is fixed without reference to any evaluation signal\", \"held-out accuracy is flat from step 300 through 900\"), process/engineering vocabulary / 流程工程术语 (\"a preregistered two-benchmark ablation\", \"criteria frozen before any readout\", \"the frozen margin\", \"early-kill gate\" — delete the modifier, keep the noun), and self-referential audit trail that no reviewer reads. Also carries the escalation rule: when a claim only survives behind a pile of caveats, delete the claim. Use when user says \"论文废话太多\", \"caveat 太多\", \"越讲越乱\", \"别解释了\", \"不要罗列数量\", \"清理废话\", \"无中生有\", \"错误的转折\", \"每一段都在讲啥\", \"我要删减文字\", \"preregistered 都删了\", \"不该出现这种工程的术语\", \"tighten the prose\", \"cut the filler\", \"too wordy\", or before submission when sections read like an audit log instead of an argument."
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

## The Nine Cut Classes

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

This class is **within-paragraph**. Its section-scale twin is class 7, which no
amount of reading one paragraph at a time will surface.

### 5. Narrated absences (无中生有)

Prose whose grammatical subject is something that does not exist:

- "Video-Odyssey publishes no row for this backbone and has no column for it."
- "X does not report Y for this setting."
- "No official number exists for Z."

A full sentence spent on an empty cell, an experiment nobody ran, a baseline
nobody published. It reads like diligent disclosure — which is why it survives
draft after draft. The deciding test: **can the reader see the gap in the
artifact?** A dash in a cell, a reduced $n$, a row missing from an enumerated
suite — visible, so the absence is load-bearing and lives as one terse legend
clause (`a dash = none published`; `Video-Odyssey has no whole-clip arm.`),
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
benchmark evaluates audio-visual retrieval jointly" as a motivation sentence)
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

**Sweep note.** Do not sweep this class with one big `-E` alternation. Under
`ugrep` (aliased to `grep` on some machines here) a pattern like
`pre-?regist|pre-?specif|…` returned **zero hits on files that held eight**.
Count each term separately as a fixed string and treat a zero from a compound
regex as unproven, not as absence. Then sweep the copies outside `sections/`:
figure/table generator strings in `paper/scripts/*.py` and `label` fields in
`paper/data/*.json` render into the PDF too.

Deleting text must never upgrade a claim. Hard stops:

- **Never delete a significance qualifier** to make a null read as a win.
  `not significant`, `directional`, `descriptive`, `post-hoc` stay.
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

1. **Map every paragraph before reading for style.** Classes 1–6 and 8 are found
   by grep; class 7 and oversized paragraphs are found only here. Emit one row per
   paragraph — file, line span, word count, and **one line saying what it
   claims**:

   ```bash
   python - <<'PY'
   import re
   for f in ['01_intro.tex','02_related.tex','03_method.tex','04_results.tex']:
       print('='*8, f)
       buf, start = [], 0
       def flush(buf, start, end):
           t = '\n'.join(buf).strip()
           if not t: return
           w = len(re.findall(r"[A-Za-z][A-Za-z'\-]*", t))
           print(f"  L{start}-{end}\t{w:4d}w\t{re.sub(r'\\s+',' ',t)[:70]}")
       for i, l in enumerate(open('sections/'+f).read().split('\n'), 1):
           if l.strip() == '': flush(buf, start, i-1); buf, start = [], i+1
           else:
               if not buf: start = i
               buf.append(l)
       flush(buf, start, i)
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
   touch them here only to sweep class 5, 6, 8 and 9 leakage, and never to decide
   what a caption should contain.

3. **Inventory.** Pull every candidate to a scratch list before editing:

   ```bash
   # numbers-in-prose density, per section
   grep -o '\$[0-9][0-9,{}.\\]*\$' sections/*.tex | sort | uniq -c | sort -rn | head -40
   # bookkeeping shapes: "N of M", "N:M", "N -> M"
   grep -nE '[0-9]+ of [0-9]|[0-9]\{?:\}?[0-9]|\\to [0-9]' sections/*.tex
   # meta-narration stems
   grep -niE 'we (report|claim|make|state|note|stress|log) (this|it|none|them)|rather than (claim|letting|running|averag)|net (it|this|that) away|averag\w* away|entitled to know|guard(ing)? against|we count it as such' sections/*.tex
   # narrated absences: sentences about things that don't exist
   grep -niE 'publishes no|has no (row|column|entry)|does not (report|publish|evaluate|include|provide)|no official|not (available|reported) (in|for)' sections/*.tex
   # false pivots: negated-alternative claims (high recall — classify by hand;
   # headers, caption titles, and section titles need an eye pass on top)
   grep -niE 'rather than|instead of|not reducible|, not |; it is|\bnor is|not by itself|not only|is not|are not' sections/*.tex tables/*.tex
   # artifact provenance / hygiene assurance (sweep tables/ too: it hides in config cells)
   grep -niE 'without reference to|pre-?specified|pre-?registered stopping|deployed checkpoint|the run.s endpoint|held-out (accuracy|acc) is flat|chosen by (benchmark|evaluation)|frozen (evaluation |)subset|seed' sections/*.tex tables/*.tex
   # process vocabulary (class 9) -- count each term separately; one big -E
   # alternation silently returns zero under ugrep (see class 9's sweep note)
   for t in preregistered pre-registered pre-specified prespecified \
            "criteria frozen" "frozen before" "frozen margin" \
            "frozen evaluation" "stopping rule" "kill gate" "acceptance gate"; do
     n=$(grep -ric -- "$t" sections/*.tex tables/*.tex 2>/dev/null | awk -F: '{s+=$NF} END{print s+0}')
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

Report as: sections touched, what was cut by class (1–9), and explicitly
**what was kept and why** — the kept-list is the evidence that tightening did
not become overclaiming. Do not report a "% reduction" as the headline; the
headline is that the argument reads straight through.

## Anti-pattern

Do not run this skill twice on the same text expecting further gain. The second
pass finds nothing safe to cut and starts eating scope qualifiers to justify
itself. One pass, then stop.

The exception is a **class-7-only** pass. Classes 1–6 and 8 are sentence-local and
are genuinely exhausted in one run; class 7 is not, because it is created fresh
every time a section is rewritten — tightening §4 to point at a table leaves the
intro bullet that pre-plays §4 untouched. After any round of section rewriting,
re-emit the paragraph map (step 1) and diff the one-line summaries. Nothing
else.
