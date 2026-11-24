"""2.10.0: one source for the hard rules, the same rules in every tool, and subagent mode."""
import contextlib
import io
import os
import re
import unittest

from zcc_testlib import REPO, load, load_module

hr = load_module("hard_rules", "shared/hard_rules.py")
ag = load_module("ag_install_rules", "antigravity/install.py")
REF = os.path.join(REPO, "skills", "zoho-command-center", "references")


def rules(text):
    """{number: rule text with whitespace and the Codex "$" folded} for rules 1 to 11."""
    out = {}
    for m in re.finditer(r"^(\d+)\. (.+?)(?=^\d+\. |^Settings:|^<!--|\Z)", text, re.M | re.S):
        out[int(m.group(1))] = " ".join(m.group(2).split()).replace("`$", "`")
    return out


def table_row(text, action):
    for line in text.splitlines():
        if line.startswith("| " + action):
            return [c.strip() for c in re.split(r"(?<!\\)\|", line)[1:-1]]
    return None


class OneSourceTest(unittest.TestCase):
    def test_every_copy_matches_the_source(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(hr.main(["--check"]), 0)

    def test_the_four_copies_say_the_same_rules(self):
        skill = load(os.path.join(REPO, "skills", "zoho-command-center", "SKILL.md"))
        skill = skill[skill.index(hr.SKILL_HEAD):]
        skill = skill[:skill.index("\n## ", 1)]
        copies = {
            "claude (SKILL.md)": rules(skill),
            "antigravity": rules(load(hr.AG_FILE)),
            "gemini block": rules(ag.gemini_block()),
            "codex": rules(load(hr.CODEX_FILE)),
        }
        for name, got in copies.items():
            self.assertEqual(sorted(got), list(range(1, 12)), name)
        base = copies["claude (SKILL.md)"]
        for name, got in copies.items():
            for n in range(1, 11):
                self.assertEqual(got[n], base[n], (name, n))
            self.assertIn("runs every check itself; Command Center never runs QA checks", got[11], name)

    def test_rule_7_names_both_modes(self):
        text = " ".join(load(hr.SOURCE).split())
        self.assertIn("in the task chat (Claude), or in the Command Center chat for a subagent (Antigravity, Codex), "
                      "quoted to the subagent", text)

    def test_codex_qa_says_its_read_only_state_rests_on_the_rule(self):
        self.assertIn("read-only by this rule", " ".join(load(hr.CODEX_FILE).split()))


class SubagentModeTest(unittest.TestCase):
    def test_subagent_rows_for_antigravity_and_both_codex_columns(self):
        text = load(os.path.join(REF, "tool-map.md"))
        for action, words in (
                ("Run a task as a subagent", ("task-worker", "zcc-task-worker", "the same")),
                ("A subagent's plan and the lead's go", ("send_message", "request_user_input", "the same")),
                ("The QA subagent", ("wp-qa", "zcc-reviewer", "the same"))):
            row = table_row(text, action)
            self.assertIsNotNone(row, action)
            self.assertEqual(len(row), 6, action)
            for cell, word in zip(row[2:5], words):
                self.assertIn(word, cell, (action, word))
        self.assertIn("## Subagent mode (Antigravity and Codex, the default)", text)
        start = table_row(text, "Start a task, QA or review chat")
        for cell in start[2:5]:
            self.assertTrue(cell.startswith("Default: the task runs as a subagent"), cell[:60])

    def test_agent_names_match_the_rules(self):
        worker = load(os.path.join(REPO, "codex", "agents", "zcc-task-worker.toml"))
        reviewer = load(os.path.join(REPO, "codex", "agents", "zcc-reviewer.toml"))
        self.assertIn('name = "zcc-task-worker"', worker)
        self.assertIn('name = "zcc-reviewer"', reviewer)
        self.assertIn("You run every check yourself", reviewer)
        self.assertIn("PLAN READY", load(os.path.join(REPO, "antigravity", "agents", "task-worker.md")))

    def test_command_center_step_2_and_skill_name_subagent_mode(self):
        self.assertIn("Antigravity and Codex: subagent mode", load(os.path.join(REF, "command-center.md")))
        skill = " ".join(load(os.path.join(REPO, "skills", "zoho-command-center", "SKILL.md")).split())
        self.assertIn("**Subagent mode** (Antigravity and Codex", skill)


class MovedRulesTest(unittest.TestCase):
    def test_code_rules_moved_unchanged(self):
        ref = " ".join(load(os.path.join(REF, "code-quality.md")).split())
        for words in ("**Lean code** (learned 19 Nov 2026)", "**Clean code** (the lead's rule, 19 Nov 2026",
                      "**Bulk scripts are safe to re-run**", "**The project folder is the site**"):
            self.assertIn(words, ref)
        skill = load(os.path.join(REPO, "skills", "zoho-command-center", "SKILL.md"))
        self.assertIn("references/code-quality.md", skill)


if __name__ == "__main__":
    unittest.main()
