# Tool map

The skill's steps say what to do in plain words. This table gives each action's tool in the Claude desktop app (Code
tab, which has the session tools) and what to do in any other AI tool (Claude Code in a terminal, Codex, Cursor,
Antigravity, OpenCode, Cline, Devin Desktop and others), where Command Center runs in one-chat mode (below).

| Action | Claude desktop app | Other AI tools (one-chat mode) |
|---|---|---|
| Start a task, QA or review chat | `start_session`: initiation "user_asked", context "fresh", use_worktree false, wake_when_done true, `name`, `title`, `background` (at least 80 characters; refused without it), `effort` "high". A read-only QA chat may set `model` to a Sonnet model id | Write `tasks/<TASK-ID>/brief.md`; tell the lead to open a new chat with "Read tasks/<TASK-ID>/brief.md and follow zoho-command-center's Worker rules" |
| Send a chat a message | `SendMessage` to its `local_...` id (or `send_message`) | Add a dated "## Follow-up" to its brief.md; tell the lead to say "read your brief's follow-up" in that chat |
| A worker messages Command Center | `send_message` with session_id "parent", or `SendMessage` to the parent's `local_...` id | Add the stop line under "## Stops" at the top of notes.md; tell the lead "Tell Command Center: check <TASK-ID>" |
| A chat's stop reaches Command Center | its stop message, and the wake note while wake notes are on (step 3) | the lead says "check <TASK-ID>"; read its notes.md |
| A chat's context % | `get_usage` with its `local_...` id ("self" for your own) | each chat reads its own tool's context meter and checkpoints itself |
| Usage limits (5-hour, weekly) | `get_usage` (plan) | the tool's usage page, or ask the lead at each start; keep the 2-chat limit |
| A chat's state and effort | `get_session` | its notes.md and the board |
| List your own chats | `list_sessions {"linked": true}`; board rows it misses: `get_session` by id | the board |
| Set a chat's effort | `set_session_effort` (a level above Command Center's needs the lead's approval) | the lead sets the tool's reasoning or model setting: its highest for "use max", else its standard high |
| Clear a chat after its checkpoint | `clear_session` on that idle chat (never "self"); the lead's "Resume previous session" undoes it | the lead opens a new chat with the resume message |
| Stop a chat | `stop_session` (only when the lead asks) | the lead stops it |
| Archive or revive a chat | `archive_session`, `unarchive_session` | the lead closes or reopens it; the revive message is the same |
| Rename your own chat | `set_session_title` ("self") | skip |
| Open a chat beside Command Center | `open_session_in` | the lead opens it |
| The next-step box | `wrap_up` with `ask` and `actions` (only for a new decision) | a last line "Decide: <question> (<option 1> / <option 2>)" |
| Resume at a set time | `CronCreate` one-shot (recurring false, minute and hour pinned) with the resume message; this chat must stay open | tell the lead the time; resume on the lead's next message |
| Record a stop | the handoff skill's stop script | the same where the tool runs commands; else by hand |
| Read Zoho, post comments, change status | Claude in Chrome | the tool's browser control with the lead's sign-in; without one, draft the comment and the lead posts it |
| Live form tests (bot checks) | the app's built-in browser pane | a browser with no AI extension, or the lead submits |
| Checkpoint before auto-compact | the Context watch (SKILL.md) | the same, from the tool's own meter |

## One-chat mode (tools without session tools)
- Command Center runs in one chat and keeps the board, `## Open requests`, the handoff files and the EOD log as usual.
- Each task keeps its own folder `tasks/<TASK-ID>/` (brief.md, plan.md, notes.md, report.md). The lead opens a task
  chat with one line: "Read tasks/<TASK-ID>/brief.md and follow zoho-command-center's Worker rules".
- Stops go into the task's notes.md ("## Stops" at the top) and the lead tells Command Center "check <TASK-ID>".
- Context comes from the tool's own meter, with a checkpoint at each page end from 50% and at 75% at once; the reset
  is a new chat with the resume message.
- Zoho comments are drafted and shown to the lead as usual; the lead posts them when the tool cannot drive a browser.
- Every gate stays: the plan, the lead's go, the comment OK, backups, the review at done.
