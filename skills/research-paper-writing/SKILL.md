---
name: research-paper-writing
description: Structure an ML/CV paper's Introduction, write its Experiments section, and plan and polish its figures, following Peng Sida's writing notes (technical challenge = limitation + reason, claim-evidence alignment). Use when planning the introduction's paragraph structure, drafting or revising Experiments, or improving figures. Never for the title, Abstract or contribution list (the authors write those), nor Method, Related Work or Conclusion.
---
# Research Paper Writing

## Scope in this fork (user ruling 2026-11-01)

Use this skill **only** for three things:

1. **Introduction structure**: the paragraph plan, the order of motivation, gap / technical challenge, insight and
   results, and how each paragraph opens. Not the contribution list.
2. **The Experiments section**: setup, results per benchmark, ablations, analysis.
3. **Figures**: the figure plan, Figure 1 / teaser / showcase choice, overview and result figures, captions.

Never draft or rewrite the **title, Abstract or contribution list**: the authors write those themselves, and an
agent only transcribes them verbatim. Steps or references below that target the title, Abstract, contributions,
Method, Related Work or Conclusion do not apply. Where this skill conflicts with the project's own paper rules
(its paper `CLAUDE.md`, memory, or the `paper-*` skills), the project wins.

## Overview

Use this skill to rewrite a research paper into a reviewer-friendly, high-clarity draft.
Prioritize first-impression quality (figures/tables/layout), logical flow, and evidence-backed claims.

## Core Workflow

1. Clarify the paper story before sentence-level edits.
2. Use section-specific guidance in `references/`.
3. Rewrite paragraph-by-paragraph with one message per paragraph.
4. Run reverse outlining after writing each section.
5. Check every major claim in Abstract/Introduction against experimental evidence.
6. Run final-paper adversarial review with `references/paper-review.md`.

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

## Section Guides

Load only the needed section file:

- Introduction: `references/introduction.md`
- Abstract: `references/abstract.md`
- Related Work: `references/related-work.md`
- Method: `references/method.md`
- Experiments: `references/experiments.md`
- Figures: `references/figures.md`
- Conclusion: `references/conclusion.md`
- Paper review (Paper Review): `references/paper-review.md`
- Paragraph clarity source: `references/does-my-writing-flow-source.md`
- Example bank index: `references/examples/index.md`

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

## Execution Rules

1. Build a mini-outline before drafting prose.
2. For each subsection, explicitly include motivation, design, and technical advantage when applicable.
3. Avoid writing style that looks like incremental patching of a naive baseline.
4. Keep terminology stable across the full paper.
5. If a claim cannot be supported by results, weaken or remove the claim.
6. Before finalizing, append and answer a five-dimension self-review question list, then revise the paper based on unresolved items.
7. Do not load all section references (Introduction/Abstract/Related Work/Method/Experiments/Conclusion) at once; load only the specific section guide needed for the current edit target.

## Output Contract

When asked to rewrite or draft sections, return:

1. A compact section outline (3-7 bullets). For the Introduction, the outline is the answers to the four backward questions, the four-step forward story and the paragraph-level plan (`references/introduction.md`). Take the contributions for backward question (2) from the authors' contribution list; never draft them.
2. Revised paragraphs with explicit paragraph roles (opening/challenge/method/advantage/evidence/limitation).
3. A short self-review checklist covering clarity, flow, terminology consistency, unsupported claims, and missing evidence.
4. A claim-evidence map for each major claim in the revised text using `Claim: ... | Evidence: ... | Status: supported/needs evidence`.
