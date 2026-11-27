# The brief and the checks list

Open when you write a brief (Command Center step 2) or a checks list (Worker rules). Added in 2.12.0 (the lead's
rule, 27 Nov 2026: a long request sent on as it came costs tokens in every chat that reads it; simplify it first).

## The brief

Command Center rewrites each request, however long, as a brief of about 8 lines before it goes to a chat or a
subagent. The lead's words go once, quoted, at the top of `tasks/<TASK-ID>/brief.md` (a Zoho task: its link and
title); the brief follows them. Write it in this shape:

```markdown
> <the lead's words, verbatim, once>

Task: <TASK-ID> <title>. Size <S|M|L>, effort <high|max for the plan>. Site or repo: <where>.
- Goal and why: <what and why, with the real numbers>.
- Quality bar: <what good looks like: the source doc, an example, the measure>.
- Tools and facts: <links, docs, skills; sign-ins the lead does; facts found so far (re-check before relying on them)>.
- Freedom: change the approach when reality differs; re-plan before acting on it.
- Checks required: <check>, <check>, <check>
- Where it goes: <local, staging or live; branch or PR; who reviews>.
- Goal in one line: <one sentence>.
Load the zoho-command-center skill and follow its Worker rules.
```

- **Never restate rules the worker already loads**: no change before the go, stop messages, the Context watch,
  Recommended additions, the hard rules. The Worker rules carry them; repeating them costs tokens in every turn.
- **Checks required** is one plain line of check names separated by commas, nothing after the last one (the evidence
  gate reads it). Each name is objective: a status, a number, a match ("home 200", "LCP under 2.5 s", "form email
  received"), never a judgement ("looks professional").
- **Add a line only when it applies:** the leads portal way (step 2, only when the settings name a portal); for a
  build or site change, the forms (plugin and where leads go), placeholders for missing content and the build
  skill's live checklist; several chats on the same site or repo: their own local ports and temp folders, the files
  they share, no whole-database restores, live uploads announced to each other.
- A follow-up or a QA brief uses the same shape; the QA brief's "Checks required:" line always names the visual check
  and the speed check (step 2).

## The checks list (checks.md)

One list per task in `tasks/<TASK-ID>/checks.md`, one line per check, written as each check runs:

```markdown
Pass | home 200 | ## home 200
Fail | LCP under 2.5 s | ## speed (3.1 s on mobile)
```

- `Pass|Fail | line | evidence`: the line is a brief's check or a plan item; the evidence names its "## <check>"
  section below the list (the command and its output in a code block, hard rule 2) or a screenshot path for a visual
  check. No subjective lines.
- A Fail is fixed and run again, or reported as Fail. Not run: "not checked". The report's "Checks:" line names them.
- These lines replace "verify your work" steps: the list is the check, and QA (a fresh reader) reads it.
