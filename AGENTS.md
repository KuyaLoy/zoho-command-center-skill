# AGENTS.md

This repository is the **zoho-command-center** skill, packaged as a Claude Code plugin and a one-plugin marketplace.

## Using it

Read `skills/zoho-command-center/SKILL.md` and follow it. It needs the Claude desktop app (Code tab).

## Changing the skill

- Keep `SKILL.md` under 300 lines and its line width under 120 characters. Plain English, no dashes as punctuation.
- No real names of people, clients, companies, portals, sites or internal task IDs. Examples use "Alex Example",
  "ABC1-T8" and example.com. Personal details belong in each user's settings block (README), never in the skill.
- Keep the section names and the Command Center step numbers 1 to 7 stable: chats in the middle of a task may
  reload the skill. Add new items as sub-bullets.
- Every rule says what to do; add the date it was learned when the reason helps.
- Before a change is done:
  - `claude plugin validate . --strict` passes;
  - every changed line is in CHANGELOG.md under Unreleased;
  - a private-name scan of the repo and its history finds nothing (keep the word list outside the repo).
- Release: move Unreleased to a new version (Semantic Versioning: fix = patch, new rule = minor, changed workflow =
  major), set the same version in `.claude-plugin/plugin.json` (only there), commit, then
  `claude plugin tag --push` (tag `zoho-command-center--v<version>`) and a GitHub Release with that CHANGELOG section.
  Users only get an update when the version changes.
- Licence: MIT.
