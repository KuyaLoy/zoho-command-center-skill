# Context watch (task chat)

Moved unchanged from SKILL.md in 2.11.0 to keep the skill light; SKILL.md says when to open each part.

## Context watch (task chat)

Why: a task chat that ran to 100% auto-compacted mid-work, lost track and broke a website. So we reset early, at a safe
point, from a checkpoint on disk: the chat writes a checkpoint, Command Center clears it (an idle task chat it
started; its own reset has rules of its own) and sends a resume message (other tools: the lead opens a new chat with
that message).
Auto-compact starts at about 97%.

Thresholds (context % of the task chat; set 17 Nov 2026: a flat 50% cut work off mid-page, so finish the page first):
- **Under 50%:** nothing to do: keep working. A chat checkpoints only at the threshold in force (the brief's or plan's,
  else these) or when Command Center asks, never earlier "to have room for the next step" (learned 17 Nov 2026).
- **50%:** finish the current page or unit of work (a page, a section, a plan step), then checkpoint and reset there.
- **75%:** hard cap. Checkpoint and reset at the next safe point, even mid-page. Never continue past 80%.
- **Fast growth** (10% or more in one turn, e.g. with a team of subagents): from 65%, don't wait for the page end.
A safe point = no half-done edit, upload, import, migration or deploy; files saved; the site in a working state; and
no subagent or teammate the chat started is still working (a clear wipes the chat's memory of them).

**Worker (task chat):**
- Check your own context % before starting each step of the plan and after any big step.
- At your page end from 50% (at 75% at once, or when Command Center asks), write `tasks/<TASK-ID>/checkpoint.md`:
  task ID and scope; the lead's go and instructions (quoted); done so far (with its checks.md line); current state
  of files/site/DB (paths, URLs, backups); the exact next step; open questions; anything not yet verified.
  First let your subagents reach a safe point (list their unfinished work). Facts only: unsure means "unverified".
- Also bring `notes.md` up to date, then send Command Center: "CHECKPOINT: <TASK-ID> at <n>%, checkpoint written,
  safe to clear." and end your turn. Don't start new work after that line.
- Command Center answers "Continue, no reset" (it could not reset you): go on from your checkpoint in this chat and
  checkpoint again at your next page end (at 75% at once).
