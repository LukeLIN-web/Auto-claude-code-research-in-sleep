# paper-prose-tighten: the procedure for a whole-paper or whole-section pass

`SKILL.md` § Procedure says when this file applies. The One Test, the cut
classes and the hard stops it refers to are in `SKILL.md`.

`sections/` and `tables/` in the commands below stand for this paper's own section and table
directories; read them off the `\input` lines of `main.tex` (some templates use `sec/`) and
substitute before running, or the globs match nothing.

1. **Map every paragraph before reading for style.** Classes 1–3, 5, 6, 8–10, 12 and 14
   are found by grep; class 4 by reading the sentences those hits sit in; class 13 by the per-baseline listing in step 3; classes 7
   and 11, and paragraphs over ~250 words, are found only here. Emit one row per
   paragraph — file, line span, word count, and **one line saying what it
   claims** (add by hand, per row, which claim of the paper that supports):

   ```bash
   python3 - <<'PY'
   import glob, re
   WORD, SPACE = re.compile(r"[A-Za-z][A-Za-z'\-]*"), re.compile(r"\s+")
   for f in sorted(glob.glob('sections/*.tex')):  # numbered names sort into \input order
       print('=' * 8, f)
       lines = open(f, encoding='utf-8').read().split('\n')
       start = None
       for i, l in enumerate(lines + [''], 1):
           if l.strip() and start is None:
               start = i
           elif not l.strip() and start is not None:
               t = SPACE.sub(' ', ' '.join(lines[start - 1:i - 1])).strip()
               print(f"  L{start}-{i - 1}\t{len(WORD.findall(t)):4d}w\t{t[:70]}")
               start = None
   PY
   ```

   Then read the map, not the paper. Three things fall out that no reading pass
   gives you:
   - **A row that supports no claim of the paper** → the One Test at paragraph
     size. The whole paragraph is a cut candidate, not its sentences one by one.
   - **Two rows whose one-line summaries are the same claim** → class 7. This is
     where the largest single cuts are.
   - **Any row over ~250 words** → it is carrying several findings at once.
     Cutting it is not enough; **split it** (see step 5). A 350-word paragraph
     stays unreadable at 250.

   Present the map to the author before editing. It is also the artifact they
   asked for when they say "每一段都在讲啥" — and their pick of which rows to cut
   is worth more than your own ranking.

2. **Scope** as `SKILL.md` § Procedure sets it: main text, then appendix; captions only for leakage.

3. **Inventory.** Pull every candidate to a scratch list before editing:

   ```bash
   # numbers-in-prose density, per section
   command grep -o '\$[0-9][0-9,{}.\\]*\$' sections/*.tex | sort | uniq -c | sort -rn | head -40
   # bookkeeping shapes: "N of M", "N:M", "N -> M"
   command grep -nE '[0-9]+ of [0-9]|[0-9]\{?:\}?[0-9]|\\to [0-9]' sections/*.tex
   # class 10 value series: slash-strung readings, and "x on A, y on B, z on C"
   command grep -nE '\$[0-9.]+\$ ?/ ?\$[0-9.]+\$' sections/*.tex | command grep -v '&'
   command grep -nE '(on|at) [A-Z][A-Za-z-]+, \$?[-+0-9]' sections/*.tex | command grep -v '&'
   # class 12 wordy phrases: recall aid only, read every sentence (class 12)
   command grep -niE 'carr(y|ies|ied) out|refer(s|red)? to .* as|for the first time|together with|none of them|loosely worded|in order to|(less|more) often|half and half|has been reported to|are what make' sections/*.tex
   # class 14 exception clauses (captions too: the generator strings, then the rendered tables/*.tex);
   # high recall: a plain contrastive `but` matches too, keep only claims about every member that then take members back
   command grep -niE '\bexcept\b|\ball but\b|\b(every|all|each|any)\b[^.]{0,60}\bbut\b|\bbut (on |for )?[A-Z$\\]|save for|apart from|aside from|with the exception|\bexcluding\b|\bbarring\b' sections/*.tex tables/*.tex
   # class 13: every sentence that compares against one baseline, across all sections
   # (run once per baseline noun; read the list for split sentences and for copies that disagree)
   for b in 'alone' 'frozen' 'kNN-style' 'zero-shot' 'greedy'; do
     echo "== $b"; python3 - "$b" <<'PY'
   import glob, re, sys
   for f in sorted(glob.glob('sections/*.tex')):
       for n, line in enumerate(open(f, encoding='utf-8'), 1):
           if line.lstrip().startswith('%'): continue
           for s in re.split(r'(?<=[.;])\s+', line.strip()):
               if sys.argv[1] in s: print(f"{f}:{n}\t{s[:180]}")
   PY
   done
   # meta-narration stems
   command grep -niE 'we (report|claim|make|state|note|stress|log) (this|it|none|them)|rather than (claim|letting|running|averag)|net (it|this|that) away|averag\w* away|entitled to know|guard(ing)? against|we count it as such' sections/*.tex
   # narrated absences: sentences about things that don't exist
   command grep -niE 'publishes no|has no (row|column|entry)|does not (report|publish|evaluate|include|provide)|no official|not (available|reported) (in|for)' sections/*.tex
   # false pivots: negated-alternative claims (high recall — classify by hand;
   # headers, caption titles, and section titles need an eye pass on top)
   command grep -niE 'rather than|instead of|not reducible|, not |; it is|\bnor is|not by itself|not only|is not|are not' sections/*.tex tables/*.tex
   # artifact provenance / hygiene assurance (sweep tables/ too: it hides in config cells)
   command grep -niE 'without reference to|pre-?specified|pre-?registered stopping|(deployed|released) checkpoint|the run.s endpoint|held-out (accuracy|acc) is flat|chosen by (benchmark|evaluation)|frozen (evaluation |)subset|seed' sections/*.tex tables/*.tex
   # process vocabulary (class 9) -- count each term separately (SKILL.md, class 9's sweep note)
   for t in preregistered pre-registered pre-specified prespecified \
            "criteria frozen" "frozen before" "frozen margin" \
            "frozen evaluation" "stopping rule" "kill gate" "acceptance gate"; do
     n=$(command grep -ric -- "$t" sections/*.tex tables/*.tex 2>/dev/null | awk -F: '{s+=$NF} END{print s+0}')
     [ "$n" != 0 ] && printf '%4s  %s\n' "$n" "$t"
   done
   ```

4. **Classify, don't rewrite yet.** Tag each hit cut / keep / rewrite, and beside
   every keep write the claim it supports; a keep with no claim beside it is a
   cut. The
   temptation is to rewrite a bloated sentence into a slightly less bloated one;
   most hits should be **whole-clause deletions**. On a paper whose claims are
   already settled, expect most hits to be keeps — in practice ~80% of
   absence-pattern hits are load-bearing protocol scope. A low cut count is the
   test working, not failing.

5. **Edit.** Prefer deleting a clause over restructuring a sentence — the fewer
   words that move, the smaller the chance of shifting a claim. The one
   restructuring worth doing is the **paragraph split** step 1 flagged: find the
   findings inside the over-long paragraph, give each its own paragraph with its
   own topic sentence, and cut in the process. Splitting without cutting is
   still a win; the reader can now see where each finding starts.

6. **Verify the claim set is unchanged.** For each edited paragraph, state in
   one line what it claimed before and after. Any difference is a bug, not a
   tightening. Re-check every hard stop in `SKILL.md`. Then re-grep the labels you
   dropped a `\ref` to — a deleted paragraph can be the only citer of an
   appendix section.

7. **Compile** and report the size change (words or lines per section), plus a
   list of anything you deliberately left because cutting it would have
   loosened a claim.
