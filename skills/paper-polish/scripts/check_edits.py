#!/usr/bin/env python3
"""Step 5's mechanical checks: compare an editor's scratch .tex with the copy it started from, paragraph by paragraph.

usage: check_edits.py <orig.tex> <edited.tex> --scope 12,13,40-45 [--terms terms.txt] [--check-draft check_draft.py]

The editor keeps the line count: a line whose whole text is cut becomes exactly `%CUT`, a split sentence stays on
its line, and no line is added. Lines outside --scope are frozen. For each changed paragraph (blank-line separated)
it reports:
  - a frozen line that changed (the edit is rejected);
  - numbers, \\cite keys and \\ref labels whose multiset changed (a number may go only with a sentence cut under a
    named /paper-prose-tighten class, and in a paper only if a table still shows it);
  - each line of TERMS (one term per line: a frozen name, a significance word) whose count changed, matched as a
    whole word;
  - hedge, pivot or concession words the edit added, and an added em dash;
  - an edited line with more than four commas outside \\cite, math and numbers (rewrite.md section 3).
It also lists every in-scope section, subsection or \\paragraph heading of EDITED longer than seven words, changed or
not (rewrite.md section 3).
With --check-draft (research-paper-writing/scripts/check_draft.py), it also lists ERROR and WARN messages the edited
file has and the original did not, and those of the same kind whose text changed (a count that grew: the owner
decides whether that is a new warning). It prints only paragraphs that need a look; the claim line per paragraph is
still the owner's to write.
"""
import argparse
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

HEDGE = re.compile(
    r"\b(may|might|could|likely|suggests?|appears?|seems?|somewhat|relatively|arguably|note that|we note|"
    r"importantly|however|although|while|partly|largely|roughly|approximately|potentially|generally|typically|"
    r"but|yet|instead|rather|admittedly|of course|only)\b", re.I)


def ranges(spec):
    out = set()
    for part in filter(None, spec.split(",")):
        lo, _, hi = part.partition("-")
        out.update(range(int(lo), int(hi or lo) + 1))
    return out


def paragraphs(lines):
    out, cur = [], []
    for i, line in enumerate(lines, 1):
        if line.strip():
            cur.append(i)
        elif cur:
            out.append(cur)
            cur = []
    return out + [cur] if cur else out


def tokens(text):
    # A subscript or superscript is part of a name (\ell_{2}), not a number the text states; the terms file counts names.
    bare = re.sub(r"\\(?:ref|eqref|[cC]ref|autoref|cite[tp]?\*?|label)\{[^}]*\}|[_^](?:\{[^{}]*\}|\w)", "", text)
    nums = Counter(re.findall(r"(?<![A-Za-z_\-])\d+(?:[.,]\d+)*", bare))
    cites = Counter(k.strip() for g in re.findall(r"\\cite[tp]?\*?(?:\[[^\]]*\])?\{([^}]*)\}", text) for k in g.split(","))
    refs = Counter(re.findall(r"\\(?:ref|eqref|[cC]ref|autoref)\{([^}]*)\}", text))
    return nums, cites, refs


def commas(line):
    """The most commas in one sentence of LINE, not counting those inside \\cite, math and numbers."""
    bare = re.sub(r"\\cite[tp]?\*?(?:\[[^\]]*\])?\{[^}]*\}|\$[^$]*\$|\d[\d,]*\d", "", line)
    return max((s.count(",") for s in re.split(r"(?<=[.!?])\s+", bare)), default=0)


HEADING = re.compile(r"\\(?:(?:sub)*section|paragraph)\*?(?:\[[^\]]*\])?\{")


def heading_words(line):
    """Printed word count of the heading on LINE, or None if it has none: a math span, a \\ref and a hyphenated
    word count as one word each, a command's name not at all."""
    m = HEADING.search(line)
    if not m:
        return None
    depth, i = 1, m.end()
    while i < len(line) and depth:
        depth += {"{": 1, "}": -1}.get(line[i], 0)
        i += 1
    text = re.sub(r"\$[^$]*\$|\\(?:ref|eqref|[cC]ref|autoref)\{[^}]*\}", "X", line[m.end():i - 1])
    text = re.sub(r"\\[A-Za-z]+\*?|[{}~]", " ", text)
    return len(re.findall(r"[^\s.,;:]+", text))


def draft_warnings(script, path):
    """ERROR and WARN messages of check_draft.py by kind (digits masked, so a message whose count changed is the same
    kind), each with its raw texts."""
    out = subprocess.run([sys.executable, script, str(path)], capture_output=True, text=True).stdout
    kinds = {}
    for l in out.splitlines():
        if re.match(r"\s*(ERROR|WARN)", l):
            msg = re.sub(r"line\s+\d+:?\s*", "", l.strip())
            kinds.setdefault(re.sub(r"\d+", "N", msg), []).append(msg)
    return kinds


def count(term, text):
    return len(re.findall(r"(?<!\w)" + re.escape(term) + r"(?!\w)", text))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("orig", type=Path)
    ap.add_argument("edited", type=Path)
    ap.add_argument("--scope", required=True, help="in-scope line numbers of ORIG, e.g. 12,13,40-45")
    ap.add_argument("--terms", type=Path)
    ap.add_argument("--check-draft")
    a = ap.parse_args()
    o = a.orig.read_text(encoding="utf-8").split("\n")
    e = a.edited.read_text(encoding="utf-8").split("\n")
    if len(o) != len(e):
        sys.exit(f"line count changed {len(o)} -> {len(e)}: the editor must keep one line per original line")
    scope = ranges(a.scope)
    terms = [t for t in a.terms.read_text().splitlines() if t.strip()] if a.terms else []
    flagged = 0
    for para in paragraphs(o):
        changed = [i for i in para if o[i - 1] != e[i - 1]]
        if not changed:
            continue
        before = " ".join(o[i - 1] for i in para)
        after = " ".join(e[i - 1] for i in para if e[i - 1] != "%CUT")
        issues = [f"frozen line {i} changed" for i in changed if i not in scope]
        for kind, x, y in zip(("numbers", "cite keys", "ref labels"), tokens(before), tokens(after)):
            if x != y:
                issues.append(f"{kind}: removed {dict(x - y)} added {dict(y - x)}")
        issues += [f"term {t!r}: {count(t, before)} -> {count(t, after)}" for t in terms if count(t, before) != count(t, after)]
        added = Counter(m.lower() for m in HEDGE.findall(after)) - Counter(m.lower() for m in HEDGE.findall(before))
        if added:
            issues.append(f"added hedge/pivot words {dict(added)}")
        if after.count("---") > before.count("---"):
            issues.append("em dash added")
        issues += [f"line {i}: a sentence with {commas(e[i - 1])} commas" for i in changed
                   if commas(e[i - 1]) > max(4, commas(o[i - 1]))]
        cut = [i for i in changed if e[i - 1] == "%CUT"]
        if issues:
            flagged += 1
            print(f"L{para[0]}-{para[-1]} changed {changed}{f' cut {cut}' if cut else ''}")
            for issue in issues:
                print("   ", issue)
    for i in sorted(scope):
        n = heading_words(e[i - 1]) if i <= len(e) else None
        if n and n > 7:
            flagged += 1
            print(f"line {i}: heading of {n} words (at most 7)")
    if a.check_draft:
        old, new = draft_warnings(a.check_draft, a.orig), draft_warnings(a.check_draft, a.edited)
        for kind, msgs in new.items():
            if len(msgs) > len(old.get(kind, [])):
                flagged += 1
                print(f"new check_draft message (x{len(msgs) - len(old.get(kind, []))}): {msgs[-1]}")
            elif sorted(msgs) != sorted(old[kind]):
                flagged += 1
                print(f"check_draft message changed: {' | '.join(old[kind])} -> {' | '.join(msgs)}")
    print(f"paragraphs or files needing a look: {flagged}")
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main())
