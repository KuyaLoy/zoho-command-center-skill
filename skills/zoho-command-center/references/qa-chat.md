# QA: the QA chat and the task chat's part

Moved unchanged from SKILL.md in 2.11.0 to keep the skill light; SKILL.md says when to open each part.

## The task chat's part

- **QA findings** (before any Zoho post; Command Center gives you the QA chat's session id): the QA chat sends its
  findings to you directly. Fix every item in one pass inside the plan and its go, verify each, update report.md, and
  send the QA chat (not Command Center) "FIXED: <TASK-ID> pass <n>" with how each was checked; that turn is not a
  stop to report, and neither are the turns that get the QA link or QA 0. QA re-checks; repeat until it sends QA 0.
  An item you dispute, or one that needs more than the plan: tell the QA chat "paused", report PLAN READY to Command
  Center naming it and why; the lead decides here; then tell the QA chat to go on.

## The QA chat

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
