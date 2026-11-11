#!/usr/bin/env python3
"""Sync the rebuttal's collaborator doc (one Markdown file) to one HackMD note.

The collaborator doc is the team-facing view of the rebuttal: status and posting order,
the decisions still open, each reviewer's weaknesses and questions in the team's
language, every response draft with its translation, experiments and results. The
board prose is authored in the doc itself. Every draft section is derived: the block

    <!-- DRAFT:<response file> -->
    <!-- /DRAFT -->

belongs to this script, which rewrites it from the canonical response file (heading
with the comment count, the internal-marker note, one comment label per PART). Never
edit a draft inside the doc or on HackMD; edit the response file and rerun.

    python collab_doc_sync.py <rebuttal_dir>            # regenerate the draft sections
    python collab_doc_sync.py <rebuttal_dir> --push     # ... and push to the note
    python collab_doc_sync.py <rebuttal_dir> --create   # first time only: create the note

Config, <rebuttal_dir>/collab_doc.json:
    doc                 the Markdown file, relative to rebuttal_dir
    title               note title
    note_id             HackMD note id, written by --create; the link never changes
    token_file          file holding a HackMD API token, relative to rebuttal_dir
                        (or set HACKMD_TOKEN); create one at hackmd.io/settings#api
    translation_suffix  e.g. ".zh.md"; a translation's first line is <!-- EN <hash> -->,
                        the first 12 hex digits of the sha256 of the English file
    labels              wording in the team's language (keys in LABEL_KEYS)
    last_pushed_sha256  written by --push / --create
    translation_note    optional {"title", "note_id", "last_pushed_sha256"}: HackMD caps one
                        update at 100 KB, so a long doc puts its translations in a second
                        note; the main note keeps each translation's heading and a link
                        (labels.translation_link, with {url})

Push guard: the note's current content must hash to last_pushed_sha256. If a
collaborator edited the note since the last push, the script saves the note next to
the doc as <doc>.remote.md and stops without pushing. Carry their edits into the doc
(board prose) or into the response files (drafts) by hand, then rerun with --force.
A translation whose hash line does not match its English file also stops the push
(--allow-stale overrides).
"""
import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

API = "https://api.hackmd.io/v1"
LABEL_KEYS = ("draft_heading", "draft_label", "translation_label", "draft_note",
              "comment", "translation_comment", "promise", "needs_user")
REGION = re.compile(r"(<!-- DRAFT:(\S+) -->\n)(.*?)(<!-- /DRAFT -->)", re.S)
PART = re.compile(r"^<!-- PART (\d+)/(\d+) -->$")
HASH_LINE = re.compile(r"^<!-- EN ([0-9a-f]+) -->$")
MAX_BODY = 102400  # HackMD rejects a note update whose request body exceeds 100 KB (HTTP 413)


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def render(path, translation, labels):
    """One response file -> the Markdown shown in the doc."""
    lines = path.read_text(encoding="utf-8").split("\n")
    if translation and lines and HASH_LINE.match(lines[0]):
        lines = lines[1:]
    total = max((int(m.group(2)) for m in map(PART.match, lines) if m), default=1)
    label = labels["translation_label" if translation else "draft_label"]
    out = [labels["draft_heading"].format(label=label, n=total), ""]
    if not translation and labels.get("draft_note"):
        out += [labels["draft_note"], ""]
    comment = labels["translation_comment" if translation else "comment"]
    for line in lines:
        m = PART.match(line)
        if m:
            if int(m.group(1)) > 1:
                out += ["", "---", ""]
            out += ["", f"**{comment.format(i=m.group(1), n=m.group(2))}**", ""]
            continue
        if re.fullmatch(r"\s*<!--.*-->\s*", line):
            continue
        line = re.sub(r"⟦PROMISE (R-\d+)(?:,[^⟧]*)?⟧ ?",
                      lambda x: "`" + labels["promise"].format(id=x.group(1)) + "` ", line)
        line = re.sub(r"⟦NEEDS USER (\S+?)(?: —[^⟧]*)?⟧ ?",
                      lambda x: "`" + labels["needs_user"].format(id=x.group(1)) + "` ", line)
        out.append(line)
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip("\n")
    return text + "\n"


def stale_translation(path, suffix):
    """A translation whose hash line does not match its English source, else None."""
    english = path.with_name(path.name[: -len(suffix)] + ".md")
    first = path.read_text(encoding="utf-8").split("\n", 1)[0]
    m = HASH_LINE.match(first)
    want = sha(english.read_text(encoding="utf-8"))[:12]
    return None if m and m.group(1) == want else f"{path.name}: hash line != {english.name} ({want})"


def regenerate(rdir, cfg):
    doc = rdir / cfg["doc"]
    text = doc.read_text(encoding="utf-8")
    suffix = cfg.get("translation_suffix", ".zh.md")
    stale = []

    def fill(m):
        path = rdir / m.group(2)
        translation = path.name.endswith(suffix)
        if translation and (s := stale_translation(path, suffix)):
            stale.append(s)
        return m.group(1) + render(path, translation, cfg["labels"]) + m.group(4)

    new, n = REGION.subn(fill, text)
    if new != text:
        doc.write_text(new, encoding="utf-8")
    return new, n, stale


def api(method, url, token, body=None):
    data = None if body is None else json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": "Bearer " + token, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read()
    return json.loads(raw) if raw else {}


def split_translations(content, cfg):
    """Main-note text with each translation replaced by a link, and the translation-note text.

    One HackMD update may not exceed 100 KB, so a long doc keeps its board and drafts in
    the main note and moves the translations to a second note, in the same order, each
    under the main note's section heading."""
    suffix, labels = cfg.get("translation_suffix", ".zh.md"), cfg["labels"]
    url = f"https://hackmd.io/{cfg['translation_note']['note_id']}"
    parts = [f"# {cfg['translation_note']['title']}", ""]

    def cut(m):
        if not m.group(2).endswith(suffix):
            return m.group(0)
        before = content[: m.start()]
        section = ([l for l in before.split("\n") if l.startswith("## ")] or [""])[-1]
        body = m.group(3)
        parts.extend([section, "", body.rstrip("\n"), ""])
        heading = body.split("\n", 1)[0]
        return m.group(1) + heading + "\n\n" + labels["translation_link"].format(url=url) + "\n" + m.group(4)

    main_text = REGION.sub(cut, content)
    return main_text, "\n".join(parts).rstrip("\n") + "\n"


def push(note, content, token, rdir, doc_name, force):
    """Guarded update of one note; returns the sha256 now on the note."""
    remote = api("GET", f"{API}/notes/{note['note_id']}", token)
    if sha(remote.get("content", "")) != note.get("last_pushed_sha256") and not force:
        path = rdir / (doc_name + ".remote.md")
        path.write_text(remote.get("content", ""), encoding="utf-8")
        sys.exit(f"Note {note['note_id']} changed since the last push (last change by "
                 f"{(remote.get('lastChangeUser') or {}).get('name', '?')}). Saved it to {path.name}; "
                 "merge the edits by hand, then rerun with --force.")
    if remote.get("content") != content:
        api("PATCH", f"{API}/notes/{note['note_id']}", token, {"content": content})
    for _ in range(20):
        if api("GET", f"{API}/notes/{note['note_id']}", token).get("content") == content:
            return sha(content)
        time.sleep(1)
    sys.exit(f"pushed, but note {note['note_id']} does not read back identical; check it by hand")


def create(title, content, token):
    return api("POST", f"{API}/notes", token, {
        "title": title, "content": content, "readPermission": "owner",
        "writePermission": "owner", "commentPermission": "owners"})["id"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("rebuttal_dir", type=Path)
    ap.add_argument("--push", action="store_true")
    ap.add_argument("--create", action="store_true", help="create the note(s) that have no note_id yet, then push")
    ap.add_argument("--force", action="store_true", help="push although a note changed since the last push")
    ap.add_argument("--allow-stale", action="store_true", help="push although a translation is out of date")
    a = ap.parse_args()
    rdir = a.rebuttal_dir.resolve()
    cfg_path = rdir / "collab_doc.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    keys = LABEL_KEYS + (("translation_link",) if "translation_note" in cfg else ())
    missing = [k for k in keys if k not in cfg.get("labels", {})]
    if missing:
        sys.exit(f"collab_doc.json labels missing: {', '.join(missing)}")

    content, n, stale = regenerate(rdir, cfg)
    print(f"{cfg['doc']}: {n} draft sections regenerated, {len(content.encode())} bytes")
    for s in stale:
        print("STALE TRANSLATION:", s)
    if not (a.push or a.create):
        return
    if stale and not a.allow_stale:
        sys.exit(3)

    token = os.environ.get("HACKMD_TOKEN") or (rdir / cfg["token_file"]).read_text().strip()
    main_note = cfg
    tr_note = cfg.get("translation_note")
    if a.create:
        for note, title in [(tr_note, (tr_note or {}).get("title")), (main_note, cfg["title"])]:
            if note is not None and not note.get("note_id"):
                note["note_id"] = create(title, "", token)
                note["last_pushed_sha256"] = sha(api("GET", f"{API}/notes/{note['note_id']}", token).get("content", ""))
    for note in [main_note] + ([tr_note] if tr_note else []):
        if not note.get("note_id"):
            sys.exit("a note has no note_id; run with --create once (the link then never changes)")
        if not note.get("last_pushed_sha256"):
            note["last_pushed_sha256"] = sha("")
    texts = [(main_note, content)]
    if tr_note:
        main_text, tr_text = split_translations(content, cfg)
        texts = [(main_note, main_text), (tr_note, tr_text)]
    for note, text in texts:
        size = len(json.dumps({"content": text}, ensure_ascii=False, separators=(",", ":")).encode())
        if size > MAX_BODY:
            sys.exit(f"note {note['note_id']}: {size} bytes > HackMD's {MAX_BODY}-byte update limit; "
                     "add a translation_note or shorten the doc")
    for note, text in texts:
        note["last_pushed_sha256"] = push(note, text, token, rdir, cfg["doc"], a.force)
        cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"pushed: https://hackmd.io/{note['note_id']} ({len(text.encode())} bytes, read back identical)")


if __name__ == "__main__":
    main()
