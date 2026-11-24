---
name: zcc-hard-rules
trigger: always_on
description: Hard rules for the zoho-command-center workflow in Antigravity (Command Center, task chats, QA).
zcc-managed: zoho-command-center antigravity setup
---

# zoho-command-center hard rules (every turn)
1. Before each phase, open the skill section you need (`zoho-command-center`: Worker rules or the Command Center step
   you run; the build skill's phase; `handoff` at start and stops) and name it in one line.
2. No check reported without its output: each one under "## <check>" in `tasks/<TASK-ID>/checks.md` (command and
   output), all named in the report's "Checks:" line, every "Checks required:" one included. Not run: "not checked".
3. Copy kit files (prefix swap only) and source text verbatim, never retyped or re-cased; a needed change goes in
   notes.md with why.
4. No guessed defaults: brief, profile or skill, else ask the lead once.
5. No secrets in .md files, logs or reports; no consent or approval flag nobody gave.
6. Zoho only at the task's own link (never profile or account pages); comments and status only on the lead's OK, by the
   "Active Command Center" in handoff.md (it alone writes the root files).
7. No change anywhere before the lead types the go on the plan: in the task chat (Claude), or in the Command Center chat
   for a subagent (Antigravity, Codex), quoted to the subagent. An answer is not a go.
8. Only the task; the rest under "Findings (not touched)". A hacked site or malware: tell the lead, fix it in the plan,
   backup first.
9. Your state at the front of your title where the tool has one, else on your message's first line (▶ RUNNING, ⏸ WAITING
   on <who>, ✋ BLOCKED, ✓ DONE); a subagent reports it to Command Center, which keeps it on the board. Each stop under
   "## Stops" in notes.md.
10. Checkpoint at every phase end (checkpoint.md, notes.md, the handoff files).
11. QA is the `wp-qa` subagent, started only after `tasks/<TASK-ID>/qa/brief.md` exists; it never edits files and runs
    every check itself; Command Center never runs QA checks, it briefs and reads the report.
Settings: the "Zoho Command Center settings" block in `~/.claude/CLAUDE.md`, before any Zoho step.
