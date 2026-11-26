# Distinguishing Your Work from the Closest Prior Work

A reviewer who reads the method as "a combination of known components" is asking one question: what do the
closest two or three papers not do that this one does? The paper must answer it in a place the reviewer will
find, in the Introduction's gap paragraph or in Related Work. This file is how to write that answer.

## Where it goes

Put each close paper in the paragraph of the line of work it belongs to. Do not add a separate
"Relation to A and B" paragraph or a "First, ... Second, ... Third, ..." list of differences at the end: it reads
as a defense bolted on after a review, and it repeats what the topic paragraphs already say.

## The shape: introduce, then the gap

Two moves per close paper, in this order.

1. **Introduce it fairly.** One sentence on what it does, in its own terms, specific enough that its authors
   would accept it. A reader who does not know the paper must be able to follow the next sentence.
2. **State what it leaves undone, as one general sentence.** Name the consequence of its design, then the
   question that design leaves open, the one your paper answers. Let the second sentence grow out of the
   first (`rather than ..., leaving ... unexplored`, `which leaves open whether ...`, `only to ...`). A bare
   "so it does not ..." is still a negation with a connective in front; say what remains open instead.

Do not itemize negations. "It does not do A, keep B, or test on C" is a checklist of your own features with
"not" in front. Find the one property of the prior work that all three follow from and say that.

| Stiff | Natural |
|---|---|
| "A trains the forecaster on reanalysis only; it does not use station data, correct for local bias, or test beyond ten days." | "A trains the forecaster on reanalysis alone. Its targets are therefore gridded fields, which leaves open whether such a model can be corrected toward point observations or stays skilful beyond ten days." |
| "B, whose recipe we follow, distills a global model into a regional one; it has no learned bias correction and trains no corrector." | "B distills a global model into a regional one. Its regional model is corrected by a fixed lookup table, leaving the pairing of a distilled model with a learned correction unexplored." |

Three things the left column gets wrong, each a separate rule:

- **No debt statements in the positioning sentence.** "Whose recipe we follow", "on which we build" belong in
  Method, where the recipe is used and cited. In Related Work they make the sentence about you before the
  reader knows the other paper.
- **No shorthand the reader has to decode.** "Trains no corrector" is a label from the authors' own notes. Say
  what the system physically does instead ("is corrected by a fixed lookup table").
- **Generalize.** One sentence about what the design implies beats three clauses about what is absent.

## Finding the differences: look past the mechanism

The mechanism difference is the first one authors see and often the thinnest. Before writing, read each close
paper for every row below and note where it does not hold up. One or two rows usually give a stronger and more
verifiable distinction than the mechanism.

| Ask of the prior work | Where to check |
|---|---|
| Are code and weights released? Is the release real or "coming soon"? | the arXiv abstract page, every version; the project page; the repository itself (commits, files, a model card) |
| Does it depend on proprietary models or a paid API, in training or at deployment? | the paper's setup section and appendix |
| Is it evaluated on the tasks it trained or collected on, or on held-out ones? | the task list and the split description |
| Does it need per-task training, per-task prompts, new demonstrations, CAD models or privileged simulator state? | method and setup |
| Simulation only, or also a real robot or real data? | experiments |
| Does it compare against the simplest strong baseline under the same protocol, and does it beat it? | the main table; whether the baseline numbers are run or quoted |
| What does one run cost in time, calls and money, and is it reported? | experiments, appendix |
| Does it test the configuration your paper cares about at all? (e.g. it reports skill on gridded fields and never at the station locations your paper targets) | the experiment list; note the experiment that is missing |

Rules for using what you find:

- **Verify before writing, and record the date and the arXiv version.** "No code released" is false the day a
  repository appears; check the repository itself, not your memory of the paper. If the paper has several
  versions, the answer can differ by version.
- **Prefer facts the paper itself states.** "Uses a proprietary reanalysis product and a paid observation feed" can be read
  off the setup section and will not change. "Has not released code" is true only as of a date; write it only
  if it matters to your claim, and keep the check in your notes.
- **Write a limitation only if your paper addresses it and shows it.** A weakness you do not fix is a jab, and
  the reviewer may be its author. Each limitation you name should have a result in your Experiments: a
  same-protocol comparison, a held-out evaluation, a run with local open models.
- **Do not claim a difference the prior work also has.** If it released code and weights, that is not your
  distinction; drop the row.
- **Concurrent work is cited and discussed, not counted against novelty**; say it is concurrent if the venue's
  rules make it so.

## Check before leaving the paragraph

1. Can a reader who has not read the prior paper say what it does after your first sentence?
2. Is the gap one sentence that follows from that description, with no list of negations?
3. Is every stated limitation verified against the paper or its release, with the version noted?
4. Does each limitation point at a result in your own Experiments?
5. Is every word in the two sentences one the field uses, with no label from your own notes?
