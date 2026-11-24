---
name: zcc-hard-rules
trigger: always_on
description: Hard rules for the zoho-command-center workflow in Antigravity (Command Center, task chats, QA).
zcc-managed: zoho-command-center antigravity setup
---

# Hard rules: zoho-command-center in Antigravity

These rules are written out here on purpose: follow them as they stand, every turn. They come from a build where
each of them was broken once and caught only by an outside check.

1. **Open the skill before each phase.** Skills here load only when opened, so open them yourself, never "if
   relevant": `zoho-command-center` at the start of every conversation in a Command Center project (Command Center
   rules in the main conversation, Worker rules in a task conversation), the task's build skill
   (`convert-to-wordpress` or `figma-to-wordpress`) before each build phase, and `handoff` at the start and at
   every stop. Say in one line which skill and which section you opened.
2. **No check is reported without its output.** Every "done", "passed", "0 findings", "matches" or "seeded" comes
   with the command you ran and its output pasted (the tail when long). No output: say "not checked". A lenient
   check (ignored case, line breaks or extra lines) is not a pass.
3. **Copy exactly.** Kit files are copied as they are, with only the prefix swapped; source text (copy, titles,
   labels) is copied verbatim, never retyped or re-cased. A change a site really needs is listed in the task's
   notes.md with why.
4. **No guessed defaults.** Admin email, users, site URL, protocol, plugin keys and any other setting come from the
   brief, the project's profile or the skill. Not there: ask the lead once; never invent one.
5. **No secrets in files, no consent on anyone's behalf.** Never write a password, key or token into a .md file,
   a log, notes or a report (name where it is kept instead). Never set a consent, approval or "confirmed" flag the
   client or a user did not give.
6. **Zoho only by the task link.** Open Zoho only at the task's own URL from the brief. Never open the lead's
   profile, account, settings or other pages. Comments and status changes only on the lead's OK, as the skill says.
7. **Plan first, then the go.** No change anywhere (no download to work from, no install, nothing live, no client
   contact) until the lead types the go on the plan in that conversation. An answer is not a go.
8. **Do only the task.** No extra scope; what you notice outside the task goes under "Findings (not touched)". A
   serious problem (a hacked site, malware) is told to the lead at once and fixed inside the plan, backup first.
9. **State in the title.** A task conversation keeps its state at the front of its title ("▶ RUNNING | ",
   "⏸ WAITING on <who> | ", "✋ BLOCKED | ", "✓ DONE | "), once per state change (the skill's tool map, Antigravity
   column), and writes every stop as a line under "## Stops" at the top of its notes.md.
10. **Checkpoint at every phase end.** This app has no context meter: at the end of each phase write the checkpoint
    and the handoff files, so a new conversation can resume from them.
11. **QA only after its brief.** The QA agent (`wp-qa`) starts only once `tasks/<TASK-ID>/qa/brief.md` exists, and
    it never edits files.

The lead's settings (lead, portal, reply language, CC) are in the "Zoho Command Center settings" block of
`~/.claude/CLAUDE.md`: read it before any Zoho step.
