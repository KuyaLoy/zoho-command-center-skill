# zoho-command-center

A Claude Code skill (packaged as a plugin) for running Zoho Projects tasks, and any other task, the way a PM or tech
lead would, with the Claude desktop app:

- **One Command Center chat per project** routes each task (a Zoho link, a client message, BugHerd, Slack, your own
  idea) to a new task chat or to an existing one that already has the context, keeps a task board in `handoff.md`,
  reviews finished work, and owns the Zoho comments and status changes.
- **Effort that fits the task:** small and normal tasks are planned and done at high effort with short plans; large or
  risky ones (go-lives, migrations, database work) are planned at max and their review at done runs at max.
- **Task chats** plan first, wait for your go, then implement, log in `tasks/<TASK-ID>/`, and report PLAN READY and
  DONE to Command Center. Reports lead with the result; one go covers the whole plan.
- **Gates you control:** nothing live changes before your go, no Zoho comment is posted before you OK the exact text
  and tags, and the Zoho status only moves after the work is done and verified.
- **Context watch and pacing:** from 50% context a task chat finishes the page it is on, then checkpoints to disk and
  resets (75% is the hard cap); Command Center resets at 35%. That is long before auto-compact, so no chat loses track
  mid-work and every turn stays cheap. At most 2 chats work at once, and all of them pause at 95% of the 5-hour usage
  limit and, by default, at 80% of the weekly limit (a project you tell "don't stop" runs on to 100%).
- **Builds with several chats:** `references/builds.md` sets up builders and QA chats for large builds (one fix list
  per QA pass, scripted checks, a Figma sweep before building).

It came out of daily use on more than 20 client projects; the rules carry the lessons learned there.

## Requirements

- The **Claude desktop app, Code tab**. Command Center starts and steers chats with the app's session tools
  (start a chat, set its effort, read its context %, clear it), so the skill does not work in a plain chat app or in
  other agents.
- **Claude in Chrome**, for reading Zoho tasks and posting comments.
- A **Zoho Projects** portal.

## Install

In a Claude Code chat:

```
/plugin marketplace add KuyaLoy/zoho-command-center-skill
/plugin install zoho-command-center@zoho-command-center
```

Then turn on automatic updates (once): `/plugin` > Marketplaces > zoho-command-center > Enable auto-update. Or add
this to `~/.claude/settings.json`:

```json
"extraKnownMarketplaces": {
  "zoho-command-center": {
    "source": { "source": "github", "repo": "KuyaLoy/zoho-command-center-skill" },
    "autoUpdate": true
  }
}
```

Without the plugin system: copy `skills/zoho-command-center/` into `~/.claude/skills/` (no automatic updates).

## Set it up (once)

Add this to your `~/.claude/CLAUDE.md` and fill in your values. The first block tells Claude when to load the skill;
the second gives the skill your details.

```markdown
## Zoho Command Center mode
- At session start, load the zoho-command-center skill and follow it when the project folder is empty (a new
  project) or when handoff.md has `Mode: Command Center` under the project rules.
- If the opening brief names a task and says you are its task chat, you are a worker: follow the Worker rules only.

## Zoho Command Center settings (read by the zoho-command-center skill)
- Lead: <your name> (approves plans, gos and Zoho comments)
- Zoho portal: https://projects.zoho.com/portal/<your-portal>
- Reply language: English
- Always CC: @<name> (optional: tagged as CC only, last line "CC: @<name>" in every Zoho comment and report)
```

Don't want every empty folder to become a Command Center? Drop "when the project folder is empty" and start one by
saying "set this folder up as a Command Center".

Then open a new chat.

## Use

1. Open an empty folder in the Code tab. The main chat sets itself up as "Command Center - <folder>".
2. Paste a task: a Zoho task link, or any request. Command Center sizes it (S, M or L), picks the chat (a new one, or
   an idle one on the same site), and tells you in one line where it went and why. Say "new chat" to override.
3. Talk to the task chat directly: read its plan, answer its questions, say **go** there.
4. When it reports DONE, Command Center reviews the work. Zoho tasks: it shows you the Zoho comment draft with the
   tags; say OK, and it posts the comment, moves the status, and asks whether to close the tabs. Other tasks: it gives
   you a reply or report draft to send.

## Update

With auto-update on (see Install), Claude Code updates the skill by itself: a few minutes after the first message of
a chat it checks this repository and installs a new version when the version number changed. It says "Plugin
updated"; run `/reload-plugins` or open a new chat to use it. Auto-update is off by default for marketplaces that
are not Anthropic's. To update by hand:

```
/plugin marketplace update zoho-command-center
/plugin update zoho-command-center@zoho-command-center
```

Then open a new chat. A git clone updates with `git pull --ff-only`. A manual copy updates by copying the new
`skills/zoho-command-center/` over the old one. Every release is a
[GitHub Release](https://github.com/KuyaLoy/zoho-command-center-skill/releases) (Watch > Custom > Releases emails
you each one); what changed is in [CHANGELOG.md](CHANGELOG.md).

Turn automatic updates off: `/plugin` > Marketplaces > zoho-command-center > Disable auto-update, or
`"autoUpdate": false` in the settings snippet above.

## Uninstall

```
/plugin uninstall zoho-command-center@zoho-command-center
/plugin marketplace remove zoho-command-center
```

Then remove the two blocks from your `~/.claude/CLAUDE.md`.

## Safety

The skill never types passwords or creates accounts (you sign in), never changes a live site, CMS, hosting, Zoho or
client document before your go, never posts in Zoho without your OK on the exact text, and keeps its planning files
(`handoff.md`, `tasks/`) off the web and out of git.

## Layout

```
.claude-plugin/plugin.json         the plugin
.claude-plugin/marketplace.json    this repo as a one-plugin marketplace
skills/zoho-command-center/SKILL.md the workflow and its rules
skills/zoho-command-center/references/builds.md  builds with builder and QA chats
CHANGELOG.md                       what changed in each version
AGENTS.md                          rules for changing the skill
```

## Licence

MIT. See [LICENSE](LICENSE). Zoho and Zoho Projects are trademarks of Zoho Corporation; this project is not
affiliated with Zoho.
