# Rewrite: active voice, cohesion, clarity, merging

`/paper-polish`'s editor reads this file in step 4, after the term fixes of `/paper-jargon-pass`'s second pass. It is about **rewriting** sentences that stay. **Cutting** is `/paper-prose-tighten`'s job and runs before this skill: never cut here, and never rewrite there (user 2026-11-12: 「改写专门开个 reference/ 里面的 .md 把, 删和改不要放一个」).

Origin: for a rebuttal, the user asked 「我们尽量用 We 这样子的主动语态，你让 AI 给你加强下表达和衔接，以及语言的 clarity」, then 「先 paper prose tighten, 再 paper jargon pass」.

Rewriting holds the claim constant in the same way cutting does: every number, qualifier, scope word, citation and address stays; for each paragraph touched, write one line of what it claimed before and after. Any difference is a bug.

## 1. Passive voice where we did it (被动语态 → We 主动)

The authors trained, compared, measured and report; the draft says *was trained*, *is compared*, *was measured*, *are reported*. An agent that ran the experiments narrates them as events that happened to the artifacts. The reader loses who did what, and the sentence gets longer.

| Before | After |
|-----|-------|
| `The judge was fine-tuned on the human scores of the training generators.` | `We fine-tuned the judge on the human scores of the training generators.` |
| `A comparison with X is performed in Table~\ref{tab:x}.` | `Table~\ref{tab:x} compares our method with X.` |
| `The per-category results are reported in Appendix~H.` | `We report the per-category results in Appendix~H.` |
| `It can be seen from Table~3 that the gap holds on every benchmark.` | `Table~3 shows that the gap holds on every benchmark.` |
| `Each filter is scored by the saliency head, and the lowest-scoring half is pruned.` | `The saliency head scores each filter, and we prune the lowest-scoring half.` |

**Pattern:** when the authors are the actor, `we` is the subject and the verb is active. When the actor is a method, a model, a table or a result, that becomes the subject (`Our judge ranks …`, `Table 3 shows …`, `The gap holds …`). `we` is the default actor, not the only one. An impersonal opener (`It should be noted that`, `It is worth noting that`) is filler; `/paper-prose-tighten` class 2 cuts it, and if one is still there, the sentence starts with its subject.

**Keep passive:**
- the actor is unknown or irrelevant and naming one would mislead or invent a fact (`each video is rated by three annotators`, `prompts are sampled uniformly`). Never invent an actor to avoid a passive;
- quoted text (a reviewer's words, another paper's sentence, a co-author's sentence in a shared draft);
- a long method list where every clause would get a filler `we`: switch to active at the first sentence where who acted matters.

**Not an improvement:** putting `We find that` / `We observe that` / `We show that` before a result. `All four contrasts are significant.` is already active and is the claim; the wrapper is meta-narration.

**Grep (recall aid; read each hit):**

```bash
command grep -niE '\b(is|are|was|were|been|being|be) ([a-z-]+ed|done|run|made|shown|given|chosen|taken|seen|written|drawn|known|built|kept|held|set|found)\b|\bit (is|can be|should be) (shown|seen|noted|observed|found)|\bit is (worth|important) ' $FILES
```

## 2. Cohesion (衔接)

Each sentence is correct, but the reader has to work out how it connects to the one before. Drafts written one result at a time read as a list of facts rather than one line of argument.

| Problem | Write |
|---------|-------|
| A sentence opens with a new term and ends with the known one (`A held-out generator family is what the second test uses`) | Known first, new last: `The second test uses a held-out generator family.` |
| A paragraph starts with no link to the question or the previous paragraph | First sentence says the relation: `To test whether …, we …`, `This result also holds for unseen prompts: …` |
| `Moreover, … Furthermore, … Additionally, …` opening consecutive sentences | A connective that names the relation (`therefore`, `since`, `for example`, `first … then`), or none |
| The same thing called by a new name each time to avoid repetition | One noun throughout; this is `/paper-jargon-pass`'s 同物异名 rule |
| `This` / `It` with two possible antecedents | Add the noun (`This gap shows`); this is `/paper-jargon-pass`'s 悬空指代 rule |

**Pattern:** read each paragraph as one argument. Its first sentence says what it answers or how it follows the last; each later sentence starts from something the reader already has.

**Not this section:** adding a transition sentence, a summary of what the paragraph is about to say, or a recap. Cohesion comes from sentence order and the first words of each sentence, not from new sentences. A paragraph does not get longer.

```bash
command grep -nE '(Moreover|Furthermore|Additionally|In addition),' $FILES
```

## 3. Clarity of each sentence (清晰)

| Problem | Write |
|---------|-------|
| Two independent claims in one sentence joined by `and` / `;` | Split: one claim per sentence (`/paper-jargon-pass`'s 一句话塞太多 is the extreme case). Claims that share a predicate are not independent: they stay in one sentence, and § 4 merges them when they are apart |
| A long qualifying clause between subject and verb | Move the clause after the verb, or into its own sentence |
| More than four commas in one sentence, or an aside wedged mid-sentence between commas (`A outperforms B and, when X holds, C.`) | Split into two sentences, or move the aside to the end (`A outperforms B. It also outperforms C when X holds.`). At most four commas per sentence; commas inside `\cite{}`, math and numbers do not count |
| Nominalizations (`a comparison is made`, `leads to an improvement in`, `the computation of`) | The verb: `we compare`, `improves`, `we compute` |
| `because` joining a reason to a claim (`because the encoder is pre-trained without the property head, fine-tuning degrades …`) | `as` or `since`: `because` asserts the cause outright, and papers rarely use it; keep it only where the text reports a test of that cause. If neither the softer word nor the evidence fits, the clause is a claim change: leave it and report |
| A number pair trailing the sentence after a comma or colon (`…, our method significantly lifts the classifier, a\% against b\%.`): it reads like a sports score (user 2026-11-16, from a forwarded review) | The pair goes into the predicate with its metric named: `significantly raises overall accuracy from b\% to a\%` when ours is the compared system plus the method's change; between two separate systems, in parentheses after the comparison (`outperforms X (a\% against b\%)`). The numbers, the significance word and the compared system stay as they were (`manuscript-craft.md` §2, Introduction) |
| An ablation paragraph, main text or appendix, walks the variants one by one (`ours outperforms variant A on X, and variants B and C on Y and Z`) (user 2026-11-23) | Merge the subjects by question: name the variants that answer one question as a group by what they share, one sentence with the verdict that holds for every member, one decisive pair of numbers and the table pointer. Scope and significance words stay as they were; sentences that read different floats for different questions stay apart (`manuscript-craft.md` §2, Experiments) |
| A relative clause ending on a stranded preposition (`evaluated on the stations it was trained on`, `tests only on stations it was calibrated on`, `sequences of the seasons it was tuned on`); several in one paragraph ending on the same word read as very awkward (user 2026-11-16, from a forwarded review) | A noun phrase that names the same set: `its training stations`, `seen stations`, `stations used during calibration`, `previously tuned seasons`. The set must not change (the stations a model was calibrated on are not the stations it was evaluated on). If no noun phrase names the same set, at most one such clause stays per paragraph |
| A section, subsection or `\paragraph` heading longer than seven words (user 2026-11-18「标题太长是不可接受的」, 「标题应该7个词之内」). A heading that carries the paragraph's conditions or two topics joined by `and` (`Training the judge without the episodes where annotators disagree, and fine-tuning on a quarter of the prompts`, 18 words) is a sentence, not a heading | At most seven words, naming the topic the paragraph answers (`Judge training without disputed episodes`); a heading with two topics names what they share (`Two reduced training sets`). Each condition the heading dropped must already be stated in the paragraph's text; if one is not, it moves into the paragraph's first sentence on the same line, with no new sentence. Count words as printed: a hyphenated word, a math span and a `\ref` are one word each. This holds for every heading in scope, edited or not; one in a frozen span goes in the list of what you would change but may not |
| Vague scope (`across settings`, `in most cases`) | The concrete scope the evidence has (`on all four benchmarks`, `in three of four`), checked in the text or the evidence files; report it only when they do not settle it |

```bash
command grep -niE '\bbecause\b' $FILES
command grep -nE '^([^,]*,){5,}' $FILES   # lines with five or more commas (one sentence per line); discount \cite, math, numbers
command grep -nE '[,:] *(in )?[0-9.]+\\?% (against|versus|vs\.?) [0-9.]' $FILES   # number pair trailing after a comma or colon
command grep -nE ' (on|in|from|with|for|at|by|of|about)( *~?\\cite\{[^}]*\})? *([,.;:)]|$)' $FILES   # clause ending on a stranded preposition
command grep -nE '\\((sub)*section|paragraph)\*?\{[^}]*( +[^ }]+){7}' $FILES   # heading of eight or more words (recall aid; count as printed)
```

**Hold the scope.** A split or reorder must not move a qualifier so that it seems to scope a different clause (`on two benchmarks` drifting to the end of a sentence, where it reads as scoping only the last clause).

## 4. Merge sentences that share a predicate (合并)

A paragraph grows by one sentence each time a result arrives, a reviewer asks about one cell, or a deleted sentence is put back. Each new sentence repeats the subject and the predicate of its neighbour to add one more case. Splitting (§ 3) never shortens this; merging does. Prefer the merge whenever it fits the limits below (user 2026-11-20「尽量合并话语, 不然话语越来越长」).

| Problem | Write |
|---------|-------|
| Consecutive sentences with one predicate over different pairs or conditions (`With and without the cache, accuracy does not differ significantly for A or for B.` / `Neither does that of A without the cache and B without the cache.`) | One sentence, the predicate once: `On Bench-1, the cache makes no significant difference to A or to B, and neither does fine-tuning without it.` |
| A sentence that restates the previous sentence's subject and setting to add one case (`On Bench-1, our method … .` / `On Bench-1, our method also … .`) | The case joins the first sentence as a second object or a second clause with `it` |
| A sentence added in a later round (a new result, an answer to a reviewer, a restored sentence) standing after a sentence with the same subject or predicate | It goes into that sentence. A revision adds a clause, not a sentence, whenever an existing sentence can carry it |
| The setting named again in every sentence (`without the cache` three times in two sentences) | Named once, as the sentence's opening adverbial or its last phrase |

**Pattern:** before keeping two neighbouring sentences, ask what they share. A shared subject becomes one subject with two verbs; a shared predicate becomes one predicate with a list. The same verb against the same baseline over several benchmarks is `/paper-prose-tighten` class 13 and was merged in step 3; this section takes what that class leaves, where the predicate is shared and the compared pairs differ.

**Limits.**
- Every case of the merged sentences is still stated. Leaving one out (keeping only the pair a reviewer asked about) is a cut, and a claim change: report it, and the user decides.
- The merged sentence has at most four commas and one layer of qualification (§ 3). When it would not fit, merge two of three, or leave them apart.
- A word stated once must be true of every case under it: `significantly` moves in front of a list only when each merged comparison had it. Its count then drops; say so in the change list, since the owner's term check flags the drop.
- Different metrics stay in separate sentences, as in class 13.
- A qualifier keeps its scope (**Hold the scope**, § 3).

**Lines.** The merged sentence goes on the line of the first sentence. Each other merged line becomes exactly `%CUT`, and the change list names the line that took it in.

## 5. Order and limits

1. Run after the term fixes of the second pass: a sentence is rewritten once, with its terms already settled.
2. One pass. A second rewrite of rewritten text trades one smooth phrasing for another and drifts terms.
3. Only rewrite; never cut a sentence here. A sentence that looks empty is reported (cutting was step 3, `/paper-prose-tighten`). A merge under § 4 is not a cut: every case it held is still stated.
4. No new terms, no new claims, no new hedges or caveats.
5. Report what was rewritten by section (voice / cohesion / clarity / merge), after the term fixes.

## 6. Common misjudgments

| Symptom | Correction |
|---|---|
| A sentence is cut while rewriting voice or cohesion | Cutting and rewriting are separate steps (user 2026-11-12「删和改不要放一个」); report it |
| "We find that" is put before a result to make it active | The result sentence is already active and is the claim; `we` goes where the authors acted |
| An unknown-actor passive is forced active ("Annotators rated each video three times" invented from "each video is rated by three annotators") | Passive stays when the actor is unknown or irrelevant; never invent an actor |
| A synonym is swapped in so the text does not repeat a noun | One noun per thing; repetition is cohesion. Comparison verbs are the exception: `outperforms` may rotate within the list in `manuscript-craft.md` §2, Experiments (`performs better than`, `achieves a higher success rate than`, …), with `significantly` kept on exactly the comparisons that had it |
| A transition sentence or recap is added for flow | Cohesion comes from order and first words; no new sentences |
| A long sentence is split and the paragraph gains a sentence each round; or two sentences with one predicate are left apart because each is short | Split only independent claims; merge the ones that share a subject or predicate (§ 4) |
| A merge quietly drops one of the cases it joined | That is a cut and a claim change; every case stays, or the edit is reported, not made |
