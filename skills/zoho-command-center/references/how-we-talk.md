# How we talk: versions, stops, titles and gos

Moved unchanged from SKILL.md in 2.11.0 to keep the skill light; SKILL.md says when to open each part.

## Versions and waiting

- **Use the newest skill version** (learned 19 Nov 2026: reload messages to 30 idle Command Centers cost about 29 points
  of the 5-hour window). Command Center on its first turn after a lead's message and after any reset, and a task chat at
  a new task or a revive: read the "Version:" line of the installed SKILL.md (the file at the skill's path on disk) and
  compare it with the one loaded in this chat. Installed newer: load the zoho-command-center and handoff skills again
  before the work (Command Center also reads `references/command-center.md` and `references/tool-map.md` again), and
  tell the lead in one line "Skills updated to <version>". A running task keeps its rules ("Which role am I?").
- **Never end a turn waiting for another chat to go idle** (learned 19 Nov 2026: two chats stalled, each waiting on
  the other). Check its state now; idle: do the step in this turn; still running: schedule a one-shot check in 2
  minutes that names the exact step (load the scheduling tool first if the tool list defers it), then one more, then
  tell the lead in one line. Details: `references/command-center.md`, Context watch.

## The next-step box

- **The next-step box only for a new decision** (Command Center, in tools that have one; learned 18 Nov 2026:
  "Proceed: wait" came back after every click while waiting for a usage reset; replaces the 17 Nov rule "a box every
  turn"). One decision, the first button its recommendation "Proceed: <action>", the second a realistic
  alternative. Once the lead has confirmed a wait, a schedule or "later", turns end with the recap and the Next line
  only, no buttons, until something new needs a decision in Command Center itself (a new task, a blocker). A task
  chat waiting on the lead's go or answer is only reported: the lead decides in that chat's own box (step 3).

## Stops, RUNNING and titles

- **No silent idle** (learned 17 Nov 2026): a turn that stops without the work going on (plan ready, waiting on
  someone, checkpoint, usage pause, blocked, a part done) ends with a short report: what was done, the state,
  decisions taken (defaults chosen) and the Next line; the recap opens with the stop reason. The stop also goes to
  Command Center as one message, whoever started the turn (Worker rules), except the turns inside a QA loop
  (findings, FIXED, QA 0), which go to the other chat of the loop; PAUSED, BLOCKED and CHECKPOINT always go to
  Command Center. No FYIs or duplicates.
- **RUNNING, not stopped** (learned 20 Nov 2026: a chat that ended its turn while its check ran looked stopped): a
  turn that ends while the chat's own work keeps running (a background command, a subagent, a check) opens its last
  message, its recap's first sentence (the sidebar status) and the progress page's Now line with "RUNNING, not
  stopped: <what>, started HH:MM; I continue by myself when it finishes." (time from the clock). It is not a stop:
  no stop message, no extra turn, no polling. The next status replaces it. A real stop never says RUNNING.
- **State at the front of the title** (learned 20 Nov 2026: the sidebar shows only titles): a chat keeps its state as
  a prefix of its own title (tool map), one call when the state changes, the rest of the title unchanged: "▶ RUNNING |
  <title>" while it or its own background work runs; "⏸ WAITING on <who> | <title>" (the lead, Command Center or the
  client); "✋ BLOCKED | <title>"; "✓ DONE | <title>" at done and in review. Never for anything else, once per state
  change (no polling, no extra turns); Command Center's own title stays as it is. A chat created without a running
  first prompt starts as "⏸ WAITING on <lead> | <title>", never RUNNING.

## Gos and messages

- A go, or an OK to post in Zoho, counts when the lead says it in that chat. A relayed or quoted go may be refused
  by the receiving chat's safety checks (learned 10 Nov 2026): then ask the lead in one line to say it there.
- A button reply or "gave go" in Command Center is never a go for a task or a phase; an "approved" typed there
  approves only the briefs, never a task's plan (learned 24 Nov 2026).
- A message to a chat that is working is queued and only read when its turn ends. Put decisions in the task files
  too (brief.md, plan.md) and confirm the chat picked them up. Never send plan changes after PLAN READY: the task
  chat re-plans instead (RE-PLAN, Worker rules).

## Vocalise early

- **Vocalise early** (learned 23 Nov 2026): a task that builds or changes a website assesses form attribution, SEO,
  site speed, testing and tracking at the plan. Its plan and the top of PLAN READY carry "Recommended additions":
  per area one line, what the site lacks and what we recommend, with size ("nothing to add" is valid). The lead
  decides: approved ones go into the plan, the rest into the report; none is built without the lead's OK (form
  attribution on a build's lead forms is the build skill's default). Anything else that changes the work (a risk,
  a blocker, a better way): one line as soon as it is known, never first at done.
  - **Form attribution is the company standard** (27 Nov 2026): the 11 labelled attribution fields on every lead
    form and in its lead email, the form layout default, and WordPress forms connected to the agency's app through
    its bridge plugin. Every website's footer also carries the agency badge with its link, set from the site's
    settings (not hard-coded), unless the task records that the client asked to hide it. Both are defaults in every
    website plan, not additions to approve: the plan names the build skill's version and points to it, no copy
    (convert-to-wordpress 0.12.0 or later, `references/forms-email.md`; a build without it: its line says what lacks).

## No change before the go

- **No change before the go** (learned 18 Nov 2026: a task chat took the lead's answer about the route as a go and
  started a download and a local copy before its plan existed; replaces "local work may start right after the
  plan"). Before the lead's go on the plan, only read and plan: no downloads to work from, no local copy or clone, no
  installs, no change to files, databases, Zoho, live sites or client docs, nothing sent to the client. An answer, a
  route choice or a preference is not a go: update plan.md (a dated line in notes.md), report PLAN READY and wait for
  an explicit go on that plan. Backups, live ones too, are plan steps run after the go.

## Only the task, straightforward

- **Only the task, straightforward** (learned 18 Nov 2026: the company works with little supervision, so no back and
  forth). Follow the task and its source doc exactly, verbatim (icons, emoji and long titles included, no rewording).
  A question with a sensible default: decide it and list the decision in the report. An obvious fix inside the task
  that we can make on our side: make it and list it. Ask the lead only about real blockers (something missing, broken
  or impossible, or outside the scope); ask the client only when really needed, through the Zoho comment or reply
  draft. Other clarifications go in the report, without holding up the work; the Zoho comment only carries what the
  client must act on.

## Re-plan

- Re-plan: if the lead answers your plan with changes instead of a go, or reality differs from the plan, re-plan right
  away at your current effort (every size) and report PLAN READY again. After the go too (learned 19 Nov 2026): an
  instruction from the lead that changes the method or scope rewrites those plan.md steps in place (never "see
  notes"), listing done steps the change affects with their undo; make no further change until the new go, then PLAN
  READY and wait; plan.md always matches what is being done. A question that changes nothing is answered right away.

## Your tool

- **In the Claude desktop app:** `get_usage` ("self") gives your context % and the usage limits; a message to Command
  Center is `send_message` with session_id "parent", or `SendMessage` to the parent's `local_...` id. In any other tool,
  read your tool's column of `references/tool-map.md` once at start (Antigravity, Codex or one-chat mode: "message
  Command Center" means a line under "## Stops" in notes.md, as it does when handoff.md names a Command Center in
  another tool).

## Done and close-out

- Done: send Command Center a handover: "DONE: <task>", path to `tasks/<TASK-ID>/report.md`, files to upload to
  Zoho, what is verified vs not, open items for the client, and anything that changes how the Zoho comment or
  status should be posted (e.g. part of the definition of done still waits on the client).
- Answer Command Center's follow-up questions about the work directly (review, comment draft); never post in Zoho.
- Told the task is in review: close every browser tab you opened for it, log "tabs closed: <ids>" in notes.md,
  reply in one line (not a stop report), and end your turn.
