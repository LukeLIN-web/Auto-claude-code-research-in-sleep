# Venue Checklists for ICLR, NeurIPS, ICML, IEEE, AAAI, ACM, TMLR, and Nature MI

Use this reference near the end of `paper-plan` and during the final checks in `paper-write`.

## When to Read

- Read once when setting the target venue.
- Read again before locking the outline.
- Read again during final submission-readiness checks.

## Universal Requirements

Across these venues, the following are usually expected:

- anonymous submission unless preparing a camera-ready version,
- references and appendices outside the main page budget,
- enough experimental detail for reproduction,
- honest limitations and scope boundaries,
- clear mapping from claims to evidence.

## NeurIPS

Planning implications:

- The paper checklist is mandatory.
- Claims in the Abstract and Introduction must align with the actual evidence.
- The paper should discuss limitations honestly.
- Reproducibility details, hyperparameters, data access, and compute usage should be documented.
- Statistical reporting should specify error bars, number of runs, and how uncertainty is computed.

Final-check implications:

- Confirm the paper checklist is complete.
- Ensure limitations, reproducibility details, and compute reporting exist somewhere appropriate.
- Verify theory papers include assumptions and full proofs in the main paper or appendix.

## ICML

Planning implications:

- The paper must budget space for an ICML-style Broader Impact statement.
- Reproducibility expectations are strong: data splits, hyperparameters, search ranges, and compute should be documented.
- Statistical reporting should state whether uncertainty uses standard deviation, standard error, or confidence intervals.

Final-check implications:

- Ensure the Broader Impact statement is present in the expected location.
- Confirm anonymization is strict: no author names, acknowledgments, grant IDs, or self-identifying repository links.
- Verify experimental details are detailed enough for replication.

## ICLR

Planning implications:

- Reproducibility and ethics statements are often recommended even if not always mandatory.
- If LLMs materially contributed to ideation or writing to the point of authorship-like contribution, plan a disclosure section or appendix note.
- Keep the story front-loaded because ICLR reviewers often judge quickly from the early pages.

Final-check implications:

- Decide whether LLM disclosure is required for this project.
- Confirm the paper includes enough reproducibility guidance, code/data availability information, and limitations discussion.
- Check that the contribution is already clear by the end of the Introduction.

## IEEE Journal (Transactions / Letters)

Planning implications:

- IEEE journals are typically **not anonymous** — include full author names, affiliations, and IEEE membership status from submission.
- Use `\documentclass[journal]{IEEEtran}` with `\cite{}` (numeric citations via `cite` package). Do NOT use `natbib`.
- References **count toward the page limit**. IEEE Transactions typically allow 12-14 pages total; IEEE Letters (e.g., WCL, CL, SPL) typically allow 4-5 pages total. Check the specific journal's author guidelines.
- Include an `\begin{IEEEkeywords}` block immediately after the abstract.
- The bibliography style must be `IEEEtran.bst` (produces numeric `[1]` style citations).
- IEEE journals may require a biosketch (`\begin{IEEEbiography}`) for each author in the camera-ready version.
- Some IEEE journals require a cover letter addressing how the paper differs from conference versions (if applicable).

Final-check implications:

- Confirm author names and IEEE membership grades are correct (Member, Senior Member, Fellow).
- Verify the total page count including references is within the journal's limit.
- Check that all figures meet IEEE quality requirements: 300 dpi minimum, proper axis labels, readable when printed in grayscale.
- Ensure the paper uses two-column IEEE format throughout (the `[journal]` option handles this).
- Verify no `\citep` or `\citet` commands are present — IEEE uses `\cite{}` only.
- Check that `\bibliographystyle{IEEEtran}` is used.

## IEEE Conference (ICC, GLOBECOM, INFOCOM, ICASSP, etc.)

Planning implications:

- Most IEEE conferences are **not anonymous** (except some like IEEE S&P). Include full author information.
- Use `\documentclass[conference]{IEEEtran}` with `\cite{}` (numeric citations).
- References **count toward the page limit**. Typical limit: 5-6 pages (e.g., ICC, GLOBECOM), some allow up to 8 pages (e.g., INFOCOM). Extra pages may incur additional charges.
- Include `\begin{IEEEkeywords}` after the abstract.
- Conference papers do NOT include author biographies.
- Some IEEE conferences accept 2-page extended abstracts — confirm the paper category before planning.

Final-check implications:

- Verify total page count including references fits within the conference limit.
- Check that figures are readable at the two-column conference format size.
- Ensure `\bibliographystyle{IEEEtran}` is used.
- Verify no `\citep` or `\citet` commands are present.
- Confirm the correct `\documentclass` option (`[conference]`, not `[journal]`).
- Some conferences require IEEE copyright notice — check submission portal for specific requirements.

## AAAI

Planning implications:

- Submission is a **single `.tex` file**. Do not ship unused figure assets.
- **No references in the abstract.**
- The reference list is not required to start on its own page — it follows the
  main body directly.
- Figures must be at least 300 dpi; 72 dpi is rejected.
- `listings` is for real code excerpts; `algorithm` is for pseudocode. Do not
  typeset pseudocode as a code listing.
- The AAAI style disables `\section` numbering by default, so plan
  cross-references accordingly (name sections, or re-enable numbering per the
  venue's own guidance).

Final-check implications:

- Nothing intrudes into the margin — no oversized figure, no long unbroken
  equation. Read the compile log for overfull boxes (`manuscript-craft.md` §5).
- Confirm the abstract is citation-free and the single-file requirement is met.

## ACM `acmart` venues (ACM MM, SIGIR, KDD, CHI, DAC 2026+, ...)

Planning implications:

- The class is `acmart.cls`; the conference layout is the `sigconf` format.
  The template ships several sample variants — **`authordraft` is the submission
  format**, the plain `sigconf` sample is what a camera-ready is reformatted to.
  Other variants differ only in bibliography engine (`biblatex`), i18n, or TeX
  engine (`lualatex`/`xelatex`); pick `authordraft` unless a specific need
  applies.
- Page budget is typically "N pages plus 1 page for references only" — check the
  CFP for whether references are excluded. Some ACM-hosted venues (e.g. DAC)
  **do not accept an appendix at all**; everything must fit the main body.
- The abstract must use the template's default formatting. No bold, no color, no
  restyling — modifying it is a format violation.
- Keep the CCS concepts block. The permission/copyright block is nominally
  removable but is best left in — it must return for the camera-ready anyway.

Final-check implications:

- Verify the correct sample variant is in use and no camera-ready-only options
  are enabled.
- Confirm author list is final: many ACM-hosted venues freeze author addition and
  reordering at the submission deadline.

## TMLR / JMLR

Planning implications:

- TMLR uses **double-blind** review and publishes reviews openly; JMLR is a
  separate track with its own scope (ML theory and methodology, not applications
  of ML to other fields).
- TMLR has **no page limit** — length must be justified by content. Papers past
  ~12 pages take longer to review. This makes TMLR a good fit for
  experiment-dense work that a conference page budget would mutilate.
- TMLR's acceptance criteria are claim-centric rather than novelty-centric:
  rejection targets bold claims without rigorous evidence, unclear writing, false
  novelty claims relative to published work, and reimplementations of already
  replicated ideas. Plan the claims-to-evidence matrix accordingly.
- JMLR-length papers (50-90 pages, derivation-heavy) are normal; do not compress
  proofs to conference density.

Final-check implications:

- Confirm every claim in the abstract has a rigorously supported counterpart in
  the body — this is TMLR's primary rejection axis.
- Confirm anonymity for TMLR.

## Nature Machine Intelligence (and Springer Nature journals)

Planning implications:

- Scope skews to genuinely new capability rather than incremental improvement.
- Classes: `sn-jnl.cls` with `sn-nature.bst`. The submission template is
  single-column; that is expected, not a mistake.
- **Article format**: main text up to ~3,500 words excluding abstract, Methods,
  references and figure legends; abstract up to ~150 words and unreferenced;
  **at most ~6 display items** (figures + tables combined); ~50 references as a
  guideline.
- Structure is fixed: Introduction (**no heading**) → Results → Discussion →
  Methods, with topical subheadings in Results and Methods but none in
  Discussion. Results is the experiments section; Methods carries settings;
  Discussion carries advantages and future work.
- The display-item cap forces composite figures — plan each figure as a panel
  grid from the start (`figure-craft.md`).
- Double-blind is opt-in; the default is not anonymous.
- The first submission does not require the final template — section order
  matching the published structure is what matters. Expect roughly two weeks to
  an editorial decision, ~6 weeks to first review if sent out, and a multi-month
  total cycle.

Final-check implications:

- Count display items against the cap before adding any figure.
- Confirm the Introduction carries no heading and Discussion carries no
  subheadings.

## Deadlines and acceptance rates

Do not hard-code deadlines or acceptance rates into skills or plans — they move
every cycle. Resolve them at planning time from the venue's own CFP, plus:

- <https://aideadlines.org/> — deadline tracker across ML/CV/NLP/RO/SP/DM.
- <https://github.com/lixin4ever/Conference-Acceptance-Rate> — historical rates.

When a plan depends on a deadline, record the date **and the URL it came from**,
so a stale number is traceable rather than silently trusted.

## Minimal Submission Checklist

Before submission, verify:

- the venue-specific required sections are present,
- the page budget is satisfied for the main body,
- the contribution bullets do not overclaim,
- citations, figures, tables, and references are internally consistent,
- the PDF is anonymized and ready for reviewer consumption.
