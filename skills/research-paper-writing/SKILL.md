---
name: research-paper-writing
description: Structure an ML/CV paper's Introduction, write its Experiments section, and plan, draw and polish its figures (Figure 1 / teaser / showcase, overview, result figures), from Peng Sida's writing notes (technical challenge = limitation + reason, claim-evidence alignment) and from the patterns of 60 CVPR/ICCV/NeurIPS award papers (exemplar bank, style and figure checkers). Use when planning the introduction's paragraph structure, drafting or revising Experiments, choosing or redesigning a figure, or distinguishing the paper from its closest prior work. Never for the title, Abstract or contribution list (the authors write those), nor Method, Related Work, Conclusion, rebuttals or proofreading.
---
# Research Paper Writing

## Scope in this fork (user ruling 2026-11-01)

Use this skill **only** for four things:

1. **Introduction structure**: the paragraph plan, the order of motivation, gap / technical challenge, insight and
   results, and how each paragraph opens. Not the contribution list.
2. **The Experiments section**: setup, results per benchmark, ablations, analysis.
3. **Figures**: the figure plan, Figure 1 / teaser / showcase choice, overview and result figures, captions.
4. **Distinguishing the paper from its closest prior work** (user ruling 2026-11-15): the two or three sentences,
   in the Introduction's gap paragraph or in Related Work, that introduce a close paper and say what it leaves
   undone; and what to check in that paper beyond its mechanism (released code and weights, proprietary
   models, evaluation on its own training tasks). `references/distinguish-prior-work.md`. The rest of Related
   Work stays out of scope.

Never draft or rewrite the **title, Abstract or contribution list**: the authors write those themselves, and an
agent only transcribes them verbatim. Steps or references below that target the title, Abstract, contributions,
Method, Related Work or Conclusion do not apply. Where this skill conflicts with the project's own paper rules
(its paper `CLAUDE.md`, memory, or the `paper-*` skills), the project wins.

## Two sources, one skill

This skill fuses two upstream skills (`SOURCE.md`, `NOTICE.md`): Peng Sida's writing notes (how to plan a section:
backward then forward, technical challenge = limitation + technical reason, one message per paragraph, the
claim-evidence map) and an annotation of 55 CVPR/ICCV/NeurIPS award papers, 5 more held out (what such papers
contain and in which order, routes by paper type, an exemplar bank, checkers for style and figures). Each section
guide in `references/` holds both under one outline.

## What Persuades

Rewrite toward a reviewer-friendly, high-clarity draft. Prioritize first-impression quality (figures, tables,
layout), logical flow and evidence-backed claims.

The award-paper half is grounded in a sentence-by-sentence annotation of **55 award papers** (2021–2025; 60 papers are analysed in total, and 5 of them (from 2024) are held out for testing, see `PAPER_LIST.md` in the repository root): what functions their abstracts and introductions contain, in which order, and how they read (`references/corpus-profile.md`). Award papers persuade through:

1. **A sharp motivation** — credit to specific prior work, then a concrete gap (what fails or is missing, when, and why), set up as a tension the paper resolves.
2. **An idea about the problem** — an observation from which the method follows, stated directly; a short handle for the idea when there is one (“next-brick prediction”).
3. **Clear positioning** — the closest work is named and one checkable difference is stated.
4. **Confident, evidenced claims told as a story** — results as claims with one or two headline numbers; the work is promoted where the evidence allows; a stance when the results support one. Weaknesses belong in the Limitations section, not in the Abstract or Introduction (author preference).
5. **Plain, rhythmic prose**. Each claim is stated once. Short, quotable sentences at the pivots (the bottleneck, the cause, the idea); the rest are full sentences (mean 20–24 words) that carry their reasons through *because*, *while*, *by*, *which*, not through trailing “, making …” clauses. Few logical connectors; colons allowed, **no dashes** (author preference). Mechanisms and examples instead of adjectives, short background, no implementation details.

## Writing Order
The order in Peng Sida's notes, for context on what exists when each part is written:

1. Sketch a clear pipeline figure.
2. Settle the paper story, write the Introduction plan, and list the comparison experiments and ablation studies.
3. Plan and write Method while running experiments.
4. Revise Introduction and Method while running experiments.
5. Once experiments are mostly done, plan and write Experiments.
6. Polish the pipeline figure and draw the teaser.
7. Plan and write Related Work.
8. Review the paper; revise Introduction, Method and Experiments.
9. Plan and write the Abstract.
10. Choose the title.
11. Review and revise repeatedly.

## Workflow

Do not write prose before Step 4. Under the scope of this fork the steps serve the Introduction's structure,
Experiments and figures; what they say about the title, Abstract and contribution list does not apply.

### Step 0 — Intake (two input modes)
**Mode A: intake form.** If the user provides an intake JSON (exported from `assets/intake_form.html`, schema `bestpaper-intake/v1`), run `python3 scripts/intake_to_brief.py <file.json> --out brief.md --bib refs.bib` (paths relative to this skill folder) and work from `brief.md`; exit code 2 means a required field is missing. If the user describes the work in free text, load `references/intake-form.md` and map the description onto it. When a user has no material ready, point them to `assets/intake_form.html` (a local, offline form that exports JSON; the form is in Chinese).

**Mode B: complete abstract in.** If the user pastes an existing abstract (optionally with the introduction), do not rewrite it blindly. First reverse-engineer it into the intake fields of `references/intake-form.md` (task, dominant prior approach, gap and its reason, closest work, key insight, method components, results with numbers) and show the user a short table: field, what the draft says, status (present / vague / missing). Facts, numbers and terminology in the draft are the user's and are kept verbatim; never add a result, baseline or reference the draft does not contain. Then handle missing fields as below, and continue with Steps 1–8. In `report.md` add a **change table** (original sentence → revised sentence → reason, citing the award-paper pattern it follows) so the author can accept or reject each change.

In both modes:
- If a **required** field is missing (key idea, concrete gap with its reason, closest work, results with numbers), ask once in a compact list **before drafting**. In the same message, ask for the memorability fields that are empty (efficiency, integration with existing pipelines, supported inputs, applications, a concrete example, what is surprising, the trend it follows, the team’s name for the idea): these, not the prose, are what made award abstracts stand out in our comparisons. If the user cannot answer now, continue with `[TODO: …]` placeholders. Ask in plain text; do not depend on any agent-specific question tool.
- Never invent results, numbers, baselines, datasets or references.

### Step 1 — Claim, tension, handle, stance, headline numbers
Clarify the paper story before any sentence-level edit: answer the four backward questions of `references/introduction.md` ("Backward First, Then Forward").
Write these for yourself (they go into `report.md`, not the paper):
- **Claim**: `We show that [method/finding] [achieves what] [under which setting], because [key reason].`
- **Tension type**: tradeoff / capability-missing / obvious-fix-too-costly / unexplained-phenomenon / open-question / belief-overturned (`routing.md`).
- **Insight**: the observation about the problem the method follows from, written as a plain statement.
- **Handle** (optional): a short phrase naming the idea, distinct from the method’s name. Use the user’s term if they have one; otherwise propose one in the report. When there is a handle, put it in the title.
- **Closest work**: 1–2 works and the checkable difference (mechanism, scope, cost, assumption, input, output, evaluation).
- **Stance** (optional): what the work changes for the field, only if the results support more than “better on benchmark B”.
- **Headline numbers**: the 1–2 results that carry the claim.

### Step 2 — Route
Load `references/routing.md`. Choose the paper type and motivation type; note the abstract arc and introduction plan.

### Step 3 — Claim map
Load `references/claim-calibration.md`. List each claim with its evidence and the **strongest wording the evidence supports**. Use it to make claims confident where supported and scoped where not — never to add disclaimers. Mark headline / supporting / table-only numbers.

### Step 4 — Skeleton
Build the plan coarse to fine: a paragraph-level plan, then a sentence-level plan under each paragraph (`references/introduction.md`, "From story to sentence plan"). For each Method or Experiments subsection the plan names motivation, design and technical advantage where they apply.
Load `references/introduction.md` and `references/abstract.md`. One line per paragraph (its message = its first sentence); one line per abstract sentence. Check against the award-paper tiers (`introduction.md`, "What Award Introductions Contain"):
- **always**: credit to specific prior work → gap with reason → method → results;
- **usual**: opening setting or concrete scene; the insight just before the method;
- **for method papers**: a contrast with the closest work after the method;
- **always last**: the contribution list, written by the authors (`introduction.md`, "Contribution List"); a stance before it is optional.
The abstract defaults to Setting → Gap → Method → Result (`abstract.md`, "Versions").
Mark the **pivot sentences** (the bottleneck, the cause, the tension, the idea); they will be short and quotable. Then make a **claim index**: list every claim (gap, insight, each advantage, each result, stance) and the one paragraph where it appears. A claim listed under two paragraphs is merged into one. Generic field background gets at most two sentences.

### Step 5 — Draft with exemplars
Rewrite paragraph by paragraph, one message per paragraph, stated in its first sentence. Load only the section guide of the section being written, not all of them.
For each paragraph, read 2–3 award-paper paragraphs with the same function and, if possible, the same paper type: `python3 scripts/find_exemplars.py --para <function> --type <L*>`; for sentences, `python3 scripts/find_exemplars.py <move>` or `--phrases <function>`; for whole introductions, the route’s card in `references/exemplars/cards/`. Learn their order of information and rhythm; never copy a sentence or a run of ≥ 6 words. Write in the authors’ voice (“we”, “our model”); never describe the user’s input as “supplied”, “provided” or “reported”.

### Step 5b — Method and Experiments (when requested)
1. Extend the claim map into an **evidence map**: claim → method subsection → experiment (table/figure) → ablation, each evidence entry marked main text or appendix. Claims without evidence are softened in the introduction or get an experiment `[TODO]`; a claim whose evidence is all in the appendix gets its decisive table, figure or number moved into the main text (Hard rules).
2. Method: follow `references/method.md` (opener, preliminaries, one subsection per component with need → mechanism → property, objective, optional discussion). Mechanisms, equations and losses the user has not given are `[TODO]`; never invent them.
3. Experiments: follow `references/experiments.md` (opener, setup, claim-first results per benchmark, ablations that mirror the claims, analysis, limitations). Tables use booktabs with `\TODO{}` cells for missing numbers.
4. Limitations are usually not written. When a paper needs them, they go in the experiments or a separate section, never in the abstract or introduction.

### Step 5c — Figure plan and figures (whenever Method/Experiments are written, or when asked)
Load `references/figures.md`.
1. Make the **figure plan** from the evidence map: one row per figure with its place, the claim it carries, its type, panels, the material needed, its status and the caption's takeaway sentence (`figures.md`, "The Figure Plan"). Every main claim has a figure or a table in the main text; every figure carries one claim.
2. Choose **Figure 1** by route (`figures.md`, "Choose by route"): `diagnosis`/`contrast-results` for `failure`, `contrast-schematic` for `cost` and `insight`, `showcase` for `capability-gap`/`trend`, `plot` for scaling and re-examination, `concept` for mechanism and theory, `resource` for datasets. In two-column templates it goes on page 1, usually full width.
3. **Draw now** what the user has stated: schematics of the mechanism (Figure 1 contrast panels, method overview, query or data-flow illustrations) in TikZ with `assets/figures/figures_preamble.tex`; parts whose mechanism is `[TODO]` are drawn dashed. **Leave as placeholders** everything that shows results (renders, qualitative grids, plots, numbers): a blank framed area of the planned size whose caption carries the full plan as `\FigPlan{…}`. Plots the user has data for use `assets/figures/plot_style.py`.
4. Captions open with the takeaway (`figures.md`, "Captions"); method colours, names and symbols are the same in every figure and match the text.

### Step 6 — Output
- **LaTeX template given** (e.g., a CVPR author kit): load `references/latex-output.md` and follow it.
- **No template**: write Markdown (`# Abstract`, `# Introduction`).
- The paper text contains no move labels, workflow comments, or bracketed notes other than `[TODO: …]` / `\todo{…}`.

### Step 7 — Check
1. Run `python3 scripts/check_draft.py <files>` on the introduction and the experiments section (an abstract file is skipped unless `--abstract` is passed; the contribution list is not checked; in experiments it flags sentences with more than two numbers). Fix every `ERROR`. Each `WARN` means the draft is outside the range of 90% of award papers (connectors, numbers, hedges, boosters, sentence length, runs of short sentences, trailing participial clauses) or shows a known AI-draft habit — revise or justify it in the report. `NOTE`s are information (e.g., the draft promotes the work less than award papers do). `python3 scripts/style_metrics.py <files>` shows every metric with its corpus percentile.
2. If the paper has figures, run `python3 scripts/check_figures.py main.tex`: fix every `ERROR`; each `WARN` (caption length, long first sentence, raster plots, absolute widths, too many floats) is fixed or justified; `NOTE`s list the placeholders still to fill.
3. Semantic checks:
   - Specific prior work is credited before the gap; the gap is concrete (what fails, when, why) and the tension is resolved by the idea.
   - The insight is an observation about the problem, stated directly, not a hypothesis and not a description of the architecture.
   - The closest work is named with one checkable difference (method papers).
   - Results are claims at the strongest supported level, with headline numbers; the work is promoted where evidence allows; nothing is claimed that the evidence does not support (no unscoped “first”, “state-of-the-art on all benchmarks”).
   - No limitation, failure case or disclaimer in the Abstract or Introduction; mixed results are scoped to the wins.
   - No defensive qualifiers about the protocol; no implementation details.
   - Abstract, introduction and contributions state the same claims with the same strength.
   - Nothing is said twice inside the introduction (insight, research questions, results, advantages).
   - Read the draft aloud once: if several consecutive sentences each carry one bare fact, merge them so that each sentence carries a relation (cause, contrast, means, consequence).

4. Reverse-outline each section after writing it (Paragraph Clarity Check below).
5. Review the finished draft as a skeptical reviewer with `references/paper-review.md`: append and answer the five-dimension self-review question list, and revise until every high-risk question is resolved.

### Step 8 — Deliver
1. The paper files (LaTeX project or Markdown).
2. `report.md` for the authors: claim, tension type, insight, handle, closest work, route, claim map, `check_draft` summary, `[TODO]` list, questions, **notes for the Limitations section** (weaknesses deliberately left out of the abstract/introduction), and, when figures were planned, the **figure plan** table with the material each placeholder needs and the `check_figures` summary.
3. When asked to rewrite or draft a section, the reply itself carries:
   - A compact section outline (3-7 bullets). For the Introduction, the outline is the answers to the four backward questions, the four-step forward story and the paragraph-level plan (`references/introduction.md`). Take the contributions for backward question (2) from the authors' contribution list; never draft them.
   - Revised paragraphs with explicit paragraph roles (opening/challenge/method/advantage/evidence).
   - A short self-review checklist covering clarity, flow, terminology consistency, unsupported claims, and missing evidence.
   - A claim-evidence map for each major claim in the revised text using `Claim: ... | Main-text evidence: ... | Appendix evidence: ... | Status: supported / appendix only / needs evidence`. A claim marked `appendix only` gets its decisive evidence moved into the main text (Execution Rule 6).

## Global Principles
1. Keep one paragraph for one message only.
2. State the paragraph message in the first sentence.
3. Make nouns self-contained; define new terms before reusing them.
4. Maintain sentence-to-sentence flow (cause, contrast, consequence, or refinement).
5. Iterate with adversarial self-review: read as a skeptical reviewer.
6. Treat visual quality as core content, not decoration.
7. Use a clean teaser and pipeline figure.
8. Use readable, minimal-ink tables.
9. Keep formatting consistent and tidy.

## Paragraph Clarity Check (Important)
Use this quick test whenever the user asks whether a paragraph "flows" or is clear.

1. Read as an external reader:
   - Does this paragraph have one explicit message?
   - Does the first sentence state what this paragraph will do?
   - Are all key nouns/terms readable without hidden context?
   - Does each sentence connect to the previous one with a clear relation (cause, contrast, consequence, refinement, example)? If it does not continue the previous sentence, is there a transition?
   - Does a sentence introduce a new noun abruptly?
2. Run reverse outlining for the current section:
   - Write down thesis/main claim.
   - Write down each paragraph topic sentence.
   - Write down the evidence/explanation points under each paragraph.
   - Check mapping: topic sentence -> thesis, and evidence -> topic sentence.
   - Revise or remove any paragraph that cannot be mapped cleanly.
3. Revise at the plan level (encode -> analyze -> improve -> decode):
   - Encode: turn the raw text into its high-level plan, one line per sentence.
   - Analyze: first list what the text must convey (for a method paragraph, e.g., the module's design and its motivation); then ask whether the plan conveys each item and whether its logic flows.
   - Improve the plan where it fails, then decode: rewrite the text from the improved plan.
4. If flow is still weak, add temporary section headers and explicit transition phrases during revision, then remove unnecessary headers before finalizing.

Source reference for this check:

- `references/does-my-writing-flow-source.md`

## Paper Review Core Points
Use `references/paper-review.md` for the full checklist and workflow.

1. Add an end-of-draft self-review question list in five dimensions:
   - contribution,
   - writing clarity,
   - experimental strength,
   - evaluation completeness,
   - method design soundness.
2. Treat claim-evidence alignment as a hard constraint, especially for Abstract and Introduction.
3. Perform adversarial writing: review as a skeptical reviewer and resolve every high-risk question.
4. Revise until major rejection risks are explicitly addressed.

## Rules
- Keep the main text self-contained (user 2026-11-11): every main-text argument carries at least one or two pieces of its evidence in the main text itself (a main-text figure or table, or its decisive number with the comparison). The appendix only adds to that evidence, and "see Appendix X" alone supports nothing. The rule and how to fix a claim whose evidence sits only in the appendix: `../shared-references/review-float-map.md`.
- If a claim cannot be supported by results, weaken or remove the claim.
- Avoid writing style that looks like incremental patching of a naive baseline.
- Keep terminology stable across the full paper.
- Never fabricate numbers, datasets, baselines, citations or results.
- Never cite a key that is not in the user’s bibliography; mark missing references with `[TODO: cite …]`.
- No limitations, self-undermining sentences or defensive qualifiers in the Abstract or Introduction.
- The Abstract and Introduction tell the story; tables tell the numbers.
- No generic openings (“has attracted increasing attention”, bare “plays an important role”).
- **No dashes** in the title, abstract or introduction (author preference): no em dash (—, `---`) and no spaced en dash. Rewrite with a colon, a comma, a short second sentence or parentheses. Numeric ranges (2–3) and hyphenated compounds (image–motion, train–test) are fine. `check_draft.py` reports each dash as an ERROR. Colons are allowed.
- **Name mechanisms, not abstractions.** When the input does not say how a component works (who inspects, what is compared, how something moves), write `[TODO: …]` and ask; do not fill the gap with abstract nouns (“state”, “record”, “inspection”, “protocol”) that sound complete but say nothing.
- **Describe components by their relation**, not as parallel items: what problem each one answers and what the next one fixes (“A keeps …; because A alone lets errors persist across edits, B …”), rather than “A does … . B does … . C does … .”
- **Figure and table numbers from notes or intake forms** refer to the author’s full draft. Do not cite them in the abstract or introduction unless the figure is part of the paper being written; list the example and its figure in `report.md`.
- **One aphorism.** Use at most one or two contrastive maxims (“X is not Y”) for the thesis; state the rest as plain fact.
- **Keep what makes the draft memorable.** When revising for a checker WARN, do not merge away the short pivot sentences, the cause sentence, or the handle in the title; fix the WARN elsewhere or justify it. A memorable draft that is slightly off the corpus statistics beats a statistically average one.
- **Never fabricate figure content.** No invented result images, renders, curves or numbers in figures; schematics show only mechanisms the user has stated. Results figures stay placeholders with their plan in the caption until the authors supply the material.
- Do not end sentences with a participial clause that restates significance (“…, making X possible”, “…, extending Y”, “…, bringing Z”). Award papers do this in ~8% of sentences; AI drafts in 30% or more.

## Files

Load only the needed section file:

- Introduction: `references/introduction.md`
- Abstract: `references/abstract.md`
- Related Work: `references/related-work.md`
- Distinguishing from the closest prior work: `references/distinguish-prior-work.md`
- Method: `references/method.md`
- Experiments: `references/experiments.md`
- Figures: `references/figures.md`
- Conclusion: `references/conclusion.md`
- Paper review (Paper Review): `references/paper-review.md`
- Paragraph clarity source: `references/does-my-writing-flow-source.md`
- Example bank index: `references/examples/index.md`

Other files, by the step that loads them:

| File | Load at |
|---|---|
| `references/intake-form.md`, `assets/intake_form.html`, `scripts/intake_to_brief.py` | Step 0 |
| `references/routing.md` | Step 2 |
| `references/claim-calibration.md` | Steps 3, 7 |
| `references/corpus-profile.md` | when you need the award-paper statistics |
| `references/exemplars/` (`paragraphs.jsonl`, `phrasebank.csv`, `moves.jsonl`, `cards/`), `scripts/find_exemplars.py` | Step 5 |
| `references/style-rules.md` | Steps 5, 7 |
| `assets/figures/` (`figures_preamble.tex`, `teaser_strip.tex`, `overview_tikz.tex`, `qualitative_grid.tex`, `bestpaper.mplstyle`, `plot_style.py`) | Step 5c |
| `references/latex-output.md` | Step 6 (LaTeX) |
| `scripts/check_draft.py`, `scripts/style_metrics.py`, `references/corpus/corpus_stats.json`, `scripts/check_figures.py` | Step 7 |

Use `python3`. Attribution and licences: `NOTICE.md`.
