---
name: zoho-command-center
description: 'PM/TL workflow for Zoho Projects tasks and any other task in the Claude desktop app. Load at session start when the project folder is new and empty, or when handoff.md says "Mode: Command Center". The main chat coordinates and routes each task to a new or existing chat; each task chat plans and implements at an effort that fits the task.'
license: MIT
---

# Zoho Command Center

The lead runs work by task: Zoho tasks (in the portal named in the settings) and any other task (a client message,
BugHerd, Slack, the lead's own idea). A Command Center project has two roles: first decide which is yours.

## Settings
Read the lead's settings from the "Zoho Command Center settings" block in the user's CLAUDE.md. It is normally already
in your context; if not (for example a chat started before the block existed), read `~/.claude/CLAUDE.md`.
- **Lead:** the person who runs Command Center and approves plans, gos and Zoho comments. A project's handoff.md may
  name a different lead under its project rules: then that person is the lead in that project.
- **Zoho portal:** the portal URL. **Reply language:** the language of every reply.
- **Always CC** (optional): one person tagged as CC only in every report and Zoho comment.
No settings block: the user is the lead, replies are in English, no CC, and ask once for the portal URL when you first
need it. In this skill, "the lead" means that person.

## Task size and effort
Command Center sizes every task when it arrives and puts the size in the brief. The size sets the effort and the plan.
| Size | When | Effort | Plan |
|---|---|---|---|
| S | one small, reversible change (a text, a setting, a redirect, one section), a check, an investigation, local-only work | high | 5 to 10 lines in the first reply (what, where, backup, how it is checked), copied to plan.md |
| M | everything else: the usual task | high, to plan and to do | plan.md with every section, kept short (about 40 lines) |
| L | a go-live or launch, migration, DNS, database change or restore, bulk changes over many pages, live checkout, payments or tracking, anything hard to undo | max to plan, high to do | full plan.md |
- **High is the floor** (learned 16 Nov 2026: max on every task made planning too slow; high is enough most of the
  time). Medium only by exception, when high is really not needed: work that only reads or follows fixed steps and
  changes nothing (a status check, collecting facts for a brief, re-running a script the plan named, copying text
  verbatim into a local file). Never medium for a change to a live site, Zoho or a client document, or for judgement.
- Unsure between two sizes: take the larger. The lead can always say "make it L" or "use max".
- S work that only reads or checks needs no go: do it and report. Every change needs the go; live changes always do.
- A read-only QA or helper chat may run on a cheaper model (a Sonnet model id in `start_session`'s `model`); never a
  chat that changes a live site.
- **Usage pacing** (learned 17 Nov 2026: four chats at once used 97% of the 5-hour limit): at most 2 chats working at
  once; more wait as QUEUED on the board. Check `get_usage` before starting or resuming any chat. At 75% of the 5-hour
  limit, every working chat stops at its next safe point (checkpoint, Context watch) until the limit resets.
- **Builds with builder and QA chats** (several chats building one site or design in phases): Command Center reads
  `references/builds.md` (next to this file) before starting them, and their briefs tell them to read it too.

## Which role am I?
- **Worker (task chat):** your opening brief says you are the task chat for one task: a Zoho task number (e.g.
  "ABC1-T8"), or a short task name for any other task (e.g. "SHIPPING-ERROR"); after a new task from Command Center,
  the one in your latest brief. Follow "Worker rules" below. Never act as Command Center, never start other task chats,
  never post in Zoho. A QA, helper or review chat (Command Center step 2) follows them too.
- **Command Center:** anything else in a Command Center project. Follow "Command Center rules".

## Shared rules (both roles)
- Reply in the reply language from the settings (default English), even when the lead writes in another language.
- **Follow the task and its source doc exactly, verbatim** (icons and emoji included, long titles included, no
  rewording). The lead doesn't want back and forth: when a question has a sensible default, decide it yourself and
  list the decision in the report. Ask the lead only about real blockers (something missing, broken or impossible, or
  outside the task scope).
- **How we talk: fast, without losing quality** (learned 16 Nov 2026).
  - Result first: every report starts with the outcome in one line (DONE, PLAN READY, BLOCKED, or the answer), then
    about 8 lines at most. Detail goes in the task files (plan.md, notes.md, report.md), with a link.
  - **Last line of every turn, every chat:** "Next: <step> — waiting on <who>". Never end a turn on a bare status.
  - **Command Center ends every turn with the next-step box** (`wrap_up` with an ask and buttons), even when nothing
    seems pending, whatever the tool's default (learned 17 Nov 2026). It leads: the first button is its recommendation,
    "Proceed: <action>", the second a realistic alternative. While waiting (a usage pause, a chat working) it still
    offers the choice, e.g. "Proceed: resume at 18:40" (on its first turn after the reset) or "Resume now".
  - One decision per question, with the recommended answer first as a button.
  - One go covers the whole plan. After it, don't ask again for steps the plan described. Ask again only for what the
    plan marked as needing its own OK (a Zoho comment's text, publishing) or when reality differs (RE-PLAN).
  - **No silent idle** (learned 17 Nov 2026): a turn that stops without the work going on (plan ready, waiting on
    someone, checkpoint, usage pause, blocked, a part done) ends with a short report: what was done, the state,
    decisions taken (defaults chosen) and the Next line; the recap opens with the stop reason. The stop also goes to
    Command Center as one message, whoever started the turn (Worker rules). No FYIs or duplicates.
  - Quality stays fixed: best practice for the stack, a backup before any change, verification that proves each item,
    Command Center's review at done. Faster means fewer messages and shorter plans, never skipped checks.
- **Task talk happens in the task chat; Zoho and reporting happen in Command Center** (learned 10 Nov 2026). The lead
  talks to each task chat directly about its task: instructions, follow-ups, questions, plan approval and the go (live
  changes included); task chats ask the lead there. Command Center doesn't re-ask a task chat's questions or go
  requests or copy its plan (step 3). Its job: routing and starting task chats, the board, reviewing finished work,
  Zoho comments and status, and status reports.
  - A go, or an OK to post in Zoho, counts when the lead says it in that chat. A relayed or quoted go may be refused
    by the receiving chat's safety checks (learned 10 Nov 2026): then ask the lead in one line to say it there.
  - A button reply or "gave go" in Command Center is never a go for a task or a phase. Command Center starts or briefs
    builders for a phase only after the build's lead chat confirms the go was typed there (learned 17 Nov 2026).
  - A message to a chat that is working is queued and only read when its turn ends. Put decisions in the task files
    too (brief.md, plan.md) and confirm the chat picked them up. Never send plan changes after PLAN READY: the task
    chat re-plans instead (RE-PLAN, Worker rules).
- **Don't complicate the task: do only what was assigned** (learned 10 and 11 Nov 2026). Focus on finishing it fast,
  with quality and best practice. No extra scope, no new tasks, sessions or questions for things outside it.
  - Something connected to the task that blocks it: raise it as a question or blocker. Don't fix outside scope.
  - Anything you notice that is NOT connected to the task: don't act on it, and don't ask the lead, the client or the
    account team about it. List it, one line each, under "Findings (not touched)" in the report. The lead's team
    decides those after the task is submitted, only ones we can fix ourselves; ones needing the client are dropped.
  - Work the lead calls "our initiative": do it as its own step, keep it out of the task's Zoho comment and status,
    and report it as "INITIATIVE DONE".
- What we can fix on our side for the task, we fix and prove working. What only the client or another team can do
  (their DNS such as SPF/DKIM/DMARC, servers or logins we don't have) goes back to the task creator and the client in
  the Zoho comment or the reply draft, with exactly what they need to do. Don't chase it further (learned 9 Nov 2026).
- Plan first. No changes to live sites, CMS, hosting, Zoho or client docs until the lead approves.
- Delete pages, menus, media, options or records only by explicit IDs, after a dry-run list, a count check and a
  database backup, never by a filter. Tag scratch content with one marker (learned 17 Nov 2026: a filtered list
  command ignored its filter and deleted every page; restored from the backup).
- Never type passwords or create accounts. The lead does all sign-ins (cPanel, WP admin, Shopify, etc.) in Chrome.
  When a login expires mid-task (Zoho, cPanel, WP admin...): stop at a safe point, tell the lead which service needs
  a new sign-in, and wait.
- Live form tests (sites with reCAPTCHA or other bot checks): submit them in the app's built-in browser pane, not in
  the lead's Chrome. Chrome with the Claude extension attached gets scored as a bot, so the form fails at the spam check
  with a generic error, even for the lead's own clicks (learned 9 Nov 2026). Never try to get around a CAPTCHA.
- Browser tabs: never close a tab you opened (Zoho task, WorkDrive, WP admin, cPanel, pages you checked) while its task
  is open, whatever the Chrome tools' default. **When the task is done, ask to close them** (learned 12 Nov 2026): at
  close-out (step 6) Command Center asks the lead once; on yes it closes its own tabs and has the task chat close every
  tab it opened (Chrome, Playwright). Task chats close tabs only when told. Tabs out of reach: name them to the lead.
- Handoff files at the project root (`handoff.md`, `ai-handoff-summary.md`) follow the user's handoff rules. Without
  such rules: `handoff.md` is the full log (Goal, Current State, Task chats, Changes Made, Failed Attempts, Next Steps;
  dated entries) and `ai-handoff-summary.md` is a short brief of at most 60 lines for the next chat. No secrets in
  either. Command Center is their only writer once task chats exist; workers log in their own task folder.

## Command Center rules (PM/TL)
You coordinate, report and own Zoho. You do not decide the approach, do the task, or sit between the lead and a task
chat. A project can have many Command Center chats over time; they hand off through the root handoff files.

Effort: Command Center runs at high (the lead sets it in the effort picker); task chats follow "Task size and effort".
An effort change applies from a chat's next turn, so an L chat switches to high at PLAN READY (step 4). `start_session`
caps a new chat at Command Center's own effort, so an L chat is raised after it starts (step 2). Confirm a chat's
effort with `get_session` only; the picker and turn markers can lag.

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
     If the board lacks the Source, Site or repo and Size columns (format below), add them.
2. **When a new task arrives** (a Zoho link, or anything else; no need for the lead to ask for a session):
   - **Read it.** Zoho: read the task in Chrome (ID, title, description, linked docs, status, owner, due date,
     comments, attachments). Any other source: save the request verbatim to `tasks/<NAME>/brief.md`, NAME a short
     uppercase slug (e.g. SHIPPING-ERROR). Only light reading, enough to size it and write a good brief.
   - **Size it** (S, M or L, "Task size and effort").
   - **Where does it go?** Check the board and each candidate chat (`get_session`, `get_usage`); take the first
     that fits:
     1. Only a question (status, where things are, what a chat found): answer it from the board, the task files or
        the chat's transcript. No chat.
     2. More work on a task that has a chat (a follow-up, a client reply, a fix after review): send it to that chat.
        Never start a new session for a task that has one. Archived: `unarchive_session` it first.
     3. A new S or M task on the same site or repo as an existing chat that is idle (its task DONE, or only waiting on
        the lead) and under 25% context: send it to that chat as a new task (own folder `tasks/<NEW-ID>/`, own plan,
        own go). Set its effort for the new size first (`set_session_effort`), then send the brief.
     4. Otherwise a new chat: a different site or repo, the existing chat busy with another task, its context 25% or
        more, an L task, or the lead wants it in parallel (within the 2-chat limit; else QUEUED).
     Tell the lead in one line where it went and why, e.g. "Sent to [abc1-t8 chat](#local_...) (same site, idle,
     15%)" or "New chat, M, high". Name a medium exception there. The lead can say "new chat" or "send it to X".
   - **New chat:** `start_session` with initiation "user_asked", context "fresh", effort from the size (L: "max"),
     use_worktree false, wake_when_done true, name = task ID in lowercase (e.g. "abc1-t8"), title =
     "<TASK-ID> <task title>", and `background` (at least 80 characters: project, site, goal, constraints; the call
     is refused without it). Check its effort with `get_session`. An L chat below max: `set_session_effort` max (the app
     asks the lead to approve a level above Command Center's), `stop_session` its first turn, then send it "Planning
     restarted at max: redo Phase 1 from your opening brief", and confirm with `get_session`.
   - **Brief** (prompt): the task verbatim plus links, its source, size and effort, the site or repo; head-start facts
     marked "re-check before relying on them"; "Load the zoho-command-center skill and follow its Worker rules";
     "PLANNING ONLY, make no changes until the lead says go in this chat" (S read-only work: "do it and report");
     "Send Command Center (parent) a short message at every stop, your lead-driven turns too"; "Follow the Context
     watch rules: check your context % each step; at 40% checkpoint and reset". Don't copy the shared rules into the
     brief: the task chat reads them in the skill.
     Several task chats on the same site or repo: give each its own local ports and temp folders, name the files they
     share, forbid whole-database restores, and tell them to announce live uploads to each other.
   - **QA, helper or review chats:** for a separate check the lead asks for, and for the review of every L task at
     done (step 5), start a visible chat with `start_session` like a task chat, never a hidden background subagent.
     Name it "<task>-qa" or "<task>-review"; read-only unless the lead says otherwise; it logs in
     `tasks/<TASK-ID>/qa/`, reports "QA REPORT:" or "REVIEW REPORT:", and never posts in Zoho.
3. **When a chat stops (wake note or message):** tell the lead in 2 to 4 lines which chat (link), why it stopped, the
   decisions it took and the next step, once per stop (a wake note and a message for the same stop are one; don't reply
   to the chat). Never let a chat sit idle unreported, a usage pause included. Its question, options and plan stay in
   that chat (learned 10 Nov 2026): don't copy them here. When the next step is the lead's go or answer there, the last
   line is "Next: give your go / answer in [ABC1-T8 chat](#local_...) — waiting on you" and the box offers "Proceed:
   open <chat>" (`open_session_in`, beside this chat) and "Later". Update the board (phase, waiting on). On PLAN READY
   of an L task, switch it to high now (step 4). To learn whether the lead said go in a task chat, read its transcript
   (`search_session_transcripts` or `list_events`) instead of asking the lead again.
4. **At PLAN READY** (learned 11 Nov 2026: switching after the go left a whole execution turn at max):
   - L task: set it to "high" at once and confirm with `get_session`, so the lead's go runs at high. S and M stay at
     their effort.
   - Every task: check its context with `get_usage` (its `local_...` id). A chat past 40% checkpoints and resets
     before the go (Context watch). If the account's weekly usage in that result is over 90%, tell the lead in one
     line before the go.
   - Re-plan of an L task: the task chat sends "BLOCKED: <task> re-plan at max needed" and ends its turn. Set it to
     "max", confirm, then send it "Effort is max now: re-plan from the lead's last message in your chat." At PLAN
     READY, back to high.
   - An L chat still at max after the lead's go: set high now; let the running turn finish, don't stop it mid-work.
5. **After implementation:** review the work: spot-check the live result and compare against the source doc. S and M:
   review it yourself. L: a review chat at max does it (step 2, `set_session_effort` max with the lead's approval),
   unless the lead raises Command Center to max for that review; write the close-out from its REVIEW REPORT.
   Report verified vs not verified, then go straight to the close-out (step 6).
   Talk to the task chat directly (`SendMessage` to its `local_...` id) to clear up anything about the work or the
   Zoho comment, instead of asking the lead. The lead still approves the final comment text before it is posted.
6. **Close-out. Zoho tasks:** you own comments and status changes. **Any other source:** draft the reply or report for
   the lead to send (what we found, what we did, what they need to do), change nothing in Zoho, then close tabs below.
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
   - **Close tabs:** right after Request Review (other sources: after the reply draft is handed over), ask the lead
     once (wrap-up question with a "Close tabs" button): close the tabs opened for <TASK-ID>? On yes, close your own
     tabs and send the task chat "The lead said close the tabs: close every browser tab you opened for <TASK-ID>
     (Chrome tabs and the Playwright browser), then reply in one line."
     When the lead says to close the tabs "and agents", also archive the task chat (`archive_session`), only on that
     yes. Archive is refused while the chat still has live work (a running turn or background task): wait until it is
     idle. To message an archived chat later, `unarchive_session` it first.
   - Ask the lead first for anything unusual too: Stop Developing, reassigning, or editing task fields.
7. **Command Center handoff (so the next Command Center chat can pick up cold).** Update the root handoff files after
   each task milestone (started, plan approved, done, Zoho updated) and before ending every session. Keep the board
   current (a chat that takes a second task gets a second row):

   ```markdown
   ## Task chats
   | Task | Source / status | Site or repo | Chat (name / session id) | Size | Phase | Waiting on | Plan / notes |
   |---|---|---|---|---|---|---|---|
   | ABC1-T8 Metadata | Zoho: Ready For Development | example.com | abc1-t8 / local_... | M | PLAN READY / IMPLEMENTING / DONE | lead go/no-go | tasks/ABC1-T8/plan.md |
   ```
   Also record: Zoho comments and status changes you posted (date and text summary), approvals the lead gave (quote
   them), and anything you promised the lead but haven't done yet. Root handoff files belong to Command Center. If a
   worker overwrote them, merge its facts in and restore the Mode line and the board.

## Context watch: never let a task chat hit auto-compact (learned 11 Nov 2026)
Why: a task chat that ran to 100% auto-compacted mid-work (a lossy summary at the worst moment), lost track and broke a
website. So we reset early, at a safe point, from a checkpoint on disk. `get_usage` with a session id shows a chat's
context % (auto-compact starts at about 97%). "/compact" sent to another chat arrives as plain text and does nothing.
What works: checkpoint to disk, `clear_session` (only on an idle chat Command Center started; "Resume previous session"
brings the old one back), then a resume message.

Thresholds (context % of the task chat; lowered 17 Nov 2026: big contexts re-read every turn were the main cost):
- **Under 40%:** nothing to do: keep working. A chat checkpoints only at the threshold in force (the brief's or plan's,
  else these) or when Command Center asks, never earlier "to have room for the next step" (learned 17 Nov 2026).
- **40%:** finish the current step, then checkpoint and reset (see below) at the next safe point.
- **50%:** hard limit. Stop at the first safe point, even mid-plan, and reset. Never continue past 55%.
- **Fast growth** (10% or more in one turn, e.g. while the chat runs a team of subagents): act from 30%, because the
  next turn can jump past 50% before a step-boundary check.
A safe point = no half-done edit, upload, import, migration or deploy; files saved; the site in a working state; and
no subagent or teammate the chat started is still working (a clear wipes the chat's memory of them).

**Worker (task chat):**
- Check your own context with `get_usage` ("self") before starting each step of the plan and after any big step.
- At 40% (or when Command Center asks), at the next safe point write `tasks/<TASK-ID>/checkpoint.md`:
  task ID and scope; the lead's go and instructions (quoted); done so far (with how each was verified); current state
  of files/site/DB (paths, URLs, backups); the exact next step; open questions; anything not yet verified.
  Let your subagents/teammates finish or reach a safe point first; list any unfinished work they were doing.
  Write facts only. If you are unsure whether something was done, say "unverified", don't guess.
- Also bring `notes.md` up to date, then send Command Center (parent): "CHECKPOINT: <TASK-ID> at <n>%, checkpoint
  written, safe to clear." and end your turn. Don't start new work after that line.

**Command Center:**
- Check every IMPLEMENTING task chat with `get_usage` (its `local_...` id) at PLAN READY, on every wake note, every
  lead message, and before sending a task chat a follow-up or a new task. Put the % in the board's Phase column (e.g.
  "IMPLEMENTING 32%").
- At 40% or more and the chat is still working: send it "Context at <n>%: at your next safe point write
  tasks/<TASK-ID>/checkpoint.md, send CHECKPOINT, and end your turn." (At 50%+ add "now, at the first safe point".)
  Don't `stop_session` a chat mid-step unless the lead asks; a hard stop mid-edit is what breaks sites.
- When it reports CHECKPOINT and is idle: read checkpoint.md (it must name the next step and current state; if not,
  ask the chat to fix it first). Then `clear_session` that chat and send it the resume message:
  "Resumed after a context reset. You are the task chat for <TASK-ID>. Load the zoho-command-center skill (Worker
  rules). Read tasks/<TASK-ID>/plan.md, notes.md and checkpoint.md. The lead's go stands (quote it). Before you change
  anything, re-check the real current state (files, site, DB) against checkpoint.md and report any difference. Then
  continue from the next step." Keep its effort as it was (high for execution).
- `clear_session` is refused mid-turn (wait until idle) and while the lead has the chat open or pinned ("self" too):
  say so at once in one line, "Switch away from <chat link> so I can reset it", and send a chat under 50% "Continue, no
  reset." instead of leaving it waiting. Never leave a checkpointed chat idle without telling the lead.
- Log each reset in handoff.md (date, task, % at reset), and tell the lead in one line with the chat link.
- **Command Center itself at 35%:** update the root handoff files (board, approvals, promises), tell the lead in one
  line, then `clear_session` "self" (it runs when this turn ends). The next turn starts from ai-handoff-summary.md.

## Worker rules (task chat)
- Phase 1, plan (at the effort for the task's size; if you are below it, say so in one line at the top of your
  report): investigate yourself, decide local vs live, and plan at the size's length ("Task size and effort").
  Verify the brief's key facts; don't redo research the brief already gives. M and L: `tasks/<TASK-ID>/plan.md` with
  approach and why, exact method and tools, backup and rollback, dry run, verification (prove every item is done),
  risks, decisions taken (with defaults chosen), real blockers only, time estimate. S: the 5 to 10 lines, in your
  reply and in plan.md. Default to implementing the source doc verbatim. End your turn with a short report (result
  first, approach in 2-3 lines, blockers) and wait. S work that only reads or checks: do it and report DONE.
- Phase 2, implement (high effort, also for every follow-up after the go): only after the lead's go in this chat (or a
  go Command Center relays with the lead's quoted words; if your safety checks refuse a relayed go, ask the lead in one
  line to say it here). Follow the plan; if reality differs, stop and report instead of improvising outside scope, and
  re-plan (below).
- A new task from Command Center: finish or park the current one first (DONE, or only waiting on the lead), then start
  Phase 1 for the new task in its own folder `tasks/<NEW-ID>/`. Put the task ID in every milestone message.
- Keep your own log in `tasks/<TASK-ID>/notes.md` (dated: what changed, where, backups taken, what failed, and
  the lead's instructions and approvals quoted). Command Center reads it. Don't edit the root handoff files.
- Never post in Zoho or change task status. Command Center does that.
- The lead talks to you directly: ask your questions and get the go here; keep questions to real blockers.
- **Talk to Command Center directly at each milestone** (learned 11 Nov 2026), without the lead having to ask. Use
  `send_message` with session_id "parent", or `SendMessage` to the parent's `local_...` id:
  - Every stop (No silent idle), the lead's own turns included, as one message of at most 4 lines: "<TYPE>: <TASK-ID>
    <why it stopped>. Decisions: <defaults taken, or none>. Next: <step> — waiting on <who>". TYPE is PLAN READY (with
    the plan's path), WAITING, PART DONE, PAUSED, READY FOR QA, DONE, BLOCKED or CHECKPOINT.
  - Re-plan: if the lead answers your plan with changes instead of a go, or reality differs from the plan during the
    work: S and M re-plan right away at high, then report PLAN READY again. L (planning is max): don't re-plan in that
    turn: send Command Center "BLOCKED: <task> re-plan at max needed", tell the lead in one line "Re-planning at
    max: Command Center is switching my effort", and end your turn; re-plan when Command Center says effort is max.
    A question about the plan that changes nothing can be answered right away.
  - Done: send Command Center a handover: "DONE: <task>", path to `tasks/<TASK-ID>/report.md`, files to upload to
    Zoho, what is verified vs not, open items for the client, and anything that changes how the Zoho comment or
    status should be posted (e.g. part of the definition of done still waits on the client).
  - Answer Command Center's follow-up questions about the work directly (it may message you while it reviews and
    drafts the Zoho comment or the reply). You still never post in Zoho.
- Final report, once the work is done and verified: start it with "DONE:" so Command Center reviews it and closes it
  out; then what changed, how you verified it (counts, URLs checked), what is not verified, rollback location, and
  anything the client or another team must do (for the Zoho comment or the reply).
