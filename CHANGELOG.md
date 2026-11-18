# Changelog

Every change to the skill, newest first. Versions follow [Semantic Versioning](https://semver.org); the format
follows [Keep a Changelog](https://keepachangelog.com).

## [Unreleased]

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
- One call to the handoff skill's stop script per stop records the EOD line, the summary's Last change and Next action
  and the board row; without it, the same records by hand (steps 3 and 7).
- Effort: high for every size, L included; max only when the lead says "use max". The max switch for L chats (raise
  after start, stopped first turn, back to high at PLAN READY, re-plan at max) is removed. L keeps its full plan and
  its review chat (now at high).
- Steps in plain words, so other AI tools can follow them; the description no longer says Claude desktop only.
- `references/builds.md` is marked retired: kept only for a build already running with builder and QA chats.

### Added

- `references/tool-map.md`: each action, its Claude desktop tool and what to do in other AI tools, plus one-chat
  mode (task folders, stops in notes.md, the lead opens task chats and posts drafted Zoho comments when needed).
- A project's own rules in its handoff.md win over the skill's defaults (for example a project that never archives).

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
