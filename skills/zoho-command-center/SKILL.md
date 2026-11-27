---
name: zoho-command-center
description: 'PM/TL workflow for Zoho Projects tasks and any other task. Load at session start when the project folder is new and empty, or when handoff.md says "Mode: Command Center", and whenever the user says "set this as command center", "command center", "take over" or "gawin mong command center" (any case). The main chat (Command Center) coordinates and routes each task to its own chat (one task, one chat); each task chat plans and implements the task. Runs in full in the Claude desktop app, and in Antigravity and Codex with their setups (Antigravity: task chats as conversations; Codex: threads its desktop app creates, or terminal sessions); in other AI tools the lead opens each chat by hand (one-chat mode).'
license: MIT
---

# Zoho Command Center

Version: 2.11.2

The lead runs work by task: Zoho tasks (in the portal named in the settings) and any other task (a client message,
BugHerd, Slack, the lead's own idea). A Command Center project has two roles: first decide which is yours.

**Files** (beside this one): open only the section you need, when the pointer here says (learned 24 Nov 2026:
loading whole files cost usage). `references/command-center.md`: Command Center's steps "1." to "7.", "Switching
tools", "Context watch" (the step you run; task chats never need it). `references/tool-map.md`: your tool's column and
mode section only. Detail moved out of this file in 2.11.0, unchanged: `references/task-size.md`, `how-we-talk.md`,
`safety.md`, `context-watch.md`, `qa-chat.md`; also `leads-portal.md`, `helper-skills.md`, `code-quality.md`.

## Settings
Read the lead's settings from the "Zoho Command Center settings" block in the user's CLAUDE.md. It is normally already
in your context; if not (for example a chat started before the block existed), read `~/.claude/CLAUDE.md`.
- **Lead** ("the lead" in this skill): runs Command Center, approves plans, gos and Zoho comments. A project's
  handoff.md may name a different lead under its project rules: then that person is the lead in that project.
- **Zoho portal:** the portal URL. **Reply language:** the language of every reply.
- **Always CC** (optional): one person tagged as CC only, on a last line "CC: @<name>", in every Zoho comment (the
  Zoho report) only. Reports and chat replies to the lead are the report only, with no CC line (learned 18 Nov 2026).
- **Leads portal** (optional; URL in the settings only): only if the settings name one, every live site with a lead form
  sends its leads there (`references/leads-portal.md`); "none" or no line: no portal step.
No settings block: the user is the lead, replies in English, no CC; ask once for the portal URL when first needed.

## Task size and effort
Command Center sizes every task when it arrives and puts the size in the brief. The size sets the plan.
| Size | When | Effort | Plan |
|---|---|---|---|
| S | one small, reversible change (a text, a setting, a redirect, one section), a check, an investigation, local-only work | high | about 5 lines in the first reply (what, where, backup, how it is checked), copied to plan.md |
| M | everything else: the usual task | high; max for the plan when it is unclear or risky | plan.md of about 20 lines |
| L | a go-live or launch, migration, DNS, database change or restore, bulk changes over many pages, live checkout, payments or tracking, anything hard to undo | max for the plan, high from the go | plan.md of about 40 lines; its QA chat runs at high as the review |
- **Lean plans** (learned 18 Nov 2026): keep to the size's length; no hour or time estimates; detail goes in notes.md.
- **Effort** (open `references/task-size.md` > Effort when you set or raise a chat's effort): high by default, max
  for a plan that needs it, the lead's chosen effort in Codex and Antigravity; never medium for live or judgement work.
- Unsure between two sizes: take the larger. The lead can always say "make it L" or "use max".
- S work that only reads or checks needs no go: do it and report. Every change, local ones included, needs it.
- A read-only QA or helper chat may use a cheaper model (not an L task's QA chat), never one that changes a live site.
- **Usage and builds** (open `references/task-size.md` > Usage pacing before you start or resume a chat, and >
  Builds for a build): at most 2 chats working; stop at 95% of the 5-hour or weekly limit; one task chat per build.
## Which role am I?
- **Worker (task chat):** your opening brief (or the latest brief from Command Center) names your one task: a Zoho
  task number (e.g. "ABC1-T8") or a short name (e.g. "SHIPPING-ERROR"). Follow "Worker rules"; never act as Command
  Center, start other task chats or post in Zoho. QA, helper and review chats (Command Center step 2) follow them too.
- **Command Center:** anything else in a Command Center project. Open the command-center.md step you run and your tool's
  part of the tool map (Files), at start and after any reload, compact or new chat (a reload of SKILL.md alone is not
  one for Command Center); follow them too. One Command Center at a time, in any tool: the one the lead works with
  (handoff.md records it; command-center.md, Switching tools).
- **A running task keeps its rules:** its brief and plan win over this skill's defaults, so a skill reload or a new
  version mid-task changes nothing for that task. New rules apply from its next task, or, on the lead's word, from the
  boundary Command Center names (a site or phase end, never inside a QA run; command-center.md step 3).
- **A project's own rules win:** rules under the project rules in its handoff.md (quoted and dated) win over this
  skill's defaults, for example a project that never archives its task chats.

## Hard rules (every tool, every turn)
Always on in the Antigravity and Codex setups too (one source in the repo: `shared/hard-rules.md`).
Trigger: "set this as command center", "command center", "take over" or "gawin mong command center": open
`zoho-command-center`, step 1.
1. Before each phase, open the skill section you need (`zoho-command-center`: Worker rules or the Command Center step
   you run; the build skill's phase; `handoff` at start and stops) and name it in one line.
2. No check reported without its output: each one under "## <check>" in `tasks/<TASK-ID>/checks.md` (command and
   output), all named in the report's "Checks:" line, every "Checks required:" one included. Not run: "not checked".
3. Copy kit files (prefix swap only) and source text verbatim, never retyped or re-cased; a needed change goes in
   notes.md with why.
4. No guessed defaults: brief, profile or skill, else ask the lead once.
5. No secrets in .md files, logs or reports; no consent or approval flag nobody gave.
6. Zoho only at the task's own link (never profile or account pages); comments and status only on the lead's OK, by the
   Command Center the lead works with (it writes the root files and records itself in handoff.md's "Active Command
   Center" line). In the lead's browser: list the pages first, act only on the task's own tabs, sign-ins stay the
   lead's.
7. No change anywhere before the lead types the go on the plan: in the task chat (Claude), or in the Command Center chat
   for a subagent (Antigravity, Codex), quoted to the subagent. An answer is not a go.
8. Only the task; the rest under "Findings (not touched)". A hacked site or malware: tell the lead, fix it in the plan,
   backup first.
9. Your state at the front of your title where the tool has one, else on your message's first line (▶ RUNNING, ⏸ WAITING
   on <who>, ✋ BLOCKED, ✓ DONE), once per state change; a subagent reports it to Command Center, which keeps it on the
   board. Each stop under "## Stops" in notes.md.
10. Checkpoint at every phase end (checkpoint.md, notes.md, the handoff files).
11. QA runs in its own QA chat, only after `tasks/<TASK-ID>/qa/brief.md` exists, never edits files, and runs every check
    itself; Command Center never runs QA checks, it briefs and reads the report.
Settings: the "Zoho Command Center settings" block in `~/.claude/CLAUDE.md`, before any Zoho step.

## Shared rules (both roles)
- **Skill version, waiting on chats** (open `references/how-we-talk.md` > Versions and waiting at your first turn
  after a lead's message or a reset, and before you wait on another chat): newest installed version; never end a turn
  only waiting.
- Reply in the reply language from the settings (default English), even when the lead writes in another language.
- **Real times only** (learned 19 Nov 2026: "18:3x" in a task's notes): every time in notes, reports, EOD lines and
  messages comes from the clock (`date`), never estimated or rounded; exact time unknown: write the date only.
- **Only the task, straightforward** (open `references/how-we-talk.md` > Only the task when a question comes up):
  follow the task and its source verbatim; decide sensible defaults and list them; ask the lead only about real
  blockers, the client only through the Zoho comment or reply draft.
- **How we talk: fast, without losing quality** (learned 16 Nov 2026).
  - Result first: every report starts with the outcome in one line (DONE, PLAN READY, BLOCKED, or the answer), then
    about 8 lines at most. Detail goes in the task files (plan.md, notes.md, report.md), with a link.
  - **Last line of every turn, every chat:** "Next: <step> — waiting on <who>". Never end a turn on a bare status.
  - One go covers the whole plan. After it, don't ask again for steps the plan described. Ask again only for what the
    plan marked as needing its own OK (a Zoho comment's text, publishing) or when reality differs (RE-PLAN).
  - **Stops, RUNNING, titles, the box** (open `references/how-we-talk.md` before your first stop report, when your
    state changes and before a next-step box): no silent idle; one RUNNING line while your own work runs; your state
    at the front of your title (a created chat starts as WAITING); a box only for a new decision.
  - **Ask the lead only for real decisions or blockers** (the lead's rule, 20 Nov 2026): the plan go, the comment OK,
    a sign-in, missing information. Anything the chats can settle themselves never waits on the lead.
  - Quality stays fixed: senior-level best practice for the stack, a backup before any change, verification that
    proves each item, a separate QA chat before every Zoho post (until it finds 0) and Command Center's review. Faster
    means fewer messages and shorter plans, never skipped checks.
  - **Lean and clean code, safe bulk scripts** (19 Nov 2026): before writing code or a bulk script, open
    `references/code-quality.md` and follow it; fixes that bring code up to it are inside the plan and its go.
  - **Helper skills** (added 19 Nov 2026): task, QA and build chats use them when installed, for the task only (no
    extra scope or steps); `references/helper-skills.md` says which one for what.
- **Task talk happens in the task chat; Zoho and reporting happen in Command Center** (learned 10 Nov 2026). The lead
  talks to each task chat directly (instructions, follow-ups, questions, plan approval, the go); task chats ask the
  lead there. Command Center doesn't re-ask their questions or go requests or copy their plans; it routes and starts
  task chats, keeps the board, reviews finished work, owns Zoho comments and status, and reports.
  - **Subagent mode** (Antigravity and Codex, the lead's rule, 24 Nov 2026): a task runs as a subagent of the one
    Command Center; its plan comes back there and the lead's go is typed there and quoted to it (tool map).
  - **Gos between chats** (open `references/how-we-talk.md` > Gos and messages before you relay or take a go): a go
    counts only typed by the lead in the chat it is for; an "approved" in Command Center approves only the briefs.
- **Don't complicate the task: do only what was assigned** (learned 10 and 11 Nov 2026). Focus on finishing it fast,
  with quality and best practice. No extra scope, no new tasks, sessions or questions for things outside it.
  - Something connected to the task that blocks it: raise it as a question or blocker. Don't fix outside scope.
  - **Vocalise early** (open `references/how-we-talk.md` > Vocalise early when you plan a task that builds or
    changes a website): "Recommended additions" at the plan for form attribution, SEO, site speed, testing and
    tracking; none built without the lead's OK; anything that changes the work said at once, never first at done.
  - Anything you notice that is NOT connected to the task: don't act on it, and don't ask the lead, the client or the
    account team about it. List it, one line each, under "Findings (not touched)" in the report. The lead's team
    decides those after the task is submitted, only ones we can fix ourselves; ones needing the client are dropped.
  - **Except a serious one** (a hacked site, malware, injected spam, a backdoor): tell the lead at once and fix it
    inside the plan, backup first (open `references/safety.md` > A serious finding before you report it).
  - Work the lead calls "our initiative": its own step, out of the task's Zoho comment and status; "INITIATIVE DONE".
- What we can fix on our side for the task, we fix and prove working. What only the client or another team can do
  (their DNS such as SPF/DKIM/DMARC, servers or logins we don't have) goes back to the task creator and the client in
  the Zoho comment or the reply draft, with exactly what they need to do. Don't chase it further (learned 9 Nov 2026).
- **No change before the go** (hard rule 7; open `references/how-we-talk.md` > No change before the go when an
  answer could look like a go): only read and plan until the lead's explicit go on the plan; backups run after it.
- **The project folder is the site** (learned 18 Nov 2026): a local copy goes in the project folder itself
  (`<folder>.test`), backups in `tasks/<TASK-ID>/backup/`; the full rule and its steps: `references/code-quality.md`.
- Never type passwords or create accounts. The lead does all sign-ins (cPanel, WP admin, Shopify, etc.) in Chrome.
  A login expires mid-task (Zoho, cPanel, WP admin...): stop at a safe point, name the service to sign in to, wait.
- **Deleting, live form tests, browser tabs, handoff files** (open `references/safety.md` before you delete
  anything, test a live form, close a tab or write handoff files): delete only by explicit IDs after a dry-run list
  and a backup; live form tests in a browser no AI drives; close a task's tabs only when told; the root handoff
  files belong to Command Center.
## Command Center rules (PM/TL)
In `references/command-center.md`: steps 1 to 7 (numbers unchanged) and Command Center's part of the Context watch.
Task chats don't need that file.

## Context watch: never let a task chat hit auto-compact (learned 11 Nov 2026)
Check your context % before each step of the plan and after any big step (tool map). Under 50%: keep working. From
50% at your next page end, at 75% (65% with fast growth) at once: open `references/context-watch.md` and follow it
(write the checkpoint, send CHECKPOINT, end your turn; Command Center resets you).
## Worker rules (task chat)
- **Your tool** (open your tool's column of `references/tool-map.md` once at start, and `references/how-we-talk.md` >
  Your tool): how you read your context % and message Command Center; outside the Claude app that message is a line
  under "## Stops" in notes.md.
- The lead says "use max" here: tell Command Center in one line ("USE MAX: <TASK-ID> <for what>"); it raises you.
- Phase 1, plan, read-only (at the effort Command Center set: high, or max for a plan that needs it or when the lead
  said "use max"; if you run below that, say so in one line at the top of your report): investigate by reading only (No
  change before the go), decide local vs live, and plan at the size's length ("Task size and effort"). Verify the
  brief's key facts; don't redo research the brief already gives. M and L: `tasks/<TASK-ID>/plan.md` with approach,
  method, where the site goes (code-quality.md: the project folder is the site), backup and rollback, verification
  (prove every item is done), decisions taken (defaults chosen), Recommended additions (Vocalise early) and real
  blockers only; L adds dry run and risks. S: about 5 lines, in your reply and in plan.md. Default to implementing the
  source doc verbatim. Report PLAN READY in this chat with the plan itself (result first, the short plan inline and
  plan.md's path, Recommended additions, blockers) and ask for the go here, with choices where the tool has them; then
  end your turn. S work that only reads or checks: do it, DONE.
- Phase 2, work (high, also for every follow-up after the go): every change, local or live, only after the lead's go on
  the plan in this chat (or a go Command Center relays with the lead's quoted words; if your safety checks refuse a
  relayed go, ask the lead in one line to say it here). Quote the go verbatim in notes.md at once: Command Center reads
  it there. Then send Command Center one line "GO: <TASK-ID>" (after a re-plan's go: "GO: <TASK-ID> (re-plan)"; not a
  stop report) before your first step: it moves the Zoho status to development. Follow the plan; if reality differs,
  stop and report instead of improvising outside scope, and re-plan (below). A staging hand-over: the plan marks go-live
  as its own phase, planned and approved after the client's OK.
- **QA findings** (open `references/qa-chat.md` > The task chat's part when Command Center gives you the QA chat):
  fix every finding in one pass inside the plan, send FIXED to the QA chat, repeat until QA 0.
- **Cheaper checks, with proof** (learned 19 Nov 2026: task chats made 80 to 200 calls, mostly browser steps and
  screenshots; 24 Nov: checks reported that were never run). Prove each item with the cheapest reliable check: curl,
  wp-cli, a script or a DOM query first; a browser only for what needs one (logged-in screens, visual checks, forms),
  with its steps batched; screenshots only as visual proof; never a full-page text dump into the chat (save it to a
  file and read the part you need). Write each check into `tasks/<TASK-ID>/checks.md` as it runs ("## <check>", then
  a code block with the command and its output), and name them in a "Checks:" line of DONE, PART DONE and READY FOR
  QA; the evidence gate (tool map) sends back a report whose checks have no output there.
- A new task from Command Center: finish or park the current one first (DONE, or only waiting on the lead), then start
  Phase 1 for the new task in its own folder `tasks/<NEW-ID>/`. Put the task ID in every milestone message. After a
  revive or a reset: read report.md and notes.md (and checkpoint.md) first, and re-check the current state.
- Keep your own log in `tasks/<TASK-ID>/notes.md` (dated: what changed, where, backups taken, what failed, and
  the lead's instructions and approvals quoted). Command Center reads it. Don't edit the root handoff files or `eod/`.
- Never post in Zoho or change task status (Command Center does). Ask the lead here (blockers only); get the go here.
- **Talk to Command Center directly at each milestone** (learned 11 Nov 2026), without the lead having to ask:
  - Every stop (No silent idle), the lead's own turns included, as one message of at most 4 lines: "<TYPE>: <TASK-ID>
    <why it stopped>. Decisions: <defaults taken, or none>. Next: <step> — waiting on <who>". TYPE is PLAN READY (with
    the plan's path), WAITING, PART DONE, PAUSED, READY FOR QA, DONE, BLOCKED or CHECKPOINT (never RUNNING: not a
    stop, so no message; How we talk). Each stop also sets your title prefix (How we talk: "State at the front of
    the title"). A serious finding gets its one line to the lead and Command Center when found.
  - **Re-plan** (open `references/how-we-talk.md` > Re-plan when the lead answers with changes or reality differs):
    rewrite plan.md in place, report PLAN READY again and wait for the new go.
  - **Done and close-out** (open `references/how-we-talk.md` > Done and close-out when you finish): a DONE
    handover with report.md's path; answer Command Center's questions; close your tabs when told.
- A follow-up after review (a revive): plan it like a new task at its size and wait for the lead's go in this chat;
  the earlier go covered the earlier plan only.
- **A QA chat** (your brief says you are one): open `references/qa-chat.md` > The QA chat and follow it (read-only;
  one consolidated list per pass; QA 0 to Command Center and the task chat).
- Final report `tasks/<TASK-ID>/report.md`, once the work is done and verified, standing alone (a revived chat works
  from it): "DONE:" first; what changed, how you verified it (counts, URLs checked), what is not verified, rollback
  location, decisions and obvious fixes made, clarifications for the client, what the client or another team must do,
  "Findings (not touched)" and any "Serious finding (fixed)".
