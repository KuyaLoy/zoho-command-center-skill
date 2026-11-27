# Task size: effort, usage pacing and builds

Moved unchanged from SKILL.md in 2.11.0 to keep the skill light; SKILL.md says when to open each part.

## Effort

- **Effort by need** (the lead's rule, 27 Nov 2026; replaces "high by default" of 19 Nov: task chats paid for high
  when they did not need it). The size table in SKILL.md shows it; the brief states it ("effort <level>").
  - **Command Center: high, always** (mandatory: it decides). At step 1 and at a takeover it confirms its own effort
    from its session info; not high: it tells the lead in one line to set it (a chat cannot raise its own). In
    Antigravity, Codex and T3 Code the lead picks high for the Command Center chat.
  - **Task chats and subagents: medium by default.** High for: any change to a live site, Zoho or a client document,
    anything hard to undo, an L task after its go, QA and review chats (judgement).
  - **Max for a plan that needs deep judgement** (unchanged): every L plan, and an M plan that is unclear or risky (a
    new approach, several systems, data or SEO at scale, a conversion or build plan). At the go the chat goes to its
    work effort (high for an L task or live work, else medium) before the first work step; a re-plan after the go stays
    at that effort. "use max" from the lead still raises any part the lead names.
  - Antigravity has no effort per chat or subagent: they run on the lead's setting (high, for Command Center), and
    the brief's level says how deep to go. Codex's agent files set it (`zcc-task-worker` medium, `zcc-reviewer`
    high); a task needing high or max says so in its brief and runs as its own session at that level.

## Usage pacing and builds

- **Usage pacing** (learned 17 Nov 2026: four chats at once used 97% of the 5-hour limit; the stops were raised later,
  as 75% wasted a quarter of the window): at most 2 chats working at once (QA and review chats count); more wait as
  QUEUED. Check the usage limits before starting or resuming any chat. Every working chat stops at its next safe point
  at 95% of the 5-hour limit and at 95% of the weekly limit (raised from 80%, the lead's rule, 19 Nov 2026: the last 20%
  of the week went unused); Command Center then sets the resume time, says it once and resumes on its own (step 3). A
  project the lead tells "don't stop" (quoted and dated in its handoff.md rules) runs on to 100%. Commit or save after
  every step, so a stop leaves a clean state.
- **Builds** (a whole site or design from Figma, HTML, Next.js or another stack; learned 18 Nov 2026: multi-chat builds
  cost far more usage than the work needed): one task chat builds it with the figma-to-wordpress or
  convert-to-wordpress skill. `references/builds.md` is retired: it is kept only for a build already running with
  builder and QA chats, and removed once that build ends.
