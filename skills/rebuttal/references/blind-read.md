# Blind read: instructions for the fresh reader

This file is the only method text the blind reader gets (Phase 6.5 step 1, and again at acceptance). The reader is a fresh subagent that has not drafted the reply, run the experiments or seen the issue board. It is handed three things: this file, one reviewer's raw review, and the stripped text of the reply to that reviewer. It opens nothing else — no other file, no grep, no git, no web — and it fixes nothing: it writes a ledger.

Whoever drafted the reply can no longer see its jargon; every invented label is silently read as "the obvious meaning". The blind read exists to keep the signal "I could not parse this", which is lost the moment the evidence is read. That is why verification, deletion and rewording live in a separate file ([wording-pass.md](wording-pass.md)) that the blind reader is not given.

## 1. Who you are reading as

| Reader | Has | So |
|---|---|---|
| The reviewer | their own review, the submitted PDF, this thread up to the current sentence | a definition must come before first use; the reviewer's own words need no definition |
| The AC | the review and this thread; will not reopen the PDF | every number needs its address (rhetoric C2) and every paragraph its conclusion (C4) |
| The table reader | one table and its caption | column heads and row labels are self-sufficient; "defined in the text below" counts as undefined |

None of them has the repository, the experiment plan, the issue board, the group chat or the other reviewers' threads.

**Vocabulary order.** When a thing needs a name, take the first that exists: (1) the word the reviewer used for it, (2) the word the submitted paper uses, (3) the standard term in the field. Never a fourth word invented while drafting or running the experiments.

## 2. What to record

Read the reply once, front to back, at normal speed, as the reviewer who wrote the review. Record three signals:

- **Stall** — had to reread or scroll back. Types: a term or abbreviation with no definition or defined later than first use; a label invented by us ("the D1 judge", "split a", "Same recipe"); a referent that has not been named ("both versions", "the two pools"); one word used for two things, or two words for one thing; a number whose noun has not appeared yet ("at rank 32" before any mention of LoRA); a name that says A while the sentence describes B; a ratio or speedup with no stated comparator ("1.6× faster" — than what?).
- **Idle** — read without effort, but the sentence defines nothing, claims nothing and answers nothing the reviewer asked. Test: delete it and reread the paragraph; if no conclusion loses support, record it. (Only mark it; whether it is deleted is decided later, with full context.)
- **Lineage and internal names** — these read smoothly and sit in load-bearing sentences, so the first two signals miss them. Internal names: experiment IDs (`A5`, `B2c`), run and checkpoint names, machine names, paths, status tags, the board's shorthand. Lineage words: "the retrained one", "the re-scored copy", "the earlier run", "the leave-one-out version", "v2". For each ask: *what does this tell the reviewer about what went into the model?* If nothing, record it.

Also recorded, never fixed by rewording (they go to the user):

- two numbers in the reply that look like the same quantity and differ;
- a count that does not add up ("four experiments" followed by five);
- a sentence that contradicts another sentence in the reply or the reviewer's quoted text;
- a sub-question of the reviewer that no sentence answers (rhetoric C13).

Not recorded: unfamiliar but standard terms (LoRA, Spearman, Holm correction, bootstrap, best-of-N); terms the reviewer used; terms the paper defines and the reply uses in the same sense. Clearing covers the word, not its number: a standard term whose number restates something the sentence already says in the reader's unit, or only describes how the run was set up (worker count, parallelism degree, hit rate), is still recorded as **idle**. The reader lists the terms it checked and cleared, so the next step does not rewrite them into plain words.

**Calibration.** A reply of 3–5k characters yields about 3–10 load-bearing entries. Above 15, the problem is structural (the reply is a diff against the plan, or assumes another thread): stop listing and say so.

Ledger, one file per reviewer under `rebuttal/wording/<UTC timestamp>/ledger-<ReviewerID>.md`, one block per entry:

```
### N. <one-line title>
- where: A2, sentence 3 (quote the first six words)
- sentence: <verbatim>
- type: undefined term | invented label | unnamed referent | number before noun | drifting word | internal name | lineage word | idle | (report) mismatch / contradiction / unanswered
- why it stalls: <one sentence>
- my guess: <what it probably means>   confidence: sure | guess | no idea
- severity: load-bearing | local | cosmetic
```

End the ledger with three sections: **Document-level findings** (problems not tied to one sentence), **Report-type findings** (mismatches, contradictions, unanswered sub-questions), **Cleared terms**.
