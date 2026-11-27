# Tool map

The skill's steps say what to do in plain words. This table gives each action's tool in the Claude desktop app (Code
tab, which has the session tools), in Antigravity and in Codex (their modes, below), and in any other AI tool (Claude
Code in a terminal, Cursor, OpenCode, Cline, Devin Desktop and others), where Command Center runs in one-chat mode
(below).

| Action | Claude desktop app | Antigravity (Antigravity mode, below) | Codex terminal (Codex mode, below) | Codex desktop app (Codex mode, below) | Other AI tools (one-chat mode) |
|---|---|---|---|---|---|
| Start a task, QA or review chat | `start_session`: initiation "user_asked", context "fresh", use_worktree false, wake_when_done true (false for a QA chat), `name`, `title`, `background` (at least 80 characters; refused without it), `effort` from the brief ("medium", "high", or "max" for a plan that needs it; task-size.md > Effort). A read-only QA chat may set `model` to a Sonnet model id | Default: the task runs as a subagent (rows below, Subagent mode). Only when the lead asks for a separate task chat: CS `CreateConversation` with `title` "▶ RUNNING \| <TASK-ID> <task title>" (with no `prompt`: "⏸ WAITING on <lead> \| ..." until it runs), `tags` ["<TASK-ID>"], `projectId` $ANTIGRAVITY_PROJECT_ID and `prompt` the first prompt (below), no `model` (it keeps the lead's current model; another only when the lead names it); keep its `id` on the board. QA: the `wp-qa` subagent (row below) | Default: the task runs as a subagent (rows below, Subagent mode). Only when the lead asks for a separate task chat: write `tasks/<TASK-ID>/brief.md`; the lead opens a separate Codex session in the project folder (the desktop app, or `codex`) with "$zoho-command-center Read tasks/<TASK-ID>/brief.md and follow its Worker rules". QA: the `zcc-reviewer` subagent (row below); a sandboxed read-only QA session only on the lead's word (a subagent keeps the parent's sandbox): `codex exec -s read-only -C <project> -o tasks/<TASK-ID>/qa/qa-<pass>.md "$zoho-command-center Read tasks/<TASK-ID>/qa/brief.md and follow its QA chat rules"`, only once qa/brief.md exists | Default: the task runs as a subagent (rows below, Subagent mode). Only when the lead asks for a separate task chat: the app creates a thread only on the lead's explicit request, so when the briefs are ready ask once with `request_user_input` ("Create the task chats now?" Create / Not yet; or the lead already said so). Then per task `create_thread` with the first prompt "$zoho-command-center Read tasks/<TASK-ID>/brief.md and follow its Worker rules" and `set_thread_title` "⏸ WAITING on <lead> \| <TASK-ID> <task title>" until its first turn runs (the thread sets RUNNING itself). QA: the `zcc-reviewer` subagent, as in the terminal | Write `tasks/<TASK-ID>/brief.md`; tell the lead to open a new chat with "Read tasks/<TASK-ID>/brief.md and follow zoho-command-center's Worker rules" |
| Run a task as a subagent (default in Antigravity and Codex; Subagent mode) | not used: task chats (row above) | `invoke_subagent` with the `task-worker` agent and the brief's path | `spawn_agent` with the `zcc-task-worker` agent and the brief's path | the same as the terminal | not used |
| A subagent's plan and the lead's go | not used | its PLAN READY comes back to Command Center: show the short plan with numbered options; the lead types the go in Command Center's chat; quote it verbatim to the same subagent (`send_message`) and log it in notes.md | the same, with `request_user_input` choices where the session has them; quote the go with `send_message` or `followup_task` | the same as the terminal | not used |
| Follow-ups, re-plans and QA rounds to a subagent | not used | `send_message` to the same subagent (it keeps its context) | `send_message` or `followup_task`; `wait_agent` to wait, `list_agents` for state, `interrupt_agent` to stop one | the same as the terminal | not used |
| A subagent's state on the board | not used | the Chat cell names it (`Antigravity: task-worker / <id> (subagent)`), the Phase cell its state: planning, waiting on the lead's go, working, QA, done | the same (`Codex: zcc-task-worker / <id> (subagent)`) | the same as the terminal | not used |
| The QA subagent (it runs every check itself) | not used: its own QA chat (step 2) | `invoke_subagent` with `wp-qa`, only after qa/brief.md exists; read-only by its tools, the sandbox and the rule | `spawn_agent` with `zcc-reviewer`, only after qa/brief.md exists; read-only by the rule alone (it keeps the parent's sandbox) | the same as the terminal | not used: its own QA chat |
| Send a chat a message | `SendMessage` to its `local_...` id (or `send_message`) | a top-level task conversation has no message call: add a dated "## Follow-up" to its brief.md and tell the lead to say "read your brief's follow-up" in it. A subagent (the QA agent, for its re-check rounds): `send_message` | add a dated "## Follow-up" to its brief.md; tell the lead to say "read your brief's follow-up" in that session | `send_message_to_thread` | Add a dated "## Follow-up" to its brief.md; tell the lead to say "read your brief's follow-up" in that chat |
| A worker messages Command Center | `send_message` with session_id "parent", or `SendMessage` to the parent's `local_...` id | its stop line under "## Stops" at the top of notes.md, and its title prefix; the lead says "check <TASK-ID>" | its stop line under "## Stops" at the top of notes.md; the lead says "check <TASK-ID>" | its stop line under "## Stops" in notes.md; Command Center follows its threads with `wait_threads` and `read_thread` | Add the stop line under "## Stops" at the top of notes.md; tell the lead "Tell Command Center: check <TASK-ID>" |
| A chat's stop reaches Command Center | its stop message, and the wake note: task chats keep wake notes on (the 19 Nov test found wake notes with no stop message behind them; step 3), QA chats start without them | the lead says "check <TASK-ID>"; read its notes.md, and its state with CS `GetConversation` (`runState`, title prefix) | the lead says "check <TASK-ID>"; read its notes.md | `wait_threads` returns when a thread ends its turn; read it (`read_thread`) and its notes.md | the lead says "check <TASK-ID>"; read its notes.md |
| A chat's context % | `get_usage` with its `local_...` id ("self" for your own) | no meter in the App: a checkpoint at every phase end (rule 10); a long phase gets a fresh conversation | each session reads its own context left (Codex shows it) and checkpoints at a page end from 50%, at 75% at once, and at every phase end | as in the terminal: each thread checkpoints from its own context left and at every phase end | each chat reads its own tool's context meter and checkpoints itself |
| Usage limits (5-hour, weekly), any chat | `get_usage` (its plan part) | the App's quota, or ask the lead at each start; keep the 2-chat limit | `/status` in the session, or ask the lead at each start; keep the 2-chat limit | the app's usage view, or ask the lead at each start; keep the 2-chat limit | the tool's usage page, or ask the lead at each start; keep the 2-chat limit |
| Keep usage low (small plans) | the 2-chat limit and the size table (SKILL.md) | subagents, not new conversations (each new one pays the full start); a subagent starts light: its agent prompt, the Worker rules section and the brief; the brief names the effort (medium by default; the lead picks the setting); one task chat at a time on a small plan; heavy visual QA in a tool with a larger plan | subagents, not new sessions; the same light start; the session-start hook injects only the summary's essentials; open only the sections you need (SKILL.md, Files) | the same as the terminal | one chat at a time on a small plan |
| Long tool output (Worker rules: Lean tool output) | Bash: `<command> > tasks/<TASK-ID>/logs/<name>.log 2>&1`, then only the result line and the failures (`tail -n 5`, `grep -inE "fail\|error"`); `Read` with offset and limit when you need more | `run_command` with the same redirect into `tasks/<TASK-ID>/logs/`, then the result line and the failures (PowerShell: `Select-Object -Last 5`, `Select-String -Pattern fail,error`); `read_file` the log only when needed | the same redirect into `tasks/<TASK-ID>/logs/`, then `tail` and `rg -i "fail\|error"` on it; compact flags first (`--porcelain`, `-q`, `--format=json --fields=...`) | the same as the terminal | the same redirect into `tasks/<TASK-ID>/logs/`; show the result line and the failures only |
| A chat's state and effort | `get_session` | CS `GetConversation`: `runState` (IDLE, RUNNING) and the title prefix; its notes.md | its notes.md (the stop lines) and the board | `read_thread`, the title prefix and its notes.md | its notes.md and the board |
| List your own chats | `list_sessions {"linked": true}`; board rows it misses: `get_session` by id | CS `ListConversations` with `projectId` and `tags` ["<TASK-ID>"]; the board | the board (`codex resume` lists the lead's sessions) | `list_threads`; the board | the board |
| Set a chat's effort | `set_session_effort` (a level above Command Center's needs the lead's approval; down to the work effort at the go needs none) | no effort setting: every conversation and subagent keeps the lead's current model and setting (Command Center's chat: high, the lead picks it); the brief names the level, a plan that needs more depth gets it from the brief (read the source in full, plan at the L length), and a different model only when the lead names it | Command Center's session at high (the lead sets it with `/model`); the agent files set the subagents' `model_reasoning_effort`: `zcc-task-worker` medium, `zcc-reviewer` high; a task that needs high or max says so in its brief and runs as a separate session at that level (`codex -c model_reasoning_effort=high`) | the same agent files as the terminal; Command Center's thread at high (the lead picks it); a task that needs high or max: its own thread at that level, said in one line | the lead sets the tool's reasoning or model setting: high for Command Center, its highest for a max plan or "use max", high for live or hard-to-undo work, else medium |
| Clear a chat after its checkpoint | `clear_session` on that idle chat (refused because it is open or pinned on the lead's screen: `start_session` a continuation chat "<task>-2" with the resume message instead, no retry, no question, but only in a turn the lead typed; in any other turn `start_session` waits for his click or is refused, so send "Continue, no reset" instead); the lead's "Resume previous session" undoes it | CS `CreateConversation` "<task>-2" (title plus "(cont.)", same tags, no `model`) with the resume message; archive the old one once idle (CS `UpdateConversation` `archived` true) | the lead starts a new session (`/new`, or a new `codex`) with the resume message | ask once with `request_user_input` ("Continue <TASK-ID> in a new thread?"), then `create_thread` "<task>-2" with the resume message; `set_thread_archived` the old one once idle | the lead opens a new chat with the resume message |
| Move Command Center to a fresh chat (only as command-center.md allows; never clear yourself) | `start_session` (initiation "user_asked", context "fresh", use_worktree false, `name` "command-center", the same effort) with "take over" as its whole prompt, only in a turn the lead typed; never `clear_session` "self" | tell the lead the one line; the lead opens a new conversation and types "take over" | tell the lead the one line; the lead starts a new session and types "take over" | `create_thread` with "take over" as its first message, or tell the lead the one line | tell the lead the one line; the lead opens a new chat and types "take over" |
| Read-only helper (branch review, QA second read, release check, research, facts) | `Agent` in the background (read-only prompt; only its result comes back) | `invoke_subagent` with a read-only prompt | `spawn_agent` with `zcc-reviewer` | the same as the terminal | do it in this chat |
| QA and task chat talk directly | `SendMessage` to the other chat's `local_...` id (both are Command Center's chats) | through Command Center: it writes each QA result verbatim to qa/qa-<pass>.md and tells the lead "fix qa/qa-<n>.md" for the task conversation; on its FIXED line, `send_message` "re-check" to the same QA subagent (it keeps its context) | through the files: each QA pass is a new `codex exec -s read-only ... -o qa/qa-<pass>.md` run (the CLI writes the file, the session cannot); the lead tells the task session "fix qa/qa-<n>.md"; on its FIXED line the next pass re-checks the fixed items and the changed code | as in the terminal, through the files; the lead's "fix qa/qa-<n>.md" can go to the task thread with `send_message_to_thread` | the QA chat writes qa-<pass>.md and tells the lead "fix qa/qa-<n>.md" for the task chat; the task chat adds "FIXED" under "## Stops" and the lead tells QA "re-check" |
| Stop a chat | `stop_session` (only when the lead asks) | the lead stops it | the lead stops it (Esc, or closes the session) | the lead stops it | the lead stops it |
| Archive or revive a chat | `archive_session`, `unarchive_session` | CS `UpdateConversation` `annotations.archived` true or false | `codex archive <id or name>`; revive: `codex unarchive`, then `codex resume <id or name>` with the revive message | `set_thread_archived` true or false | the lead closes or reopens it; the revive message is the same |
| Rename your own chat | `set_session_title` ("self") | CS `UpdateConversation` with `conversationId` $ANTIGRAVITY_CONVERSATION_ID and `annotations.title` | skip (no title call; the session name is set when the lead starts it) | `set_thread_title` on your own thread; Command Center sets "Command Center - <project>" at step 1 and at a takeover without being asked | skip |
| The state prefix in a title | `set_session_title` ("self"; Command Center: a chat it started) with "▶ RUNNING \| ", "⏸ WAITING on <who> \| ", "✋ BLOCKED \| " or "✓ DONE \| " before the title, once per state change | CS `UpdateConversation` `annotations.title` with the same prefixes, once per state change: the task conversation sets its own ($ANTIGRAVITY_CONVERSATION_ID); Command Center fixes a stale one on a conversation it created | skip: the first line of each message says the state (RUNNING, WAITING on <who>, BLOCKED, DONE) and the stop line goes into notes.md | `set_thread_title` with the same prefixes, once per state change (a thread sets its own; Command Center fixes a stale one on a thread it created) | skip (the RUNNING line and the stop types carry the state) |
| Open a chat beside Command Center (only when the lead asks) | `open_session_in` | the lead opens it | the lead opens it | the lead opens it | the lead opens it |
| The next-step box | `wrap_up` with `ask` and `actions` (only for a new decision) | a last line "Decide: <question> (<option 1> / <option 2>)" | a last line "Decide: <question> (<option 1> / <option 2>)" | `request_user_input` with the choices | a last line "Decide: <question> (<option 1> / <option 2>)" |
| The recap (sidebar status) | `wrap_up`'s `recap`: its first sentence is the sidebar status, so a turn ending while its own work runs opens it with the RUNNING line (how-we-talk.md "Stops, RUNNING and titles") | the first line of the last message, and the title prefix | the first line of the last message | the first line of the last message, and the title prefix | the first line of the last message |
| What is on the lead's screen | `get_window_layout` (read-only: the main pane, split panes and pop-out windows); `open_session_in` acts only while this chat is on screen | ask the lead | ask the lead | ask the lead | ask the lead |
| Wait for a chat to go idle | `get_session` now; still running: a `CronCreate` one-shot (load it first when deferred) 2 minutes ahead (recurring false) whose prompt names the exact step; never end a turn only "waiting" | CS `GetConversation` `runState` now; never end a turn only waiting: the lead says "check <TASK-ID>" when it stops | the lead says "check <TASK-ID>" when that session has stopped | `wait_threads` | the lead says "check <TASK-ID>" when that chat has stopped |
| Resume at a set time | `CronCreate` one-shot (load it first with the tool search when the tool list defers it; recurring false; minute, hour, day and month pinned to the reset) with the resume message; this chat must stay open, and idle at that time: a timer fires only between turns, so never leave a turn blocked on a call that waits for the lead | tell the lead the time (or the lead sets `/schedule`); resume on the lead's next message | tell the lead the time; resume on the lead's next message | tell the lead the time; resume on the lead's next message | tell the lead the time; resume on the lead's next message |
| Record a stop | the handoff skill's stop script, `scripts/record-stop.sh` (needs a shell) | the stop script through `run_command` | the stop script in the shell | the stop script in the shell | the same where the tool runs commands; else by hand |
| Read Zoho, post comments, change status | Claude in Chrome: page text and element search first, steps batched, a screenshot only to confirm something visual | the lead's own Chrome through the `chrome-devtools` MCP (`list_pages`, `select_page`, `navigate_page`, `click`, `fill`, `take_screenshot`), under the Browser rules below, at the task's own link only (rule 6); the built-in browser pane only when that MCP is unavailable; comment text, tags, transition and Request Review only on the lead's OK | Codex's browser control at the task's own link only, with the lead's sign-in; otherwise show the lead the comment, tags, transition and Request Review values, and the lead clicks them | as in the terminal | the tool's browser control with the lead's sign-in; without one, show the lead the comment, tags, transition and Request Review values, and the lead clicks them |
| Close a task's browser tabs | the browser tools' close-tab action (Chrome, the app's pane, the automation browser) | `close_page` (chrome-devtools) on the tabs the task opened, never others; else name them | the lead closes them; name them | the lead closes them; name them | the lead closes them; name them |
| Link a chat for the lead | `[title](#local_...)` | its title and task ID | its task ID and folder | its thread title and task ID | its task ID and folder |
| Live form tests (bot checks) | the app's built-in browser pane | a browser with no AI control, or the lead submits | a browser with no AI control, or the lead submits | a browser with no AI control, or the lead submits | a browser with no AI extension, or the lead submits |
| Take over as Command Center (command-center.md, Switching tools) | the lead's phrase alone, no questions: read light; re-check each task (files, site, Zoho by its link); write the holder line "Active Command Center: Claude since <time> (chat: local_...)"; then a continuation chat per open task with `start_session` | the same steps; holder line "Active Command Center: Antigravity since <time> (chat: <conversation id>)"; continuation chats with CS `CreateConversation` | the same steps; holder line "Active Command Center: Codex since <time> (chat: <session name>)"; continuation chats are sessions the lead opens from the briefs | the same steps; holder line "Active Command Center: Codex since <time> (chat: <thread title>)"; set your own title; continuation threads with `create_thread` after one `request_user_input` choice | the same steps; the lead opens each continuation chat |
| Hand over to another tool | nothing to do: the next Command Center takes over from the files (Switching tools) | the same | the same | the same | the same |
| Checkpoint before auto-compact | the Context watch (`references/context-watch.md`) | phase-end checkpoints (the App compacts by itself, with no meter) | the Context watch, from Codex's context left | as in the terminal | the same, from the tool's own meter |

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
  `--dry-run`, from this repo's clone (README, "Use it in Antigravity"). It writes the hard rules ("rule <n>" in the
  table is its number) and the lead's settings block (copied from CLAUDE.md at install) as one marked block in
  `~/.gemini/GEMINI.md`, the only copy (2.11.0), and installs the `task-worker` and `wp-qa` agents and three hooks:
  the handoff brief injected at the start of each conversation, a write that puts a secret into a .md file denied, and
  the evidence gate at Stop (below).
- **Command Center** is the project's main conversation; the lead opens it with `/zoho-command-center`.
- **CS** in the table is Antigravity's ConversationService, called from the shell: `curl -sS -X POST
  "http://$ANTIGRAVITY_LS_ADDRESS/product.v1.ConversationService/<Method>" -H "Content-Type: application/json"
  -H "Connect-Protocol-Version: 1" -H "x-antigravity-csrf-token: $ANTIGRAVITY_CSRF_TOKEN" -d '<json>'`. When the
  terminal sandbox refuses it, rerun only that call outside the sandbox (the app may ask the lead).
- **Task work runs as subagents** of Command Center by default (Subagent mode, below). Only when the lead asks for a
  separate task chat: a top-level conversation Command Center creates, which the lead sees, opens and steers as in
  the Claude app. First prompt: "/zoho-command-center Open the zoho-command-center skill (Worker rules) and
  handoff now, then read tasks/<TASK-ID>/brief.md and follow it." The brief names the build skill to open before each
  phase. Each task conversation keeps its title prefix current, like `set_session_title` in the Claude app.
- **QA** is the `wp-qa` agent: read-only by its rules plus a sandboxed shell (`commandExecutionPolicy` "sandbox") and
  no file-editing tools; the tool list alone is not the guard, as `run_command` can still write. Command Center
  starts it as its subagent only after it wrote `qa/brief.md`, writes its result to qa/qa-<pass>.md verbatim, and runs
  step 5's loop through the same subagents (`send_message`).
- **Context:** the App shows no context meter, so every phase end is a checkpoint (checkpoint.md, notes.md, the
  handoff files); "<task>-2" resumes from it.
- **Browser:** the lead's own Chrome through the `chrome-devtools` MCP (setup: README, "Antigravity and your
  Chrome"), under the Browser rules below; Antigravity's built-in browser pane (its own cookies, no sign-ins) only
  when that MCP is unavailable. Zoho only through the task's own link.
- **Models:** conversations and agents keep the lead's current model (`model: inherit`); another only when the
  lead names it. Agent tool names are the ones seen in real transcripts (a wrong name can hang a subagent):
  `read_file`, `edit_file`, `write_file`, `run_command`, `manage_task`, `update_steps`, `webview_browser`.
- **Evidence gate** (2.8.0): a Stop hook sends a chat back once when its DONE, PART DONE, READY FOR QA or QA report
  names a check with no command output in `tasks/<TASK-ID>/checks.md` (Worker rules: "Cheaper checks, with proof").
- Not verified yet (check on the first task): that a custom agent's `tools` list hides the write tools, that the
  secrets guard's empty answer leaves the app's own permission prompt as it is, how the App shows a subagent's card,
  and what a subagent costs against the lead's quota.

## Codex mode
Task work runs as subagents of Command Center by default, in the terminal and the desktop app (Subagent mode, below;
multi-agent tools `spawn_agent`, `send_message`, `followup_task`, `wait_agent`, `list_agents`, `interrupt_agent`).
Separate task chats only when the lead asks: in a terminal, sessions the lead opens, as in one-chat mode, with the
skill forced and the rules made mechanical (added 24 Nov 2026). The Codex desktop app has
thread tools (`create_thread`, `set_thread_title`, `send_message_to_thread`, `wait_threads`, `list_threads`,
`read_thread`, `set_thread_archived`) and `request_user_input` for choices, but creates a thread only when the lead
explicitly asks: Command Center asks once with choices when the briefs are ready, then creates, titles and follows the
task threads itself (learned 24 Nov 2026: the lead had to type every request). It sets its own title at step 1 and at
a takeover without being asked. The setup, hooks and rules below are the same for both.
- **Setup, once per machine** (on the lead's OK): `python codex/install.py --dry-run`, then without `--dry-run`, from
  this repo's clone (README, "Use it in Codex"). It adds a marked block with the hard rules and the lead's settings
  block (copied from CLAUDE.md at install) to `~/.codex/AGENTS.md`
  (all AGENTS.md files together are read up to 32 KiB), the `zcc-task-worker` and `zcc-reviewer` agents
  (`~/.codex/agents/`), and three hooks in `~/.codex/hooks.json`: the handoff brief at session start, a write that
  puts a secret into a .md file denied, and the evidence gate at Stop. Codex runs a hook only after the lead trusts it
  once in `/hooks` (again after it changes).
- **Force the skill** with `$zoho-command-center` (and `$convert-to-wordpress`, `$figma-to-wordpress`, `$handoff`):
  Codex opens a skill by itself only when it judges it relevant. Skills are read from `~/.agents/skills`.
- **Task work** runs as `zcc-task-worker` subagents (Subagent mode); a separate session only when the lead asks, the
  lead opening it in the project folder, with stops through notes.md ("## Stops") and the lead's "check <TASK-ID>".
- **QA** is the `zcc-reviewer` subagent, read-only by the rule alone: a subagent keeps its parent's sandbox, and an
  agent file cannot set its own. A sandboxed read-only QA only on the lead's word: `codex exec -s read-only`, with `-o`
  saving the final report to qa/qa-<pass>.md.
- **Evidence gate:** the same Stop hook as in Antigravity (it answers "block", and Codex prompts the session again
  with the reason). One push back per turn, so it never loops.
- **Hooks are a second line** (the rules are the first): before relying on them, run `python shared/hook_selftest.py`
  (README) to see that SessionStart, PreToolUse and Stop fire on this machine.
- Not verified yet (check on the first task): `-s read-only` with this machine's Windows sandbox setting, the hook
  field `additionalContextLimit`, and the session names `codex archive` and `codex resume` take.

## T3 Code
T3 Code (added 24 Nov 2026) is a desktop app that runs the real tools as its providers: Claude through the Claude Agent
SDK with the lead's login, Codex through `codex app-server` (its own `~/.codex`), Antigravity through `agy acp` with a
private profile folder. So each provider follows its own column above, with these limits:
| Provider in T3 | Skills | Always-on rules | Hooks | Custom agents |
|---|---|---|---|---|
| Claude | yes (`~/.claude/skills`, plugins) | `~/.claude/CLAUDE.md` | yes | n/a |
| Codex | yes (`~/.agents/skills`) | `~/.codex/AGENTS.md` (the zcc block) | only hooks already trusted in Codex `/hooks`; new or changed ones are skipped silently | yes |
| Antigravity | yes (`~/.gemini/config/skills`) | `~/.gemini/GEMINI.md` and `~/.gemini/AGENTS.md` only: the install writes the hard rules there as a marked block | no (hooks.json is not passed) | no |
- **Rules carry it in Antigravity:** inside T3 its hooks (handoff brief, secrets guard, evidence gate) and the
  `task-worker` and `wp-qa` agents do not run; the hard rules in GEMINI.md still load. Rule 2 (checks with their
  output in checks.md) is the evidence gate there, and Command Center's review checks it.
- **Codex hooks:** after installing or updating the Codex setup, open `codex` once and trust the "zcc:" hooks in
  `/hooks` before using Codex in T3.
- **T3 adds its own instructions** on top of ours and they cannot be turned off; where they differ, the skill's rules
  and the lead's word win, and a chat that is unsure asks the lead.
- **Task chats are T3 threads**, one per task, started with the same first prompt as the provider's column; the status
  prefix goes in the thread's name (T3's rename). Run every thread in the project checkout, never "New worktree": a T3
  worktree has no local handoff files, `tasks/` or parent-folder CLAUDE.md.
- Stay on T3's stable release (not the nightly builds).
- **The trigger phrases work in T3 too** ("set this as command center", "command center", "take over"): T3 loads the
  same three always-loaded places as the tools themselves, the Claude skill description, the Antigravity
  `~/.gemini/GEMINI.md` block and the Codex `~/.codex/AGENTS.md` block, so the phrase sets up or takes over there the
  same way (command-center.md step 1).

## Subagent mode (Antigravity and Codex, the default)
The lead's rule, 24 Nov 2026: where a tool makes separate task chats badly or at a high usage cost, task work runs as
subagents of the one Command Center. In Antigravity, conversations created for task chats came out empty and
mis-titled; in Codex, a Command Center and two task chats used a small plan's limit in about 20 minutes.
- **Brief, then a subagent:** Command Center writes `tasks/<TASK-ID>/brief.md` and starts the task as a subagent
  (Antigravity: `task-worker`; Codex: `zcc-task-worker`) with the brief's path. It starts light: its agent prompt, the
  Worker rules section and the brief, at the brief's effort (Codex: its agent file sets it; Antigravity: the lead's
  setting).
- **Plan, then the go, in Command Center's chat:** the subagent plans by reading only and returns PLAN READY with the
  short plan inline. Command Center shows it in at most 8 lines (what, where, backup, check, rollback) plus the options
  as a numbered list (Codex `request_user_input` where the session has it), with the paths of plan.md, notes.md and
  checks.md for the details, and waits. The lead types the go in Command Center's chat; Command Center quotes it
  verbatim to the same subagent and logs it in notes.md (hard rule 7). Follow-ups, re-plans and QA rounds go the same
  way.
- **QA** is its own subagent (`wp-qa`, `zcc-reviewer`) that runs every check itself (hard rule 11); Command Center
  briefs it and reads its report. In Codex its read-only state rests on the rule.
- **The board** lists each task's subagent (tool, agent, id) and its state; Command Center keeps its own title prefix.
- **Report once per state change** (learned 25 Nov 2026: a Command Center repeated its RUNNING line on every poll of
  the same subagent): one RUNNING line when a subagent starts working, then nothing until its state changes; never a
  repeat while waiting on the same subagent. Details live in the task files, not in the chat.
- **A separate task chat** only when the lead asks for one (Antigravity `CreateConversation`, Codex `create_thread`),
  titled "⏸ WAITING on <lead> | ..." until it runs; the columns' "Start a task" row says how.

## Browser rules (any tool that drives the lead's own browser)
Learned 25 Nov 2026: Antigravity could only drive its own browser pane, so it now drives the lead's Chrome through the
Chrome DevTools MCP, which sees every tab of that browser.
- List the open pages first (titles and addresses only) and act only on the task's own tabs: its site, its local or
  staging copy, and Zoho by the task's own link. Never read, change or close any other tab.
- Never read or type a password, key or code; sign-ins stay the lead's. A page asks for one: stop and name the
  service (SKILL.md, the sign-in rule).
- Open the task's pages in new tabs and close only those at close-out.
- Live form tests stay in a browser with no AI control attached (the row above): a controlled browser is scored as
  a bot.

