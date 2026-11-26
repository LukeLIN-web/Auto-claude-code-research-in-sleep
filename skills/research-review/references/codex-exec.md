# Codex route without the MCP tool

For a session whose `codex` MCP server is not connected: registering the bridge
mid-session does not connect it before the session reconnects. Run the command
the bridge itself builds (`mcp-servers/codex-exec/server.py`, `build_argv`).
`<REVIEWER_MODEL>` and `<effort>` are the pair in the skill's *Constants*
(capability fallback per `reviewer-routing.md`). Each thread's whole prompt goes
on stdin, so it has no length limit and needs no quoting.

## Round 1

```bash
C=<review cwd>; P=<prompt dir>; T=<trace dir>   # PDF-only mode: C = P = the review directory
for k in logic structure; do       # an idea or project: logic only
  setsid nohup codex exec --skip-git-repo-check --json --cd "$C" --sandbox read-only \
    -m <REVIEWER_MODEL> -c 'model_reasoning_effort="<effort>"' -o "$T/$k.last_message.md" - \
    < "$P/${k}_prompt.txt" > "$T/$k.events.jsonl" 2> "$T/$k.stderr.log" &
  sleep 15                         # the two children share one single-use refresh token
done
```

The thread id is `thread_id` on the first line of `$k.events.jsonl`. The thread
has finished when `"turn.completed"` or `"turn.failed"` appears there; its reply
is `$k.last_message.md`.

## Follow-up rounds

Resume each thread from the cwd it was created with. `resume` takes no `--cd` or
`--sandbox` and does not keep the model or effort, so pass them again:

```bash
cd "$C" && setsid nohup codex exec resume <thread_id> --skip-git-repo-check --json \
  -c 'sandbox_mode="read-only"' -m <REVIEWER_MODEL> -c 'model_reasoning_effort="<effort>"' \
  -o "$T/$k.r2.last_message.md" - < "$P/${k}_prompt_round2.txt" \
  > "$T/$k.r2.events.jsonl" 2> "$T/$k.r2.stderr.log" &
```

Record `tool: codex exec` or `codex exec resume` in the trace.
