#!/usr/bin/env python3
"""Build the annotatable HTML page (Step 9) from a Markdown file.

  md_to_annot_html.py ZH.md OUT.html [--en EN.md] [--notes NOTES.md] [--legacy OLD.html | --applied]

ZH.md      the text the user annotates (review_*.zh.md, or NOTES_*.zh.md alone)
--en       line-aligned English file; adds the "显示英文原文" toggle and the
           英文原文 line in 批改清单.
--notes    candidate-findings Markdown appended after the review on the same
           page (no English twin); its lines are reported as "NOTES 第 n 行".
--legacy   the previous HTML for the same file: keeps its localStorage key and
           maps saved edits/notes to the new line indices by exact text match
           (lines whose text changed are reported as lost).
--applied  use after applying the user's annotations: the page starts clean
           (new localStorage key) instead of showing the applied edits again.
"""
import argparse, html, json, re, sys, time
from pathlib import Path

TEMPLATE = Path(__file__).with_name("annot_template.html")

def inline(t):
    t = html.escape(t, quote=False)
    codes = []
    t = re.sub(r"`([^`]+)`", lambda m: codes.append(m.group(1)) or f"\x00{len(codes)-1}\x00", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", t)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', t)
    return re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{codes[int(m.group(1))]}</code>", t)

def parse(lines):
    out = []
    for i, raw in enumerate(lines):
        line = raw.rstrip("\n")
        if not line.strip():
            continue
        b = {"i": i, "kind": "p", "level": 0, "marker": "", "num": ""}
        body = line
        if m := re.match(r"(#{1,3}) (.*)", line):
            b["kind"], b["marker"], body = f"h{len(m.group(1))}", m.group(1) + " ", m.group(2)
        elif re.fullmatch(r"\s*(-{3,}|\*{3,})\s*", line):
            b["kind"], b["marker"], body = "hr", line.strip(), ""
        elif m := re.match(r"(\s*)([-*]) (.*)", line):
            b.update(kind="li", level=len(m.group(1)) // 2 + 1, marker=m.group(1) + m.group(2) + " ")
            body = m.group(3)
        elif m := re.match(r"(\s*)(\d+)\. (.*)", line):
            b.update(kind="ol", level=len(m.group(1)) // 2 + 1, marker=f"{m.group(1)}{m.group(2)}. ", num=m.group(2))
            body = m.group(3)
        elif m := re.fullmatch(r"`(\d+: .*)`", line.strip()):
            b["kind"], body = "rating", m.group(1)
        b["zh"] = inline(body)
        out.append(b)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("zh"); ap.add_argument("out")
    ap.add_argument("--en"); ap.add_argument("--notes"); ap.add_argument("--legacy")
    ap.add_argument("--applied", action="store_true",
                    help="the saved annotations have been applied: start the page clean instead of migrating them")
    a = ap.parse_args()
    zl = Path(a.zh).read_text(encoding="utf-8").splitlines()
    blocks = parse(zl)
    if a.en:
        el = Path(a.en).read_text(encoding="utf-8").splitlines()
        if len(el) != len(zl):
            sys.exit(f"not line-aligned: {len(zl)} zh lines vs {len(el)} en lines")
        for b in blocks:
            e = parse([""] * b["i"] + [el[b["i"]]])
            b["en"] = e[0]["zh"] if e else ""
    else:
        for b in blocks:
            b["en"] = ""
    for b in blocks:
        b["src"], b["ln"] = "review", b["i"] + 1
    if a.notes:
        nl = Path(a.notes).read_text(encoding="utf-8").splitlines()
        off = len(zl) + 1
        for b in parse(nl):
            b.update(en="", src="notes", ln=b["i"] + 1, i=b["i"] + off)
            blocks.append(b)
    base = Path(a.out).name.removesuffix(".html")
    legacy, layout = {}, 1
    if a.applied:
        # a new localStorage key, so the browser does not reload annotations Claude already applied
        base = f"{base}:{int(time.time())}"
    elif a.legacy:
        old = Path(a.legacy).read_text(encoding="utf-8")
        base = re.search(r'const KEY = "review-markup:(.*?)";', old).group(1)
        legacy = json.loads(re.search(r"const LEGACY = (\{.*?\});", old).group(1))
        prev = int(re.search(r"const LAYOUT = (\d+);", old).group(1))
        oldb = json.loads(re.search(r"const BLOCKS = (\[.*?\]);\n", old, re.S).group(1))
        new_by_text = {}
        for b in blocks:
            new_by_text.setdefault(b["zh"], b["i"])
        m = {str(b["i"]): new_by_text.get(b["zh"]) for b in oldb}
        lost = [k for k, v in m.items() if v is None]
        # chain earlier layouts through this mapping
        legacy = {L: {k: (m.get(str(v)) if v is not None else None) for k, v in mp.items()} for L, mp in legacy.items()}
        legacy[str(prev)] = m
        layout = prev + 1
        if lost:
            print("annotations on these old line indices will be lost:", ", ".join(lost), file=sys.stderr)
    title = re.sub(r"<[^>]+>", "", next((b["zh"] for b in blocks if b["kind"] == "h1"), base))
    if a.en and a.notes:
        help_ = ('<b>怎么用：</b>上半部分是审稿意见（中文，可切换显示英文），下半部分是候选问题清单。直接点击任意段落即可修改（左侧绿线 = 已改）；悬停在一条上点右侧 <b>＋批注</b> 写“采纳 / 删 / 改成什么”；选中文字可用 <b>高亮</b>、<b>删除线</b>、<b>插入</b>、<b>批注</b>。\n'
                 '    改动会自动存在<b>这个浏览器</b>里，Claude 读不到；写完点 <b>保存到文件</b> 写回这个 HTML 文件（Chrome / Edge：第一次选中本页文件，之后直接覆盖；其他浏览器会下载一份快照），或点 <b>导出批改清单</b>。')
        ph = "总体意见：哪几条作为主要缺点、哪些放进问题、分数是否要调整……"
    elif a.en:
        help_ = ('<b>怎么批改：</b>直接点击任意段落即可修改文字（左侧绿线 = 已改）。选中一段文字会弹出工具条：<b>高亮</b>、<b>删除线</b>（建议删除）、<b>插入</b>（标为新增）、<b>批注</b>、<b>清除</b>。\n'
                 '    鼠标悬停在段落上，右侧有 <b>＋批注</b> 和 <b>还原</b>。改动会自动存在<b>这个浏览器</b>里，Claude 读不到；点 <b>保存到文件</b> 写回这个 HTML 文件（Chrome / Edge：第一次选中本页文件，之后直接覆盖；其他浏览器会下载一份快照），Claude 就能读到。<b>导出批改清单</b>会生成一份含英文原文、原译文、修改后文本与批注的 Markdown。')
        ph = "对这份审稿意见的整体看法、要加强或删掉的论点、分数是否要调整……"
    else:
        help_ = ('<b>怎么批注：</b>鼠标悬停在任意一条上，点右侧 <b>＋批注</b> 写“采纳 / 删 / 改成什么”；也可以直接点击文字修改（左侧绿线 = 已改），或选中文字用 <b>高亮</b>、<b>删除线</b>、<b>插入</b>、<b>批注</b>。\n'
                 '    改动会自动存在<b>这个浏览器</b>里，Claude 读不到；写完点 <b>保存到文件</b> 写回这个 HTML 文件（Chrome / Edge：第一次选中本页文件，之后直接覆盖；其他浏览器会下载一份快照），或点 <b>导出批改清单</b>。')
        ph = "总体意见：比如哪几条作为主要缺点、哪些放进问题、评分是否要调整……"
    s = TEMPLATE.read_text(encoding="utf-8")
    js = lambda o: json.dumps(o, ensure_ascii=False).replace("</", "<\\/")
    for k, v in {"__TITLE__": html.escape(title), "__HELP__": help_, "__OVERALL_PH__": ph,
                 "__BLOCKS__": js(blocks), "__HAS_EN__": "true" if a.en else "false",
                 "__BASE__": base, "__LEGACY__": js(legacy), "__LAYOUT__": str(layout)}.items():
        assert k in s, k
        s = s.replace(k, v)
    Path(a.out).write_text(s, encoding="utf-8")
    print(f"wrote {a.out}: {len(blocks)} blocks")

if __name__ == "__main__":
    main()
