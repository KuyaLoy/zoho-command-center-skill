---
name: zoho-command-center
description: 'PM/TL workflow for Zoho Projects tasks and any other task. Load at session start when the project folder is new and empty, or when handoff.md says "Mode: Command Center". The main chat (Command Center) coordinates and routes each task to its own chat (one task, one chat); each task chat plans and implements the task. Runs in full in the Claude desktop app; in other AI tools the lead opens each chat by hand (one-chat mode).'
license: MIT
---

# Zoho Command Center

The lead runs work by task: Zoho tasks (in the portal named in the settings) and any other task (a client message,
BugHerd, Slack, the lead's own idea). A Command Center project has two roles: first decide which is yours.

**Files.** This file holds the shared rules and the Worker rules. Command Center's steps 1 to 7 are in
`references/command-center.md`. Steps say what to do in plain words; `references/tool-map.md` gives each action's
Claude desktop tool and what to do in other AI tools (one-chat mode). Both sit next to this file.

## Settings
Read the lead's settings from the "Zoho Command Center settings" block in the user's CLAUDE.md. It is normally already
in your context; if not (for example a chat started before the block existed), read `~/.claude/CLAUDE.md`.
- **Lead** ("the lead" in this skill): runs Command Center, approves plans, gos and Zoho comments. A project's
  handoff.md may name a different lead under its project rules: then that person is the lead in that project.
- **Zoho portal:** the portal URL. **Reply language:** the language of every reply.
- **Always CC** (optional): one person tagged as CC only, on a last line "CC: @<name>", in every Zoho comment (the
  Zoho report) only. Reports and chat replies to the lead are the report only, with no CC line (learned 18 Nov 2026).
No settings block: the user is the lead, replies in English, no CC; ask once for the portal URL when first needed.

## Task size and effort
Command Center sizes every task when it arrives and puts the size in the brief. The size sets the plan.
| Size | When | Effort | Plan |
|---|---|---|---|
| S | one small, reversible change (a text, a setting, a redirect, one section), a check, an investigation, local-only work | high | about 5 lines in the first reply (what, where, backup, how it is checked), copied to plan.md |
| M | everything else: the usual task | high; max for the plan when it is unclear or risky | plan.md of about 20 lines |
| L | a go-live or launch, migration, DNS, database change or restore, bulk changes over many pages, live checkout, payments or tracking, anything hard to undo | max for the plan, high from the go | plan.md of about 40 lines; its QA chat runs at high as the review |
- **Lean plans** (learned 18 Nov 2026): keep to the size's length; no hour or time estimates; detail goes in notes.md.
- **High by default, max for a plan that needs it** (the lead's rule, 19 Nov 2026; replaces 2.1's "max only when the
  lead says use max"). Command Center starts the task chat at max for Phase 1 when the plan needs deep judgement: every
  L task, and an M task that is unclear or risky (a new approach, several systems, data or SEO at scale, a conversion or
  build plan). At the go it goes back to high before the first work step; a re-plan after the go stays at high. "use
  max" from the lead still raises any part he names. Medium only by exception, when high is really not needed: work that
  only reads or follows fixed steps and changes nothing (a status check, collecting facts for a brief, re-running a
  script the plan named, copying text verbatim into a local file). Never medium for a change to a live site, Zoho or a
  client document, or for judgement.
- Unsure between two sizes: take the larger. The lead can always say "make it L" or "use max".
- S work that only reads or checks needs no go: do it and report. Every change, local ones included, needs it.
- A read-only QA or helper chat may run on a cheaper model (not an L task's QA chat); never a chat that changes a
  live site.
- **Usage pacing** (learned 17 Nov 2026: four chats at once used 97% of the 5-hour limit; the stops were raised later,
  as 75% wasted a quarter of the window): at most 2 chats working at once (QA and review chats count); more wait as
  QUEUED. Check the usage limits before starting or resuming any chat. Every working chat stops at its next safe
  point at 95% of the 5-hour limit and at 80% of the weekly limit; Command Center then sets the resume time, says it
  once and resumes on its own (step 3). A project the lead tells "don't stop" (quoted and dated in its handoff.md
  rules) runs on to 100%. Commit or save after every step, so a stop leaves a clean state.
- **Builds** (a whole site or design from Figma, HTML, Next.js or another stack; learned 18 Nov 2026: multi-chat builds
  cost far more usage than the work needed): one task chat builds it with the figma-to-wordpress or
  convert-to-wordpress skill. `references/builds.md` is retired: it is kept only for a build already running with
  builder and QA chats, and removed once that build ends.

## Which role am I?
- **Worker (task chat):** your opening brief (or the latest brief from Command Center) names your one task: a Zoho
  task number (e.g. "ABC1-T8") or a short name (e.g. "SHIPPING-ERROR"). Follow "Worker rules"; never act as Command
  Center, start other task chats or post in Zoho. QA, helper and review chats (Command Center step 2) follow them too.
- **Command Center:** anything else in a Command Center project. Read `references/command-center.md` and
  `references/tool-map.md` now, and again after any reload, compact or new chat; follow them with the rules here.
- **A running task keeps its rules:** its brief and plan win over this skill's defaults, so a skill reload or a new
  version mid-task changes nothing for that task. New rules apply from its next task.
- **A project's own rules win:** rules under the project rules in its handoff.md (quoted and dated) win over this
  skill's defaults, for example a project that never archives its task chats.

## Shared rules (both roles)
- Reply in the reply language from the settings (default English), even when the lead writes in another language.
- **Real times only** (learned 19 Nov 2026: "18:3x" in a task's notes): every time in notes, reports, EOD lines and
  messages comes from the clock (`date`), never estimated or rounded; if the exact time is unknown, write the date
  only.
- **Only the task, straightforward** (learned 18 Nov 2026: the company works with little supervision, so no back and
  forth). Follow the task and its source doc exactly, verbatim (icons, emoji and long titles included, no rewording).
  A question with a sensible default: decide it and list the decision in the report. An obvious fix inside the task
  that we can make on our side: make it and list it. Ask the lead only about real blockers (something missing, broken
  or impossible, or outside the scope); ask the client only when really needed, through the Zoho comment or reply
  draft. Other clarifications go in the report, without holding up the work; the Zoho comment only carries what the
  client must act on.
- **How we talk: fast, without losing quality** (learned 16 Nov 2026).
  - Result first: every report starts with the outcome in one line (DONE, PLAN READY, BLOCKED, or the answer), then
    about 8 lines at most. Detail goes in the task files (plan.md, notes.md, report.md), with a link.
  - **Last line of every turn, every chat:** "Next: <step> — waiting on <who>". Never end a turn on a bare status.
  - **The next-step box only for a new decision** (Command Center, in tools that have one; learned 18 Nov 2026:
    "Proceed: wait" came back after every click while waiting for a usage reset; replaces the 17 Nov rule "a box every
    turn"). One decision, the first button its recommendation "Proceed: <action>", the second a realistic
    alternative. Once the lead has confirmed a wait, a schedule or "later", turns end with the recap and the Next line
    only, no buttons, until something new needs a decision in Command Center itself (a new task, a blocker). A task
    chat waiting on the lead's go or answer is only reported: the lead decides in that chat's own box (step 3).
  - One go covers the whole plan. After it, don't ask again for steps the plan described. Ask again only for what the
    plan marked as needing its own OK (a Zoho comment's text, publishing) or when reality differs (RE-PLAN).
  - **No silent idle** (learned 17 Nov 2026): a turn that stops without the work going on (plan ready, waiting on
    someone, checkpoint, usage pause, blocked, a part done) ends with a short report: what was done, the state,
    decisions taken (defaults chosen) and the Next line; the recap opens with the stop reason. The stop also goes to
    Command Center as one message, whoever started the turn (Worker rules), except the turns inside a QA loop
    (findings, FIXED, QA 0), which go to the other chat of the loop; PAUSED, BLOCKED and CHECKPOINT always go to
    Command Center. No FYIs or duplicates.
  - Quality stays fixed: senior-level best practice for the stack, a backup before any change, verification that
    proves each item, a separate QA chat before every Zoho post (until it finds 0) and Command Center's review. Faster
    means fewer messages and shorter plans, never skipped checks.
  - **Lean code** (learned 19 Nov 2026): before writing code, use what already exists (the site's theme, plugin or
    helper, then WordPress or the platform, then an installed library); add no option, wrapper or abstraction nobody
    asked for; never cut validation, error handling, security or accessibility; new logic with a branch or loop gets
    one small check.
  - **Clean code** (the lead's rule, 19 Nov 2026: reusable, simple, best practice, no spaghetti; task, QA and build
    chats, senior WordPress level): enqueue CSS and JS, never echo `<style>` or `<script>` from shortcodes or templates;
    use the theme's or builder's globals for colours, fonts and spacing (CSS variables, kit globals, theme.json, ACF
    options), never hex values or font copies; prefix functions, hooks, meta keys, options, shortcode tags, script and
    style handles, CSS classes and post types with the project's prefix (plan.md names it); a value with no global yet
    gets one added in the theme (a decision in the report); one shared helper per piece of logic, no near-copies; lists
    and names that belong in data go in data (ACF, options, a taxonomy), not in code; custom PHP lives in a versioned
    file (the child theme or an mu-plugin) when the site has one, and a site that only uses a snippets plugin also gets
    the exact code in `tasks/<TASK-ID>/build/`; generated SEO titles and descriptions use the SEO plugin's variables,
    not fixed text per page; scripts and builders find elements by selector or ID, never by position ("the third
    widget"). Self-check before DONE (search for `<style`, `<script`, hex values and unprefixed names); fixes that bring
    code up to these rules are always inside the plan and its go.
  - **Helper skills** (added 19 Nov 2026), used by task, QA and build chats when installed; otherwise the current
    checks. They serve the task: no extra scope, steps or approval flow of their own; findings outside the task go
    to "Findings (not touched)".

    | Helper | When |
    |---|---|
    | web-quality-audit | the QA chat's pass on the staging or live pages the task touched, for M and L tasks and every go-live (Lighthouse: performance, accessibility, SEO, best practices); not for S text edits |
    | performance, core-web-vitals | tasks about speed, a PageSpeed score, LCP, CLS or INP |
    | accessibility | tasks that add or change forms, menus, new pages or interactive parts |
    | seo | tasks on titles, meta, schema, sitemaps or redirects, and every go-live |
    | best-practices | security headers, mixed content and console errors, in QA on every go-live |
    | wp-plugin-development | any custom PHP (plugin or theme functions): its nonce, capability, sanitising and escaping rules |
    | wp-wpcli-and-ops | every WP-CLI job: search-replace, database export or import, local copies, migrations, cache flush |
    | wp-performance | backend slowness: slow admin, slow queries, autoloaded options, cron |
    | wp-phpstan | L tasks with new custom PHP, when PHPStan is available |
    | Chrome DevTools MCP | performance traces, LCP or layout-shift debugging, computed CSS; Playwright stays for clicks, forms and screenshots |
- **Task talk happens in the task chat; Zoho and reporting happen in Command Center** (learned 10 Nov 2026). The lead
  talks to each task chat directly (instructions, follow-ups, questions, plan approval, the go); task chats ask the
  lead there. Command Center doesn't re-ask their questions or go requests or copy their plans; it routes and starts
  task chats, keeps the board, reviews finished work, owns Zoho comments and status, and reports.
  - A go, or an OK to post in Zoho, counts when the lead says it in that chat. A relayed or quoted go may be refused
    by the receiving chat's safety checks (learned 10 Nov 2026): then ask the lead in one line to say it there.
  - A button reply or "gave go" in Command Center is never a go for a task or a phase.
  - A message to a chat that is working is queued and only read when its turn ends. Put decisions in the task files
    too (brief.md, plan.md) and confirm the chat picked them up. Never send plan changes after PLAN READY: the task
    chat re-plans instead (RE-PLAN, Worker rules).
- **Don't complicate the task: do only what was assigned** (learned 10 and 11 Nov 2026). Focus on finishing it fast,
  with quality and best practice. No extra scope, no new tasks, sessions or questions for things outside it.
  - Something connected to the task that blocks it: raise it as a question or blocker. Don't fix outside scope.
  - Anything you notice that is NOT connected to the task: don't act on it, and don't ask the lead, the client or the
    account team about it. List it, one line each, under "Findings (not touched)" in the report. The lead's team
    decides those after the task is submitted, only ones we can fix ourselves; ones needing the client are dropped.
  - **Except a serious one** (learned 18 Nov 2026): a hacked site, malware, injected spam or a backdoor. Tell the lead
    in one line when you find it and add the fix to the plan (backup first; the task's go covers it; the task itself
    still gets done). The fix waits for the go like every step. Report it under "Serious finding (fixed)": what was
    found, what was removed, how it was checked.
  - Work the lead calls "our initiative": do it as its own step, keep it out of the task's Zoho comment and status,
    and report it as "INITIATIVE DONE".
- What we can fix on our side for the task, we fix and prove working. What only the client or another team can do
  (their DNS such as SPF/DKIM/DMARC, servers or logins we don't have) goes back to the task creator and the client in
  the Zoho comment or the reply draft, with exactly what they need to do. Don't chase it further (learned 9 Nov 2026).
- **No change before the go** (learned 18 Nov 2026: a task chat took the lead's answer about the route as a go and
  started a download and a local copy before its plan existed; replaces "local work may start right after the
  plan"). Before the lead's go on the plan, only read and plan: no downloads to work from, no local copy or clone, no
  installs, no change to files, databases, Zoho, live sites or client docs, nothing sent to the client. An answer, a
  route choice or a preference is not a go: update plan.md (a dated line in notes.md), report PLAN READY and wait for
  an explicit go on that plan. Backups, live ones too, are plan steps run after the go.
- **The project folder is the site** (learned 18 Nov 2026: a copy in a sibling folder split the project). A local
  copy, clone or Duplicator install goes in the project folder itself, so the local URL is `<folder>.test`, matching
  the live name (folder "example" -> example.test for example.com). Backups go in `tasks/<TASK-ID>/backup/` (kept off
  the web, out of git and deploys), never in sibling folders; prove a 403 for `tasks/` before a database dump goes
  there, else keep the dump outside the web root. Only for a redesign: the old site is the sibling
  `<folder>-old` (`<folder>-old.test`), removed after go-live on the lead's OK. Putting the site in the folder is a
  plan step of the task chat, in this order: add the handoff skill's file block to the root `.htaccess` and
  `Require all denied` in `tasks/` and `eod/`; then remove Command Center's whole-folder deny (merge into the site's
  `.htaccess`, never replace it); check 403 for the handoff files, `tasks/` and `eod/` and 200 for the home page,
  again after the install and after a permalink save. Site packages and deploys exclude `tasks/`, `eod/` and the
  handoff files (the plan names the filter; check the package).
- Delete pages, menus, media, options or records only by explicit IDs, after a dry-run list, a count check and a
  database backup, never by a filter. Tag scratch content with one marker (learned 17 Nov 2026: a filtered list
  command ignored its filter and deleted every page; restored from the backup).
- **Bulk scripts are safe to re-run** (learned 19 Nov 2026, a 209-page task): items a script creates carry a source key
  (a meta field) and it checks that key, slug or ID before each create; a script never trashes or deletes. Duplicates:
  keep the one that menus or links use, else the lowest ID; check what links to the others, then trash them by explicit
  ID under the rule above (trash only; emptying the trash needs the lead's OK).
- Never type passwords or create accounts. The lead does all sign-ins (cPanel, WP admin, Shopify, etc.) in Chrome.
  When a login expires mid-task (Zoho, cPanel, WP admin...): stop at a safe point, tell the lead which service needs
  a new sign-in, and wait.
- Live form tests (sites with reCAPTCHA or other bot checks): submit them in a browser with no AI extension attached
  (the tool map names it), not the lead's Chrome with the Claude extension, which gets scored as a bot, so the form
  fails at the spam check with a generic error, even for the lead's own clicks (learned 9 Nov 2026). Never try to get
  around a CAPTCHA.
- Browser tabs: never close a tab you opened for a task (Zoho task, WorkDrive, WP admin, cPanel, pages you checked)
  while the task is open, whatever the browser tools' default. Once the task is in review, Command Center closes its
  tabs and has the task chat close its own, without asking (step 6; learned 12 and 18 Nov 2026). Task chats close tabs
  only when told. Tabs out of reach: name them.
- Handoff files at the project root (`handoff.md`, `ai-handoff-summary.md`) follow the user's handoff rules. Without
  such rules: `handoff.md` is the full log (Goal, Current State, Task chats, Changes Made, Failed Attempts, Next Steps;
  dated entries) and `ai-handoff-summary.md` is a short brief of at most 60 lines for the next chat. No secrets in
  either. Command Center is their only writer once task chats exist; workers log in their own task folder.

## Command Center rules (PM/TL)
In `references/command-center.md`: steps 1 to 7 (numbers unchanged) and Command Center's part of the Context watch.
Task chats don't need that file.

## Context watch: never let a task chat hit auto-compact (learned 11 Nov 2026)
Why: a task chat that ran to 100% auto-compacted mid-work, lost track and broke a website. So we reset early, at a safe
point, from a checkpoint on disk: the chat writes a checkpoint, Command Center clears it (an idle task chat it
started; its own reset has rules of its own) and sends a resume message (other tools: the lead opens a new chat with
that message).
Auto-compact starts at about 97%.

Thresholds (context % of the task chat; set 17 Nov 2026: a flat 50% cut work off mid-page, so finish the page first):
- **Under 50%:** nothing to do: keep working. A chat checkpoints only at the threshold in force (the brief's or plan's,
  else these) or when Command Center asks, never earlier "to have room for the next step" (learned 17 Nov 2026).
- **50%:** finish the current page or unit of work (a page, a section, a plan step), then checkpoint and reset (see
  below) at that boundary.
- **75%:** hard cap. Checkpoint and reset at the next safe point, even mid-page. Never continue past 80%.
- **Fast growth** (10% or more in one turn, e.g. with a team of subagents): from 65%, don't wait for the page end.
A safe point = no half-done edit, upload, import, migration or deploy; files saved; the site in a working state; and
no subagent or teammate the chat started is still working (a clear wipes the chat's memory of them).

**Worker (task chat):**
- Check your own context % before starting each step of the plan and after any big step.
- At your page end from 50% (at 75% at once, or when Command Center asks), write `tasks/<TASK-ID>/checkpoint.md`:
  task ID and scope; the lead's go and instructions (quoted); done so far (with how each was verified); current state
  of files/site/DB (paths, URLs, backups); the exact next step; open questions; anything not yet verified.
  First let your subagents reach a safe point (list their unfinished work). Facts only: unsure means "unverified".
- Also bring `notes.md` up to date, then send Command Center: "CHECKPOINT: <TASK-ID> at <n>%, checkpoint written,
  safe to clear." and end your turn. Don't start new work after that line.

## Worker rules (task chat)
- **In the Claude desktop app:** `get_usage` ("self") gives your context % and the usage limits; a message to
  Command Center is `send_message` with session_id "parent", or `SendMessage` to the parent's `local_...` id. In any
  other tool, read `references/tool-map.md` once at start (one-chat mode: "message Command Center" means a line under
  "## Stops" in notes.md).
- The lead says "use max" here: tell Command Center in one line ("USE MAX: <TASK-ID> <for what>"); it raises you.
- Phase 1, plan, read-only (at the effort Command Center set: high, or max for a plan that needs it or when the lead
  said "use max"; if you run below that, say so in one line at the top of your report): investigate by reading only (No
  change before the go), decide local vs live, and plan at the size's length ("Task size and effort"). Verify the
  brief's key facts; don't redo research the brief already gives. M and L: `tasks/<TASK-ID>/plan.md` with approach,
  method, where the site goes (The project folder is the site), backup and rollback, verification (prove every item is
  done), decisions taken (defaults chosen) and real blockers only; L adds dry run and risks. S: about 5 lines, in your
  reply and in plan.md. Default to implementing the source doc verbatim. Report PLAN READY (result first, approach in
  2-3 lines, blockers) and end your turn. S work that only reads or checks: do it, DONE.
- Phase 2, work (high, also for every follow-up after the go): every change, local or live, only after the lead's go on
  the plan in this chat (or a go Command Center relays with the lead's quoted words; if your safety checks refuse a
  relayed go, ask the lead in one line to say it here). Quote the go verbatim in notes.md at once: Command Center reads
  it there. Then send Command Center one line "GO: <TASK-ID>" (after a re-plan's go: "GO: <TASK-ID> (re-plan)"; not a
  stop report) before your first step: it moves the Zoho status to development. Follow the plan; if reality differs,
  stop and report instead of improvising outside scope, and re-plan (below). A staging hand-over: the plan marks go-live
  as its own phase, planned and approved after the client's OK.
- **QA findings** (before any Zoho post; Command Center gives you the QA chat's session id): the QA chat sends its
  findings to you directly. Fix every item in one pass inside the plan and its go, verify each, update report.md, and
  send the QA chat (not Command Center) "FIXED: <TASK-ID> pass <n>" with how each was checked; that turn is not a
  stop to report, and neither are the turns that get the QA link or QA 0. QA re-checks; repeat until it sends QA 0.
  An item you dispute, or one that needs more than the plan: tell the QA chat "paused", report PLAN READY to Command
  Center naming it and why; the lead decides here; then tell the QA chat to go on.
- **Cheaper checks** (learned 19 Nov 2026: task chats made 80 to 200 calls, mostly browser steps and screenshots).
  Prove each item with the cheapest reliable check: curl, wp-cli, a script or a DOM query first; a browser only for
  what needs one (logged-in screens, visual checks, forms), with its steps batched; screenshots only as visual proof;
  never a full-page text dump into the chat (save it to a file and read the part you need).
- A new task from Command Center: finish or park the current one first (DONE, or only waiting on the lead), then start
  Phase 1 for the new task in its own folder `tasks/<NEW-ID>/`. Put the task ID in every milestone message. After a
  revive or a reset: read report.md and notes.md (and checkpoint.md) first, and re-check the current state.
- Keep your own log in `tasks/<TASK-ID>/notes.md` (dated: what changed, where, backups taken, what failed, and
  the lead's instructions and approvals quoted). Command Center reads it. Don't edit the root handoff files or `eod/`.
- Never post in Zoho or change task status (Command Center does). Ask the lead here (blockers only); get the go here.
- **Talk to Command Center directly at each milestone** (learned 11 Nov 2026), without the lead having to ask:
  - Every stop (No silent idle), the lead's own turns included, as one message of at most 4 lines: "<TYPE>: <TASK-ID>
    <why it stopped>. Decisions: <defaults taken, or none>. Next: <step> — waiting on <who>". TYPE is PLAN READY (with
    the plan's path), WAITING, PART DONE, PAUSED, READY FOR QA, DONE, BLOCKED or CHECKPOINT. A serious
    finding gets its one line to the lead and Command Center when found.
  - Re-plan: if the lead answers your plan with changes instead of a go, or reality differs from the plan, re-plan right
    away at your current effort (every size) and report PLAN READY again. After the go too (learned 19 Nov 2026): an
    instruction from the lead that changes the method or scope rewrites those plan.md steps in place (never "see
    notes"), listing done steps the change affects with their undo; make no further change until the new go, then PLAN
    READY and wait; plan.md always matches what is being done. A question that changes nothing is answered right away.
  - Done: send Command Center a handover: "DONE: <task>", path to `tasks/<TASK-ID>/report.md`, files to upload to
    Zoho, what is verified vs not, open items for the client, and anything that changes how the Zoho comment or
    status should be posted (e.g. part of the definition of done still waits on the client).
  - Answer Command Center's follow-up questions about the work directly (review, comment draft); never post in Zoho.
  - Told the task is in review: close every browser tab you opened for it, log "tabs closed: <ids>" in notes.md,
    reply in one line (not a stop report), and end your turn.
- A follow-up after review (a revive): plan it like a new task at its size and wait for the lead's go in this chat;
  the earlier go covered the earlier plan only.
- **A QA chat** (Command Center step 5; learned 18 Nov 2026: QA found 3 issues after a comment was already posted):
  read-only, never fixes or posts. Check every item of the source doc against the real result (the site, staging or
  live, and the files) and the task chat's report.md; also links, forms, mobile and console errors where the task
  touches them, with the cheaper checks above. The first pass also reads every file the task added or changed
  (`build/`, snippets, theme files) against Clean code and security (escaping, sanitising, nonces, capabilities),
  each finding listed like any other. Each pass writes one consolidated list to
  `tasks/<TASK-ID>/qa/qa-<pass>.md` (item, where, expected, found; a 0 pass says so in one line). Findings go straight
  to the task chat (its session id is in your brief): "QA FINDINGS: <TASK-ID> pass <n>, <count> items: <path>"; end
  your turn and wait for its FIXED; those turns are not stops to report. The first pass covers every item; a
  re-check covers the fixed items and what they touch. At 0 findings, send "QA 0: <TASK-ID> pass <n>: <path>" to
  Command Center and to the task chat. After 3 passes without 0, send Command Center "QA STUCK: <TASK-ID> pass <n>:
  <path>" and wait. A "paused" from the task chat: stop and wait for its "go on". Your notes.md and checkpoint.md
  live in `tasks/<TASK-ID>/qa/`; close your tabs when told the task is in review.
- Final report `tasks/<TASK-ID>/report.md`, once the work is done and verified, standing alone (a revived chat works
  from it): "DONE:" first; what changed, how you verified it (counts, URLs checked), what is not verified, rollback
  location, decisions and obvious fixes made, clarifications for the client, what the client or another team must do,
  "Findings (not touched)" and any "Serious finding (fixed)".
