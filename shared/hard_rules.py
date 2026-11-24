"""Render the zoho-command-center hard rules from their one source, shared/hard-rules.md.

    python shared/hard_rules.py --write    rewrite the three generated copies from the source
    python shared/hard_rules.py --check    exit 1 when a copy differs from the source (the tests do the same)

Copies: antigravity/rules/zcc-hard-rules.md (Antigravity, and the GEMINI.md block built from it),
codex/AGENTS-block.md (Codex) and the "Hard rules" section of skills/zoho-command-center/SKILL.md (Claude).
"""
import os
import re
import sys
import textwrap

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(REPO, "shared", "hard-rules.md")
AG_FILE = os.path.join(REPO, "antigravity", "rules", "zcc-hard-rules.md")
CODEX_FILE = os.path.join(REPO, "codex", "AGENTS-block.md")
SKILL_FILE = os.path.join(REPO, "skills", "zoho-command-center", "SKILL.md")
TOOLS = ("claude", "antigravity", "codex")
AG_FRONT = """---
name: zcc-hard-rules
trigger: always_on
description: Hard rules for the zoho-command-center workflow in Antigravity (Command Center, task chats, QA).
zcc-managed: zoho-command-center antigravity setup
---
"""
TITLE = "zoho-command-center hard rules (every turn)"
SKILL_HEAD = "## Hard rules (every tool, every turn)"
SKILL_NOTE = "Always on in the Antigravity and Codex setups too (one source in the repo: `shared/hard-rules.md`)."


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def render(tool):
    """The rules for one tool, wrapped at 120 characters."""
    body = re.sub(r"<!--.*?-->\n?", "", read(SOURCE), flags=re.S)
    out = []
    for line in body.splitlines():
        if not line.strip():
            continue
        m = re.match(r"^\[([a-z, ]+)\]\s+(.*)$", line)
        if m:
            if tool not in [t.strip() for t in m.group(1).split(",")]:
                continue
            line = m.group(2)
        line = line.replace("{$}", "$" if tool == "codex" else "")
        n = re.match(r"^(\d+\.) ", line)
        indent = " " * (len(n.group(1)) + 1) if n else ""
        out += textwrap.wrap(line, width=120, subsequent_indent=indent, break_on_hyphens=False,
                             break_long_words=False)
    return "\n".join(out) + "\n"


def antigravity_file():
    return AG_FRONT + "\n# " + TITLE + "\n" + render("antigravity")


def codex_block():
    return ("<!-- zcc-managed:start (zoho-command-center Codex setup; the install script replaces this block) -->\n"
            "## " + TITLE + "\n" + render("codex") + "<!-- zcc-managed:end -->\n")


def skill_section():
    note = "\n".join(textwrap.wrap(SKILL_NOTE, width=120))
    return SKILL_HEAD + "\n" + note + "\n" + render("claude") + "\n"


def skill_with_section(skill):
    start = skill.index(SKILL_HEAD)
    end = skill.index("\n## ", start + len(SKILL_HEAD)) + 1
    return skill[:start] + skill_section() + skill[end:]


def targets():
    return {AG_FILE: antigravity_file(), CODEX_FILE: codex_block(), SKILL_FILE: skill_with_section(read(SKILL_FILE))}


def main(argv):
    diff = [p for p, text in targets().items() if read(p) != text]
    if "--write" in argv:
        for p, text in targets().items():
            if read(p) != text:
                write(p, text)
                print("wrote     " + os.path.relpath(p, REPO))
        return 0
    for p in diff:
        print("differs   " + os.path.relpath(p, REPO))
    if not diff:
        print("OK: every copy of the hard rules matches shared/hard-rules.md.")
    return 1 if diff else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
