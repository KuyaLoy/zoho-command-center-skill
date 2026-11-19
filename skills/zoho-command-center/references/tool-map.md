# Tool map

The skill's steps say what to do in plain words. This table gives each action's tool in the Claude desktop app (Code
tab, which has the session tools) and what to do in any other AI tool (Claude Code in a terminal, Codex, Cursor,
Antigravity, OpenCode, Cline, Devin Desktop and others), where Command Center runs in one-chat mode (below).

| Action | Claude desktop app | Other AI tools (one-chat mode) |
|---|---|---|
| Start a task, QA or review chat | `start_session`: initiation "user_asked", context "fresh", use_worktree false, wake_when_done true (false for a QA chat), `name`, `title`, `background` (at least 80 characters; refused without it), `effort` "high" (or "max" for a plan that needs it). A read-only QA chat may set `model` to a Sonnet model id | Write `tasks/<TASK-ID>/brief.md`; tell the lead to open a new chat with "Read tasks/<TASK-ID>/brief.md and follow zoho-command-center's Worker rules" |
| Send a chat a message | `SendMessage` to its `local_...` id (or `send_message`) | Add a dated "## Follow-up" to its brief.md; tell the lead to say "read your brief's follow-up" in that chat |
| A worker messages Command Center | `send_message` with session_id "parent", or `SendMessage` to the parent's `local_...` id | Add the stop line under "## Stops" at the top of notes.md; tell the lead "Tell Command Center: check <TASK-ID>" |
| A chat's stop reaches Command Center | its stop message, and the wake note: task chats keep wake notes on (the 19 Nov test found wake notes with no stop message behind them; step 3), QA chats start without them | the lead says "check <TASK-ID>"; read its notes.md |
| A chat's context % | `get_usage` with its `local_...` id ("self" for your own) | each chat reads its own tool's context meter and checkpoints itself |
| Usage limits (5-hour, weekly), any chat | `get_usage` (its plan part) | the tool's usage page, or ask the lead at each start; keep the 2-chat limit |
| A chat's state and effort | `get_session` | its notes.md and the board |
| List your own chats | `list_sessions {"linked": true}`; board rows it misses: `get_session` by id | the board |
| Set a chat's effort | `set_session_effort` (a level above Command Center's needs the lead's approval; back to high at the go needs none) | the lead sets the tool's reasoning or model setting: its highest for a max plan or "use max", else its standard high |
| Clear a chat after its checkpoint | `clear_session` on that idle chat; the lead's "Resume previous session" undoes it | the lead opens a new chat with the resume message |
| Reset Command Center (only as command-center.md allows) | `clear_session` "self": it runs when this turn ends, so send the one line first; dropped if the lead's message comes first; the lead's "Resume previous session" undoes it | tell the lead the one line and ask for a new Command Center chat |
| QA and task chat talk directly | `SendMessage` to the other chat's `local_...` id (both are Command Center's chats) | the QA chat writes qa-<pass>.md and tells the lead "fix qa/qa-<n>.md" for the task chat; the task chat adds "FIXED" under "## Stops" and the lead tells QA "re-check" |
| Stop a chat | `stop_session` (only when the lead asks) | the lead stops it |
| Archive or revive a chat | `archive_session`, `unarchive_session` | the lead closes or reopens it; the revive message is the same |
| Rename your own chat | `set_session_title` ("self") | skip |
| Open a chat beside Command Center (only when the lead asks) | `open_session_in` | the lead opens it |
| The next-step box | `wrap_up` with `ask` and `actions` (only for a new decision) | a last line "Decide: <question> (<option 1> / <option 2>)" |
| Resume at a set time | `CronCreate` one-shot (recurring false; minute, hour, day and month pinned to the reset) with the resume message; this chat must stay open | tell the lead the time; resume on the lead's next message |
| Record a stop | the handoff skill's stop script, `scripts/record-stop.sh` (needs a shell) | the same where the tool runs commands; else by hand |
| Read Zoho, post comments, change status | Claude in Chrome: page text and element search first, steps batched, a screenshot only to confirm something visual | the tool's browser control with the lead's sign-in; without one, show the lead the comment, tags, transition and Request Review values, and the lead clicks them |
| Close a task's browser tabs | the browser tools' close-tab action (Chrome, the app's pane, the automation browser) | the lead closes them; name them |
| Link a chat for the lead | `[title](#local_...)` | its task ID and folder |
| Live form tests (bot checks) | the app's built-in browser pane | a browser with no AI extension, or the lead submits |
| Checkpoint before auto-compact | the Context watch (SKILL.md) | the same, from the tool's own meter |

## One-chat mode (tools without session tools)
- Install: link the skill folder into the tool's skills folder (README); where a tool has no skills, a line in its
  rules file points to SKILL.md.
- Command Center keeps its own chat and never does the task. It keeps the board, `## Open requests`, the handoff
  files and the EOD log as usual; when its tool compacts or the lead starts a new Command Center chat, it starts from
  the handoff files (step 1).
- Each task gets its own chat, which the lead opens by hand, and its own folder `tasks/<TASK-ID>/` (brief.md,
  plan.md, notes.md, report.md), with one line: "Read tasks/<TASK-ID>/brief.md and follow zoho-command-center's
  Worker rules". Briefs keep their wording: "message Command Center" means the "## Stops" line in notes.md.
- QA chat (step 5): Command Center writes `tasks/<TASK-ID>/qa/brief.md` and the lead opens it like a task chat; the
  loop then runs between the two chats through the lead (the row above), and Command Center hears only QA 0.
- Stops go into the task's notes.md ("## Stops" at the top) and the lead tells Command Center "check <TASK-ID>".
- Context comes from the tool's own meter, with a checkpoint at each page end from 50% and at 75% at once; on
  "check <TASK-ID>" after a CHECKPOINT, Command Center gives the lead the resume message to paste into a new chat.
- Close-out: after Request Review, the lead closes the task and QA chats and their tabs; Command Center marks the
  row ARCHIVED.
- Zoho comments are drafted and shown to the lead as usual; the lead posts them when the tool cannot drive a browser.
- Every gate stays: the plan, the lead's go, the comment OK, backups, the review at done.
