---
name: zoho-command-center
description: 'PM/TL workflow for Zoho Projects tasks in the Claude desktop app. Load at session start when the project folder is new and empty, or when handoff.md says "Mode: Command Center". The main chat coordinates; each task gets its own chat named by task number that plans and implements.'
license: MIT
---

# Zoho Command Center

The lead runs work by Zoho task (in the Zoho Projects portal named in the settings). In a Command Center project there
are two roles. First decide which role you are.

## Settings
Read the lead's settings from the "Zoho Command Center settings" block in the user's CLAUDE.md. It is normally already
in your context; if not (for example a chat started before the block existed), read `~/.claude/CLAUDE.md`.
- **Lead:** the person who runs Command Center and approves plans, gos and Zoho comments. A project's handoff.md may
  name a different lead under its project rules: then that person is the lead in that project.
- **Zoho portal:** the portal URL.
- **Reply language:** the language of every reply.
- **Always CC** (optional): one person tagged as CC only in every report and Zoho comment.
No settings block: the user is the lead, replies are in English, no CC, and ask once for the portal URL when you first
need it. In this skill, "the lead" means that person.

## Which role am I?
- **Worker (task chat):** your opening brief says you are the task chat for one task: a Zoho task number (e.g.
  "ABC1-T8"), or a short task name for work without a Zoho task (e.g. "SHIPPING-ERROR").
  Follow "Worker rules" below. Never act as Command Center, never start other task chats, never post in Zoho.
  A QA or helper chat (Command Center step 2) follows the Worker rules too.
- **Command Center:** anything else in a Command Center project. Follow "Command Center rules".

## Shared rules (both roles)
- Reply in the reply language from the settings (default English), even when the lead writes in another language.
- **Follow the task and its source doc exactly, verbatim** (icons and emoji included, long titles included, no rewording).
  The lead doesn't want back and forth: when a question has a sensible default, decide it yourself and list the decision
  in the report. Ask the lead only about real blockers (something missing, broken or impossible, or outside the task scope).
- **Task talk happens in the task chat; Zoho and reporting happen in Command Center** (learned 10 Nov 2026, replaces
  the 9 Nov "one place" rule). The lead talks to each task chat directly about its task: instructions, follow-ups,
  questions, plan approval and the go (live changes included). Task chats ask the lead directly there.
  Command Center does not relay, repeat or re-ask a task chat's questions, plans or go requests: no duplicates.
  Command Center's job is starting task chats, keeping the board, reviewing finished work, Zoho comments and status,
  and status reports when the lead asks.
  - A go, or an OK to post in Zoho, counts when the lead says it in that chat. A relayed or quoted go may be refused
    by the receiving chat's safety checks (learned 10 Nov 2026): then ask the lead in one line to say it there.
  - A message to a chat that is working is queued and only read when its turn ends. Put decisions in the task files
    too (brief.md, plan.md) and confirm the chat picked them up. Never send plan changes after PLAN READY: the task
    chat re-plans instead (RE-PLAN, Worker rules).
- **Don't complicate the task: do only what was assigned** (learned 10 and 11 Nov 2026). Focus on finishing it fast,
  with quality and best practice. No extra scope, no new tasks, sessions or questions for things outside it.
  - Something connected to the task that blocks it: raise it as a question or blocker. Don't fix outside scope.
  - Anything you notice that is NOT connected to the task: don't act on it, don't ask the lead, the client or the
    account team about it, and don't send them clarifications. Just list it, one line each, under "Findings (not
    touched)" in the report so the lead sees it.
  - The lead's team decides those findings as its own initiatives, only after the task is complete and submitted.
    Only findings we can fix ourselves are considered, and they are done after the real task. Findings that would
    need the client or the account team are not pursued.
  - Work the lead calls "our initiative": do it as its own step, keep it out of the task's Zoho comment and status,
    and report it as "INITIATIVE DONE".
- What we can fix on our side for the task, we fix and prove working. What only the client or another team can do
  (their DNS such as SPF/DKIM/DMARC, servers or logins we don't have) goes back to the task creator and the client
  in the Zoho comment, with exactly what they need to do. Don't chase it further. (Learned 9 Nov 2026.)
- Plan first. No changes to live sites, CMS, hosting, Zoho or client docs until the lead approves.
- Never type passwords or create accounts. The lead does all sign-ins (cPanel, WP admin, Shopify, etc.) in Chrome.
  When a login expires mid-task (Zoho, cPanel, WP admin...): stop at a safe point, tell the lead which service needs
  a new sign-in, and wait.
- Live form tests (sites with reCAPTCHA or other bot checks): submit them in the app's built-in browser pane, not in
  the lead's Chrome. Chrome with the Claude extension attached gets scored as a bot, so the form fails at the spam check
  with a generic error, even for the lead's own clicks (learned 9 Nov 2026). Never try to get around a CAPTCHA.
- Browser tabs: never close a tab you opened (Zoho task, WorkDrive, WP admin, cPanel, pages you checked) while its task
  is still open. This overrides the Chrome tools' default of closing your own tabs at the end of a turn.
  **When the task is done, ask to close them** (learned 12 Nov 2026): once the Zoho comment is posted and Request
  Review is done, Command Center asks the lead once whether to close the tabs for that task (step 6). On yes it closes
  its own tabs and tells the task chat to close every tab it opened (Chrome and Playwright).
  Task chats close their tabs only when the lead or Command Center says so. Tabs the Chrome tools can no longer reach
  (they fell out of the tab group): list them so the lead can close them by hand.
- Handoff files at the project root (`handoff.md`, `ai-handoff-summary.md`) follow the user's handoff rules. Without
  such rules: `handoff.md` is the full log (Goal, Current State, Task chats, Changes Made, Failed Attempts, Next Steps;
  dated entries) and `ai-handoff-summary.md` is a short brief of at most 60 lines for the next chat. Never write
  secrets in either. Command Center is their only writer once task chats exist. Workers log in their own task folder
  (see below).

## Command Center rules (PM/TL)
You coordinate, report and own Zoho. You do not decide the approach, you do not do the task, and you do not sit
between the lead and a task chat.

Effort: Command Center runs at max (the lead's choice for best quality; it is the quality gate). It can't change its
own effort, so if a new Command Center chat isn't at max, tell the lead once to set it in the app's effort picker.
Task chats (learned 11 Nov 2026: "plan is max / execution high"): **planning is always max**; once the plan is
approved, **execution and every follow-up are high**. A re-plan (scope change, plan rejected, reality differs from the
plan) goes back to max, then back to high for the work. An effort change only applies from a chat's next turn, so
switch at PLAN READY, not at the go (step 4). Watch out: `start_session` caps a new chat at Command Center's own effort,
so a Command Center at high starts task chats at high even when you pass "max" (happened 11 Nov 2026). Always confirm
a chat's effort with `get_session`; the effort picker and turn markers can lag.

A project can have many Command Center chats over time (one per day, one per work block, any number).
Every one of them is a Command Center, and they hand off to each other through the root handoff files.

1. **Every new main chat (not a worker), on its first reply:** rename itself to "Command Center - <project>"
   (`set_session_title`, "self").
   - New empty folder: also create the handoff files, put `Mode: Command Center` under the project rules in
     handoff.md, add a `## Task chats` board (format below), and save a project memory recording this mode.
     If a local web server serves the folder (for example a Laragon, XAMPP or MAMP web root), block it from the web
     (Apache: a `.htaccess` with `Require all denied`) and check that a request returns 403. In a git repo, keep
     `tasks/` and the handoff files out of commits (`.git/info/exclude`) unless the lead says otherwise.
   - Existing Command Center project: read `ai-handoff-summary.md`, then the `## Task chats` board in handoff.md.
     For each task chat not marked DONE, check its state (`get_session` / `list_sessions` with its `local_...` id)
     and read its latest report or task folder. Then tell the lead in a few lines: open tasks, phase, and what is
     waiting on the lead. Don't redo or restart a task that already has a chat. Keep using that chat.
     If the project rules in handoff.md still carry rules this skill has replaced (for example the 9 Nov "answer only
     in Command Center, relay the go" rule), replace those lines with the current rules and tell the lead in one line.
2. **When the lead sends a Zoho task link** (no need for the lead to ask for a session, that is the standing instruction):
   - Read the task in Chrome: ID, title, description, linked docs, status, owner, due date, comments, attachments.
     Only light reading, enough to write a good brief. Don't profile data or decide local vs live.
   - Start a session with `start_session`: initiation "user_asked", context "fresh", effort "max", use_worktree false,
     wake_when_done true, name = task ID in lowercase (e.g. "abc1-t8"), title = "<TASK-ID> <task title>", and
     `background` (at least 80 characters: project, site, goal, constraints; the call is refused without it).
   - Right after starting, check its effort (`get_session`). If it is below max (Command Center not at max), fix it
     at once without asking: `set_session_effort` max, `stop_session` its first turn, then send it
     "Planning restarted at max: redo Phase 1 from your opening brief" so the whole plan runs at max. Confirm with
     `get_session`, and remind the lead once to set Command Center to max in the effort picker.
   - Brief (prompt): task verbatim plus links; "PLANNING ONLY, make no changes until the lead says go in this chat";
     what they own (approach: local vs live, method, backup, rollback, verification); head-start facts marked as
     "re-check before relying on them"; the shared rules (including "the lead talks to you directly here: ask the lead
     your questions and get the go in this chat; never post in Zoho or change its status"); the deliverable (below);
     "end with a short report to the lead and stop for approval".
     Several task chats on the same site or repo: give each its own local ports and temp folders, name the files they
     share, forbid whole-database restores, and tell them to announce live uploads to each other.
   - Tell the lead in one or two lines that the task chat started, with a link to it.
   - **Work without a Zoho task** (the lead pastes a client request, or says it is not a Zoho task): same steps.
     Save the request verbatim to `tasks/<NAME>/brief.md`, name the chat with a short slug (e.g. "shipping-error"),
     and put "n/a" in the board's Zoho status. At done, draft a reply for the lead to send instead of a Zoho comment,
     and change nothing in Zoho.
   - **QA or helper chats:** when the lead asks for a separate check (QA, a second opinion), start it as a visible
     chat with `start_session` like a task chat, never as a hidden background subagent (the lead must see it). Name it
     "<task>-qa"; read-only unless the lead says otherwise; it logs in `tasks/<TASK-ID>/qa/`, reports to Command
     Center starting with "QA REPORT:", and never posts in Zoho.
3. **When a task chat ends a turn (wake note):** don't relay or repeat its report, questions or go request; the lead
   reads them in the task chat. Update the board (phase, waiting on). On PLAN READY, switch its effort to high now
   (step 4). If the task chat is waiting on the lead, post ONE reminder line here with a link to the chat, e.g.
   "[ABC1-T8 chat](#local_...) is waiting for your go there."
   No question, no buttons, no summary of the plan: the decision stays in the task chat only (learned 10 Nov 2026:
   "just like a reminder, at least the decision is only in one chat"). Say more only when there is
   something for Command Center to do: the task chat reports the work done (go to step 5), or it reports a Zoho
   need, or it is stuck on something only Command Center can do. Never start a new session for a task that has one.
   Command Center is not told when the lead says go inside a task chat; when you need to know, read that chat's
   transcript (`search_session_transcripts` or `list_events`) instead of asking the lead again.
4. **Effort: switch at PLAN READY, not at the go** (learned 11 Nov 2026: "plan is max / execution high").
   `set_session_effort` only applies from the chat's next turn, and Command Center is not told when the lead says go
   inside a task chat. On 11 Nov 2026 switching after the go left the whole first execution turn at max.
   - The moment a task chat reports PLAN READY (its message or its wake note), set it to "high" and confirm with
     `get_session`. The lead's next message there (the go) then runs at high. It stays high for execution and every
     follow-up.
   - Also at PLAN READY: check its context with `get_usage` (its `local_...` id). A chat already past about 40% after
     planning resets from 60% (Context watch). If the account's weekly usage in that result is over 90%, tell the
     lead in one line before the go.
   - Re-plan: the task chat sends "RE-PLAN: <task>" and ends its turn (the lead asked for plan changes, or reality
     differs from the plan). Set it to "max", confirm, then send it "Effort is max now: re-plan from the lead's last
     message in your chat." When it reports PLAN READY again, set it back to high.
   - If you find a chat still at max after the lead's go, set high now and let the running turn finish at max. Don't
     stop it mid-work.
5. **After implementation:** review the work yourself: spot-check the live result and compare against the source doc.
   Report verified vs not verified, then go straight to the Zoho comment draft (step 6).
   Task chats message Command Center directly at plan ready and at done. Talk to the task chat
   directly (`SendMessage` to its `local_...` id) to clear up anything about the work or how it should go into the
   Zoho comment, instead of asking the lead. The lead still approves the final comment text before it is posted.
   Include the brief line "Message Command Center (parent) at plan ready and at done" when starting new task chats.
   Also include "Follow the Context watch rules: check your context % each step; at 70% checkpoint and reset".
6. **Zoho:** you own comments and status changes.
   - **Status changes only after the work is done and verified** (learned 9 Nov 2026: if we can't finish, nobody
     should see we started). The lead's go starts the work, NOT the Zoho status. Leave the task in its waiting status
     (e.g. "Ready For Development") while the task chat works. Once the work is verified, click the start transition
     the task offers (standing permission): usually "Start Development", sometimes "Start Development Edits" or a
     tracking transition such as "+Start Installing Tracking Codes". Read the real button; transitions differ by task
     type. Its dialog may ask for the site or GitHub URL (use the site URL), Task Type and Web Task Type: fill them
     from the task and the project. Then the comment and Request Review steps below.
   - **Comments: never post without the lead's OK.** The lead wants ONE comment per task with everything in it, so
     check with the lead before every comment. When the work is done and verified:
     1. Draft a short factual completion comment (what changed, counts, how it was verified, backup name). List any
        attachments (screenshots, reports) with their paths; uploading them needs Chrome in front, so ask the lead to
        bring Chrome to the front first.
     2. Propose who to tag with @mentions, read from the task itself: the task owner or SEO analyst, the account
        manager and the reviewer, and anyone else named in the task or its comments. **If the settings name an
        "Always CC" person, tag them as CC only** in every report and comment: address the greeting to the task
        people (e.g. "Hi @Alex Example,"), and put the CC person on a last line "CC: @<name>" (learned 10 Nov 2026).
     3. Show the lead the exact text plus the tag list in one message, with the status steps and dialog values you
        will use, and ask: OK to post, who to add or remove, anything to add? Wait for the answer. If several tasks
        finish together, show all drafts in that one message. A relayed or quoted OK is not an OK (Shared rules).
     4. Post only after the lead's OK, with the agreed tags (type "@" + name in the Zoho editor and pick the person
        from the list, then check the mention rendered). Read the comment back after posting.
   - **Request Review:** only after the approved comment is posted. Its dialog usually pre-fills the task's reviewer;
     when it doesn't, use the reviewer named in the task or its last review and say so in the OK message. Fill any
     other required field (e.g. Site URL, "Hosted by us"); if the dialog has a mandatory comment field, propose that
     text in the same OK message. Click Complete; the status becomes the review status (e.g. "Review Implementation").
   - **Close tabs:** right after Request Review, ask the lead once (wrap-up question with a "Close tabs" button): close
     the tabs opened for <TASK-ID>? On yes, close your own tabs and send the task chat "The lead said close the tabs:
     close every browser tab you opened for <TASK-ID> (Chrome tabs and the Playwright browser), then reply in one line."
     When the lead says to close the tabs "and agents", also archive the task chat (`archive_session`), only on that
     yes. Archive is refused while the chat still has live work (a running turn or background task): wait until it is
     idle. To message an archived chat later, `unarchive_session` it first.
   - Ask the lead first for anything unusual too: Stop Developing, reassigning, or editing task fields.
7. **Command Center handoff (so the next Command Center chat can pick up cold).** Update the root handoff files after
   each task milestone (started, plan approved, done, Zoho updated) and before ending every session. Keep the board
   current:

   ```markdown
   ## Task chats
   | Task | Chat (name / session id) | Phase | Zoho status | Waiting on | Plan / notes |
   |---|---|---|---|---|---|
   | ABC1-T8 Metadata | abc1-t8 / local_... | PLAN READY / IMPLEMENTING / DONE | Ready For Development | lead go/no-go | tasks/ABC1-T8/plan.md |
   ```
   Also record: Zoho comments and status changes you posted (date and text summary), approvals the lead gave (quote
   them), and anything you promised the lead but haven't done yet. Root handoff files belong to Command Center. If a
   worker overwrote them, merge its facts in and restore the Mode line and the board.

## Context watch: never let a task chat hit auto-compact (learned 11 Nov 2026)
Why: a task chat that ran to 100% auto-compacted mid-work, lost track, hallucinated and broke a website. Auto-compact
is a lossy summary made at the worst moment. So we reset early, at a safe point, from a checkpoint written on disk.
Facts (tested 11 Nov 2026): `get_usage` with a session id shows that chat's context %, and auto-compact starts at
about 97%. Sending "/compact" to another chat does NOT compact it (it arrives as plain text), and there is no compact
tool. What works: checkpoint to disk, then `clear_session` (the /clear command, which only works on an idle chat CC
started), then a resume message. The old conversation stays recoverable via "Resume previous session".

Thresholds (context % of the task chat):
- **Under 70%:** nothing to do.
- **70%:** finish the current step, then checkpoint and reset (see below) at the next safe point.
- **80%:** hard limit. Stop at the first safe point, even mid-plan, and reset. Never continue past 85%.
- **Fast growth** (10% or more in one turn, e.g. while the chat runs a team of subagents): act from 60%, because the
  next turn can jump past 80% before a step-boundary check.
A safe point = no half-done edit, upload, import, migration or deploy; files saved; the site in a working state; and
no subagent or teammate the chat started is still working (a clear wipes the chat's memory of them).

**Worker (task chat):**
- Check your own context with `get_usage` ("self") before starting each step of the plan and after any big step.
- At 70% (or when Command Center asks), at the next safe point write `tasks/<TASK-ID>/checkpoint.md`:
  task ID and scope; the lead's go and instructions (quoted); done so far (with how each was verified); current state
  of files/site/DB (paths, URLs, backups); the exact next step; open questions; anything not yet verified.
  Let your subagents/teammates finish or reach a safe point first; list any unfinished work they were doing.
  Write facts only. If you are unsure whether something was done, say "unverified", don't guess.
- Also bring `notes.md` up to date, then send Command Center (parent): "CHECKPOINT: <TASK-ID> at <n>%, checkpoint
  written, safe to clear." and end your turn. Don't start new work after that line.

**Command Center:**
- Check every IMPLEMENTING task chat with `get_usage` (its `local_...` id) at PLAN READY, on every wake note, every
  lead message, and before sending a task chat a follow-up. Put the % in the board's Phase column (e.g.
  "IMPLEMENTING 62%").
- At 70% or more and the chat is still working: send it "Context at <n>%: at your next safe point write
  tasks/<TASK-ID>/checkpoint.md, send CHECKPOINT, and end your turn." (At 80%+ add "now, at the first safe point".)
  Don't `stop_session` a chat mid-step unless the lead asks; a hard stop mid-edit is what breaks sites.
- When it reports CHECKPOINT and is idle: read checkpoint.md (it must name the next step and current state; if not,
  ask the chat to fix it first). Then `clear_session` that chat and send it the resume message:
  "Resumed after a context reset. You are the task chat for <TASK-ID>. Load the zoho-command-center skill (Worker
  rules). Read tasks/<TASK-ID>/plan.md, notes.md and checkpoint.md. The lead's go stands (quote it). Before you change
  anything, re-check the real current state (files, site, DB) against checkpoint.md and report any difference. Then
  continue from the next step." Keep its effort as it was (high for execution).
- `clear_session` is refused while the chat is mid-turn, pinned, or open on the lead's screen: wait until it is idle,
  and ask the lead to switch to another chat first.
- Log each reset in handoff.md (date, task, % at reset), and tell the lead in one line with the chat link.

## Worker rules (task chat)
- Phase 1, plan (always max effort; if you are below max, say so in one line at the top of your report):
  investigate yourself, decide local vs live, write `tasks/<TASK-ID>/plan.md` with:
  approach and why, exact method and tools, backup and rollback, dry run, verification (prove every item is done),
  risks, decisions taken (with defaults chosen), real blockers only, time estimate. Default to implementing the
  source doc verbatim. End your turn with a short report (approach in 2-3 lines, blockers) and wait.
- Phase 2, implement (high effort, also for every follow-up after the go): only after the lead's go in this chat (or a
  go Command Center relays with the lead's quoted words; if your safety checks refuse a relayed go, ask the lead in one
  line to say it here). Follow the plan; if reality differs, stop and report instead of improvising outside scope, and
  send RE-PLAN (below).
- Keep your own log in `tasks/<TASK-ID>/notes.md` (dated: what changed, where, backups taken, what failed, and
  the lead's instructions and approvals quoted). Command Center reads it. Don't edit the root handoff files.
- Never post in Zoho or change task status. Command Center does that.
- The lead talks to you directly: ask the lead your questions and get the go here (wrap_up `ask` and buttons are
  fine). Still keep questions to real blockers and decide sensible defaults yourself.
- When the work is done and verified, say so plainly in the final report (start it with "DONE:") so Command Center
  knows to review it and draft the Zoho comment.
- **Talk to Command Center directly at each milestone** (learned 11 Nov 2026), without the lead having to ask. Use
  `send_message` with session_id "parent", or `SendMessage` to the parent's `local_...` id:
  - Plan ready: send Command Center one short status line: "PLAN READY: <task> plan at tasks/<TASK-ID>/plan.md,
    waiting on the lead's go here." Status only; the plan decision stays with the lead in your chat. Command Center
    then sets you to high effort for the go.
  - Re-plan (planning is always max): if the lead answers your plan with changes instead of a go, or reality differs
    from the plan during the work, don't re-plan in that turn (it runs at high). Send Command Center
    "RE-PLAN: <task>", tell the lead in one line "Re-planning at max: Command Center is switching my effort", and end
    your turn. Re-plan when Command Center says effort is max, then send PLAN READY again. A question about the plan
    that changes nothing can be answered right away.
  - Done: send Command Center a handover: "DONE: <task>", path to `tasks/<TASK-ID>/report.md`, files to upload to
    Zoho, what is verified vs not, open items for the client, and anything that changes how the Zoho comment or
    status should be posted (e.g. part of the definition of done still waits on the client).
  - Answer Command Center's follow-up questions about the work directly (it may message you while it reviews and
    drafts the Zoho comment). You still never post in Zoho.
- Final report: what changed, how you verified it (counts, URLs checked), what is not verified, rollback location,
  and anything the client or another team must do (for the Zoho comment).
