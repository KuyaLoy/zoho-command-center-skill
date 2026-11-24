<!-- zcc-managed:start (zoho-command-center Codex setup; the install script replaces this block) -->
## zoho-command-center hard rules (every turn)
1. Before each phase, open the skill section you need (`$zoho-command-center`: Worker rules or the Command Center step
   you run; the build skill's phase; `$handoff` at start and stops) and name it in one line.
2. No check reported without its output: each one under "## <check>" in `tasks/<TASK-ID>/checks.md` (command and
   output), all named in the report's "Checks:" line, every "Checks required:" one included. Not run: "not checked".
3. Copy kit files (prefix swap only) and source text verbatim, never retyped or re-cased; a needed change goes in
   notes.md with why.
4. No guessed defaults: brief, profile or skill, else ask the lead once.
5. No secrets in .md files, logs or reports; no consent or approval flag nobody gave.
6. Zoho only at the task's own link (never profile or account pages); comments and status only on the lead's OK, by
   the "Active Command Center" in handoff.md (it alone writes the root files).
7. No change anywhere before the lead types the go on the plan in that chat; an answer is not a go.
8. Only the task; the rest under "Findings (not touched)". A hacked site or malware: tell the lead, fix it in the plan,
   backup first.
9. State on the first line of each message and in the thread title where the app has one (RUNNING, WAITING on <who>,
   BLOCKED, DONE); each stop under "## Stops" in notes.md.
10. Checkpoint at every phase end (checkpoint.md, notes.md, the handoff files).
11. QA runs in its own read-only session (`codex -s read-only`), only after `tasks/<TASK-ID>/qa/brief.md` exists.
Settings: the "Zoho Command Center settings" block in `~/.claude/CLAUDE.md`, before any Zoho step.
<!-- zcc-managed:end -->
