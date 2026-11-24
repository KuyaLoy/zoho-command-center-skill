# Tool map

The skill's steps say what to do in plain words. This table gives each action's tool in the Claude desktop app (Code
tab, which has the session tools), in Antigravity and in Codex (their modes, below), and in any other AI tool (Claude
Code in a terminal, Cursor, OpenCode, Cline, Devin Desktop and others), where Command Center runs in one-chat mode
(below).

| Action | Claude desktop app | Antigravity (Antigravity mode, below) | Codex (Codex mode, below) | Other AI tools (one-chat mode) |
|---|---|---|---|---|
| Start a task, QA or review chat | `start_session`: initiation "user_asked", context "fresh", use_worktree false, wake_when_done true (false for a QA chat), `name`, `title`, `background` (at least 80 characters; refused without it), `effort` "high" (or "max" for a plan that needs it). A read-only QA chat may set `model` to a Sonnet model id | Task chat: CS `CreateConversation` with `title` "▶ RUNNING \| <TASK-ID> <task title>", `tags` ["<TASK-ID>"], `projectId` $ANTIGRAVITY_PROJECT_ID and `prompt` the first prompt (below), no `model` (it keeps the lead's current model; another only when the lead names it); keep its `id` on the board. QA: the `wp-qa` agent as Command Center's subagent (`invoke_subagent`), only once `tasks/<TASK-ID>/qa/brief.md` exists | Task chat: write `tasks/<TASK-ID>/brief.md`; the lead opens a separate Codex session in the project folder (the desktop app, or `codex`) with "$zoho-command-center Read tasks/<TASK-ID>/brief.md and follow its Worker rules". QA: its own read-only session, never a subagent (an agent file cannot set its own sandbox): `codex exec -s read-only -C <project> -o tasks/<TASK-ID>/qa/qa-<pass>.md "$zoho-command-center Read tasks/<TASK-ID>/qa/brief.md and follow its QA chat rules"`, only once qa/brief.md exists | Write `tasks/<TASK-ID>/brief.md`; tell the lead to open a new chat with "Read tasks/<TASK-ID>/brief.md and follow zoho-command-center's Worker rules" |
| Send a chat a message | `SendMessage` to its `local_...` id (or `send_message`) | a top-level task conversation has no message call: add a dated "## Follow-up" to its brief.md and tell the lead to say "read your brief's follow-up" in it. A subagent (the QA agent, for its re-check rounds): `send_message` | add a dated "## Follow-up" to its brief.md; tell the lead to say "read your brief's follow-up" in that session | Add a dated "## Follow-up" to its brief.md; tell the lead to say "read your brief's follow-up" in that chat |
| A worker messages Command Center | `send_message` with session_id "parent", or `SendMessage` to the parent's `local_...` id | its stop line under "## Stops" at the top of notes.md, and its title prefix; the lead says "check <TASK-ID>" | its stop line under "## Stops" at the top of notes.md; the lead says "check <TASK-ID>" | Add the stop line under "## Stops" at the top of notes.md; tell the lead "Tell Command Center: check <TASK-ID>" |
| A chat's stop reaches Command Center | its stop message, and the wake note: task chats keep wake notes on (the 19 Nov test found wake notes with no stop message behind them; step 3), QA chats start without them | the lead says "check <TASK-ID>"; read its notes.md, and its state with CS `GetConversation` (`runState`, title prefix) | the lead says "check <TASK-ID>"; read its notes.md | the lead says "check <TASK-ID>"; read its notes.md |
| A chat's context % | `get_usage` with its `local_...` id ("self" for your own) | no meter in the App: a checkpoint at every phase end (rule 10); a long phase gets a fresh conversation | each session reads its own context left (Codex shows it) and checkpoints at a page end from 50%, at 75% at once, and at every phase end | each chat reads its own tool's context meter and checkpoints itself |
| Usage limits (5-hour, weekly), any chat | `get_usage` (its plan part) | the App's quota, or ask the lead at each start; keep the 2-chat limit | `/status` in the session, or ask the lead at each start; keep the 2-chat limit | the tool's usage page, or ask the lead at each start; keep the 2-chat limit |
| A chat's state and effort | `get_session` | CS `GetConversation`: `runState` (IDLE, RUNNING) and the title prefix; its notes.md | its notes.md (the stop lines) and the board | its notes.md and the board |
| List your own chats | `list_sessions {"linked": true}`; board rows it misses: `get_session` by id | CS `ListConversations` with `projectId` and `tags` ["<TASK-ID>"]; the board | the board (`codex resume` lists the lead's sessions) | the board |
| Set a chat's effort | `set_session_effort` (a level above Command Center's needs the lead's approval; back to high at the go needs none) | no effort setting: every conversation keeps the lead's current model; a plan that needs more depth gets it from the brief (read the source in full, plan at the L length), and a different model only when the lead names it | the lead sets the model and reasoning effort in the session (`/model`); keep the lead's model | the lead sets the tool's reasoning or model setting: its highest for a max plan or "use max", else its standard high |
| Clear a chat after its checkpoint | `clear_session` on that idle chat (refused because it is open or pinned on the lead's screen: `start_session` a continuation chat "<task>-2" with the resume message instead, no retry, no question, but only in a turn the lead typed; in any other turn `start_session` waits for his click or is refused, so send "Continue, no reset" instead); the lead's "Resume previous session" undoes it | CS `CreateConversation` "<task>-2" (title plus "(cont.)", same tags, no `model`) with the resume message; archive the old one once idle (CS `UpdateConversation` `archived` true) | the lead starts a new session (`/new`, or a new `codex`) with the resume message | the lead opens a new chat with the resume message |
| Reset Command Center (only as command-center.md allows) | `clear_session` "self": it runs when this turn ends, so send the one line first; dropped if the lead's message comes first; the lead's "Resume previous session" undoes it | tell the lead the one line; the lead opens a new conversation and types /zoho-command-center | tell the lead the one line; the lead starts a new session with $zoho-command-center | tell the lead the one line and ask for a new Command Center chat |
| QA and task chat talk directly | `SendMessage` to the other chat's `local_...` id (both are Command Center's chats) | through Command Center: it writes each QA result verbatim to qa/qa-<pass>.md and tells the lead "fix qa/qa-<n>.md" for the task conversation; on its FIXED line, `send_message` "re-check" to the same QA subagent (it keeps its context) | through the files: each QA pass is a new `codex exec -s read-only ... -o qa/qa-<pass>.md` run (the CLI writes the file, the session cannot); the lead tells the task session "fix qa/qa-<n>.md"; on its FIXED line the next pass re-checks the fixed items and the changed code | the QA chat writes qa-<pass>.md and tells the lead "fix qa/qa-<n>.md" for the task chat; the task chat adds "FIXED" under "## Stops" and the lead tells QA "re-check" |
| Stop a chat | `stop_session` (only when the lead asks) | the lead stops it | the lead stops it (Esc, or closes the session) | the lead stops it |
| Archive or revive a chat | `archive_session`, `unarchive_session` | CS `UpdateConversation` `annotations.archived` true or false | `codex archive <id or name>`; revive: `codex unarchive`, then `codex resume <id or name>` with the revive message | the lead closes or reopens it; the revive message is the same |
| Rename your own chat | `set_session_title` ("self") | CS `UpdateConversation` with `conversationId` $ANTIGRAVITY_CONVERSATION_ID and `annotations.title` | skip (no title call; the session name is set when the lead starts it) | skip |
| The state prefix in a title | `set_session_title` ("self"; Command Center: a chat it started) with "▶ RUNNING \| ", "⏸ WAITING on <who> \| ", "✋ BLOCKED \| " or "✓ DONE \| " before the title, once per state change | CS `UpdateConversation` `annotations.title` with the same prefixes, once per state change: the task conversation sets its own ($ANTIGRAVITY_CONVERSATION_ID); Command Center fixes a stale one on a conversation it created | skip: the first line of each message says the state (RUNNING, WAITING on <who>, BLOCKED, DONE) and the stop line goes into notes.md | skip (the RUNNING line and the stop types carry the state) |
| Open a chat beside Command Center (only when the lead asks) | `open_session_in` | the lead opens it | the lead opens it | the lead opens it |
| The next-step box | `wrap_up` with `ask` and `actions` (only for a new decision) | a last line "Decide: <question> (<option 1> / <option 2>)" | a last line "Decide: <question> (<option 1> / <option 2>)" | a last line "Decide: <question> (<option 1> / <option 2>)" |
| The recap (sidebar status) | `wrap_up`'s `recap`: its first sentence is the sidebar status, so a turn ending while its own work runs opens it with the RUNNING line (SKILL.md "RUNNING, not stopped") | the first line of the last message, and the title prefix | the first line of the last message | the first line of the last message |
| What is on the lead's screen | `get_window_layout` (read-only: the main pane, split panes and pop-out windows); `open_session_in` acts only while this chat is on screen | ask the lead | ask the lead | ask the lead |
| Wait for a chat to go idle | `get_session` now; still running: a `CronCreate` one-shot (load it first when deferred) 2 minutes ahead (recurring false) whose prompt names the exact step; never end a turn only "waiting" | CS `GetConversation` `runState` now; never end a turn only waiting: the lead says "check <TASK-ID>" when it stops | the lead says "check <TASK-ID>" when that session has stopped | the lead says "check <TASK-ID>" when that chat has stopped |
| Resume at a set time | `CronCreate` one-shot (load it first with the tool search when the tool list defers it; recurring false; minute, hour, day and month pinned to the reset) with the resume message; this chat must stay open, and idle at that time: a timer fires only between turns, so never leave a turn blocked on a call that waits for the lead | tell the lead the time (or the lead sets `/schedule`); resume on the lead's next message | tell the lead the time; resume on the lead's next message | tell the lead the time; resume on the lead's next message |
| Record a stop | the handoff skill's stop script, `scripts/record-stop.sh` (needs a shell) | the stop script through `run_command` | the stop script in the shell | the same where the tool runs commands; else by hand |
| Read Zoho, post comments, change status | Claude in Chrome: page text and element search first, steps batched, a screenshot only to confirm something visual | the built-in `browser` subagent, opened only at the task's own link (rule 6); comment text, tags, transition and Request Review only on the lead's OK | Codex's browser control at the task's own link only, with the lead's sign-in; otherwise show the lead the comment, tags, transition and Request Review values, and the lead clicks them | the tool's browser control with the lead's sign-in; without one, show the lead the comment, tags, transition and Request Review values, and the lead clicks them |
| Close a task's browser tabs | the browser tools' close-tab action (Chrome, the app's pane, the automation browser) | the `browser` subagent closes them; else name them | the lead closes them; name them | the lead closes them; name them |
| Link a chat for the lead | `[title](#local_...)` | its title and task ID | its task ID and folder | its task ID and folder |
| Live form tests (bot checks) | the app's built-in browser pane | a browser with no AI control, or the lead submits | a browser with no AI control, or the lead submits | a browser with no AI extension, or the lead submits |
| Checkpoint before auto-compact | the Context watch (SKILL.md) | phase-end checkpoints (the App compacts by itself, with no meter) | the Context watch, from Codex's context left | the same, from the tool's own meter |

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

## Antigravity mode
Learned 24 Nov 2026 from a build run in Antigravity: skills there load only when the model judges them relevant, so a
task chat skipped them, guessed defaults, reported checks it had not run and opened the wrong Zoho page; one
conversation did everything. This mode makes those rules mechanical.
- **Setup, once per machine** (on the lead's OK): `python antigravity/install.py --dry-run`, then without
  `--dry-run`, from this repo's clone (README, "Use it in Antigravity"). It installs the always-on hard rules
  (`zcc-hard-rules`; "rule <n>" in the table is its number), the `task-worker` and `wp-qa` agents and three hooks:
  the handoff brief injected at the start of each conversation, a write that puts a secret into a .md file denied, and
  the evidence gate at Stop (below).
- **Command Center** is the project's main conversation; the lead opens it with `/zoho-command-center`.
- **CS** in the table is Antigravity's ConversationService, called from the shell: `curl -sS -X POST
  "http://$ANTIGRAVITY_LS_ADDRESS/product.v1.ConversationService/<Method>" -H "Content-Type: application/json"
  -H "Connect-Protocol-Version: 1" -H "x-antigravity-csrf-token: $ANTIGRAVITY_CSRF_TOKEN" -d '<json>'`. When the
  terminal sandbox refuses it, rerun only that call outside the sandbox (the app may ask the lead).
- **Task chats are top-level conversations** that Command Center creates, so the lead sees, opens and steers each one
  as in the Claude app. First prompt: "/zoho-command-center Open the zoho-command-center skill (Worker rules) and
  handoff now, then read tasks/<TASK-ID>/brief.md and follow it." The brief names the build skill to open before each
  phase. Each task conversation keeps its title prefix current, like `set_session_title` in the Claude app.
- **QA** is the `wp-qa` agent: read-only by its rules plus a sandboxed shell (`commandExecutionPolicy` "sandbox") and
  no file-editing tools; the tool list alone is not the guard, as `run_command` can still write. Command Center
  starts it as its
  subagent only after it wrote `qa/brief.md`; its result is written to qa/qa-<pass>.md verbatim, and step 5's loop
  runs through the lead as in one-chat mode.
- **Context:** the App shows no context meter, so every phase end is a checkpoint (checkpoint.md, notes.md, the
  handoff files); "<task>-2" resumes from it.
- **Zoho** is read and written only through the task's own link, by the built-in `browser` subagent.
- **Models:** conversations and agents keep the lead's current model (`model: inherit`); another only when the
  lead names it. Agent tool names are the ones seen in real transcripts (a wrong name can hang a subagent):
  `read_file`, `edit_file`, `write_file`, `run_command`, `manage_task`, `update_steps`, `webview_browser`.
- **Evidence gate** (2.8.0): a Stop hook sends a chat back once when its DONE, PART DONE, READY FOR QA or QA report
  names a check with no command output in `tasks/<TASK-ID>/checks.md` (Worker rules: "Cheaper checks, with proof").
- Not verified yet (check on the first task): that a custom agent's `tools` list hides the write tools, that the
  secrets guard's empty answer leaves the app's own permission prompt as it is, how the App shows a subagent's card,
  and what a subagent costs against the lead's quota.

## Codex mode
Codex (the desktop app or `codex` in a terminal) has no session tools for Command Center, so task chats are sessions
the lead opens, as in one-chat mode, with the skill forced and the rules made mechanical (added 24 Nov 2026).
- **Setup, once per machine** (on the lead's OK): `python codex/install.py --dry-run`, then without `--dry-run`, from
  this repo's clone (README, "Use it in Codex"). It adds a marked block with the hard rules to `~/.codex/AGENTS.md`
  (all AGENTS.md files together are read up to 32 KiB), the `task-worker` and `reviewer` agents
  (`~/.codex/agents/`), and three hooks in `~/.codex/hooks.json`: the handoff brief at session start, a write that
  puts a secret into a .md file denied, and the evidence gate at Stop. Codex runs a hook only after the lead trusts it
  once in `/hooks` (again after it changes).
- **Force the skill** with `$zoho-command-center` (and `$convert-to-wordpress`, `$figma-to-wordpress`, `$handoff`):
  Codex opens a skill by itself only when it judges it relevant. Skills are read from `~/.agents/skills`.
- **Task chats** are separate sessions the lead opens in the project folder; Command Center writes the brief and keeps
  the board, and stops come through notes.md ("## Stops") and the lead's "check <TASK-ID>". Subagents (the agents
  above) only when the lead asks for one.
- **QA** is its own read-only session, never a subagent: a subagent keeps its parent's sandbox, and an agent file
  cannot set its own. Command Center (or the lead) runs each pass with `codex exec -s read-only`, and `-o` saves the
  final report to qa/qa-<pass>.md; the loop then runs through the files as in one-chat mode.
- **Evidence gate:** the same Stop hook as in Antigravity (it answers "block", and Codex prompts the session again
  with the reason). One push back per turn, so it never loops.
- **Hooks are a second line** (the rules are the first): before relying on them, run `python shared/hook_selftest.py`
  (README) to see that SessionStart, PreToolUse and Stop fire on this machine.
- Not verified yet (check on the first task): `-s read-only` with this machine's Windows sandbox setting, the hook
  field `additionalContextLimit`, and the session names `codex archive` and `codex resume` take.
