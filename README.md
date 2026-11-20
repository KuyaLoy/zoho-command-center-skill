# zoho-command-center

A skill (packaged as a Claude Code plugin, in the open Agent Skills format) for running Zoho Projects tasks, and any
other task, the way a PM or tech lead would. It runs in full in the Claude desktop app and in one chat in other AI
tools:

- **One Command Center chat per project** gives each task (a Zoho link, a client message, BugHerd, Slack, your own
  idea) its own task chat: the same link or task ID always goes back to the same chat, an archived chat is revived
  from its report and notes. It keeps a task board and your open requests in `handoff.md`, a daily EOD log in `eod/`,
  reviews finished work, and owns the Zoho comments and status changes. It answers from files and checks, not memory.
- **Effort and plans that fit the task:** every task runs at high effort; large tasks, and unclear or risky normal ones,
  plan at max and go back to high at your go (and "use max" raises any part you name); small tasks get a 5-line plan,
  normal ones about 20 lines, large or risky ones (go-lives, migrations, database work) about 40 lines, with no hour
  estimates.
- **Task chats** do only the task: short plans, sensible defaults and obvious fixes decided themselves and listed in
  the report, questions only for blockers. Until your go on the plan they only read and plan (no download, local
  copy or install); a site copy goes in the project folder itself (`<folder>.test`). They log in `tasks/<TASK-ID>/`
  and report every stop to Command Center. One go covers the whole plan.
  Unrelated problems are only listed, except a hacked site or malware, which is fixed with the task and reported.
- **QA before every Zoho post:** a separate, read-only QA chat checks the work and sends its findings straight to the
  task chat, which fixes them and tells QA; QA checks again until it finds nothing. Command Center only hears that QA
  started and that it passed. Task and QA chats prove each item with the cheapest reliable check (curl, wp-cli, a
  script) and use the browser only where it is needed.
- **Gates you control:** nothing changes before your go, and no Zoho comment is posted before you OK the exact text,
  tags and Request Review values. The Zoho status moves to development at your go, so the team sees the work, and to
  review only after QA finds nothing and the approved comment is posted.
- **Context watch and pacing:** from 50% context a task chat finishes the page it is on, then checkpoints to disk and
  resets (75% is the hard cap). That is long before auto-compact, so no chat loses track mid-work. Command Center keeps
  the handoff files current at every stop and resets itself to save usage only when it is safe (about 200K tokens or a
  new day, nothing pending, everything recorded). At most 2 chats work at once, and all of them pause at 95% of the
  5-hour usage limit and, by default, at 95% of the weekly limit (a project you tell "don't stop" runs on to 100%).
- **Builds** run in one task chat with a conversion skill (figma-to-wordpress or convert-to-wordpress);
  `references/builds.md` is kept only for builds already running with builder and QA chats.
- **Quiet close-out:** one short Zoho comment (greeting, links, "Done:" one line per item, the CC line), then the
  status moves to review; Command Center closes the tabs, archives the task and QA chats and tells you in one line,
  with no follow-up questions. You message it when a reviewer or the client comes back, and the same chats are
  revived. The question box only appears for a new decision. Task chats idle for 2 days are archived.

It came out of daily use on more than 20 client projects; the rules carry the lessons learned there.

## Requirements

- The **Claude desktop app, Code tab**, for the full workflow: Command Center starts and steers chats with the app's
  session tools (start a chat, set its effort, read its context %, clear it).
- **Other AI tools** (Claude Code in a terminal, Codex, Cursor, Antigravity, OpenCode, Cline, Devin Desktop and others
  that read Agent Skills): one-chat mode. Each task keeps its folder, you open task chats with one line, and stops go
  into the task's notes. `references/tool-map.md` lists each action and what to do there.
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

Without the plugin system, or for another AI tool: clone this repository once and link (or copy)
`skills/zoho-command-center/` into the tool's skills folder (`~/.claude/skills/`, `~/.agents/skills/`, or the folder
your tool documents). A clone updates with `git pull --ff-only`.

## Check it works in another AI tool

Link the clone's `skills/zoho-command-center/` into the folder the tool reads skills from: `~/.agents/skills/` for
Codex and Cursor, `~/.gemini/config/skills/` for Antigravity. Link the
[handoff skill](https://github.com/KuyaLoy/handoff-skill) the same way, from its own clone, as its README says.

Then make a new empty folder outside any web root, open it in the tool, start an agent chat and paste this prompt:

```
Smoke test of the zoho-command-center skill in one-chat mode. This folder is a new, empty project for a Command
Center. Load the zoho-command-center skill from your skills folder and follow it for a new main chat in an empty
folder (its first step), in its one-chat mode, since you have no session tools. Do not open Zoho or any website. Then
stop. Report in at most 6 lines: the skill files you read (paths), the files you created, and a last line in the
skill's Next format.
```

It passes when the skill's SKILL.md and both reference files were read; handoff.md (with "Mode: Command Center",
"## Open requests", "## Task chats"), ai-handoff-summary.md, AGENTS.md and eod/<date>.md were created; the summary
checker says OK; the last line reads "Next: ... — waiting on <the lead>".

Tested: Codex CLI 0.146.0 on 2026-11-18 with gpt-5.6-sol: pass. If Codex says a model "is not supported when using
Codex with a ChatGPT account", run it with `-m` and a model your account supports.

## Team setup: everything a teammate installs

Four skills work together. Everything below comes from each one's own README: follow that README where this is
short.

| Skill | Repository (README) | Must have, per its README |
|---|---|---|
| zoho-command-center | [this repo](https://github.com/KuyaLoy/zoho-command-center-skill) | the Claude desktop app (Code tab) for the full workflow, other AI tools in one-chat mode; Claude in Chrome; a Zoho Projects portal |
| handoff | [handoff-skill](https://github.com/KuyaLoy/handoff-skill) | its stop and checker scripts are plain sh and awk ("chats without a shell make the same edits by hand") |
| convert-to-wordpress | [convert-wordpress-skill](https://github.com/KuyaLoy/convert-wordpress-skill) | Python 3.9+; a local WordPress app (Local, Laragon, Herd, MAMP, XAMPP, WampServer, DDEV, wp-env, or PHP 8.1 to 8.4 with MySQL or MariaDB); Node.js 18+ with Playwright and Chromium; Composer for PHPCS; WP-CLI optional |
| figma-to-wordpress | [figma-to-wordpress-skill](https://github.com/KuyaLoy/figma-to-wordpress-skill) | a Figma MCP server connected; Python 3 and Node.js 18+; `npm i -D playwright pixelmatch pngjs` and `npx playwright install chromium`; for WordPress builds a local web stack and convert-to-wordpress |

**Where each skill goes.** Claude Code: zoho-command-center, handoff and figma-to-wordpress install as plugins
(`/plugin marketplace add KuyaLoy/<repo>`, then `/plugin install`, then turn on auto-update once, as each README
shows); convert-to-wordpress is cloned into `~/.claude/skills/convert-to-wordpress`. Other tools: clone each repo once
and link its skill folder into the tool's skills folder (handoff's README: "link (don't copy)", so one `git pull`
updates every tool):

| Tool | Skills folder | Link on Windows (handoff's README) |
|---|---|---|
| Codex | `~/.agents/skills` | `New-Item -ItemType Junction -Path <folder>\<skill> -Target <clone>\skills\<skill>` |
| Antigravity | `~/.gemini/config/skills` | the same; macOS and Linux: `ln -s <clone>/skills/<skill> <folder>/<skill>` |
| Cursor | `~/.cursor/skills` or `~/.agents/skills` (also reads `~/.claude/skills`) | the same |

convert-to-wordpress has no `skills/` folder: the clone itself is the skill and its folder must be named
`convert-to-wordpress`. It updates with `scripts/update.py` (or `git pull`); the other clones with
`git pull --ff-only`.

**What you fill in yourself.** convert-to-wordpress: copy `profile.example.json` to `profile.local.json` (never
committed) with your defaults: your name, the Bcc list for lead emails, your task tracker, your local stack, your
host, the path to your ACF PRO zip if you use it, and `level`. Its README: the skill never types passwords, licence
or API keys; the one exception is your default local admin password, read from that private profile for local sites
only. Command Center: the settings block below (Set it up).
handoff: its README's "Make it load every session" block in `~/.claude/CLAUDE.md` (recommended).

**Recommended extras (the helper skills in `references/helper-skills.md`).** Free and open source; the skill uses
them when installed:
[addyosmani/web-quality-skills](https://github.com/addyosmani/web-quality-skills) (web-quality-audit, performance,
core-web-vitals, accessibility, seo, best-practices) and
[WordPress/agent-skills](https://github.com/WordPress/agent-skills) (only wp-plugin-development, wp-performance,
wp-wpcli-and-ops, wp-phpstan). Clone each once and link its skills like ours, into `~/.claude/skills` (Claude
Code), `~/.agents/skills` (Codex, Cursor) and `~/.gemini/config/skills` (Antigravity):

```powershell
git clone https://github.com/addyosmani/web-quality-skills <repos>\web-quality-skills
git clone https://github.com/WordPress/agent-skills <repos>\wordpress-agent-skills
foreach ($s in "web-quality-audit","performance","core-web-vitals","accessibility","seo","best-practices") {
  New-Item -ItemType Junction -Path <folder>\$s -Target <repos>\web-quality-skills\skills\$s }
foreach ($s in "wp-plugin-development","wp-performance","wp-wpcli-and-ops","wp-phpstan") {
  New-Item -ItemType Junction -Path <folder>\$s -Target <repos>\wordpress-agent-skills\skills\$s }
```

Chrome DevTools MCP for Claude Code, with both privacy flags (no usage statistics, no CrUX field-data lookups);
on Windows put `cmd /c` before `npx`. Other tools: the same command in their MCP settings.

```
claude mcp add chrome-devtools --scope user -- npx -y chrome-devtools-mcp@latest --no-usage-statistics --no-performance-crux
```

**Check each one loads.**
- zoho-command-center: the test in "Check it works in another AI tool" above.
- handoff: in a project folder it creates `handoff.md` and `ai-handoff-summary.md` the first time it works there.
- convert-to-wordpress: `python3 scripts/doctor.py` (Windows: `py -3`) checks your computer and lists what is missing.
- figma-to-wordpress: "Build this Figma design in WordPress: <Figma link>" makes it ask its intake questions once.

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
- Always CC: @<name> (optional: CC only, last line "CC: @<name>" in Zoho comments only; reports and chat replies to
  you have none)
- Leads portal: <admin URL> (optional: the company's leads portal; every live site with a lead form then sends its
  leads there)
```

Don't want every empty folder to become a Command Center? Drop "when the project folder is empty" and start one by
saying "set this folder up as a Command Center".

Then open a new chat.

## Use

1. Open an empty folder in the Code tab. The main chat sets itself up as "Command Center - <folder>".
2. Paste a task: a Zoho task link, or any request. Command Center sizes it (S, M or L), gives it its own chat (the
   same task's chat when it has one), and tells you in one line where it went. Say "send it to X" to override.
3. Talk to the task chat directly: read its plan, answer its questions, say **go** there.
4. When it reports DONE, Command Center has a QA chat check the work, and the task chat fixes what QA finds until
   QA finds nothing. Zoho tasks: Command Center then shows you the short comment draft with the tags and the status
   steps; say OK, and it posts the comment, moves the status to review, then closes the tabs and archives the task
   and QA chats without asking. Other tasks: it gives you a reply or report draft to send. Say "EOD" for the day's
   summary.

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

A release reaches every Command Center the next time it is used: on its first turn it compares the "Version:" line
of the installed SKILL.md with the one it has loaded and reloads the skills when the installed one is newer. Reload
messages to every chat are not needed (each one costs an idle chat a full cache rewrite).

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
(`handoff.md`, `tasks/`, `eod/`) off the web and out of git.

## Layout

```
.claude-plugin/plugin.json         the plugin
.claude-plugin/marketplace.json    this repo as a one-plugin marketplace
skills/zoho-command-center/SKILL.md the shared rules and the task chat (Worker) rules
skills/zoho-command-center/references/command-center.md  Command Center's steps 1 to 7
skills/zoho-command-center/references/tool-map.md  each action's tool, and one-chat mode for other AI tools
skills/zoho-command-center/references/leads-portal.md  the leads portal: when it is required, which way per stack, proof
skills/zoho-command-center/references/helper-skills.md  the helper skills: which one for what
skills/zoho-command-center/references/builds.md  retired: builds already running with builder and QA chats
CHANGELOG.md                       what changed in each version
AGENTS.md                          rules for changing the skill
```

## Licence

MIT. See [LICENSE](LICENSE). Zoho and Zoho Projects are trademarks of Zoho Corporation; this project is not
affiliated with Zoho.
