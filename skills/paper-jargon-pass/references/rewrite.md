# Rewrite: active voice, cohesion, clarity

`/paper-jargon-pass` reads this file in its rewrite step (改写), after the term fixes of the second pass. It is about **rewriting** sentences that stay. **Cutting** is `/paper-prose-tighten`'s job and runs before this skill: never cut here, and never rewrite there (user 2026-11-12: 「改写专门开个 reference/ 里面的 .md 把, 删和改不要放一个」).

The usual entry point is [`/paper-polish`](../../paper-polish/SKILL.md), which has a fresh editor subagent run `/paper-prose-tighten`, then `/paper-jargon-pass` and this file, and has the text's owner check every edit.

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
| `Each block is scored by the localization LoRA, and the top three are kept.` | `The localization LoRA scores each block, and we keep the top three.` |

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
| `Moreover, … Furthermore, … Additionally, …` opening consecutive sentences | A connective that names the relation (`therefore`, `because`, `for example`, `first … then`), or none |
| The same thing called by a new name each time to avoid repetition | One noun throughout; this is the skill's 同物异名 rule |
| `This` / `It` with two possible antecedents | Add the noun (`This gap shows`); this is the skill's 悬空指代 rule |

**Pattern:** read each paragraph as one argument. Its first sentence says what it answers or how it follows the last; each later sentence starts from something the reader already has.

**Not this section:** adding a transition sentence, a summary of what the paragraph is about to say, or a recap. Cohesion comes from sentence order and the first words of each sentence, not from new sentences. A paragraph does not get longer.

```bash
command grep -nE '(Moreover|Furthermore|Additionally|In addition),' $FILES
```

## 3. Clarity of each sentence (清晰)

| Problem | Write |
|---------|-------|
| Two independent claims in one sentence joined by `and` / `;` | Split: one claim per sentence (the skill's 一句话塞太多 is the extreme case) |
| A long qualifying clause between subject and verb | Move the clause after the verb, or into its own sentence |
| Nominalizations (`a comparison is made`, `leads to an improvement in`, `the computation of`) | The verb: `we compare`, `improves`, `we compute` |
| Vague scope (`across settings`, `in most cases`) | The concrete scope the evidence has (`on all four benchmarks`, `in three of four`), only when the text already states it somewhere; otherwise leave it and report |

**Hold the scope.** A split or reorder must not move a qualifier so that it seems to scope a different clause (`on two benchmarks` drifting to the end of a sentence, where it reads as scoping only the last clause).

## 4. Order and limits

1. Run after the term fixes of the second pass: a sentence is rewritten once, with its terms already settled.
2. One pass. A second rewrite of rewritten text trades one smooth phrasing for another and drifts terms.
3. Only rewrite; never cut a sentence here. A sentence that looks empty goes back to `/paper-prose-tighten` (or, for a reply, is reported).
4. No new terms, no new claims, no new hedges or caveats.
5. Report what was rewritten by section (voice / cohesion / clarity), after the term fixes in the skill's report.
