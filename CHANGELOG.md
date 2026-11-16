# Changelog

Every change to the skill, newest first. Versions follow [Semantic Versioning](https://semver.org); the format
follows [Keep a Changelog](https://keepachangelog.com).

## [Unreleased]

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
