# Safety: records, live forms, browser tabs and handoff files

Moved unchanged from SKILL.md in 2.11.0 to keep the skill light; SKILL.md says when to open each part.

## Deleting records

- Delete pages, menus, media, options or records only by explicit IDs, after a dry-run list, a count check and a
  database backup, never by a filter. Tag scratch content with one marker (learned 17 Nov 2026: a filtered list
  command ignored its filter and deleted every page; restored from the backup).

## Live form tests, browser tabs and handoff files

- Live form tests (sites with reCAPTCHA or other bot checks): submit them in a browser with no AI control (the tool map
  names it), never one an AI drives (an extension or an MCP): it gets scored as a bot and the form fails at the spam
  check, even for the lead's own clicks (learned 9 Nov 2026). Never get around a CAPTCHA.
- Browser tabs: never close a tab you opened for a task (Zoho task, WorkDrive, WP admin, cPanel, pages you checked)
  while the task is open, whatever the browser tools' default. Once the task is in review, Command Center closes its
  tabs and has the task chat close its own, without asking (step 6; learned 12 and 18 Nov 2026). Task chats close tabs
  only when told. Tabs out of reach: name them.
- Handoff files at the project root (`handoff.md`, `ai-handoff-summary.md`) follow the user's handoff rules. Without
  such rules: `handoff.md` is the full log (Goal, Current State, Task chats, Changes Made, Failed Attempts, Next Steps;
  dated entries) and `ai-handoff-summary.md` is a short brief of at most 60 lines for the next chat. No secrets in
  either. Command Center is their only writer once task chats exist; workers log in their own task folder.

## A serious finding

- **Except a serious one** (learned 18 Nov 2026): a hacked site, malware, injected spam or a backdoor. Tell the lead
  in one line when you find it and add the fix to the plan (backup first; the task's go covers it; the task itself
  still gets done). The fix waits for the go like every step. Report it under "Serious finding (fixed)": what was
  found, what was removed, how it was checked.
