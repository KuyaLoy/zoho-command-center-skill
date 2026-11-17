# Builds with builder and QA chats

Read this when one site or design is built by several chats in phases. Everything in SKILL.md still applies; this
file adds the build rules (learned 17 Nov 2026 on a multi-chat design build).

## Who is who
- **Lead chat:** the task chat that owns the build: its plan, its phases and the lead's go for each phase.
- **Builders:** task chats Command Center starts for a phase, after the lead chat confirms the lead typed the go for
  that phase in the lead chat (a button reply or "gave go" in Command Center is never a phase go).
- **QA chats:** the visible, read-only QA chats from SKILL.md step 2. They may run on a Sonnet model.
- **READY FOR QA:** the message a builder sends Command Center when a part is built and self-checked:
  "READY FOR QA: <task> <part>", where it is, and the measured numbers (below).

## Builders
- One builder by default. A second only when a phase is too big for one chat; then name the files each one owns.
- No helper subagents unless Command Center approves. (Helpers, and parallel builders sending each other dependency
  messages, were the largest avoidable cost.)
- Self-check every page by script before READY FOR QA.
- Hand over measured numbers next to the design values (for example sizes, spacing, font sizes and colours as
  measured on the page, beside the Figma values), not screenshots.

## QA method
- Every QA pass ends in ONE consolidated fix list per builder. The builder fixes everything on it at once; QA then
  re-checks only the fixed items, once.
- QA verifies by script and by sampling. Screenshots only for failures. Lighthouse once per page, at the gate.

## QA flow
- Builder self-check on every page (scripted).
- Strict QA once per NEW section type (site-wide issues such as letter-spacing, the CSS approach, form markup, a
  static map, hard-coded images or a missing LCP preload then get caught once, before they spread).
- One strict pass at each phase checkpoint, and one full-site strict pass before go-live.

## Builds from Figma
- At task start, sweep every final frame frame by frame and section by section, in the original file and in any
  editable copy: video fills, GIFs, motion, prototype interactions, hover and pressed variants, hidden layers, and
  differences between the original and the copy. (A hero video fill was missed by a first inventory.)
- Before building each section, fill its checklist row: sweep read; MCP calls made; video, GIF, motion,
  interactions, images, forms and icons (or "none" for each).
- QA fails a section that has no checklist row.
