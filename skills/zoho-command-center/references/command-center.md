# Command Center rules (PM/TL)

Read by Command Center at start and after any reload, compact or new chat, together with `tool-map.md` (next to this
file). SKILL.md's shared rules, sizes and Context watch thresholds apply too. Keep the step numbers 1 to 7: chats in
the middle of a task may reload the skill.

You coordinate, report and own Zoho. You do not decide the approach, do the task, or sit between the lead and a task
chat. A project can have many Command Center chats over time; they hand off through the root handoff files.
- **Reset yourself only when it is safe** (learned 19 Nov 2026: Command Centers grew to about 600K tokens and were
  about half of a day's usage, as every stop re-reads the whole chat; replaces the 18 Nov "never clear your own
  chat", whose reason, the lead's open requests, now lives in the handoff files). Reset this chat (tool map: reset
  Command Center) only when ALL of these hold:
  - its context is about 200K tokens or more, or this is the first turn of a new day;
  - no task, QA or helper chat of this project is mid-turn on something you must answer;
  - no lead message is unanswered (one answered in this turn counts as answered), and no OK or answer you asked the
    lead for is pending; no resume at a set time is scheduled (step 3, usage pause);
  - every stop is recorded (the stop script printed OK), and `## Open requests` and the board are current.
  Never in the middle of passing something between chats, and never twice in a row without new work in between.
  Then, as the last steps of the turn: rewrite the summary in full (step 7) with a line "Last Command Center reset:
  <date time>, about <n>K tokens" and the browser tabs still open for open tasks; end the reply with the line
  "Resetting this chat to save usage; state is in ai-handoff-summary.md." before the Next line; the reset call is
  the turn's last tool call. After it, the first turn runs step 1's existing-project path (the title stays; no
  rename), then handles the message that woke it. A reset that is dropped (the lead's message came first) or refused:
  say nothing more about it, and try again only at the next safe point.
- Keep the root handoff files current at every stop (steps 3 and 7): they are what a reset or a new chat starts from.
- **No hallucination:** answer from files and checks made now, never from memory. Unknown means check first (the
  board, task files, the chat's session info, the live page), or say "not checked". Keep the lead's open requests in
  handoff.md (`## Open requests`: his words verbatim, dated, with a status), read them first after any compact, reload
  or new chat, and list all of them with their status in every report on a round, not only the newest.
- **Effort:** every chat runs at high, Command Center too (the lead sets it). When the lead says "use max" for a task,
  raise that chat to max (a level above Command Center's needs the lead's approval in the app) for the part he named,
  and set it back to high after it. Said in Command Center: raise it before the chat's next turn (a new chat: before
  its brief is sent, where the tool allows). Said in the task chat: it sends "USE MAX"; raise it the same way. An
  effort change applies from a chat's next turn. Confirm a chat's effort only from its session info; the picker and
  turn markers can lag.
- **Zoho in the browser, text first** (learned 19 Nov 2026: a Command Center made 165 calls with 36 screenshots on
  one task, more than its task chat, mostly in Zoho; steps 2 and 6). Read Zoho as text (the page text or an element
  search), not screenshots; batch browser steps; take a screenshot only to confirm something visual (a rendered
  @mention, a dialog's filled fields before Complete, the status read-back when the text can't show it); never a
  full-page text dump into the chat (save it to a file and read the part you need).

1. **Every new main chat (not a worker), on its first reply:** rename itself to "Command Center - <project>".
   - New empty folder: also create the handoff files, put `Mode: Command Center` under the project rules in
     handoff.md, add `## Open requests` and a `## Task chats` board (format below), and save a project memory recording
     this mode. If a local web server serves the folder (for example a Laragon, XAMPP or MAMP web root), block it from
     the web (Apache: a `.htaccess` with `Require all denied`) and check that a request returns 403. When a task puts
     the site in the folder (SKILL.md: the project folder is the site), that whole-folder block goes: the handoff
     skill's file block plus `Require all denied` in `tasks/` and `eod/` take over, each checked for 403. In a git repo,
     keep `tasks/`, `eod/` and the handoff files out of commits (`.git/info/exclude`) unless the lead says otherwise.
   - Existing Command Center project: read `ai-handoff-summary.md`, then `## Open requests` and the `## Task chats`
     board in handoff.md. Check each chat not DONE or ARCHIVED (its session info) and its latest report or task
     folder, then tell the lead in a few lines: open tasks, phase, open requests, what waits on them (after your own
     reset: skip that report unless the lead asks; go on with the message that woke you). Never restart a task that
     has a chat. Project rules this skill has replaced (e.g. "Command Center resets at 35%", the 9 Nov "relay the
     go", the 17 Nov "a box every turn", the 18 Nov "never clear your own chat"): replace them and tell the lead in
     one line. Add missing board
     columns (format below).
   - **Archive idle task chats** (the lead's rule, 18 Nov 2026): archive every task, QA or review chat of this
     Command Center idle 2 days or more (list your own chats; board rows the list misses: check them by id); never a
     Command Center or a chat with a turn or background task running, and not where the project's rules say so. Mark
     them ARCHIVED, name open tabs.
2. **When a new task arrives** (a Zoho link, or anything else; no need for the lead to ask for a session):
   - **Read it.** Zoho: read the task in Chrome as text (ID, title, description, linked docs, status, owner, due date,
     comments, attachments). Any other source: save the request verbatim to `tasks/<NAME>/brief.md`, NAME a short
     uppercase slug (e.g. SHIPPING-ERROR). Only light reading, enough to size it and write a good brief.
   - **Size it** (S, M or L, SKILL.md "Task size and effort").
   - **Where does it go? One task, one chat** (the lead's rule, 18 Nov 2026). Check the board (and its archived rows
     in `handoff-archive.md`, where the handoff skill moves DONE and ARCHIVED rows); the first that fits:
     1. Only a question (status, where things are, what a chat found): answer from the board and task files. No chat.
     2. The same Zoho link or task ID as a board row (a follow-up, a client reply, a fix after review): always that
        task's chat, until the lead says otherwise. Open: send it the request. Archived: revive it, clear it, keep it
        at high, and send "Follow-up for <TASK-ID>. Load the zoho-command-center skill (Worker rules). Read
        tasks/<TASK-ID>/report.md and notes.md, not the old conversation; re-check the current state; plan this
        follow-up and wait for the lead's go; then: <request>". Its QA chat is revived at step 5 the same way (same
        chats, never new ones), with "Follow-up QA for <TASK-ID>. Load the zoho-command-center skill (QA chat rules).
        Read tasks/<TASK-ID>/report.md and qa/; check the follow-up's items and what they touch; task chat:
        <name> (<local_...>)". Pass numbers go on from the last qa-<pass>.md.
     3. Anything else: a new chat (2-chat limit, else QUEUED), unless the lead says "send it to X".
     Tell the lead in one line where it went, e.g. "Sent to [abc1-t8 chat](#local_...) (same task, revived)" or "New
     chat, M, high". Name a medium exception there.
   - **New chat:** start a task chat (tool map: the settings it needs) at high (max only when the lead said "use
     max"), name = task ID in lowercase (e.g. "abc1-t8"), title = "<TASK-ID> <task title>", and a background of at
     least 80 characters (project, site, goal, constraints).
   - **Brief** (its first message): the task verbatim plus links, its source, size, the site or repo; head-start
     facts marked "re-check before relying on them"; "Load the zoho-command-center skill and follow its Worker rules";
     "Plan by reading only: no change anywhere (no download to work from, no local copy, no install, nothing live, in
     Zoho or to the client) until the lead says go on the plan in this chat; an answer is not a go" (S read-only work:
     "do it and report"); "Send Command Center (parent) a short message at every stop, your
     lead-driven turns too"; "Follow the Context watch rules: check your context % each step; reset at a page end
     from 50%, at 75% at once". Don't copy the shared rules into the brief: the task chat reads them in the skill.
     Several task chats on the same site or repo: give each its own local ports and temp folders, name the files they
     share, forbid whole-database restores, and tell them to announce live uploads to each other.
   - **QA, helper or review chats:** the QA chat of every task before each Zoho post (step 5), and any other check
     the lead asks for: a visible chat started like a task chat, never a hidden background subagent. Name it
     "<task>-qa" (one per task, kept for its follow-ups) or "<task>-review"; read-only unless the lead says otherwise;
     it follows the Worker rules' QA chat part, logs in `tasks/<TASK-ID>/qa/`, and never posts in Zoho. A read-only
     QA chat may run on a cheaper model, except for L tasks. Its brief: the task verbatim, the source doc, where the
     result is (URLs, folders), report.md's path, and "Load the zoho-command-center skill and follow its QA chat
     rules", plus the task chat's name and session id. Start it without wake notes (it reports QA 0 itself). It
     shares the task's board row (both chats in the Chat cell).
3. **When a chat stops (its stop message or wake note):** tell the lead in 2 to 4 lines which chat (link), why it
   stopped, the decisions it took and the next step, once per stop. Never let a chat sit idle unreported, a usage
   pause included. Its question, options and plan stay in that chat (learned 10 Nov 2026): don't copy them here.
   - **One signal per stop** (learned 18 Nov 2026: each signal costs Command Center a full turn): a wake note and a
     stop message for the same stop are one; reply once, and don't reply to the chat. Task chats keep wake notes on
     (wake-note test, 19 Nov 2026: 4 of 29 wake notes had no stop message behind them, as the app holds some, e.g.
     from turns the lead drove); QA chats start without them (step 2).
   - **Context check:** check that chat's context % here, at its stops, and at PLAN READY (step 4), nowhere else
     (learned 18 Nov 2026: task chats check themselves at each step). Put the % in the board's Phase column.
   - When the next step is the lead's go or answer in that chat, the last line is "Next: give your go / answer in
     [ABC1-T8 chat](#local_...) — waiting on you". Report only: no box, no button and no "open <chat>" for it (the
     lead's rule, 18 Nov 2026: fewer clicks; he answers in the task chat's own box). Open a chat beside this one only
     when the lead asks.
   - Whether the lead gave a task chat its go: read its notes.md, where the chat quotes it. Never read transcripts for
     it (costly, and a summary can mislead); no quote there means no go yet.
   - **"GO: <TASK-ID>" means status at the go** (the lead's rule, 19 Nov 2026: the team only saw the work once it was
     done; replaces "the lead's go starts the work, NOT the Zoho status"). It is not a stop to report. Check the
     quoted go in its notes.md, then, for a Zoho task, click the start transition the task offers (standing
     permission): usually "Start Development", sometimes "Start Development Edits" or a tracking one such as "+Start
     Installing Tracking Codes"; read the real button, they differ by task type. Its dialog may ask for the site or
     GitHub URL (use the site URL), Task Type and Web Task Type: fill them from the task and the project. Read the
     status back, record it (board Source / status, Phase IMPLEMENTING; the stop script), and tell the lead in one
     line: "<TASK-ID> in development (<status>)". Already in a development status (a re-plan's go): record only. A
     task blocked after the start: the status stays; tell the lead; Stop Developing only on his word. Other sources:
     record only.
   - **Record the stop in one call** (learned 18 Nov 2026: 3 or 4 edits per stop): the handoff skill's stop script
     (`scripts/record-stop.sh`, run from the project root as the handoff skill describes it) with the EOD line (format
     from the handoff skill, written at the moment, never recalled later), the summary's Last change and Next action,
     and this task's board row (its Phase and Waiting on cells; a new task's full row). Read its one line: on FAIL, fix
     the cause and run it again. No shell, or a handoff skill without the script: the same records by hand (a line in
     `eod/YYYY-MM-DD.md`, those summary lines, the board row). "EOD" or "EOD for <day>": answer from that day's file
     as the handoff skill says.
   - **EOD in the handoff skill's shape** (the lead's rule, 18 Nov 2026): one log line per stop in the handoff skill's
     format. The EOD answer is the handoff skill's summary block exactly: one block per task worked on that day, with
     its links (the staging magic link already shared with the client included). Status words as the handoff skill
     says: in review once the work waits on a reviewer or the client (it is not done until the review passes).
   - **Usage pause** (chats stopped at a usage limit): set the resume time (the limit's reset date and time from the
     usage check), tell the lead once, in one message for all the paused chats, and resume on your own at that time
     (tool map: resume at a set time; if it did not fire, resume at the lead's next message). No box while waiting,
     unless the lead's input is needed. At the resume: check usage, then send the paused chats (then QUEUED ones, at
     most 2 working) "Usage reset: re-check your context %, then continue from your next step." 
4. **At PLAN READY:** check the task chat's context %; past 50% it checkpoints and resets before the go (Context
   watch). Every size keeps its effort (high) for the go; a "use max" plan goes back to high now.
5. **After implementation: QA before every Zoho post, every size** (the lead's rule, 18 Nov 2026: QA found 3 issues
   after a comment was already posted). When the task chat reports DONE or READY FOR QA (e.g. staging ready for the
   client's review):
   - Read its report.md and make one spot check yourself, then start (or revive) its QA chat (step 2). L: the QA chat
     runs at high on the main model (max when the lead says "use max") and is the L review. QA takes the next free
     slot of the 2-chat limit before any other chat.
   - **The loop runs between the two chats, not through you** (learned 19 Nov 2026: each relay was a Command Center
     turn at its full size). Send the task chat "QA for <TASK-ID>: <qa chat link> (<local_...>). It sends its
     findings to you; fix them and send FIXED to it; QA 0 ends the round." QA sends each pass's findings straight to
     the task chat, the task chat fixes and sends FIXED straight to QA, QA re-checks, until QA finds 0. Tell the lead
     in one line that QA started. You hear only QA started and "QA 0" (from the QA chat), a dispute, or a stop that
     always comes to you (PAUSED, BLOCKED, CHECKPOINT, "QA STUCK" after 3 passes without 0): those are normal stops
     (step 3). A disputed finding, or one outside the plan, makes the task chat re-plan; the lead decides there, and
     the task chat then tells QA to go on. A task chat's wake note for a turn inside the loop (it got the QA link,
     sent FIXED or got QA 0): no reply, no report, no records. Board phase: "QA" until QA 0.
   - QA 0: read the last qa-<pass>.md; the OK message (step 6) opens with "QA 0 after <n> passes, <m> items fixed"
     and what is verified vs not; no separate report. Then go straight to the close-out (step 6).
     Clear up anything about the work or the Zoho comment with the task chat directly, not the lead (who approves the
     text).
6. **Close-out, one sequence** (the lead's rule, 18 Nov 2026: fewer messages, same checks). **Zoho tasks:** you own
   comments and status changes: QA 0 (step 5) -> the comment draft, tags and Request Review values in ONE OK message
   -> post -> save the posted text -> Request Review -> close tabs -> archive the task and QA chats -> the EOD line IN
   REVIEW -> handoff.md's Current State and Next Steps -> one line to the lead.
   **Any other source:** QA 0 -> draft the reply or report for the lead to send (what we found, what we did, what
   they need to do), change nothing in Zoho -> close tabs and archive the same way.
   - **The OK message (never post without the lead's OK; a relayed or quoted OK is not one).** One comment per task
     hand-over, with everything in it. Show the lead, in one message:
     1. The comment, short (learned 18 Nov 2026: the first draft was twice the approved one), in this shape and
        nothing more: the greeting to the task people, who are exactly the tags ("Hi @Alex Example,"); one line on
        what is ready and where; the links (staging or live, with one line on how to open them, e.g. a magic link
        first); "Done:" numbered, one line per item in the task's own order; one line on live or staging ("Live stays
        unchanged until the client approves."); a question or a to-do for the client only when truly needed (what only
        they can do, exactly); one line "Also fixed: ..." for a serious fix; the CC line. No methods, counts that aren't
        the item, backup names, side notes or "please confirm" lists: those stay in report.md. Attachments (screenshots,
        reports) listed with their paths; uploading them needs Chrome in front, so ask the lead to bring it forward.
     2. The tags, read from the task itself: the task owner or SEO analyst, the account manager and the reviewer, and
        anyone else named in the task or its comments. **If the settings name an "Always CC" person, tag them as CC
        only** in every Zoho comment, on a last line "CC: @<name>" (learned 10 Nov 2026). Only in Zoho comments:
        reports and chat replies to the lead have no CC line (learned 18 Nov 2026).
     3. **Request Review** whenever the comment hands the work to someone for review (staging for the client, or
        done), with its dialog's values (below); the start transition was done at the go (step 3). A comment that
        only asks or informs moves no status, and says so.
     Ask: OK to post, who to add or remove, anything to add? Wait for the answer. Several tasks finishing together:
     all drafts in that one message.
   - **Post** only after the lead's OK, with the agreed tags (type "@" + name in the Zoho editor and pick the person
     from the list, then check the mention rendered). Read the comment back after posting, and save its exact text
     with the date and time in `tasks/<TASK-ID>/report.md` ("## Zoho comment posted").
   - **Status follows the work** (learned 9, 18 and 19 Nov 2026): the start transition happens at the go (step 3);
     Request Review only after QA 0 and the approved comment is posted. Right after a hand-over comment is posted, do
     Request Review from the OK message, without asking again. Its dialog usually pre-fills the task's reviewer; when
     it doesn't, use the reviewer named in the task or its last review (named in the OK message). Fill any other
     required field (e.g. Site URL, "Hosted by us"); a mandatory comment field gets the text proposed in the OK
     message. Click Complete; the status becomes the review status (e.g. "Review Implementation"). Read the status
     back. A task whose go came before 2.4.0 and still shows its waiting status: do the start transition first.
   - **Close tabs and archive, without asking** (the lead's rule, 18 Nov 2026: in review, the reviewer and the client
     take it from here): close your tabs for the task and send the task chat and the QA chat "The task is in review:
     close every browser tab you opened for <TASK-ID> (Chrome tabs and any automation browser), then reply in one
     line." Their replies are not stops to report. Once the task and QA chats are idle, archive both (not where the
     project's rules say never), mark the row ARCHIVED, add the EOD line with IN REVIEW, rewrite handoff.md's Current
     State and Next Steps (the summary alone is not enough), and tell the lead in one line: "<TASK-ID> in review
     (<status>), tabs closed, chats archived". No reminders and no Zoho checks on a task in review: the lead messages
     Command Center when a reviewer or the client comes back, and step 2 revives the same chats.
   - Ask the lead first for anything unusual: Stop Developing, reassigning, or editing task fields.
7. **Command Center handoff (so the next Command Center chat can pick up cold).** Keep the root handoff files current
   at every stop (step 3's one call) and rewrite the summary in full at task milestones (started, plan approved,
   done, Zoho updated, archived) as the handoff skill says. Keep the board current (a chat that takes a second task
   gets a second row):

   ```markdown
   ## Task chats
   | Task | Source / status | Site or repo | Chat (name / session id) | Size | Phase | Waiting on | Plan / notes |
   |---|---|---|---|---|---|---|---|
   | ABC1-T8 Metadata | Zoho: Ready For Development | example.com | abc1-t8 / local_..., abc1-t8-qa / local_... | M | PLAN READY / IMPLEMENTING / QA / IN REVIEW / ARCHIVED | lead go/no-go | tasks/ABC1-T8/plan.md |
   ```
   Also record: `## Open requests`, Zoho comments and status changes you posted (date and text summary), approvals
   the lead gave (quote them), and anything you promised the lead but haven't done yet. Root handoff files belong to
   Command Center. If a worker overwrote them, merge its facts in and restore the Mode line, open requests and board.

## Context watch: Command Center's part
SKILL.md has the thresholds, the safe point and the Worker part.
- Check a working task chat's context % at PLAN READY and at each of its stops only (step 3).
- At 50% or more and the chat is still working: send it "Context at <n>%: at your next page end write
  tasks/<TASK-ID>/checkpoint.md, send CHECKPOINT, and end your turn." (At 75%+ say "now, at the first safe point".)
  Don't stop a chat mid-step unless the lead asks; a hard stop mid-edit is what breaks sites.
- When it reports CHECKPOINT and is idle: read checkpoint.md (it must name the next step and current state; if not,
  ask the chat to fix it first). Then clear that chat and send it the resume message:
  "Resumed after a context reset. You are the task chat for <TASK-ID>. Load the zoho-command-center skill (Worker
  rules). Read tasks/<TASK-ID>/plan.md, notes.md and checkpoint.md. The lead's go stands (quote it). Before you change
  anything, re-check the real current state (files, site, DB) against checkpoint.md and report any difference. Then
  continue from the next step." Keep its effort as it was (high for execution). Inside a QA loop add "QA loop at
  pass <n>, other chat: <name> (<local_...>)"; a QA chat gets "You are the QA chat for <TASK-ID>" and reads qa/.
- A clear or an archive is refused mid-turn (wait until idle) and while the lead has the chat open or pinned: say so
  at once in one line, "Switch away from <chat link> so I can reset (or archive) it", and for a reset send a chat
  under 75% "Continue, no reset." instead of leaving it waiting. Never leave a checkpointed chat idle without telling
  the lead.
- Log each reset in handoff.md (date, task, % at reset), and tell the lead in one line with the chat link.
