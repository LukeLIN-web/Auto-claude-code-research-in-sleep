---
name: new-project-repo
description: "Start a new project repository that follows the layout of an existing one the user already works in — the root rule file and every per-folder rule file, the todo ledger, the issue-and-PR workflow with its commit gate, hooks and CI — then create the GitHub repo and push. Use when the user says 建一个新仓库, 新建 repo, 创建新项目, 按我们的文件夹架构, 复制 CLAUDE.md, 照这个仓库起一个新的, 'new repo like this one', 'bootstrap a project from our template', 'set up a repo with our rules'."
argument-hint: "[new repo name] [optional: template repo path, visibility]"
allowed-tools: Bash(*), Read, Grep, Glob, Write, Edit
---

# New Project Repo

Create a new repository that works the way an existing one does. The existing
repository (the *template*) carries rules its owner wrote over time; the new
one inherits them unchanged, receives the machinery those rules name, and is
gated green before its first push.

Three rules hold for every step:

- **Rule files are copied byte for byte.** A rule file records the owner's
  rulings. Do not adapt, trim or translate one because part of it concerns the
  old project; report the parts that no longer apply and let the owner decide.
  Remove a section only when the owner names it.
- **Machinery is adapted until it runs.** A gate script, hook or workflow that
  fails in the new repo is worse than none. Change exactly what ties it to the
  template and nothing else.
- **A document moved into the new repo leaves a link behind**, never a second
  copy.

## Step 1: Settle the four facts

| Fact | Default | Check |
|---|---|---|
| Name | given by the user | free locally and on the remote: `ls <parent>/<name>`, `gh repo view <owner>/<name>` |
| Owner | the account the user publishes under | `gh api user --jq .login` returns that account, before anything is created |
| Visibility | **private** | the user says otherwise |
| Local path | sibling of the template | the parent directory already holds the user's other projects |

Creating a remote repository is visible to others and awkward to undo. Private
is reversible in one command; public is not. Do not ask about visibility:
create private and say so in the report.

`gh auth login --with-token` can hang on a headless machine while a working
login is already stored. Test the login (`gh api user`) before trying to log in.

## Step 2: Read the template's layout

```bash
cd <template>
git ls-files | awk -F/ '{print $1}' | sort | uniq -c | sort -rn      # where the tracked files are
git ls-files | grep -E '(^|/)(CLAUDE|AGENTS)\.md$'                    # every rule file
cat .gitignore                                                        # which top-level folders are local-only
ls .githooks .github/workflows 2>/dev/null
```

Classify what you find:

| Kind | Typical files | What the new repo gets |
|---|---|---|
| Rule files | root and per-folder `CLAUDE.md` / `AGENTS.md` | byte-for-byte copy, every one, in the same folder |
| Workflow | `CONTRIBUTING.md`, merge script, claim script, commit gate, hooks, lint config, CI workflow | copied, then adapted (Step 4) |
| Ledgers | todo list, reference overview, benchmark overview | the page with its header, no entries |
| Project content | results, experiment scripts, configs, paper source, data | nothing |
| Local-only folders | data, outputs, virtual environments | the `.gitignore` lines only |

Skip a rule file that sits in a gitignored folder or in a vendored checkout: it
belongs to another repository.

## Step 3: Build the skeleton and copy the rule files

```bash
mkdir -p <new> && cd <new> && git init -q -b main
for f in $(git -C <template> ls-files | grep -E '(^|/)(CLAUDE|AGENTS)\.md$'); do
  mkdir -p "$(dirname "$f")" && cp "<template>/$f" "$f"
done
```

- A folder that holds a rule file needs no placeholder. A folder that is part of
  the layout and holds nothing yet gets a `.gitkeep`.
- Take the generic lines of the template's `.gitignore`; leave out the lines
  that name the template's own vendored checkouts.
- Write a short `README.md`: one sentence on what the project is, and a table of
  the folders and what goes in each.

## Step 4: Port the workflow

Copy the files the rule files name as the way work is done, then adapt:

| Symptom in the new repo | Cause | Change |
|---|---|---|
| Gate exempts files by name | exemption list of the template's legacy files | delete the list and the branch that reads it; drop the sentence in the rule file that describes the exemption |
| Gate builds a tool environment named after the template | hard-coded name | rename it |
| Gate cannot create its environment | the system Python lacks `venv` | run the gate once with an interpreter that has it on `PATH` |
| CI job never starts | a self-hosted runner is registered per repository; its labels do not follow | use a hosted runner, or register a runner for the new repo |
| Gate's test step fails with "no tests collected" | the test runner exits non-zero on an empty suite | copy the tests that cover the ported scripts |
| CI job syncs or deploys something | it serves the template's own artifacts | leave that job out |
| Hook does nothing | hooks path is per clone | `git config core.hooksPath <hooks dir>` |

Copy the tests of every script you port. They are the proof that the adaptation
kept the script working.

Machinery that needs infrastructure the new repo lacks (scheduled jobs on a
self-hosted runner, a shared memory or rule store) is left out of the first
pass and listed in the report. When the owner says to port it:

- **Check that it works in the template first.** Read the last runs of each
  scheduled workflow. Carry a failing job's cause into the report rather than
  into the new repo (a host that no longer exists in a host list, for example).
- **Self-hosted runner.** Register a second runner for the new repo on the same
  machine, with the same labels, in its own directory, reusing the installed
  runner's binaries and its environment files. Start it detached from the
  session, then trigger each scheduled workflow once by hand.
- **Shared stores.** When the template takes files, rule text or memory from a
  central store, register the new repo there and let the store's tool deliver
  them; do not hand-copy what the store owns. Before delivering, diff the
  store against the template: where the template is newer, take its version
  into the store first, or delivery rolls the new repo back.
- **Tags shared across repos on one machine.** A marker a scheduled job acts on
  (a session tagged with an issue number that gets closed with the issue) must
  carry the repo name once two repos use it on the same hosts.
- **Empty ledgers.** A job that edits a fixed set of pages needs each page to
  exist; create them with their header only.

## Step 5: Seed the content

- The todo ledger starts with its header and the one line saying how to claim.
- When the user has notes that started this project, **move** them in: the new
  repo holds the text, and the old location is replaced by a link to it.
- Put each piece in the folder whose rule file says it belongs there. One survey
  note is often two pages by the template's rules — what a benchmark is goes in
  one folder, what papers did goes in another. Split it; do not file the whole
  note under whichever folder comes first.
- Follow the destination folder's rule file while you write. If it forbids
  listing numbers in overview tables, the moved text loses its number lists.
- Work the rule files call for and you did not do (per-paper notes, a full
  reading) becomes an entry in the todo ledger.

## Step 6: Gate, commit, create, push

```bash
git add -A && bash <gate script>           # green before the first push
git commit -m "<what the first commit holds>"
gh repo create <owner>/<name> --private --description "<one line>"
git remote add origin https://github.com/<owner>/<name>.git
git push -u origin main
gh repo view <owner>/<name> --json visibility,url
```

Push with the credentials the user publishes under, passed explicitly when the
machine's default identity is someone else's. Filter a token out of any output
you print.

## Step 7: Report what does not resolve

A byte-for-byte copy points at files the new repo does not have. List them
mechanically:

```bash
python3 scripts/dangling_refs.py <new>
```

Report, in this order:

1. The repo URL, visibility, local path and first commit.
2. A table of what was placed where, marking each file *copied*, *adapted* or
   *new*.
3. Every adaptation to copied machinery, one line each.
4. The dangling pointers, grouped by rule file, and any rule that is about the
   old project's subject. Do not fix these yourself: say which need the owner's
   rewrite and which need a file ported.
5. What was left out and why (infrastructure the repo lacks).

## Do not

- Rewrite a rule so that it reads well for the new project.
- Copy results, experiment logs, memory files or anything naming the old
  project's machines and paths.
- Create the remote before the local gate is green.
- Keep two copies of a moved document.
