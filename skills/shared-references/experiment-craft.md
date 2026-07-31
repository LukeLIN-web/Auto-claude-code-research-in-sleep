# Experiment Craft: Search Order, Comparability, Reuse

`experiment-integrity.md` draws the line between an honest experiment and a
fraudulent one. This file is about the layer above: **which experiment to run
next, and how to run it so the result is still usable three months later.**

Source: practitioner notes in
[LukeLIN-web/blogs — How-to-write-paper](https://github.com/LukeLIN-web/blogs/blob/master/How-to-write-paper.md),
distilled into rules.

## When to Read

- `experiment-plan` / `ablation-planner`: when ordering the run queue.
- `experiment-bridge` / `run-experiment`: before launching a batch.
- Whenever the next run is being chosen by intuition rather than by a table.

## 1. Search order: big swings first

- **Try the large change before the small one.** If the large change works, the
  small ones become unnecessary; if it fails, the entire direction may be dead
  and every hyperparameter sweep under it was wasted. Ordering by cost is a trap;
  order by *how much of the search space the outcome eliminates*.
- Same logic within a single run: start at the aggressive setting (large learning
  rate, full method, every component enabled) and only fine-tune downward when
  time is running out.
- **Do not iterate on the second-best setting.** Swap the few decisive knobs in
  large steps, find the best regime, and only then refine locally.
- If a component makes the method stronger, **use it** — keep stacking working
  ideas until the metric stops moving. A method held back "for simplicity" while
  the numbers are still climbing is an unfinished method.
- Hesitation is more expensive than a run. If deciding takes longer than the
  experiment, launch the experiment.
- Reading papers is not a substitute for running one. Form a hypothesis, run it,
  and keep reading while it runs.

## 2. Everything is an ablation — if it is comparable

The reason to enforce comparability up front is that it converts every side
experiment into paper material for free.

- **Keep the baseline setting fixed** for every run unless the run's whole point
  is to vary it. A run that differs from the baseline on two axes cannot enter
  any table.
- **Equal effective batch size across compared rows** — use gradient accumulation
  when hardware forces different micro-batches. Different batch sizes in one
  table is the single most common "unfair comparison" objection.
- **Do not delete checkpoints.** Storage is cheaper than a rerun, and a
  mid-training checkpoint is often exactly the ablation a reviewer asks for.
- **Never resume from a checkpoint trained with buggy code.** Fix the bug and
  retrain from scratch — a patched-forward checkpoint carries state you cannot
  describe in the paper.
- Every extra table has a home in the appendix, so no completed, comparable run
  is wasted.

## 3. Run a table, not a hunch

- Write the target table out in full — all rows, all columns — **before** running
  anything, then fill cells one by one. Sampling many directions shallowly
  produces a set of results that supports no claim; one table filled completely
  supports a section.
- When writing the paper, maintain an explicit list of experiments still to add,
  and work it down in order.
- Choose the strongest known setting as the reference point, not the setting a
  weak prior paper happened to use. Matching a weak baseline's configuration is
  defensible as a *fairness ablation*, but the headline comparison should be
  against the best available configuration. Under time pressure, run the best
  setting first.
- Verify the mechanism, not just the metric: visualize what the method actually
  selects/attends/produces and confirm it matches the story being told.

## 4. Reporting

- Report **standard deviation or standard error** across seeds. Plan the seed
  budget when planning the table, not after the numbers look good.
- Check GPU memory occupancy right after launch — a job that silently fell back
  to a smaller effective configuration invalidates the row.
- Declare the evaluation type honestly (`experiment-integrity.md`) and label
  pilot-scale runs as pilots.

## 5. Collaboration

- **Ship runnable code, not verbal instructions.** A collaborator who has to
  modify your code to run it will modify it differently than you did, and the
  two sides silently diverge. Hand over something that runs unchanged.
- Fix author order early and keep it. People calibrate their effort to it, and
  changing it later costs more than it saves.
- Pull collaborators in per need, and let the contribution record set the author
  list. A collaborator unwilling to spend time is not a collaborator.
- Automate once the workflow is stable — do the loop by hand a few times first,
  so what gets automated is the real procedure and not a guess at it.

## Related

- `experiment-integrity.md` — what makes a result honest (hard boundary).
- `evidence-precheck.md` — mechanical checks before claiming a result.
- `manuscript-craft.md` — how completed runs become tables in the paper.
