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
  - every changed line is in CHANGELOG.md: a change to the skill or the manifests (`skills/`, `.claude-plugin/`)
    under its new version (see Release), a docs-only change under Unreleased;
  - a private-name scan of the repo and its history finds nothing (keep the word list outside the repo).
- Release: a merge to main that changes the skill is a release, so main is always a released version.
  1. In the pull request: raise the version in `.claude-plugin/plugin.json` (only there; Semantic Versioning: fix =
     patch, new rule = minor, changed workflow = major) and add its `## [x.y.z] - YYYY-MM-DD` section to CHANGELOG.md
     (move any Unreleased lines into it). The `check` workflow fails a pull request that changes the skill without both.
  2. Run the private-name scan, then merge.
  3. The `release` workflow tags `zoho-command-center--v<version>` and publishes the GitHub Release with that
     CHANGELOG section. Users with auto-update get it in their next chat; clones with a scheduled pull within days.
  If the workflow fails: `claude plugin tag --push` and a GitHub Release with that CHANGELOG section, by hand.
  Users only get an update when the version changes.
- Licence: MIT.
