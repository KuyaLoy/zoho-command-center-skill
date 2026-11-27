# Changelog

Every change to the skill, newest first. Versions follow [Semantic Versioning](https://semver.org); the format
follows [Keep a Changelog](https://keepachangelog.com).

## [Unreleased]

## [2.12.0] - 2026-11-27

Token diet (the lead, 27 Nov 2026: fewer tokens per chat, and long requests simplified before they go out). Effort
stays high.

### Added

- `references/brief.md`: the brief of about 8 lines (goal and why, quality bar, tools and facts, freedom to re-plan,
  "Checks required:", where it goes, the goal in one line), the lead's words quoted once at the top of brief.md, and
  never a restated Worker rule. Also the checks list: one `Pass|Fail | line | evidence` line per check in checks.md,
  objective lines only, each pointing to its "## <check>" evidence section.
- Chat or subagent (SKILL.md, command-center.md step 2): its own chat for work that needs the lead's go, live changes
  or long work; a background subagent for read-only work (branch review, QA second read, release check, research,
  facts); a fresh chat for each new task or release. Tool map row "Read-only helper".
- `tests/test_token_diet.py`: the template's checks line is read by the evidence gate, the self-check phrases are
  gone, the chat choice and the move are in place.

### Changed

- Command Center step 2's brief bullet points to the template instead of listing rules the worker already loads (no
  change before the go, stops, Context watch, Recommended additions); "All rules at the plan" points to the
  template's "only when it applies" lines; a request is quoted at the top of brief.md.
- Command Center moves itself to a fresh chat at milestones (about 200K tokens, nothing pending) with the phrase
  "take over", and never clears itself; replaces the 19 Nov self-reset. Tool map row "Move Command Center to a fresh
  chat" replaces "Reset Command Center"; step 1's replaced-rules list and the README follow.
- Self-check lines removed (the Opus 5 guidance: remove them rather than rewrite them): SKILL.md's quality line,
  "we fix and prove working", Phase 1's "Verify the brief's key facts" and "verification (prove every item is done)",
  the Final report's "done and verified"; qa-chat.md "verify each"; context-watch.md; builds.md and code-quality.md
  "self-check" become checks.md lines; step 5's spot check becomes a read of the checks list.
- Hard rule 2: a "Pass|Fail" line and a "## <check>" section in checks.md (all four copies regenerated). Worker rules'
  "Cheaper checks, with proof" points to hard rule 2 and the evidence gate instead of restating the format.
- QA, helper or review chats: QA stays a visible chat; read-only helper work goes to a subagent.

## [2.11.2] - 2026-11-27

The leads portal is optional (the lead, 27 Nov 2026: "not needed anymore"; leads go by email and the form's own store).

### Changed

- Wherever the skill treated the leads portal as required, it now applies only when the lead's settings name one;
  "none" or no line means no portal step anywhere: SKILL.md's settings line, command-center.md step 2 (the brief's
  leads portal line) and step 5 (the go-live review), `references/leads-portal.md` (skip it without a portal) and the
  README's settings template. Nothing else changed.

## [2.11.1] - 2026-11-25

One simple phrase sets up or takes over a Command Center (the lead, 25 Nov 2026: no long prompt just to take over,
and a short summary of the last job or two).

### Added

- **Trigger phrases** in the skill's description and in the always-on rules of every tool (a new first line of the
  hard rules, so the skill opens even where the model would not pick it): "set this as command center", "command
  center", "take over" or "gawin mong command center", any case; in Codex `$zoho-command-center` still works.
- **Step 1 from the phrase alone:** an empty or new folder is set up; an existing Command Center (any skill version,
  any tool) is taken over at once (Switching tools, reading light), with what an old layout lacks added (holder line,
  open requests, board columns) and all its history kept; continuation chats or subagents only for open work.
- **The takeover brief:** at most 10 lines, always Project, Last jobs (the last 1 or 2 from the newest eod/ files and
  handoff.md's Changes Made: task ID, what was done, state, date), Open now, Next. Switching tools' takeover reports it.
- `scripts/takeover_brief.py` (in the skill folder, so every tool's installed copy has it): drafts the takeover brief
  from handoff.md, the newest eod/ files and ai-handoff-summary.md, in at most 10 lines; it writes nothing.
- Tests: the phrases in the description and in every rule copy; the brief's order; a fixture project with an old
  Command Center (eod/ files, Changes Made, a board) gives the 10-line brief with the last 2 jobs.

### Changed

- **Taking over is effortless** (the lead, 25 Nov 2026: one person uses these chats, never two at once): no handover
  step, no questions, no waiting on the old chat. The holder line in handoff.md is a record, never a lock or a check:
  the phrase (or simply working with a chat in another tool) makes that chat the Command Center; it overwrites the line
  silently, marks the old chats "moved to <tool>" on the board and logs one line. "Switching tools" is simplified to
  match and names T3 Code; hard rule 6 says the Command Center the lead works with writes the root files.
- Tool map, T3 Code: the trigger phrases work there too, from the same three always-loaded places (the Claude skill
  description, the Antigravity `GEMINI.md` block, the Codex `AGENTS.md` block). "Hand over to another tool": nothing
  to do.

Re-run both installs (the rule block changed).

## [2.11.0] - 2026-11-25

Usage fixes (the lead, 25 Nov 2026: "check any redundant that will cost as usage"). Every rule stays; chats load less.

### Changed

- **SKILL.md is about 5,000 tokens** (33 KB to about 20.7 KB): detail moved unchanged into five new reference files,
  each with an "open when" pointer left in SKILL.md: `references/task-size.md` (effort, usage pacing, builds),
  `how-we-talk.md` (versions and waiting, stops, RUNNING and titles, the next-step box, gos, Vocalise early, no
  change before the go, only the task, re-plan, your tool, done and close-out), `safety.md` (deleting records, a
  serious finding, live form tests, browser tabs, handoff files), `context-watch.md` (the task chat's part) and
  `qa-chat.md` (the QA chat and the task chat's part). Section names and the hard rules stay in SKILL.md; references
  point to the new places.
- **No CLAUDE.md read per chat in Antigravity and Codex:** both installs copy the lead's "Zoho Command Center
  settings" block from `~/.claude/CLAUDE.md` into their managed block at install time (local files only, never this
  repository; never printed). The rules' "Settings:" line becomes "Settings (copied ... at install; open that file only
  for a rule not covered here)". No CLAUDE.md or no block: the old pointer line stays and the install says so. Re-run
  the install after changing the settings.
- **One rules copy in Antigravity:** the hard rules and the settings live only in the `~/.gemini/GEMINI.md` block
  (Antigravity and T3 load it always); the install removes the `config/rules/zcc-hard-rules.md` it installed before
  (only that marked file).

### Added

- Tests: no rule of 2.10.2 lost (every bullet and paragraph of a 2.10.2 snapshot is still in SKILL.md or a reference
  file, word for word), every moved part has a pointer, SKILL.md under 21 KB; the settings copy (both installs,
  re-run, missing CLAUDE.md, never printed, never in the repo); the old rules file removed, a foreign one kept.

Re-run both installs (Command Center does).

## [2.10.2] - 2026-11-25

Antigravity works in the lead's own Chrome (the lead, 25 Nov 2026: Claude and Codex controlled Chrome, Antigravity
could only use its own browser pane).

### Added

- **Browser rules** (tool map; hard rule 6 in short): list the open pages first and act only on the task's own tabs
  (its site, its local or staging copy, Zoho by the task's link); never read or type a password, key or code, sign-ins
  stay the lead's; close only the tabs the task opened; live form tests stay in a browser no AI drives.
- `antigravity/install.py --with-chrome` (opt-in): adds the `chrome-devtools` MCP server
  (`npx -y chrome-devtools-mcp@latest --autoConnect`) to `~/.gemini/config/mcp_config.json`, idempotent, with a backup;
  it never prints, changes or removes another server, and keeps a `chrome-devtools` entry set differently.
  `--uninstall --with-chrome` removes only that exact entry. README: "Antigravity and your Chrome" (the Chrome remote
  debugging toggle, a new conversation, a work-only Chrome profile).

### Changed

- Tool map, Antigravity: the browser is the lead's Chrome through the chrome-devtools MCP (`list_pages`,
  `select_page`, `navigate_page`, `click`, `fill`, `take_screenshot`, `close_page`); the built-in browser pane only when
  that MCP is unavailable. The Claude and Codex columns are unchanged.
- SKILL.md: the live form test line names any AI-driven browser (an extension or an MCP).

Re-run the Antigravity install (rule 6 changed); add `--with-chrome` if the chrome-devtools entry is not there yet.

## [2.10.1] - 2026-11-25

Hotfix: in Antigravity the secrets guard blocked every file write.

### Fixed

- **Antigravity hooks always answer with a decision.** On a clean write the secrets guard answered `{}`, which
  Antigravity treats as deny, so every write_file and edit_file was blocked (found 25 Nov 2026; the self-test had only
  proved that a password write is blocked). Now: "allow" for a write inside the conversation's workspace, "ask" outside
  it or when no target is named, "deny" for a secret in a .md file, and "ask" when the hook itself fails. The evidence
  gate answers "stop" when a report passes (never an empty answer), the session-start hook an empty `injectSteps`, and
  the self-test hook "ask". Codex keeps "no output" for a clean write, which it reads as no decision.
- The Antigravity install re-enables a zcc hook that was set to `"enabled": false` and says so.
- **The evidence gate sends a report back only once per turn in Antigravity.** Its CLI leaves `continuationActive`
  false on the second Stop of a turn, so the gate also counts `executionNum`; and a check listed as "not checked" is
  the honest answer hard rule 2 asks for, so it needs no output (a required check still has to be listed).

### Added

- `shared/agy_smoke.py --run`: an opt-in test with the real Antigravity CLI in a throwaway folder: a clean write goes
  through, a password write is denied, a normal turn ends cleanly with the gate (under 60 seconds), and a DONE report
  with no checks.md is sent back once and then ends. All four passed on 25 Nov 2026 with agy 1.5.16. Tests for allow,
  ask, deny, errors, the re-enable and the gate's one push back.
- Report style in subagent mode (the lead, 25 Nov 2026): the RUNNING line once per state change, never repeated while
  polling the same subagent; PLAN READY in at most 8 lines (what, where, backup, check, rollback) plus the options as a
  numbered list, details in the task files. Hard rule 9: "once per state change".

Re-run the Antigravity install to get the fix (and the Codex one for rule 9).

## [2.10.0] - 2026-11-24

One Command Center with subagents in Antigravity and Codex, the same hard rules in every tool, and a lighter start
(this release also carries the unreleased 2.9.3 work). The lead's rule, 24 Nov 2026: where a tool makes separate task
chats badly or at a high usage cost, task work runs as subagents of the one Command Center, and the rules are the same
in every tool.

### Added

- **Subagent mode, the default in Antigravity and Codex** (tool map "Subagent mode", new rows in the Antigravity and
  both Codex columns; command-center.md step 2; SKILL.md "Subagent mode"): Command Center briefs a task and starts it
  as a subagent (`task-worker`, `zcc-task-worker`); the subagent plans by reading only and returns PLAN READY; Command
  Center shows the plan with choices; the lead types the go in Command Center's chat and it is quoted verbatim to the
  subagent and logged in notes.md; follow-ups, re-plans and QA rounds go the same way. QA is its own subagent
  (`wp-qa`, `zcc-reviewer`) that runs every check itself; in Codex its read-only state rests on the rule (a subagent
  keeps the parent's sandbox). The board names each subagent and its state. A separate task chat only when the lead
  asks for one, titled "⏸ WAITING on <lead> | ..." until it runs.
- **One source for the hard rules** (`shared/hard-rules.md` and `shared/hard_rules.py --write`): it writes the
  Antigravity rule file (and so the GEMINI.md block), the Codex AGENTS.md block and a new "Hard rules" section in
  SKILL.md, so Claude carries the same 11 rules. Rule 7 per mode: the go is typed in the task chat (Claude) or in the
  Command Center chat for a subagent (Antigravity, Codex), quoted to the subagent. Rule 9 covers subagents (state on
  the board); rule 11 names each tool's QA. A test checks all four copies match.
- Agents for subagent mode: `task-worker` returns PLAN READY and works only after the quoted go; the Codex agents are
  now named `zcc-task-worker` and `zcc-reviewer`, and the reviewer runs every check itself.

### Moved

- The Lean code, Clean code, Bulk scripts and "The project folder is the site" rules moved unchanged from SKILL.md to
  `references/code-quality.md` (SKILL.md keeps pointers), to make room for the Hard rules section under the line cap.

### From 2.9.3 (never released on its own)

A lighter start (learned 24 Nov 2026: a Command Center and two task chats used three quarters of a small Codex plan's
5-hour limit in under 20 minutes). Every rule stays; chats load less, and later.

### Changed

- **Session-start hook** (both tools): injects only the summary's Status line, "## Now", "## Next action" and any
  "Waiting on" line, at most 1,500 characters, with the full summary's path; Codex `additionalContextLimit` 2000.
- **Load on demand** (SKILL.md "Files"): each role opens only the section it needs; task chats never open
  command-center.md; Command Center opens the step it runs; the tool map only for its own tool's column and mode.
- **Takeover reads light** (Switching tools): the summary, the holder line, the board and each open task's
  "## Stops" and checkpoint; handoff.md history only for what a check needs.
- **Shorter always-on rules:** the Antigravity rule file (and so the GEMINI.md block) and the Codex AGENTS.md block
  say the same 11 rules in about half the words (3,870 to 1,832 bytes; 2,656 to 1,811); rule 1: open the skill
  section you need.

### Added

- **QA runs its own checks** (learned 24 Nov 2026: Command Center took the screenshots and ran Lighthouse itself, QA
  only reviewed them; the shots showed the top of each page and a preloader, and an LCP of 4 to 5 s passed as
  "0 defects"). Rule 11 in both rule files: QA runs every check itself; Command Center never runs QA checks, it
  briefs and reads the report. Step 5 and the QA brief: full-page screenshots after the loading state has finished
  and one scroll has triggered the reveals; the speed check measures the source or preview as the baseline, and an
  LCP above 2.5 s or clearly worse than the baseline is a finding. The `wp-qa` agent says the same.
- Tool map: a "Keep usage low (small plans)" row for every tool. README: "Keep usage low".
- Tests: the hook's output cap and kept lines, the rule files' size and all 11 rules, the load-on-demand wording.

Re-run both install scripts: the hooks and the rule files changed.

## [2.9.2] - 2026-11-24

Codex desktop app and polish from the lead's first runs in Codex and Antigravity.

### Added

- **Codex desktop column** in the tool map (the terminal one is now "Codex terminal"): the app creates a thread only
  on the lead's explicit request, so Command Center asks once with `request_user_input` choices when the briefs are
  ready, then creates each task thread (`create_thread`, first prompt = the brief line), titles it
  (`set_thread_title`), follows it (`wait_threads`, `read_thread`), sends follow-ups (`send_message_to_thread`) and
  archives it at close-out (`set_thread_archived`). It sets its own title at step 1 and at a takeover unasked.
- **Evidence gate:** a report is also sent back when its "Checks:" line leaves out a check that the task's brief (or,
  for a QA report, the QA brief) names in its "Checks required:" line. Step 2's briefs carry that line; a QA brief
  always names the visual check (screenshots at the widths compared) and the speed check.

### Changed

- **Plan review in the task chat:** PLAN READY shows the plan itself (the short plan inline, plan.md's path) and asks
  for the go there, with choices where the tool has them; an "approved" typed in Command Center approves only the
  briefs, never a task's plan.
- **Effort in Codex and Antigravity:** the lead's chosen effort is the task chats' default (usage); high only for an
  L task or live or irreversible work, said in one line. The Claude app keeps its table.
- **Created-chat title:** a chat created without a running first prompt starts as "⏸ WAITING on <lead> | ", never
  "▶ RUNNING" (Antigravity with an empty prompt, a Codex thread before its first turn).
- Hard rules (Antigravity rule file, GEMINI.md block, Codex AGENTS.md block): rule 2 names the required checks. Re-run
  both install scripts to get this and the new evidence gate.
- SKILL.md: four lines tightened to stay at 329 lines.

## [2.9.1] - 2026-11-24

T3 Code support: the rules reach every provider T3 Code runs.

### Added

- The Antigravity install also writes the hard rules as a marked block into `~/.gemini/GEMINI.md`, built from the rule
  file: T3 Code runs Antigravity with a private profile that loads GEMINI.md but not `config/rules`, hooks or agents.
  The rest of GEMINI.md stays, a backup is written first, a second run changes nothing, and `--uninstall` removes only
  the block.
- Tool map: a "T3 Code" section (skills, rules, hooks and agents per provider; Codex hooks must be trusted in Codex
  first; T3's own instructions; task chats as T3 threads renamed for the status prefix, run in the project checkout,
  never "New worktree"; T3 stable). README: "Use it in T3 Code".
- Tests for the GEMINI.md block (add, idempotent, uninstall, other text kept, same rules as the rule file).

### Changed

- The marked-block code is shared by the Codex and Antigravity installs (`shared/setup_lib.py`).

## [2.9.0] - 2026-11-24

Switching tools: one project's Command Center can move between the Claude desktop app, Antigravity and Codex (a lost
subscription, a move back). Two Command Center chats may exist; only one works at a time.

### Added

- **Switching tools** (references/command-center.md): the holder line in handoff.md, `Active Command Center:
  <Claude|Antigravity|Codex> since <YYYY-MM-DD HH:MM> (chat: <id or name>)`; only the holder writes the root files,
  `eod/`, the board, Zoho comments and status. Handing over (checkpoint, log, stop writing), taking over (read every
  task folder, re-check each task's real state, write the holder line, report in 6 lines), continuation chats in the
  new tool for each open task (the old chat marked "moved to <tool>"; the lead's go still covers the approved plan;
  a task waiting on the go stays waiting), and switching back the same way.
- Tool map: "Take over as Command Center" and "Hand over to another tool" rows for every tool.
- Board: the Chat column names each chat's tool (`Claude:`, `Antigravity:`, `Codex:`).
- Hard rules (Antigravity rule file, Codex AGENTS.md block): Zoho comments, status and the root files only by the
  Command Center in the holder line. Re-run each tool's install script to get this line.
- Tests: the holder-line format, the takeover steps in each tool's column, the hard-rule line.

### Changed

- SKILL.md: "Which role am I?" names the holder line; the Worker line sends stops to notes.md when the holder is
  another tool; two lines tightened (328 lines). Step 1 writes the holder line in a new project and checks it in an
  existing one.

## [2.8.0] - 2026-11-24

Codex mode and the evidence gate.

### Added

- **Codex column in the tool map** and a "Codex mode" section: task chats are separate sessions the lead opens with
  `$zoho-command-center` (Command Center writes the brief and keeps the board; stops through notes.md); QA is its own
  read-only session (`codex exec -s read-only`, `-o` saves the report to qa/qa-<pass>.md), never a subagent; skills
  forced with `$name`; AGENTS.md files read up to 32 KiB.
- **Codex setup** (`codex/`): a marked AGENTS.md block with the hard rules, the `task-worker` and read-only
  `reviewer` agents (TOML), three hooks in hooks.json, and `codex/install.py` (dry run, idempotent, touches only its
  own marked pieces, backups, `--uninstall`). Codex runs each hook only after the lead trusts it in `/hooks`.
- **Evidence gate** in both tools: a Stop hook sends a DONE, PART DONE, READY FOR QA or QA report back once when a
  check named in its "Checks:" line has no command output in `tasks/<TASK-ID>/checks.md` (Antigravity: continue;
  Codex: block). SKILL.md Worker rules: "Cheaper checks, with proof" (checks.md and the Checks line).
- **Hook self-test** (`shared/hook_selftest.py`): installs a log-only hook, reports whether SessionStart, PreToolUse
  and Stop fired in Antigravity and Codex on this machine, and removes it.
- Check workflow: the Agent Skills spec check (`.github/scripts/skill-spec.py`) and all setup tests (`tests/`).

### Changed

- The hooks moved to `shared/hooks/` and take `--tool antigravity|codex`; the Antigravity install adds the evidence
  gate. README: "Use it in Codex", "The evidence gate and the hook self-test".
- SKILL.md: description, Files line and Worker line name Codex mode; three lines tightened to keep it at 329 lines.

## [2.7.0] - 2026-11-24

Antigravity mode, from a build run in Antigravity where the chat skipped the skills, guessed defaults, reported
checks it had not run and opened the wrong Zoho page.

### Added

- **Antigravity column in the tool map** (references/tool-map.md) and an "Antigravity mode" section: Command Center
  creates each task chat as a top-level conversation (ConversationService `CreateConversation`, task ID tag, first
  prompt that opens the skills and the brief), reads its state with `GetConversation`, archives it with
  `UpdateConversation`; no model is passed, so every conversation keeps the lead's current model; every chat keeps
  the same title prefixes as in the Claude app ("▶ RUNNING | ", "⏸ WAITING on <who> | ", "✋ BLOCKED | ",
  "✓ DONE | "); QA is the read-only `wp-qa` agent, started by Command
  Center only after `qa/brief.md` exists; a checkpoint at every phase end (the App has no context meter); Zoho only
  by the task link.
- **Antigravity setup** (`antigravity/`): an always-on rule file with the hard rules written out, the `task-worker`
  and `wp-qa` custom agents (the lead's current model; tool names from real transcripts; QA read-only by its rules plus
  a sandboxed shell), a SessionStart hook (injects ai-handoff-summary.md) and a PreToolUse hook (denies a
  write that puts a password, key or token into a .md file). `antigravity/install.py` installs them into
  `~/.gemini/config/` (dry run, idempotent, never touches a file it did not install, backs up hooks.json,
  `--uninstall`). Tests in `antigravity/tests`, run by the check workflow.
- README: "Use it in Antigravity".

### Changed

- SKILL.md: the description and the Files line name Antigravity mode next to one-chat mode.

## [2.6.0] - 2026-11-23

Vocalise early: what a site lacks is raised at the plan, not at the end.

### Added

- **Vocalise early** (SKILL.md, next to "Do only what was assigned"): a task that builds or changes a website
  assesses form attribution, SEO, site speed, testing and tracking at the plan. Its plan and the top of PLAN READY
  carry "Recommended additions", one line per area with size ("nothing to add" is valid); the lead decides, and none
  is built without the lead's OK. Form attribution on the lead forms a build makes is the build skill's default.
  Anything else that changes the work is said in one line as soon as it is known, never first at done.
- Worker Phase 1: the plan and PLAN READY carry the Recommended additions.
- Command Center step 2: the brief asks for them; step 5: the review checks they were raised at the plan.

## [2.5.3] - 2026-11-20

The chat's state in its title, as the sidebar shows only titles.

### Added

- **State at the front of the title** (SKILL.md, How we talk; Worker stops): a chat keeps its state as a prefix of
  its own title, "▶ RUNNING", "⏸ WAITING on <who>", "✋ BLOCKED" or "✓ DONE", set once per state change; never for
  anything else, no polling or extra turns. Command Center's own title stays as it is.
- Command Center step 2 starts each task chat with "▶ RUNNING | " in its title; step 3 reads the prefix as the
  chat's state and may fix a stale one on a chat it started. Tool map: a state prefix row (other tools skip it).

### Changed

- The helper skills table moved unchanged from SKILL.md to `references/helper-skills.md` (SKILL.md keeps a two-line
  pointer), to stay under the line cap.

## [2.5.2] - 2026-11-20

A visible sign that a chat is still working.

### Added

- **RUNNING, not stopped** (SKILL.md, How we talk): a turn that ends while the chat's own work keeps running (a
  background command, a subagent, a check) opens its last message, its recap's first sentence and the progress
  page's Now line with "RUNNING, not stopped: <what>, started HH:MM; I continue by myself when it finishes." It is
  not a stop (no stop message, no extra turn, no polling), and a real stop never uses it. The Worker stop types say so.
- Command Center step 3: a task chat idle with a RUNNING line is working, not stalled; check its work before calling
  it stopped. Tool map: a recap row (its first sentence is the sidebar status).

## [2.5.1] - 2026-11-20

From a build retro: no idle nights, every rule at the plan, live status, QA that converges.

### Fixed

- A refused reset left a task chat idle for 7 hours overnight. Cause (from the transcript): the continuation chat was
  started in a turn a chat's CHECKPOINT had started, not the lead; the app waits for the lead's click there, so the
  start blocked the whole turn until morning and the turn's timers never fired. Now the continuation chat starts only
  in a turn the lead typed; in any other turn the chat gets "Continue, no reset" (under 75%) and its next CHECKPOINT
  tries the clear again; at 75% it waits at its checkpoint for the lead's next turn. A usage stop still wins.
- When the lead leaves with work running, Command Center does any due reset in that same turn and asks him to leave
  Command Center on screen with no task chat open, so clears work overnight. Tool map: the window layout row, and
  a set-time resume needs this chat idle (a timer fires only between turns).

### Added

- Step 2: all rules at the plan: the brief carries every rule the task needs (forms, placeholders, the build skill's
  live checklist, the leads portal), so nothing arrives mid-build.
- Step 3: status from the task's own progress page or tracker; a page older than the chat's current step is a stop
  to fix, one line to the task chat. A skill update for a running task, on the lead's word, applies at the boundary
  Command Center names (its next site or phase end), never inside a QA run.
- Step 5: QA converges as the build skill says (one full run, then the fixed items and changed code); the review
  never asks for an extra full run.
- Worker rules: what to do on "Continue, no reset".

## [2.5.0] - 2026-11-20

The leads portal in every go-live.

### Added

- A "Leads portal" setting (optional; the admin URL lives only in the settings).
- `references/leads-portal.md`: the company's leads portal keeps every lead even when the site's email fails. Required
  on every live site with a lead form, for every new build and every go-live (existing live sites as their own task;
  the lead can exclude a project). Command Center picks the way by stack: the convert-to-wordpress leads sender for
  kit-built WordPress sites, the same sender as a must-use plugin for other WordPress sites, the portal's PHP or
  Next.js example, a finding for platforms without our server code. The lead is sent whether the email worked or
  not; the endpoint and key only on live, pasted by the developer, never in git, notes or reports; proof at go-live
  is the GET check and one TEST lead per form in the portal.
- Step 2 puts the way in the brief; step 5's review checks the proof before the close-out comment.

## [2.4.6] - 2026-11-20

### Changed

- A refused reset never waits on the lead (Context watch, Command Center's part; tool map): when clearing a
  checkpointed chat is refused because it is open or pinned on the lead's screen, Command Center doesn't retry or
  ask; it starts a continuation chat "<task>-2" with the resume message (the go quoted), updates the board, tells
  the lead in one line and archives the old chat later. A refused archive waits for step 1's sweep or the close-out.
  A revive uses the task's newest chat.

### Added

- Ask the lead only for real decisions or blockers (Shared rules, next to No silent idle): the plan go, the comment
  OK, a sign-in, missing information.

## [2.4.5] - 2026-11-19

### Changed

- Usage pacing: working chats stop at 95% of the weekly limit, raised from 80% (the lead's rule, 19 Nov 2026: the
  last 20% of the week went unused). The 5-hour stop stays at 95%. SKILL.md and README.

## [2.4.4] - 2026-11-19

### Fixed

- The stall rule where every chat sees it (Shared rules): never end a turn waiting for another chat to go idle;
  check now, else a one-shot check in 2 minutes naming the exact step (load the scheduling tool first if it is
  deferred), one more, then tell the lead. 2.4.3 had it only in references/command-center.md, which a Command Center
  that reloaded SKILL.md alone did not re-read, so two chats stalled again.
- A reload always re-reads the references: "Which role am I?" and the version-check rule say Command Center reads
  references/command-center.md and tool-map.md again; a reload of SKILL.md alone is not one.
- Tool map: the one-shot scheduler is loaded first when the tool list defers it.

## [2.4.3] - 2026-11-19

### Fixed

- No stall after a CHECKPOINT (Context watch, Command Center's part): Command Center never ends a turn waiting on
  another chat to go idle. For every step that needs a chat idle (a clear, an archive, a revive, the close-out) it
  checks the chat's state now; still running, it sets a one-shot check in 2 minutes naming the exact step (tool map),
  then one more, then tells the lead.
- Revived and resumed chats keep their stop signal: the revive and resume messages repeat "Send Command Center
  (parent) a short message at every stop", as a revived chat may not bring back its wake notes.

## [2.4.2] - 2026-11-19

### Added

- Command Center re-checks the task's Zoho comments at PLAN READY, at the go and before drafting the close-out
  comment (step 4, with steps 3 and 6): as text, only newer comments, plus new attachments or a changed
  description, logged as "comments to <date time>" in the board row. A change goes to the task chat as a re-plan; the
  close-out comment answers anything new; a new request outside the plan is never silently skipped.
- Use the newest skill version (Shared rules): a "Version:" line at the top of SKILL.md; Command Center on its first
  turn (and after a reset) and task chats at a new task or a revive compare it with the installed file and reload
  the zoho-command-center and handoff skills when the installed one is newer. The release guard checks the line
  matches plugin.json (AGENTS.md release step).

### Docs

- README Update: a release reaches every Command Center the next time it is used; reload messages to every chat are
  not needed.

## [2.4.1] - 2026-11-19

### Changed

- Max for the plan when the task needs it (Task size and effort; command-center.md Effort, steps 2, 3 and 4; tool
  map): Command Center starts the task chat at max for Phase 1 for every L task and an unclear or risky M (a new
  approach, several systems, data or SEO at scale, a conversion or build plan), says so in one line before the start,
  and sets it back to high at "GO" before the first work step. High stays the default; a re-plan after the go stays
  at high; "use max" still raises any part the lead names. Replaces 2.1's "max only when the lead says use max".

## [2.4.0] - 2026-11-19

Quality of the work, and the Zoho status at the go.

### Changed

- Status at the go (step 3, step 6, Worker Phase 2): after the lead's go on the plan the task chat sends "GO:
  <TASK-ID>" (not a stop report) before its first step, and Command Center clicks the start transition then, so the
  team sees the work in progress. Close-out keeps only Request Review, after QA 0 and the posted comment. A task
  blocked after the start keeps its status; Stop Developing only on the lead's word. Replaces "the lead's go starts
  the work, NOT the Zoho status".
- Re-plan after the go (Worker rules): a method or scope change from the lead rewrites those plan.md steps in place
  (never "see notes"), then PLAN READY and a new go; plan.md always matches the work.

### Added

- Clean code (Shared rules): enqueue CSS and JS; theme or builder globals, never hex or font copies; the project's
  prefix; one shared helper per piece of logic; data in data, not code; custom PHP in a versioned file (or a copy in
  `build/` for snippet-only sites); SEO plugin variables for generated titles; selectors or IDs, never positions.
- Bulk scripts are safe to re-run: check by slug or ID before each create; never trash or delete in a script;
  duplicates trashed by explicit ID.
- QA reviews code: the first pass reads every added or changed file against Clean code and security.
- Close-out records: a 403 for `tasks/` before a database dump goes there; the posted Zoho comment saved in
  report.md; "tabs closed: <ids>" in the task chat's notes; handoff.md's Current State and Next Steps rewritten.
- Details from the dry read: GO updates the board row only (no EOD line), no quoted go means no click, a re-plan's
  go is sent as "GO: <TASK-ID> (re-plan)"; a method change lists affected done steps with their undo and stops
  changes until the new go; plan.md names the prefix, which also covers shortcode tags, handles, CSS classes and post
  types; a missing global is added in the theme; a self-check before DONE; clean-code fixes are inside the plan;
  script-created items carry a source key; duplicates keep the linked one (else the lowest ID), links are checked,
  trash only.

## [2.3.3] - 2026-11-19

### Changed

- Zoho in the browser, text first (command-center.md, steps 2 and 6, tool map): Command Center reads Zoho as page
  text or element search, batches browser steps, and takes a screenshot only to confirm something visual (a rendered
  @mention, a dialog's filled fields, a status read-back the text can't show); no full-page text dumps.

### Added

- Real times only (Shared rules): every time in notes, reports, EOD lines and messages comes from the clock, never
  estimated or rounded; the date only when the exact time is unknown.

## [2.3.2] - 2026-11-19

### Added

- Helper skills (SKILL.md Shared rules): when task, QA and build chats use web-quality-audit, performance,
  core-web-vitals, accessibility, seo, best-practices, wp-plugin-development, wp-wpcli-and-ops, wp-performance,
  wp-phpstan and the Chrome DevTools MCP; only when installed, otherwise the current checks; they never add scope,
  steps or approvals.

### Docs

- README Team setup: the helper skills as recommended extras (clone and link for Claude Code, Codex, Cursor and
  Antigravity) and the Chrome DevTools MCP line with both privacy flags.

## [2.3.1] - 2026-11-19

### Changed

- A Command Center reset that is dropped (the lead's message came first) or refused: say nothing more about it and
  try again only at the next safe point.
- Task chats keep wake notes on (step 3, tool map): the 19 Nov test found 4 of 29 wake notes with no stop message
  behind them. Replaces "until a test shows the stop message always arrives". QA chats still start without them.

### Added

- Lean code (Shared rules): use what already exists first (the site's theme, plugin or helper, then the platform,
  then an installed library); no option, wrapper or abstraction nobody asked for; never cut validation, error
  handling, security or accessibility; one small check for new logic with a branch or loop.

### Docs

- README: "Team setup: everything a teammate installs": the four skills' requirements, where each goes in Claude
  Code, Codex, Antigravity and Cursor, what to fill in, and how to check each one loads, taken from their READMEs.

## [2.3.0] - 2026-11-19

Usage: a lean Command Center, a QA loop that runs between the task and QA chats, and cheaper checks.

### Changed

- Command Center resets itself only when it is safe (references/command-center.md): about 200K tokens or the first
  turn of a new day, no chat mid-turn on something it must answer, no unanswered lead message or pending OK, every
  stop recorded, open requests and the board current, the summary just rewritten. One line to the lead first; after
  it, step 1's existing-project path without the status report. Never mid-relay, never twice without new work.
  Replaces the 18 Nov "never clear your own chat" (a usage check showed Command Centers at about 600K tokens and
  half of a day's usage).
- The QA loop runs directly between the QA chat and the task chat (step 5, Worker rules): QA FINDINGS to the task
  chat, FIXED to the QA chat, until QA 0, which goes to Command Center and the task chat. Command Center hears only
  that QA started and QA 0, or a dispute (the task chat re-plans; a normal stop). QA chats start without wake notes;
  a task chat's wake for a loop turn gets no reply. Board phase "QA".

### Added

- Cheaper checks for task and QA chats (Worker rules): curl, wp-cli, a script or a DOM query first; a browser only
  where needed, steps batched; screenshots only as visual proof; no full-page text dumps into the chat.
- Tool map rows: reset Command Center (self-clear) and QA and task chat talking directly, with one-chat fallbacks.
- Reset details: the summary is rewritten in full as the last step, with "Last Command Center reset" and the open
  tabs; no reset while a timed resume is scheduled; the reset line comes before the Next line and the reset call is
  the turn's last tool call; the title stays.
- QA loop details: PAUSED, BLOCKED and CHECKPOINT always go to Command Center; "QA STUCK" after 3 passes without 0;
  after a dispute the task chat tells QA to go on; QA 0 opens the OK message ("QA 0 after <n> passes, <m> items
  fixed") instead of a separate report; a revived QA chat gets its own follow-up message and pass numbers go on;
  resume messages name the loop's pass and the other chat; QA chats start with wake notes off (tool map).

## [2.2.1] - 2026-11-18

### Changed

- EOD (step 3): the EOD answer is the handoff skill's summary block exactly, one block per task worked on that day
  with its links (the staging magic link already shared with the client included), status words as the handoff
  skill says. Replaces 2.2.0's "no custom sections": the handoff skill owns the shape.

## [2.2.0] - 2026-11-18

Lessons from the first real task on 2.1: no change before the go, the site in the project folder, QA before every
Zoho post, a short comment with the status steps, lean plans and EOD, and one close-out sequence.

### Changed

- No change before the go (SKILL.md shared rules, Worker Phase 1 and 2, the brief in step 2): Phase 1 only reads and
  plans, with no download to work from, local copy, install or change anywhere; an answer, a route choice or a
  preference is not a go (re-plan, PLAN READY, wait). Replaces "local work may start right after the plan". A serious
  finding is reported at once and fixed after the go.
- QA before every Zoho post, every size (step 5): a separate read-only QA chat; QA REPORT -> Command Center -> the task
  chat fixes and reports FIXED -> QA re-checks, until 0 findings. An L task's QA chat runs at high on the main model
  and is its review (replaces the L review chat). The QA chat is archived with the task chat and revived for its
  follow-ups (step 2).
- One close-out sequence (step 6): QA 0 -> comment, tags and status steps in one OK message -> post -> status ->
  close tabs -> archive the task and QA chats -> EOD line IN REVIEW -> one line to the lead.
- The Zoho comment in a fixed short shape: greeting, what is ready, links, "Done:" one line per item in the task's
  order, one line on live or staging, a client question only when needed, one line for a serious fix, the CC line. No
  methods, side notes, backup names or "please confirm" lists.
- Status follows the work: a hand-over comment (staging review or done) carries the start transition and Request
  Review in the same OK message, done right after posting; the status never stays "Ready For Development" while the
  work waits on a review.
- Plans: L about 40 lines, no hour or time estimates for any size. EOD: one line per stop in the handoff skill's
  format, IN REVIEW once the work waits on a reviewer or the client, no custom EOD blocks (step 3).

### Added

- The project folder is the site (SKILL.md): a local copy, clone or Duplicator install goes in the project folder
  (`<folder>.test`), backups in `tasks/<TASK-ID>/backup/`, a sibling `<folder>-old` only for a redesign. Step 1's
  whole-folder web block then gives way to the handoff skill's file block plus `tasks/` and `eod/` blocks, each
  checked for 403.
- QA chat rules and the FIXED stop in the Worker rules (one `qa-<pass>.md` per pass, the first pass covers every
  item, a disputed finding goes to the lead as PLAN READY in the task chat); the QA chat in one-chat mode (tool map).
- The site's web block in a safe order (file blocks first, then the whole-folder deny goes, 403 and 200 checks after
  the install), packages and deploys exclude the project notes, and a staging hand-over plans go-live as its own phase.
- Board Phase values QA <pass> and IN REVIEW; the QA chat shares the task's row and closes its tabs at close-out.

### Docs

- README: QA before every Zoho post, no change before the go, the site in the project folder, the short comment and
  status steps.

## [2.1.3] - 2026-11-18

### Fixed

- The "Always CC" line goes in Zoho comments (the Zoho report) only. Reports and chat replies to the lead have no CC
  line, and neither do other reports or reply drafts (the lead's rule, 18 Nov 2026; SKILL.md Settings, step 6,
  README).

## [2.1.2] - 2026-11-18

### Fixed

- The "Always CC" line goes only in Zoho comments and in reports or replies written for the client or team, never in
  chat replies to the lead (SKILL.md Settings, step 6, README): a new Command Center ended its chat reply with it.

### Docs

- README: "Check it works in another AI tool": where Codex, Cursor and Antigravity read skills, a smoke-test prompt
  with its pass marks, and the Codex CLI result (2026-11-18: pass).

## [2.1.1] - 2026-11-18

### Changed

- A task chat waiting on the lead's go or answer is only reported (step 3): no box, no button and no "open <chat>"
  for it; the lead answers in the task chat's own box (the lead's rule, 18 Nov 2026: fewer clicks). Command Center
  opens a chat beside itself only when the lead asks. The box rule in SKILL.md matches.

## [2.1.0] - 2026-11-18

A quiet close-out, the question box only for a new decision, fewer steps per stop, high effort for every size, and a
skill that task chats carry at about half the size and other AI tools can run.

### Changed

- Split: SKILL.md keeps the settings, sizes, roles, shared rules, Context watch thresholds and the Worker rules
  (33 KB to 19 KB, the text every task chat carries). Command Center's steps 1 to 7 (numbers unchanged) and its part
  of the Context watch move to `references/command-center.md`, read by Command Center at start and after any reload.
- Close-out (step 6): after Request Review, Command Center closes its tabs, has the task chat close its own, archives
  the chat once it is idle and tells the lead in one line. No "Close tabs and archive?" question, no reminders and no
  Zoho checks on a task in review; the lead messages Command Center when someone comes back and the same chat is
  revived. Stop Developing, reassigning and editing task fields are still asked first. The Browser tabs rule matches.
- The next-step box only for a new decision (replaces "a box every turn", 17 Nov). After the lead confirms a wait, a
  schedule or "later", turns end with the recap and the Next line only.
- Usage pause: Command Center sets the resume time, says it once and resumes on its own (step 3).
- Context checks on working chats only at PLAN READY and at each stop (step 3 and 4), no longer on every wake note,
  lead message and follow-up.
- One signal per stop: a wake note and a stop message for the same stop are one reply; wake notes stay on until a test
  shows the stop message always arrives (step 3).
- One call to the handoff skill's stop script (`scripts/record-stop.sh`, handoff 1.3) per stop records the EOD line,
  the summary's Last change and Next action and the board row; without it, the same records by hand (steps 3 and 7).
- Routing (step 2) also searches the board's archived rows in `handoff-archive.md`.
- Effort: high for every size, L included; max only when the lead says "use max". The max switch for L chats (raise
  after start, stopped first turn, back to high at PLAN READY, re-plan at max) is removed. L keeps its full plan and
  its review chat (now at high).
- Steps in plain words, so other AI tools can follow them; the description no longer says Claude desktop only.
- `references/builds.md` is marked retired: kept only for a build already running with builder and QA chats.

### Added

- `references/tool-map.md`: each action, its Claude desktop tool and what to do in other AI tools, plus one-chat
  mode (task folders, stops in notes.md, the lead opens task chats and posts drafted Zoho comments when needed).
- A project's own rules in its handoff.md win over the skill's defaults (for example a project that never archives).
- A revived chat plans its follow-up and waits for the lead's go; the earlier go covered the earlier plan only.
- "use max" said in a task chat: the chat tells Command Center ("USE MAX: <TASK-ID> <for what>"), which raises it.
- QA and review chats count toward the 2-chat limit. The usage-pause resume message, one message to the lead for all
  paused chats, and resuming at the lead's next message when the timer did not fire.
- Archive refusals (the lead has the chat open) are handled like clear refusals; the tab-close reply is not a stop.

### Docs

- README: other AI tools (one-chat mode, install by clone and link), the quiet close-out, effort high for every size,
  the new reference files. AGENTS.md: the reference files, frontmatter fields and plain-word steps.

## [2.0.1] - 2026-11-18

### Fixed

- Archive idle task chats (step 1): Command Center lists its own chats with `list_sessions {"linked": true}` (all of
  them) instead of `list_sessions`, whose default list (the newest 20 across all projects) missed its older idle chats.
  Board rows the list doesn't show (chats an earlier Command Center chat started) are checked by id with `get_session`.

## [2.0.0] - 2026-11-18

One task, one chat, straight to the point, and a Command Center that never clears itself and answers from files.
Major: the routing and the Command Center workflow changed.

### Changed

- Routing (step 2): one task, one chat. The same Zoho link or task ID always goes to that task's chat until the lead
  says otherwise (an open chat gets the request; an archived one is revived); anything else gets a new chat. Replaces
  the reuse of an idle chat on the same site under 25%. An archived chat is revived (`unarchive_session`), cleared,
  and resumes from its report.md and notes.md, not from its old conversation.
- Only the task, straightforward: sensible defaults and obvious fixes inside the task are made and listed in the
  report; the lead is asked only about blockers, the client only when really needed (through the Zoho comment or
  reply draft); other clarifications go in the report and that draft.
- Plans: S about 5 lines, M about 20 (was about 40), L in full. Local work (a local copy, a branch, drafts) may start
  right after the plan; the lead's go is needed before live changes, Zoho or the client. The brief line says so.
- Command Center never clears its own chat: the 35% self-reset is removed (no `clear_session` "self" at any %). It
  keeps the root handoff files current at every stop and milestone instead. Task chat resets are unchanged.
- A go is read from the task chat's notes.md, where the chat quotes it at once; Command Center no longer reads
  transcripts to check a go.
- Reviews sized to the task (step 5): S and M, the report plus one live spot check; L keeps the review chat.
- Close-out (step 6): one question, "Close tabs and archive?"; on yes the task chat closes its tabs, then Command
  Center archives it (was a separate "and agents" request).
- Builds: one task chat with the figma-to-wordpress or convert-to-wordpress skill; `references/builds.md` stays only
  for builds already running with builder and QA chats.
- Plugin description: one task, one chat. README matches.

### Added

- No hallucination: Command Center answers from files and checks made now, never from memory; unknown means check
  first. It keeps the lead's open requests (verbatim, dated, with a status) under `## Open requests` in handoff.md,
  reads them first after any compact, reload or new chat, and lists all of them in every report on a round.
- Serious unrelated findings (a hacked site, malware, injected spam, a backdoor) are fixed with the task, backup
  first, as part of its plan and go; the lead gets one line when found, and the report has a "Serious finding
  (fixed)" part. Other unrelated findings stay untouched and listed.
- Archive idle task chats: when Command Center starts, it archives task, QA and review chats idle for 2 days or more,
  never a Command Center or a working chat, and names any of their tabs still open. Board phase ARCHIVED.
- EOD log: Command Center writes one line per stop to `eod/YYYY-MM-DD.md` (format from the handoff skill) and answers
  "EOD" from that file. Task chats never write `eod/`; new projects keep `eod/` out of git.
- A running task keeps its brief and plan rules, so a skill reload or new version mid-task changes nothing for it.
- Worker: after a revive or reset, read report.md and notes.md first; the final report stands alone (decisions,
  obvious fixes, client clarifications, findings).

### Kept

- Effort rules (high floor), usage pacing (2 chats, 95% 5-hour, 80% weekly), task chat context watch (page end from
  50%, cap 75%), Zoho comment and status rules, the next-step box, the "Next:" line, no silent idle.

## [1.4.0] - 2026-11-17

New usage limits from the lead: faster work with fewer stops while the lead is out of the office.

### Changed

- Context watch: under 50% keep working; from 50% finish the current page or unit of work, then checkpoint and
  reset at that boundary (was a flat 40%); 75% is the hard cap, a checkpoint at the next safe point even mid-page, never
  past 80% (were 50% and 55%); fast growth from 65% (was 30%); Command Center asks for a checkpoint at the next page end
  from 50% and at once from 75%; "Continue, no reset." for a chat under 75% (was 50%); step 2's brief line and step 4
  (past 50% at PLAN READY, reset before the go) follow. Why: a flat 50% cut work off mid-page; the cap still stops
  before a big context gets costly on every step.
- Usage pacing: every working chat stops at its next safe point at 95% of the 5-hour limit (was 75%, which left a
  quarter of the window unused).
- README matches the new numbers.

### Added

- Weekly limit: by default every working chat stops at its next safe point at 80% of the weekly limit and Command
  Center tells the lead; a project the lead tells "don't stop" (quoted and dated in its handoff.md rules) runs on to
  100%. Replaces step 4's "tell the lead over 90% before the go".
- Commit or save after every step, so a stop at a limit leaves a clean state.

### Unchanged

- At most 2 chats working; routing reuses an idle chat only under 25%; Command Center resets itself at 35%.

## [1.3.1] - 2026-11-17

Every stop reaches Command Center promptly, whoever started the turn.

### Changed

- No silent idle: a stop also goes to Command Center as one short message, whoever started the turn, the lead's own
  turns included (wake notes for those come late). Shape: "<TYPE>: <TASK-ID> <why it stopped>. Decisions: <defaults
  taken, or none>. Next: <step> — waiting on <who>"; TYPE is PLAN READY, WAITING, PART DONE, PAUSED, READY FOR QA,
  DONE, BLOCKED or CHECKPOINT. The `wrap_up` recap opens with the stop reason. Replaces 1.3.0's "no second message".
- Worker rules: "Plan ready: no message" becomes the stop message above; the task chat brief says the same.
- Command Center step 3: a wake note and a message for the same stop are one stop, reported to the lead once, with
  no reply to the chat.
- Unchanged: the next-step box, the Next line, task chat decisions stay in the task chat, only Command Center posts
  in Zoho.

## [1.3.0] - 2026-11-17

The lead always knows the next step: a next-step box at the end of every Command Center turn, and no chat stops
silently.

### Added

- Command Center ends every turn with the next-step box (`wrap_up` with an ask and buttons), even when nothing seems
  pending. It leads: the first button is its recommendation, "Proceed: <action>", the second a realistic alternative;
  while waiting (a usage pause, a chat working) it still offers the choice.
- No silent idle: every turn that stops without the work going on (plan ready, waiting for a go, checkpoint, usage
  pause, blocked, a part done) ends with a short report: what was done, the state, decisions taken (with the default
  chosen) and the Next line. Its first 400 characters reach Command Center as the wake note, so no second message.

### Changed

- The last line of every turn, in every chat, is "Next: <step> — waiting on <who>" (replaces 1.2.1's "Waiting on
  you" / "Nothing needed from you" line).
- Command Center step 3: on every stop, Command Center tells the lead in 2 to 4 lines which chat, why it stopped, the
  decisions it took and the next step, and never lets a chat sit idle unreported. A task chat's question, options and
  plan still stay in that chat; for the lead's go or answer there, the box offers "Proceed: open <chat>" and "Later".
- Kept: separate messages to Command Center only for READY FOR QA, DONE, BLOCKED and CHECKPOINT; a button reply in
  Command Center is never a go for a task or a phase; only Command Center posts in Zoho.
- Wording tightened to stay under the line cap (Command Center intro, task talk rule).

## [1.2.2] - 2026-11-17

Ties the "Waiting on you" line to the rule that a task chat's decisions stay in the task chat.

### Changed

- Command Center step 3: the one reminder for a task chat that waits on the lead is Command Center's "Waiting on you"
  line with a link to that chat (e.g. "Waiting on you: your go in [ABC1-T8 chat](#local_...)"); still no question,
  options, buttons or plan summary in Command Center.
- The "Waiting on you" rule says a decision that belongs to a task chat stays there; Command Center's line only links
  to it.
- Unchanged and confirmed: only Command Center posts Zoho comments and changes Zoho status; task, QA and review chats
  never post in Zoho.
- One paragraph rewrapped to keep SKILL.md under its line cap. No rule removed.

## [1.2.1] - 2026-11-17

Three flow fixes after a lead could not tell whether a go had worked.

### Added

- Every turn's message to the lead, from Command Center or a task chat, ends with exactly one line: "Waiting on you:
  <one action, where>" or "Nothing needed from you."
- A refused `clear_session` because the lead has the chat open or pinned (Command Center's own clear too): say so at
  once in one line ("Switch away from <chat link> so I can reset it"); a chat under 50% gets "Continue, no reset."
  instead of waiting; a checkpointed chat is never left idle without telling the lead.

### Changed

- Context watch: a chat checkpoints only at the threshold in force (the brief's or plan's, else 40%) or when Command
  Center asks, never earlier "to have room for the next step".
- Wording tightened to keep SKILL.md under its line cap (intro, worker role, browser tabs, Context watch intro, the
  worker's final report now carries the "DONE:" rule). No rule removed.

## [1.2.0] - 2026-11-17

Rules from a multi-chat design build retro: pacing, cheaper contexts, fewer messages, safer deletes, and a builds
reference.

### Added

- Usage pacing: at most 2 chats working at once (others wait as QUEUED); `get_usage` before starting or resuming any
  chat; at 75% of the 5-hour limit every working chat stops at its next safe point.
- Command Center resets itself at 35% context, after updating the root handoff files.
- Go handling: a button reply or "gave go" in Command Center is never a go for a task or a phase; builders start only
  after the build's lead chat confirms the go was typed there.
- Safe deletes: only by explicit IDs, after a dry-run list, a count check and a database backup, never by a filter;
  scratch content carries one marker.
- `references/builds.md`: lead chat, builders and QA chats; one builder by default, no helper subagents without
  Command Center's OK; one consolidated fix list per QA pass; QA by script and sampling; the QA flow; the Figma sweep
  and a checklist row per section.

### Changed

- Context watch: checkpoint and reset at 40% (was 70%), hard limit 50% (was 80%), never past 55% (was 85%), fast
  growth from 30% (was 60%).
- Routing: reuse an existing chat only under 25% context (was 60%).
- Messages to Command Center only for READY FOR QA, DONE, BLOCKED or CHECKPOINT. PLAN READY opens the report to the
  lead and is no longer sent; Command Center reads it in its wake note. An L re-plan is sent as "BLOCKED: re-plan at
  max needed".
- Wording tightened to keep SKILL.md under 330 lines; no rule removed.
- AGENTS.md: the name scan covers commit author and committer emails; merge by fast-forward; `references/`.

## [1.1.0] - 2026-11-16

Effort that fits the task, any task source, routing to new or existing chats, and faster talk without losing quality.

### Added

- "Task size and effort": Command Center sizes every task S, M or L. S and M run at high with short plans; L plans at
  max and works at high. High is the floor: medium only for named read-only or fixed-step work. A read-only QA or
  helper chat may use a cheaper model.
- Routing (step 2): a question is answered without a chat; more work on a task goes to its chat; a new S or M task on
  the same site or repo goes to an idle chat under 60% context; anything else gets a new chat. The lead gets one line
  saying where it went and why, and can override.
- A task chat can take a later task in its own folder, with its own plan and go.
- "How we talk": result first, about 8 lines at most, one decision per question, one go per plan, messages only at
  milestones or blockers; quality checks stay.
- Review of an L task at done runs at max in a visible review chat ("REVIEW REPORT:"), or in Command Center raised to
  max if the lead prefers.
- Board columns: Source / status, Site or repo, Size (added to old boards on resume).
- Release automation: the `check` workflow validates every pull request and makes a skill change come with a new
  version; the `release` workflow tags and publishes each new version. README: how to turn on automatic updates.

### Changed

- Command Center runs at high (was max). Max planning, the PLAN READY switch to high and the RE-PLAN round trip now
  apply to L tasks only; S and M re-plan at once.
- Any task source: step 2 reads Zoho or saves any other request verbatim; step 6 is the close-out, with the Zoho steps
  for Zoho tasks and a reply or report draft for every other source.
- Briefs no longer copy the shared rules: they tell the task chat to load the skill (Worker rules).
- S work that only reads or checks needs no go.
- AGENTS.md: SKILL.md cap raised from 300 to 330 lines.

## [1.0.0] - 2026-11-13

First shared version. The workflow was used daily on more than 20 client projects before this release; this version
generalizes it for any lead and adds the lessons from those projects.

### Added

- Settings block in the user's CLAUDE.md: lead, Zoho portal, reply language, optional Always CC. A project's
  handoff.md can name a different lead.
- Work without a Zoho task: brief saved verbatim, short task name, Zoho status "n/a", a reply draft instead of a
  Zoho comment.
- QA and helper chats: visible, read-only, report "QA REPORT:", never post in Zoho.
- "Our initiative" work stays out of the task's Zoho comment and status.
- Several chats on one site: own ports and temp folders, shared files named, no whole-database restore.
- A login that expires mid-task: stop, tell the lead which service, wait.
- New-project setup: block the folder when a local web server serves it, keep `tasks/` and handoff files out of git.
- At PLAN READY: check the task chat's context (reset from 60% when it is past about 40% after planning) and warn the
  lead when the account's weekly usage is over 90%.
- Resuming an old project: replace project rules this skill has replaced.
- Command Center reads a task chat's transcript to find the lead's go instead of asking again.
- A short definition of the two handoff files for users without their own handoff rules.

### Changed

- Names and company details moved out of the skill into the settings; "the lead" replaces a person's name.
- Zoho status: read the start transition the task really offers ("Start Development", "Start Development Edits",
  tracking transitions) and put the dialog values in the OK message.
- Request Review: handle a reviewer that is not pre-filled, other required fields, and a mandatory comment field.
- A go or an OK to post counts when the lead says it in that chat; a relayed go may be refused.
- Messages to a busy chat are queued: decisions also go in the task files; no plan changes after PLAN READY.
- Zoho comment drafts list attachments; uploads need Chrome in front.
- Closing "tabs and agents" also archives the task chat; archive waits for an idle chat, unarchive before messaging.
- Tabs the Chrome tools can no longer reach are listed for the lead to close by hand.

### Fixed

- The Zoho start button is "Start Development", not "Start Developing".
- `start_session` with context "fresh" needs `background` (80+ characters).
- `clear_session` is refused while the chat is mid-turn, pinned or open on screen: wait, and ask the lead to switch away.
- Effort is confirmed with `get_session` only; the picker and turn markers can lag.
- The skill's YAML frontmatter did not parse (an unquoted "Mode: Command Center" in the description), so Claude Code
  loaded it with empty metadata. The description is now quoted; `claude plugin validate --strict` passes.
