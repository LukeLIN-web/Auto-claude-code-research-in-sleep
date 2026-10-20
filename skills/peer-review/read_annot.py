#!/usr/bin/env python3
"""Print the annotations saved in an annotatable page, for Claude to apply.

  read_annot.py PAGE.html [PAGE2.html ...]

PAGE.html  a 批改快照.html from the page's snapshot button, or the page saved
           with the browser's "Save Page As" (complete page / single file).
           Reads the embedded state, then lists every edited or annotated
           line with its line number, original zh, English (if any), the
           edited text and the notes. The live localStorage copy cannot be
           read from disk; ask the user for a snapshot or 批改清单.md instead.
"""
import html, json, re, sys
from pathlib import Path

def text(s):
    s = re.sub(r"<del>(.*?)</del>", r"[删除:\1]", s or "", flags=re.S)
    s = re.sub(r"<ins>(.*?)</ins>", r"[插入:\1]", s, flags=re.S)
    s = re.sub(r"<mark>(.*?)</mark>", r"[高亮:\1]", s, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", s))

for path in sys.argv[1:]:
    t = Path(path).read_text(encoding="utf-8")
    st = re.search(r'<script id="embedded-state" type="application/json">(.*?)</script>', t, re.S)
    state = json.loads(st.group(1)) if st else None
    if not state:
        print(f"{path}: no saved annotations embedded (state is empty)"); continue
    blocks = {str(b["i"]): b for b in json.loads(re.search(r"const BLOCKS = (\[.*?\]);\n", t, re.S).group(1))}
    layout = int(re.search(r"const LAYOUT = (\d+);", t).group(1))
    print(f"# {path}\nsaved layout v{state.get('v', 1)}, page layout v{layout}"
          + ("" if state.get("v", 1) == layout else "  (MISMATCH: indices may refer to an older page)"))
    for k in sorted(set(state.get("edits", {})) | set(state.get("notes", {})), key=int):
        b = blocks.get(k, {})
        print(f"\n## {'NOTES ' if b.get('src') == 'notes' else ''}line {b.get('ln', int(k) + 1)} (block i={k})")
        print("原文:", text(b.get("zh", "?")))
        if b.get("en"): print("英文:", text(b["en"]))
        if k in state.get("edits", {}): print("修改为:", text(state["edits"][k]))
        for n in state.get("notes", {}).get(k, []):
            if n.strip(): print("批注:", n.strip())
    if (state.get("overall") or "").strip(): print("\n## 总体意见\n" + state["overall"].strip())
