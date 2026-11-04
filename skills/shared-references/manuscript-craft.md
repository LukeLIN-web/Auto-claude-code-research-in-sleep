# Manuscript Craft: Section Policy, Floats, and LaTeX Mechanics

`writing-principles.md` governs *narrative and prose*. This file governs the
**mechanical layer**: what goes in which section, how floats are placed, and the
LaTeX details that reviewers notice within seconds.

Source: practitioner notes in
[LukeLIN-web/blogs — How-to-write-paper](https://github.com/LukeLIN-web/blogs/blob/master/How-to-write-paper.md),
distilled into rules. Venue instructions always override this file.

## When to Read

- `paper-write`: before drafting Method / Experiments, and during the final pass.
- `paper-compile`: when fixing overfull boxes, float placement, or citation style.
- `resubmit-pipeline` / `paper-writing`: during submission-readiness checks.

## 1. Order of work

1. Figures and tables first (`figure-craft.md`).
2. Then the claims those artifacts support.
3. Prose last — **write no results text before the figures and tables are final.**

Results prose is the least-read part of the paper; it exists to point at the
table, not to re-narrate it. Time saved here goes into figures.

## 2. Section policy

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
  one empirical. Write those first; the supporting results follow.
- If two techniques are introduced, write the **connection** between them.
  Presenting them side by side signals "two unrelated tricks bolted together";
  presenting the mechanism that links them signals one method.

### Experiments

- **One section for all experiments.** Multiple experiment sections read as an
  unfocused paper (and several venues state this explicitly).
- Report **speedup / reduction ratios**, not just raw latency and throughput.
  A reviewer wants `2.3$\times$ faster`, not two tables to divide mentally.
- Analysis prose is the lowest-value text in the paper — tables and figures carry
  the argument.

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

- [ ] Method has a road-map paragraph and (near-)zero citations; comparisons live
      in a dedicated Advantages paragraph.
- [ ] Exactly one Experiments section; speedups reported as ratios.
- [ ] Every appendix section is referenced from the main text.
- [ ] Every float sits on/next to the page of first discussion, in order.
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
