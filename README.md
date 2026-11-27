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
- **Antigravity**: Antigravity mode, with the setup below (Use it in Antigravity): Command Center creates each task
  chat as a conversation and keeps its state in the title.
- **Codex**: Codex mode, with the setup below (Use it in Codex): task chats are sessions you open with
  `$zoho-command-center`, and QA runs as its own read-only session.
- **T3 Code**: runs those tools as its providers (Use it in T3 Code below).
- **Other AI tools** (Claude Code in a terminal, Codex, Cursor, OpenCode, Cline, Devin Desktop and others
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

## Use it in Antigravity

Antigravity opens a skill only when the model judges it relevant, so on its own a task chat there can skip the
skills. The `antigravity/` folder makes the rules mechanical:

- The hard rules written out (open the skill before each phase, no check reported without its output, copy kit
  files and source text exactly, no guessed defaults, no secrets in files and no consent set for anyone, Zoho only by
  the task link, plan first, state in the title, phase-end checkpoints) and your "Zoho Command Center settings" block
  (copied from `~/.claude/CLAUDE.md` at install, so chats need not read that file), as one marked block in
  `~/.gemini/GEMINI.md`, which Antigravity and T3 load always. That is the only copy: since 2.11.0 the install removes
  the old `config/rules/zcc-hard-rules.md` it put there. Re-run the install after you change your settings.
- `agents/task-worker.md` (the task chat, with its skills attached) and `agents/wp-qa.md` (QA). QA is read-only by
  its rules plus a sandboxed shell, not by its tool list alone: it has no file-editing tools, but its shell could
  still write. Both keep your current model.
- Three hooks (from `shared/hooks/`): the essentials of the project's `ai-handoff-summary.md` (Status, Now, Next action,
  Waiting on; about 1,500 characters) are injected at the start of each conversation, a write that puts a password, key
  or token into a .md file is denied, and the evidence gate (below) sends a report back once when a check it names has
  no command output in the task's `checks.md`.

Install from the clone (link the skills first, as "Where each skill goes" below shows). It needs Python 3, writes
only its own files into `~/.gemini/config/`, keeps every other rule, agent and hook, stops before any change if a
file at its paths is not its own, and is safe to run again after each `git pull`:

```powershell
python <clone>\antigravity\install.py --dry-run
python <clone>\antigravity\install.py
```

`--uninstall` removes only what it installed. Then open the project in Antigravity and start the main conversation
with `/zoho-command-center`: each task runs as a `task-worker` subagent of that one Command Center (subagent mode,
below); a separate task conversation only when you ask for one. The Antigravity column of `references/tool-map.md`
lists every action there.

### Antigravity and your Chrome

The Antigravity app drives only its own browser pane (its own cookies, so none of your sign-ins). To let it work in
your Chrome, as Claude and Codex do, add the Chrome DevTools MCP server once (opt-in; it adds only that one entry to
`~/.gemini/config/mcp_config.json` and leaves your other servers alone):

```powershell
python <clone>\antigravity\install.py --with-chrome
```

Then in Chrome (version 144 or later) open `chrome://inspect/#remote-debugging`, turn on "Allow remote debugging for
this browser instance", and start a new Antigravity conversation. The agent can see every tab of that Chrome, so use a
work-only Chrome profile for it. It follows the Browser rules in `references/tool-map.md`: it lists the pages first,
works only in the task's own tabs, and leaves every sign-in and password to you. `--uninstall --with-chrome` removes
the entry again.

## Use it in Codex

Codex also opens a skill by itself only when it judges it relevant. The `codex/` folder sets the same rules up there:

- `AGENTS-block.md`: the hard rules, added with your "Zoho Command Center settings" block (copied from
  `~/.claude/CLAUDE.md` at install) as a marked block to `~/.codex/AGENTS.md` (the rest of that file stays).
- `agents/zcc-task-worker.toml` and `agents/zcc-reviewer.toml`: the `zcc-task-worker` subagent that does each task
  and the `zcc-reviewer` QA subagent (read-only by its rule: a subagent keeps the parent's sandbox).
- The same three hooks, in `~/.codex/hooks.json`.

```powershell
python <clone>\codex\install.py --dry-run
python <clone>\codex\install.py
```

Then run `codex`, open `/hooks` and trust the three "zcc:" hooks: Codex runs a hook only after you trust it, and asks
again when it changes. `--uninstall` removes only what it installed. Start the main session in the project with
`$zoho-command-center`: each task runs as a subagent of it (subagent mode, below). A separate task session only when
you want one (`$zoho-command-center Read tasks/<TASK-ID>/brief.md and follow its Worker rules`); a sandboxed read-only
QA only on your word (`codex exec -s read-only ... -o tasks/<TASK-ID>/qa/qa-<n>.md`). The Codex columns of
`references/tool-map.md` list every action there.

In the **Codex desktop app**, Command Center does more itself: the app creates a thread only when you ask, so when the
briefs are ready it asks you once with choices ("Create the task chats now?"), then creates each task thread with its
first prompt, titles it ("⏸ WAITING on <you> | ..." until it runs), follows it and sends it follow-ups. It also titles
its own thread "Command Center - <project>". Each task's plan is shown and approved in its own thread, with choices;
an "approved" in Command Center approves only the briefs. Task chats use the effort you chose for the app; high only
for an L task or live or irreversible work, and the chat says so.

## Subagent mode: one Command Center (Antigravity and Codex)

In Antigravity and Codex, separate task chats came out empty, mis-titled or used a small plan's limit fast, so task work
runs as subagents of the one Command Center: it briefs each task and starts it as a subagent (`task-worker` /
`zcc-task-worker`); the plan comes back to Command Center, which shows it to you with choices; you type the go in
Command Center's chat and it quotes your words to the subagent; QA is its own subagent (`wp-qa` / `zcc-reviewer`) that
runs every check itself. The board lists each subagent and its state. A separate task chat only when you ask for one.
The 11 hard rules are the same in every tool, from one source (`shared/hard-rules.md`, written into all copies by
`python shared/hard_rules.py --write`).

## Use it in T3 Code

T3 Code runs Claude, Codex and Antigravity themselves, so each follows its own setup above, with these limits:

- **Antigravity in T3** uses a private profile: it loads `~/.gemini/GEMINI.md` but not `config/rules`, the hooks or
  the custom agents. The Antigravity install therefore writes the hard rules (and your settings) as a marked block
  into `~/.gemini/GEMINI.md` (your own text there stays; `--uninstall` removes only the block). Inside T3 the rules
  carry it; the hooks and agents work only in Antigravity itself.
- **Codex in T3** runs only hooks you already trusted in Codex: after each install or update, open `codex` and trust
  the "zcc:" hooks in `/hooks` before using T3.
- **Claude in T3** loads your `~/.claude/CLAUDE.md`, skills and plugins as usual.
- One T3 thread per task, run in the project checkout, never "New worktree" (a T3 worktree has no local handoff files
  or task folders). Rename the thread for its status prefix. Stay on T3's stable release.

The "T3 Code" section of `references/tool-map.md` has the per-tool table.

## Keep usage low (Codex and Antigravity)

A new chat loads only what it needs: the session-start hook injects the summary's essentials, not the whole file;
each role opens only its own sections (SKILL.md "Files"); a takeover reads the summary, the board and each open
task's stops and checkpoint; the always-on rules are about 1.8 KB. On a small plan, suggest a cheaper model or low
effort for small tasks (you pick), keep one task chat at a time, and run heavy visual QA in a tool with a larger plan.

## The evidence gate and the hook self-test

Every DONE, PART DONE, READY FOR QA and QA report lists its checks in a "Checks:" line, and each check is a
"## <check>" section of `tasks/<TASK-ID>/checks.md` with a code block holding the command and its output. The Stop
hook sends a report back once (Antigravity: continue; Codex: block) when a named check has no output there; it never
loops.

Hooks are a second line; the always-on rules are the first. A forum report says some Antigravity hooks never fire on
Windows 11, so check them on your machine before relying on them:

```powershell
python <clone>\shared\hook_selftest.py install --tool antigravity
python <clone>\shared\hook_selftest.py report
python <clone>\shared\hook_selftest.py remove --tool antigravity --clear-log
```

`install` adds a log-only hook and says what to do in the tool (one message that runs a command); `report` shows
whether SessionStart, PreToolUse and Stop fired; `remove` takes it out. Use `--tool codex` for Codex (trust the
"zcc-selftest" hooks in `/hooks` first). Tests for all of this: `python -m unittest discover -s tests`.

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
- Leads portal: <admin URL> or none (optional: only when you name a portal does every live site with a lead form
  send its leads there; "none" or no line: no portal step)
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
skills/zoho-command-center/references/tool-map.md  each action's tool: Claude app, Antigravity, one-chat mode
skills/zoho-command-center/references/leads-portal.md  the leads portal, only when the settings name one: way, proof
skills/zoho-command-center/references/helper-skills.md  the helper skills: which one for what
skills/zoho-command-center/references/builds.md  retired: builds already running with builder and QA chats
antigravity/install.py             installs the Antigravity setup (rules, agents, hooks) into ~/.gemini/config
antigravity/rules, agents          the files it installs
codex/install.py                   installs the Codex setup (AGENTS.md block, agents, hooks) into ~/.codex
codex/AGENTS-block.md, agents      the files it installs
shared/hooks/                      the hooks both install (handoff brief, secrets guard, evidence gate)
shared/hook_selftest.py            shows whether hooks fire on this machine
tests/                             tests for the setups and hooks (run by the check workflow)
CHANGELOG.md                       what changed in each version
AGENTS.md                          rules for changing the skill
```

## Licence

MIT. See [LICENSE](LICENSE). Zoho and Zoho Projects are trademarks of Zoho Corporation; this project is not
affiliated with Zoho.
