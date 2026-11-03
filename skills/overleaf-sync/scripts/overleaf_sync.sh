#!/usr/bin/env bash
# Sync Overleaf clones that ARE the paper (the shared-clone layout in SKILL.md): fetch → rebase → push.
# usage: overleaf_sync.sh <clone>...
#
# Syncs only: it never adds or commits. The clone is a shared working tree that often holds other
# sessions' regenerated tables and figures, and only the author of a change knows which files are theirs:
#   git -C <clone> add sec/3_method.tex && git -C <clone> commit -m "what changed" && overleaf_sync.sh <clone>
# A staged but uncommitted change makes it stop: the rebase would autostash it away, the remote would not
# change, and the run would still look like a sync. Unstaged changes are autostashed and put back, so a
# locally compiled PDF is never pushed.
#
# Auth: OVERLEAF_TOKEN_FILE names a file holding the git token (masked in all output); unset, git's
# credential helper answers. The project id is the clone's directory name if it is 24 hex digits, else the
# last part of its origin URL.
#
# A push is confirmed by fetching the remote again and comparing trees, never by "ahead N" or by push's
# exit code: with a token URL refs/remotes/origin/main never moves, and Overleaf can accept a push whose
# reply never arrives. A failure prints how long the clone has gone without a confirmed sync.
set -euo pipefail
[ "$#" -gt 0 ] || { sed -n '2,3p' "$0" >&2; exit 2; }

tok=""
if [ -n "${OVERLEAF_TOKEN_FILE:-}" ]; then
  [ -s "$OVERLEAF_TOKEN_FILE" ] || { echo "OVERLEAF_TOKEN_FILE is empty or missing: $OVERLEAF_TOKEN_FILE" >&2; exit 1; }
  tok="$(tr -d '\n' < "$OVERLEAF_TOKEN_FILE")"
fi
mask() { if [ -n "$tok" ]; then sed "s|${tok}|***|g"; else cat; fi; }

warn_stale() {  # $1 = the step that failed
  local last age
  last="$(cat .git/last-overleaf-sync 2>/dev/null || true)"
  if [ -n "$last" ]; then
    age="last confirmed sync $(( ($(date +%s) - last) / 3600 )) h ago ($(date -d "@$last" '+%Y-%m-%d %H:%M'))"
  else
    age="no confirmed sync recorded"
  fi
  printf '\n  ## OVERLEAF NOT SYNCED: %s\n  ## failed at: %s\n  ## %s; the web editor still shows the old draft\n\n' \
    "$id" "$1" "$age" >&2
}

failed=0
for clone in "$@"; do
  cd "$clone"
  id="$(basename "$(pwd)")"
  [[ "$id" =~ ^[0-9a-f]{24}$ ]] || id="$(git remote get-url origin | sed 's|.*/||; s|\.git$||')"
  url="https://git.overleaf.com/${id}"
  [ -z "$tok" ] || url="https://git:${tok}@git.overleaf.com/${id}"
  echo "==== $id"

  if ! git diff --cached --quiet; then
    echo "staged but uncommitted changes in $clone; this script does not commit:" >&2
    git diff --cached --stat >&2
    failed=1; cd - >/dev/null; continue
  fi
  if ! git fetch "$url" main 2>&1 | mask; then
    warn_stale "fetch"; failed=1; cd - >/dev/null; continue
  fi
  # a conflict needs a person: the clone stays mid-rebase, unstaged changes wait in `git stash list`
  if ! git -c rebase.autoStash=true rebase FETCH_HEAD; then
    warn_stale "rebase (conflict with web edits; resolve by hand)"; failed=1; cd - >/dev/null; continue
  fi
  if ! git diff --quiet FETCH_HEAD HEAD; then
    git push "$url" HEAD:main 2>&1 | mask || true
    git fetch "$url" main 2>&1 | mask || true
    if ! git diff --quiet FETCH_HEAD HEAD; then
      warn_stale "push (remote tree differs from HEAD after pushing)"; failed=1; cd - >/dev/null; continue
    fi
  fi
  git update-ref refs/remotes/origin/main FETCH_HEAD
  date +%s > .git/last-overleaf-sync
  echo "==> remote tree equals HEAD"
  cd - >/dev/null
done
[ "$failed" -eq 0 ] || { echo "at least one clone did not sync; see above" >&2; exit 1; }
