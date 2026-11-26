---
name: close-reading
description: Close-read one paper from its LaTeX source to answer a specific question about it (how labels are built, thresholds, inference cadence, what an ablation compares, what is and is not reported). Use when the user says 精读、细读、仔细读一下某篇、"read X closely", "what exactly does paper X do for Y". Fetches the latest arXiv version with arxiv-to-prompt, reads all of it including the appendix, and updates the project's existing note on the paper. Not for a first-pass summary of a new paper (reading-paper) or a literature search (novelty-check).
---

# Close reading

Close reading answers a question from what the paper itself says. The source is the authors' LaTeX, read in full, in a version you can name.

## Steps

1. **Find what the project already has.** `grep -rl '<arxiv id>' --include='*.md' .` finds an existing note and the notes directory. If that directory has its own rules file (a `CLAUDE.md` next to the notes), read it now. Such a file loads only when a file in its directory is opened, and a reading request opens none.

2. **Look up the latest version.** `curl -s 'https://export.arxiv.org/api/query?id_list=<id>'`. Inside `<entry>`, `<id>` ends in the latest `vN`, `<published>` is v1's date and `<updated>` is the latest version's date.

3. **Fetch the source with arxiv-to-prompt.** `arxiv-to-prompt <id>vN > <scratch>/<Name>.tex` (install with `uv tool install arxiv-to-prompt` if missing).
   - Never use the HTML rendering, the abstract page or a web-fetch summary. Fetch tools summarize with a small model, and HTML loses table cells and footnotes. The details a close reading is for live in tables, footnotes and the appendix.
   - If the project already keeps a `.tex` for the paper, diff it against the fresh one. When the kept one is an older version, replace it and treat the note as stale.
   - Not on arXiv: read the PDF with `Read` page ranges.

4. **Read all of it, appendix included**, in chunks of at most about 500 lines. Write "the paper does not say" only after the appendix, the table and figure captions, and the experimental-setup paragraphs have been read. A later version often answers what an earlier one left out.

5. **Answer the question.**
   - Point to where each fact comes from (section, table, figure, equation, appendix) and name the version read (`vN`, date).
   - Mark what you inferred, as opposed to what the paper states.
   - List what the question needs that the paper does not report, such as a baseline's success rate, a threshold's value or a detection delay. That gap is often where a new method can differ.

6. **Update the project note**, if the project keeps one, under its rules file.
   - Fix "not stated" claims that the version you read now answers, and add results the note lacks.
   - Record the version read.
   - Save the `.tex` next to the note, under the note's name.
