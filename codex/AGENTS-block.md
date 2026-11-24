<!-- zcc-managed:start (zoho-command-center Codex setup; the install script replaces this block) -->
## Hard rules: zoho-command-center in Codex

Follow these as they stand, every turn. Each was broken once in a real task and caught only by an outside check.

1. **Open the skill before each phase:** `$zoho-command-center` at the start of every session in a Command Center
   project (Command Center rules in the main session, Worker rules in a task session), the build skill
   (`$convert-to-wordpress` or `$figma-to-wordpress`) before each build phase, `$handoff` at the start and at each stop.
2. **No check is reported without its output.** Write each check into `tasks/<TASK-ID>/checks.md` as it runs
   ("## <check>", then a code block with the command and its output) and name them in a "Checks:" line of DONE, PART
   DONE and READY FOR QA. No output: "not checked". A lenient check (ignored case or line breaks) is not a pass.
3. **Copy exactly:** kit files with only the prefix swapped; source text verbatim, never retyped or re-cased. A change a
   site really needs goes in notes.md with why.
4. **No guessed defaults:** settings come from the brief, the project's profile or the skill; else ask the lead once.
5. **No secrets in files, no consent for anyone:** never write a password, key or token into a .md file, log or report;
   never set a consent, approval or "confirmed" flag nobody gave.
6. **Zoho only by the task link;** never the lead's profile, account or settings pages. Comments and status only on the
   lead's OK, and only by the Command Center named in handoff.md's "Active Command Center" line (it alone writes the
   root files).
7. **Plan first:** no change anywhere until the lead types the go on the plan in that session. An answer is not a go.
8. **Do only the task;** the rest goes under "Findings (not touched)". A serious problem (a hacked site, malware) is
   told to the lead at once and fixed inside the plan, backup first.
9. **State and stops:** each stop is a line under "## Stops" at the top of the task's notes.md, and the first line of
   your message says the state (RUNNING, WAITING on <who>, BLOCKED, DONE).
10. **Checkpoint at every phase end** (checkpoint.md, notes.md, the handoff files), so a new session can resume.
11. **QA runs in its own read-only session** (`codex -s read-only` in the project folder), only once
    `tasks/<TASK-ID>/qa/brief.md` exists, and never edits files.

The lead's settings are in the "Zoho Command Center settings" block of `~/.claude/CLAUDE.md`: read it before any
Zoho step.
<!-- zcc-managed:end -->
