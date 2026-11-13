# Changelog

Every change to the skill, newest first. Versions follow [Semantic Versioning](https://semver.org); the format
follows [Keep a Changelog](https://keepachangelog.com).

## [Unreleased]

- Release automation: the `check` workflow validates every pull request and makes a skill change come with a new
  version; the `release` workflow tags and publishes each new version. README: how to turn on automatic updates.

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
