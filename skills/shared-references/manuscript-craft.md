# Manuscript Craft: Section Policy, Floats, and LaTeX Mechanics

`writing-principles.md` governs *narrative and prose*. This file governs the
**mechanical layer**: what goes in which section, how floats are placed, and the
LaTeX details that reviewers notice within seconds.

Source: practitioner notes in
[LukeLIN-web/blogs — How-to-write-paper](https://github.com/LukeLIN-web/blogs/blob/master/How-to-write-paper.md),
distilled into rules. Venue instructions always override this file.

## When to Read

- `paper-write`: before drafting Method / Experiments, and during the final pass.
- `research-paper-writing`: before drafting the Introduction, a Method, or an
  Abstract the authors asked for.
- `research-review`: the structure reviewer judges every section against §2.
- `paper-compile`: when fixing overfull boxes, float placement, or citation style.
- `resubmit-pipeline` / `paper-writing`: during submission-readiness checks.

## 1. Order of work

1. Figures and tables first (`figure-craft.md`).
2. Then the claims those artifacts support.
3. Prose last — **write no results text before the figures and tables are final.**

Results prose is the least-read part of the paper; it exists to point at the
table, not to re-narrate it. Time saved here goes into figures.

## 2. Section policy

### Abstract

User ruling 2026-11-16.

- **One or two headline numbers**: the results a reader should remember,
  usually the main comparison against the simplest strong baseline and the one
  that isolates the core component. No number at all, or a third comparison,
  is a defect.
- **The framework by what it can do, each component by its objective.** One
  sentence says what the whole system can do; then "Specifically, ..." gives
  each component's design objective, never its mechanics (user ruling
  2026-11-16, from a co-author note: "only introduce the high-level design and
  objective of each module"). The training signal and labels, the teacher a
  model is distilled from, selection rules, data mixtures and which weights
  change belong to the Method: "supervised with the planner's subgoal rather
  than the task instruction" and "trained on a proprietary planner's calls"
  interrupt the abstract.
- **Each headline comparison is one range over its benchmarks.** "Across
  several benchmarks, the method improves the backbone by a–b pp over the
  same-stack official recipe, and transfers to a second backbone, surpassing
  its published results by c–d pp", never "from x% to y% on A and from u% to
  v% on B" (user ruling 2026-11-16, 「分数你应该概括一下」). A range counts
  as one headline number. It spans every benchmark the sentence counts, its
  significance word holds only if every one of them is significant, and each
  endpoint is the difference of the exact rates rounded like a table cell, not
  of two printed cells.
- **Results in at most two sentences, each in its own frame, then the
  take-home message.** Result sentences that repeat one predicate ("X
  significantly outperforms Y" three times running) read like a lab report;
  merge them. The last sentence says what the reader should take away, a stance
  the results support; it is not one more comparison and not generic impact.

From a second review the user forwarded, 2026-11-16 (「更新 paper review skill」):

- **Each headline number says which comparison it belongs to.** The sentence
  names what the two sides share and the one thing that differs. The full
  system's gain over the bare baseline changes several components at once, so
  it is framed as the whole system's, never as evidence that one component
  works; the comparison that changes only that component says so. Which of
  the two comes first is the authors' call (user ruling 2026-11-16, 「这个顺序
  还是让 user 定」): a reviewer raises the order as a question, never as a
  defect, and an agent does not swap it unasked.
- **A number beside a property was obtained with that property.** When a
  sentence highlights a setting ("needs no privileged signal") and the next
  gives the best number, the number comes from that setting. If the best
  number needs the privileged signal, give the number the deployable setting
  reaches and the best one, each with its setting; the two settings of one
  comparison count as one comparison under the headline-number cap.
- **Background in at most two sentences, naming the specific difficulty.**
  "Instructions that must be interpreted" is true of every instruction; write
  the kind the method targets ("vague or knowledge-intensive instructions").
  Verbs say what the method does to its object: distillation trains a local
  model on a teacher's outputs; it does not "move" the teacher. When the
  abstract spills past the page it starts on, cut background and repeated
  conclusions first, the results last.

### Introduction

User ruling 2026-11-16, from a review the user forwarded.

- **Nothing before it is introduced.** No component of the method ("our
  distilled planner") appears before the paragraph that presents the method:
  state the motivating evidence without it, or move that evidence later. A set
  is named where it is counted: "four planners" says which four, or what they
  are ("one proprietary and three open models").
- **A reason joins the gap to the method.** Between the paragraph where the
  obvious fix fails and the one that presents the method, one sentence says why
  the method avoids that failure. It states a cause that the cited work or the
  paper's own ablation supports, or a property the method has by construction;
  never a mechanism nothing tested.
- **The method paragraph is not a Method summary.** It says what each
  component does and why it is needed. The benchmark the training data comes
  from, mixing ratios, the code base the method builds on, and the names of
  baselines or ablation rows ("Ours (frozen backbone)") stay in the Method and
  Experiments.
- **The results paragraph states conclusions, not a table.** Summarize by kind
  of generalization (new tasks, other simulators or datasets, other embodiments
  or models), with the one or two headline numbers and a pointer to the table;
  never a roll call of benchmark names. No "slightly": a result that cannot be
  stated without it is folded into its category or left to the tables.
- **Contributions are takeaways.** Each item runs at most about six printed
  lines (about 60 words) and repeats no sentence of the Introduction's prose;
  the cap on the whole list is under Method below.

From a second review the user forwarded, 2026-11-16:

- **One spine.** The Introduction runs one chain: the problem, why the obvious
  fix fails, why the method's ingredient may work, the method, how it is
  validated. A second motivation (cost, privacy, running locally) enters as
  what a component makes possible (large-scale collection, local deployment),
  beside that component; a paragraph of its own between the failed fix and
  the method breaks the chain.
- **A failure breakdown is a phenomenon, not an attribution.** "No tool ran in
  most failed episodes" or "the most common failure releases the object off
  its target" says what failures look like, not which component caused them:
  a wrong subgoal, a wrong completion judgment or a missed tool call from the
  planner ends the same way. State it as the motivation for studying the
  component the method changes; a sentence that blames that component needs an
  intervention that changes only it.
- **Universal qualifiers hold for every stage**, here, in the Abstract and in
  the contribution list. "All new training data come from X", "only W
  changes" and "without new demonstrations" are checked against each stage
  the paper describes, including stages trained on a teacher's outputs or
  mixed with external data. One that holds for a single stage names that stage
  ("the executor stage collects no expert demonstrations"), and "only W
  changes" names its reference point ("relative to the agent before
  fine-tuning").
- **Contribution items are independent, and an empirical item claims only what
  its controls isolate.** Proposing a method and showing that it works are one
  item. Beating alternative recipes shows that the recipe is better, not that
  one of its factors ("the model's own data") is "the primary driver"; that
  needs a variant changing only that factor. Otherwise state the item as a
  controlled comparison and name the factors it controlled.

From a third review the user forwarded, 2026-11-16 (「更新 skill」):

- **The method item names the whole method and carries what the prose sells.**
  Its title says what the method is as a whole ("A fully local, <property>
  <kind of system>"), never one of its stages, with the other stage left as a
  clause in the body. The body states the stages in order as one pipeline,
  each with its role. A property the Introduction's prose argues for a
  component (that it transfers to other datasets, embodiments or models)
  appears in that component's part of the item, stated in general terms; its
  numbers and benchmarks stay in the prose.
- **An item's title is a short noun phrase naming what the item contributes**:
  the method, the subject of a finding ("Empirical insights into adapting
  <component> within <system>"), the improvement ("Significant improvements on
  six benchmarks"). A sentence that states a finding ("Keeping only X
  outperforms Y and Z") is the body's first sentence, not the title. The body
  names each compared alternative by what it is ("scripted demonstrations",
  not a table row's label) and the property the finding is about.
- **The list introduces no name.** Every benchmark, split, coined term and
  variant name in an item appears in the Introduction's prose before the list.
  A name the paper itself defines (a task subset named by its size, an
  internal arm name) is described in words ("on held-out tasks") unless the
  prose has introduced it.

From a fourth review the user forwarded, 2026-11-16 (「更新 skill」):

- **No evaluation protocol in the Introduction.** Episodes or trials per
  task, seeds, step or time caps and the statistical test belong to the Setup
  and the protocol table. A result sentence opened by one ("With ten episodes
  per task on B, ours lifts ...") spends the Introduction on a detail and reads
  as trivia; it becomes "On B, ours lifts ...". The Experiments keep the
  protocol where the comparison needs it.
- **A result sentence carries its numbers in the predicate.** "Raises
  overall success from b% to a%" when ours is the compared system plus the
  method's change; between two separate systems, the pair in parentheses after
  the comparison. A pair trailing the sentence after a comma ("..., ours
  significantly lifts the agent, a% against b%.") reads like a sports score.
  This holds in every section; the rewrite pattern is `paper-polish`'s
  `references/rewrite.md` §3, and `check_draft.py` flags the trailing form.

### Method

- Open with a **road-map paragraph** that states what the section will build,
  then keep summarizing as the section proceeds.
- **Aim for a citation-free Method section.** Every `\cite` inside the method
  reads as "this part is someone else's". If a comparison is genuinely needed,
  move it out (see below). This is a strong default, not an absolute: cite when
  you genuinely build on a named prior construction, and let the surrounding
  text make the delta explicit.
- Do not explain other people's methods here. Write *your* method; put the
  comparison in a dedicated **Advantages** paragraph or subsection that contrasts
  against prior work in one place.
- Structure the contribution as ~3 novelty points — typically two technical and
  one empirical. Write those first; the supporting results follow. The
  contribution list runs **at most 263 words**: the p90 of award papers'
  lists, whose median is 87 (user ruling 2026-11-16).
- If two techniques are introduced, write the **connection** between them.
  Presenting them side by side signals "two unrelated tricks bolted together";
  presenting the mechanism that links them signals one method.

User ruling 2026-11-16, from a review the user forwarded:

- **The Method describes the configuration the main rows run.** When a
  component can take its input from two sources (a ground-truth signal or a
  learned judge, a privileged input or a deployable one), say which one the
  method's reported rows use, and introduce the other as a variant under the
  name its table row carries, with a pointer to the experiment. A capability
  the Abstract or Introduction claims ("needs no X") reads in the Method as
  what that variant does, never as the default pipeline while the main rows
  use X; otherwise a reviewer finds the main table running on X and charges
  the paper with overclaiming.
- **Every filter or exclusion in an equation carries its reason, next to the
  equation.** The reason is a property the design has by construction (what
  triggers the excluded event, what the kept data are guaranteed to contain),
  cited work, or the paper's own ablation with a significant difference; never
  a plausible mechanism nothing tested, and never an ablation cell that did not
  reach significance. A by-construction reason is checked against the code or
  prompt that defines the trigger, and that trigger is described where the
  component is introduced.
- **The unit of training is stated before the first results table.** Whether
  one set of trained weights serves every benchmark or each domain (simulator,
  embodiment, dataset) gets its own run, from which starting weights and with
  which data in place of the default ones, is said in the Method subsection
  that defines training. Not first in the Setup, an Advantages paragraph or the
  appendix: a table that mixes domains otherwise reads as one model sweeping
  all of them.

### Experiments

- **One section for all experiments.** Multiple experiment sections read as an
  unfocused paper (and several venues state this explicitly).
- Report **speedup / reduction ratios**, not just raw latency and throughput.
  A reviewer wants `2.3$\times$ faster`, not two tables to divide mentally.
- Analysis prose is the lowest-value text in the paper — tables and figures carry
  the argument.

User ruling 2026-11-16, on the section's shape:

- **Setup, then three results subsections of similar length, each answering
  one reader question.** Setup keeps run-in headings (`\paragraph{Benchmarks
  and protocol.}`, `\paragraph{Systems.}`, `\paragraph{Variants.}`); the
  significance definition is the last sentence of the protocol paragraph, not
  a paragraph of its own. The results follow in this order:
  1. *End-to-end performance and generalization*: the full method against the
     simplest strong baseline and the published alternatives, what the
     component kept at deployment adds, and transfer to other simulators,
     robots or models.
  2. *Dissecting the method's pipeline*: the ablations in pipeline order
     (against the unmodified model, where the training data come from and how
     they are labeled, how they are selected, the training recipe, the data
     scale).
  3. *Behavior and cost*: the change in behavior behind the gains (failure and
     recovery breakdowns, which object the policy acts on), then what the gains
     cost (time per episode, latency).
  Subsections follow these questions, not the contribution list: a
  contribution whose evidence is one paragraph is that paragraph, found by its
  topic sentence, not a subsection of its own. "Main Results" plus one
  subsection holding every other result, and a subsection of one paragraph,
  are both wrong shapes.
- **No run-in headings in the results.** After Setup, paragraphs carry no
  `\paragraph{}`; a bold heading on every results paragraph fragments the
  section. Each paragraph opens with a topic sentence that states its finding
  and carries the transition from the paragraph before. When a heading is
  removed and the paragraph's first sentence is a definition or a baseline's
  behavior, the paragraph gets a topic sentence built from its own finding,
  with no claim the paragraph does not already make.

User ruling 2026-11-16, from a review the user forwarded:

- **A results paragraph states a finding; it does not narrate the tests.** The
  first sentence gives the finding for a kind of setting ("the gain holds on
  every long-horizon benchmark"), then one or two representative numbers, then
  the reason. Group the benchmarks by what they test and give each group one
  verdict, the one that holds for every member; name a single benchmark only
  where it departs from its group or carries the reason. The values stay in the
  table. Three sentences in one paragraph in the frame "X (significantly)
  outperforms Y on A, B and C, and outperforms it on D", or one comparison
  sentence naming four or more benchmarks, is a test log pasted into prose.
  Merging the list into a verdict keeps every scope word it carried: each
  benchmark against several combined, the averaged metric, `slightly`, a
  control's matching condition ("for as many steps as ours"). After the
  rewrite a fresh reader compares old and new claim by claim.
- **The reason comes from the paper's own evidence.** A sentence on why a gain
  occurs cites a measurement in the paper (an ablation, a breakdown of failure
  states) or a property the data have by construction. A mechanism a reviewer
  proposes is checked against the method's definitions first (what the
  training data actually contain); with no evidence, no reason sentence.
  What a component does by construction is not why the gain occurred: when the
  compared systems differ in several components, a reason naming one of them
  needs a variant that changes only that one. Where the gain concentrates is a
  verdict, not a reason; it stands when the comparison that changes only that
  variable is significant on each benchmark of the group.
- **An ablation paragraph answers its question once; it does not walk the
  variants.** A paragraph whose sentences each compare ours with one more
  variant, each with its own pair of numbers ("it significantly outperforms A,
  a% against b%. It also outperforms B, c% against d%."), is the ablation
  table in prose even when each sentence names one benchmark, and a topic
  sentence in front of the walk does not change that. The paragraph gives the
  answer for the whole family of variants ("every other source of training
  data falls below ours, each significantly in at least one setting"), keeps
  the one comparison the answer turns on, gives the reason, and points to the
  table for the rest. A paragraph carries at most four number pairs
  (`a% against b%`): the per-sentence limit alone lets through a paragraph of
  seven sentences with one pair each. When every appendix experiment needs a
  main-text mention, the mentions join the answer to the question they belong
  to, one pointer sentence per question, not one sentence per variant.
- **A measurement that explains a gain is that gain's reason, written as
  one.** A breakdown of failure kinds, which object the policy acts on first,
  or which kind of task gains most is the paper's insight. Written as one more
  comparison with no gain named ("Ours stalls in significantly fewer
  episodes"), it reads as more log, and the gain it explains stays
  unexplained. It goes into the behavior-and-cost subsection, in a paragraph
  that opens with the gain it explains and gives the measurement as its
  reason ("the fine-tuned policy's gain comes from fewer stalled episodes and
  fewer wrong-object grasps"). That sentence holds only when the two systems
  differ only in the component the measurement concerns, the breakdown's
  difference is significant, and the breakdown accounts for the gain: its
  classes split the failed episodes one class each, so their differences add
  up to the success difference. States that overlap one another or also occur
  in successful episodes (stalled at some point, released the object once)
  cannot add up to a gain; nor can exclusive classes whose differences are
  not significant. Then the paragraph opens on the breakdown's own finding
  against the same comparison ("with the fine-tuned policy, the agent stalls in
  significantly fewer episodes"), with no "comes from". When no
  measurement in the paper explains a main gain, a breakdown of the episodes
  already run (by failure kind, by task kind) can supply one; until then the
  paragraph gives its verdict with no reason, never a mechanism the data do not
  show.
- **A section of one repeated frame reads as generated.** When most sentences
  of a results section share one frame ("With X, ours (significantly)
  outperforms Y on Z, a% against b%"), reviewers take it for text generated
  from a results script and say so, the more readily when the paper carries an
  LLM usage statement. Swapping synonyms does not fix it. Each paragraph is
  rebuilt as question, answer and reason under the two rules above, and every
  scope word survives the rebuild as in the roll-call rule.
- **One row, one training condition, or mark the columns.** When a row's model
  differs by column (trained in that domain for some columns, transferred for
  others), a symbol defined in the caption marks those columns, or the row
  splits in two. Every transfer claim in the Abstract or Introduction ("trained
  in one domain, it outperforms on another") has main-text evidence produced
  exactly that way, never only an appendix table.
- **The main Setup defines what the main text uses, and only that.** A variant
  or data subset the final method does not use is defined with its ablation,
  not in the main Setup, unless a main-text float reports it; every term a
  main-text sentence or float uses is defined in the main text at first use. A
  main-text pointer to such an ablation names the variant by what it changes
  ("pre-selecting objects by success rate"), not by a name defined only in the
  appendix, and a difference that was not significant is not written as "brings
  no gain".
- **Every number argues for a claim; a number that argues for nothing is not
  reported.** For each number in the Experiments prose (a result pair, a
  count, a dataset size, a cost, a latency), name the claim it supports: the
  paragraph's verdict, the reason for a gain, a confound it rules out, or a
  claim the Introduction or a contribution bullet makes. An implied claim is
  stated in a few words in the number's sentence ("Less data also works: on a
  quarter of the collection, ..."; "it wins while training on fewer episodes
  than the demonstrations"; "it is faster because its replies are shorter").
  With no claim the number leaves the main text; the appendix may keep it as
  a record. The usual orphans: a cost or wall-clock line with no comparison
  and no claim about cost; two near-equal counts printed beside a comparison
  they do not change; a secondary measurement placed after a gain without
  saying it is the reason; a comparison in a paragraph about something else.
  Before cutting, check whether a sentence elsewhere (an Introduction claim, a
  contribution bullet) rests on the number; then it stays. Stating the claim
  never widens it: a count that holds for one control set is scoped to that
  set, a not-significant pair keeps its plain verb, and a "because" needs the
  evidence the reason rule above asks for. Setup constants that define what
  is evaluated (task counts, the size of a held-out split a column uses) are
  definitions, not reports, and stay. Table rows the authors placed for
  context, such as reported rows of other systems, are their decision, not
  this rule's.
- **Each instance a claim names is an argument of its own.** "With two models"
  or "on three simulators" needs main-text evidence for each model or
  simulator, under the self-contained rule of `review-float-map.md` (a float
  cell, or the decisive number with its comparison in the prose). Before
  flagging one, read which instance the claim means: the second model of a
  claim may be one a main-text table already carries, not the one an appendix
  table shows.

### Background / Related Work

- Related Work is read by almost nobody; do not spend the page budget defending
  it. Keep it organized by method family, not paper-by-paper.
- **Two paragraphs, one per line of prior work** (user ruling 2026-11-01:
  「一般 related work 两段就行了」). Works enter as cite clusters, at most one
  clause per work; a paragraph may end with the gap that whole line shares.
  How *our* method differs goes in the method's Advantages paragraph (above),
  not here. A third paragraph needs a third line of work the method answers,
  never a family split out for room. Cutting to two paragraphs keeps every
  `\cite` key, concurrent work included; the procedure is cut class 11 of
  `paper-prose-tighten`.
- Anything that a reader needs in order to follow the method belongs **in the
  method**, not in Background. Material buried in Background is material nobody
  reads.

### Summaries cascade upward

Write the summary three times, at increasing compression:
section opening → Introduction → Abstract. Each level is a strict summary of the
one below, so any claim change propagates in one direction only. The Conclusion
stays simple: no detail, no new qualifiers — plain enough for a non-specialist.
It is short, a few sentences that restate the claim; it does not re-list the
benchmarks, settings or numbers the body already reports (user ruling
2026-11-16: 「conclusion 就不应该这么一堆 benchmark 枚举, 应该简短一点」).
It names no benchmark, simulator, physics engine or set of tasks a result
was measured on, not even as a group ("the benchmarks in simulator A",
"every benchmark built on engine B", "on newly generated tasks"): the
Conclusion generalizes, saying what the method beats, and the body says where
(user ruling 2026-11-16: 「conclusion 不应该有具体的 benchmark 名字」, then
「不对, … 这些细节也不应该有」 and 「conclusion 就是要概括」). Nor does it list
the baselines it beats: it names them as one class ("the alternatives to the
core component"), true of every member (user ruling 2026-11-16: 「不要枚举,
记住, 论文枚举越少越好」).
It runs **at most 110 words**; CVPR/ICCV award papers' conclusions without
a limitations part have a median of 94 (user ruling 2026-11-16).
The cap is a ceiling, not a target: the Conclusion restates every advantage
the Abstract claims, the success comparison and each thing the method does
not need, and a trim never drops one to get shorter (user ruling 2026-11-16:
「只说了一个优点? 还有两个没说? 结论也不要限制太短」).

### Terminology

One concept, one name, everywhere — including figure labels and table headers.
When using an LLM for polish, instruct it explicitly to preserve terminology;
left alone it will paraphrase the same term three different ways.

## 3. Appendix and supplementary

- Everything in the appendix must be **pointed at from the main text** at the
  place it belongs ("further details in Appendix B"). An unreferenced appendix
  is an unread appendix.
- If the appendix is submitted as a separate file, only *some* reviewers will
  open it — put nothing load-bearing there.
- Practical workflow: write the paper complete with the appendix, then produce
  the submission PDF by cropping the appendix pages off, so main-text
  cross-references stay correct.
- Extra tables always have a home in the appendix — no completed experiment is
  wasted (see `experiment-craft.md`).
- Reproducibility material is weighed by reviewers: state compute, seeds,
  hyperparameters, and data access somewhere concrete.
- Released code: the README should be as complete as possible. Whether core
  implementation ships at submission time is the authors' call and the venue's
  policy — do not silently ship something the authors did not agree to release.

## 4. Floats: placement and typesetting

- **The main (hero) figure lands on page 2** (user ruling 2026-10-31). A
  `figure*` lands on the next page at the earliest, so its source goes in the
  Introduction text of the page before the one it should land on. Read the page
  from the compiled float→page map (`paper-float-compact` Step 1), not the
  `.tex`.
- **Cite a table or figure where the reader needs it to understand or check
  that sentence** (user ruling 2026-11-04). When the conclusion itself belongs
  to the later analysis, move the sentence and its citation together into the
  Experiments.
- In the Introduction, cite Figure 1 where it helps the reader grasp the
  problem or the method. Summarize the core results in words, usually without
  pointing at several experiment tables; a result figure that is itself the
  paper's main selling point may be cited early too.
- In the Method, cite an architecture, training-pipeline or algorithm figure
  where the step it shows is first explained. The main results and ablation
  tables wait for the Experiments: "we mix the two sources 1:1" describes the
  method and needs no table pointer; "1:1 beats other ratios" is an
  experimental conclusion and moves, with its citation, to the Experiments.
- Place each figure/table on the page where it is **first discussed**, or the
  following page. Never group floats at the end.
- Numbering must follow discussion order; if a table appears out of order, move
  the float in the source rather than renumbering references.
- Nudge a float toward its text by moving the `\begin{table}` block in the
  source — that, not `[h!]` alone, is what actually reflows things.
- Tighten caption spacing when a float floats too far from its text:
  `\setlength{\abovecaptionskip}{2pt}`.
- Long column headers: break into two lines, with the unit or arrow (`ms`, `GB`,
  `↑`) on the second line, centered.
- If a column takes only two values (e.g. two hardware platforms), delete the
  column and use **block subheadings** inside the table instead.
- Table font must be set deliberately (usually `\small` / `\footnotesize`) —
  a table in body size rarely fits a two-column layout.

## 5. LaTeX mechanics

```latex
% Non-breaking space before every reference — keeps "Table 1" from splitting
Table~\ref{tab:main},  Figure~\ref{fig:arch},  Section~\ref{sec:method}
as shown in~\cite{key}              % numeric, parenthetical
\citet{key} showed that ...          % author-prominent: "Smith et al. showed"

% Compressed numeric citations with author names available (natbib)
\PassOptionsToPackage{numbers, compress}{natbib}
{
  \small                       % otherwise the bibliography eats the page budget
  \bibliographystyle{plainnat} % default styles print every author name
  \bibliography{ref}
}

% Multi-author drafting: one color macro per co-author
\newcommand{\wang}[1]{\textcolor{blue}{#1}}
\wang{this sentence is mine}    % strip all of these before submission

2.3$\times$ faster              % NOT "2.3x faster"
$\mathcal{X}$, $\mathcal{D}$    % \mathcal takes UPPERCASE only
```

Additional rules:

- `\bm` or `\mathbf` for vectors/matrices — pick one and never mix.
- **No raster images in the source.** If a PNG is unavoidable, convert/compose it
  into a PDF first, so the included asset is a single vector container.
- Figures need ≥ 300 dpi if a raster path is truly unavoidable; 72 dpi is
  rejected by several venues.
- **Read the log file.** Nothing may intrude into the margin or gutter — every
  `Overfull \hbox` that pushes into the margin is a format violation, not a
  cosmetic warning. Long equations and wide tables are the usual culprits.
- Never leave private notes, TODOs, or commented-out snark in the `.tex`.
  arXiv publishes the source; anyone can read what you commented out.
- Do not submit unused figure files — some venues require a single `.tex` and
  reject stray assets.
- Fix `\vspace` / spacing hacks **on the last day**. Content is still moving
  before that, so early height tuning is wasted work and hides real overflow.

## 6. Final pass checklist

- [ ] Abstract: one or two headline numbers, each comparison one range over
      its benchmarks; each component by its objective, no implementation
      detail (training signal, labels, teacher); results in at most two
      differently framed sentences, ending on the take-home message. Each
      headline number says its comparison (their order is the authors' call);
      a number beside a property comes from that setting; background at most
      two sentences; it ends on its first page.
- [ ] Introduction: no method component before the method paragraph, every
      counted set named; one sentence of reason between gap and method; no
      ratio, data source or baseline name in the method paragraph; results by
      kind of generalization, no benchmark roll call, no "slightly";
      contribution items about 60 words each. One spine, a second motivation
      entering as a component's property; a failure breakdown stated as
      motivation, not blame; every "all / only / without" holds for each stage;
      contribution items independent, an empirical one claiming only what its
      controls isolate. The method item names the whole method, its stages in
      order and the capabilities the prose argues for; every title is a short
      noun phrase, never a finding; no name in the list that the prose has not
      introduced. No evaluation protocol (episodes per task, seeds, caps) in
      the Introduction.
- [ ] Method has a road-map paragraph and (near-)zero citations; comparisons live
      in a dedicated Advantages paragraph.
- [ ] Method names the configuration the main rows run and presents the
      alternative as a named variant; every filter in an equation has its
      reason; one model or one per domain is stated before the first results table.
- [ ] Exactly one Experiments section; speedups reported as ratios.
- [ ] Results paragraphs: finding first, one or two numbers, a reason from the
      paper's own evidence; one verdict per group of benchmarks, one answer per
      ablation question, at most four number pairs per paragraph, no roll call of
      benchmarks or variants; a measurement that explains a gain sits beside it
      as its reason; no section of one repeated sentence frame; every number
      pair in the predicate or in parentheses, never trailing after a comma. A
      row whose training differs by column is marked; every transfer claim, and
      every instance a claim names, has main-text evidence; the main Setup
      defines only what the main text uses.
- [ ] Every appendix section is referenced from the main text.
- [ ] Every float sits on/next to the page of first discussion, in order: first references
      come in numbering order, Figure 4 never cited before Figure 3 (`paper-compile`'s `check_tex.py`).
- [ ] Main (hero) figure on page 2; every citation before the Experiments is
      one the reader needs there.
- [ ] No `\cite`/`\ref` without a preceding `~`.
- [ ] `$\times$` everywhere a multiplier appears; `\mathcal` only on uppercase.
- [ ] All co-author color macros and draft comments removed.
- [ ] Log file clean: no overfull boxes intruding into the margin.
- [ ] No PNG/JPEG included directly; all figures vector.
- [ ] Terminology consistent across text, figures, and tables.
- [ ] Page budget satisfied under the venue's counting rule
      (`venue-checklists.md` — IEEE counts references, ML venues usually do not).

## Related

- `writing-principles.md` — narrative, abstract, sentence-level clarity.
- `figure-craft.md` — how the figures themselves are built.
- `venue-checklists.md` — per-venue formatting and page-count rules.
- `citation-discipline.md` — verifying that the citations are real.
