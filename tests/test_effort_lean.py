"""2.13.0: effort by need (Command Center high always, task chats and subagents medium, high for live or judgement
work, max for a deep plan) and lean tool output (long output in a file, the chat shows the result and failures)."""
import os
import re
import tomllib
import unittest

from zcc_testlib import REPO, load

SKILL_DIR = os.path.join(REPO, "skills", "zoho-command-center")
REF = os.path.join(SKILL_DIR, "references")


def flat(path):
    return " ".join(load(path).split())


class EffortByNeedTest(unittest.TestCase):
    def test_size_table_and_effort_line(self):
        skill = load(os.path.join(SKILL_DIR, "SKILL.md"))
        self.assertIn("| medium (high for live work) |", skill)
        self.assertIn("| M | everything else: the usual task | medium (high for live work); max for the plan", skill)
        self.assertIn("| max for the plan, high from the go |", skill)
        text = flat(os.path.join(SKILL_DIR, "SKILL.md"))
        self.assertIn("Command Center always high; task chats and subagents medium, high for live or hard-to-undo "
                      "work, an L task after its go, QA and review", text)
        self.assertNotIn("high by default", text)

    def test_task_size_effort(self):
        text = flat(os.path.join(REF, "task-size.md"))
        for words in ("**Command Center: high, always** (mandatory: it decides)",
                      "**Task chats and subagents: medium by default.**",
                      "any change to a live site, Zoho or a client document, anything hard to undo, an L task after "
                      "its go, QA and review chats",
                      "**Max for a plan that needs deep judgement** (unchanged)",
                      "the lead picks high for the Command Center chat"):
            self.assertIn(words, text)

    def test_command_center_checks_its_own_effort(self):
        cc = flat(os.path.join(REF, "command-center.md"))
        self.assertIn("you run at high, always (mandatory: you decide); confirm it from your session info at step 1 "
                      "and at a takeover", cc)
        self.assertIn("a chat cannot raise its own", cc)
        self.assertNotIn("every chat runs at high by default", cc)
        self.assertNotIn("goes back to high at its go", cc)

    def test_brief_names_the_level(self):
        self.assertIn("effort <medium|high|max for the plan>", load(os.path.join(REF, "brief.md")))

    def test_always_on_blocks_and_readme_tell_the_lead(self):
        for path in (os.path.join(REPO, "antigravity", "rules", "zcc-hard-rules.md"),
                     os.path.join(REPO, "codex", "AGENTS-block.md")):
            self.assertIn("Effort: the lead picks high for the Command Center chat", flat(path))
        self.assertNotIn("Effort: the lead picks", load(os.path.join(SKILL_DIR, "SKILL.md")))
        readme = flat(os.path.join(REPO, "README.md"))
        self.assertIn("Command Center always runs at high", readme)
        self.assertIn("in Antigravity, Codex and T3 Code you pick it", readme)

    def test_codex_agent_files_set_the_effort(self):
        want = {"zcc-task-worker.toml": "medium", "zcc-reviewer.toml": "high"}
        for name, level in want.items():
            data = tomllib.loads(load(os.path.join(REPO, "codex", "agents", name)))
            self.assertEqual(data["model_reasoning_effort"], level, name)

    def test_tool_map_start_and_set_effort(self):
        tool_map = load(os.path.join(REF, "tool-map.md"))
        self.assertIn('`effort` from the brief ("medium", "high", or "max" for a plan that needs it', tool_map)
        row = next(l for l in tool_map.splitlines() if l.startswith("| Set a chat's effort"))
        self.assertIn("`zcc-task-worker` medium, `zcc-reviewer` high", row)
        self.assertNotIn("back to high at the go", row)


class LeanToolOutputTest(unittest.TestCase):
    def test_worker_rule(self):
        text = flat(os.path.join(SKILL_DIR, "SKILL.md"))
        self.assertIn("**Lean tool output**", text)
        for words in ("output over about 50 lines goes to a file in `tasks/<TASK-ID>/logs/`",
                      "the result line and failures only", "`--porcelain`", "`-q`", "`--format=json --fields=...`",
                      "stable first, changing last"):
            self.assertIn(words, text)

    def test_tool_map_row_has_every_column(self):
        line = next(l for l in load(os.path.join(REF, "tool-map.md")).splitlines()
                    if l.startswith("| Long tool output"))
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line)[1:-1]]
        self.assertEqual(len(cells), 6)
        self.assertTrue(all(cells))
        self.assertTrue(all("logs/" in c or c == "the same as the terminal" for c in cells[1:]))

    def test_checks_list_keeps_the_command_and_the_log_path(self):
        text = flat(os.path.join(REF, "brief.md"))
        self.assertIn('"full output: tasks/<TASK-ID>/logs/<name>.log"', text)
        self.assertIn("the evidence gate reads that block as the check's output", text)


class SkillNotLargerTest(unittest.TestCase):
    def test_not_larger_than_2_12_1(self):
        path = os.path.join(SKILL_DIR, "SKILL.md")
        self.assertLessEqual(len(load(path).splitlines()), 214)
        self.assertLessEqual(os.path.getsize(path), 20959)


if __name__ == "__main__":
    unittest.main()
