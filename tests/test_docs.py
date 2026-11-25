"""The skill's own documents: switching tools between Claude, Antigravity and Codex."""
import os
import re
import unittest

from zcc_testlib import REPO, load

REF = os.path.join(REPO, "skills", "zoho-command-center", "references")
HOLDER = re.compile(r"Active Command Center: <Claude\|Antigravity\|Codex>\s+since <YYYY-MM-DD HH:MM> "
                    r"\(chat: <id or name>\)")


def table_row(text, action):
    for line in text.splitlines():
        if line.startswith("| " + action):
            return [c.strip() for c in re.split(r"(?<!\\)\|", line)[1:-1]]
    return None


class SwitchingToolsTest(unittest.TestCase):
    def test_holder_line_format_is_defined(self):
        text = load(os.path.join(REF, "command-center.md"))
        self.assertRegex(text, HOLDER)
        for step in ("Handing over", "Taking over", "Continuation chats across tools", "Switching back"):
            self.assertIn(step, text)

    def test_board_names_each_chats_tool(self):
        text = load(os.path.join(REF, "command-center.md"))
        self.assertIn("Chat (tool: name / id)", text)
        self.assertIn("moved to Codex", text)

    def test_takeover_is_in_every_tools_column(self):
        text = load(os.path.join(REF, "tool-map.md"))
        for action in ("Take over as Command Center", "Hand over to another tool"):
            row = table_row(text, action)
            self.assertIsNotNone(row, action)
            self.assertEqual(len(row), 6, action)
            self.assertTrue(all(row), action)
        row = table_row(text, "Take over as Command Center")
        for tool, cell in zip(("Claude", "Antigravity", "Codex", "Codex"), row[1:5]):
            self.assertIn("Active Command Center: " + tool, cell)

    def test_hard_rules_name_the_holder(self):
        for rel in ("antigravity/rules/zcc-hard-rules.md", "codex/AGENTS-block.md"):
            self.assertIn("Active Command Center", load(os.path.join(REPO, rel)), rel)


class Polish292Test(unittest.TestCase):
    def test_codex_desktop_column(self):
        text = load(os.path.join(REF, "tool-map.md"))
        header = table_row(text, "Action")
        self.assertIn("Codex desktop app", header[4])
        start = table_row(text, "Start a task, QA or review chat")[4]
        for word in ("request_user_input", "create_thread", "set_thread_title", "⏸ WAITING on <lead>"):
            self.assertIn(word, start)
        self.assertIn("wait_threads", table_row(text, "Wait for a chat to go idle")[4])
        self.assertIn("set_thread_archived", table_row(text, "Archive or revive a chat")[4])
        self.assertIn("Command Center - <project>", table_row(text, "Rename your own chat")[4])

    def test_created_chat_title_is_waiting_until_it_runs(self):
        skill = " ".join((load(os.path.join(REPO, "skills", "zoho-command-center", "SKILL.md")) +
                          load(os.path.join(REF, "how-we-talk.md"))).split())  # 2.11.0: moved there unchanged
        self.assertIn("created without a running first prompt starts as \"⏸ WAITING on <lead>", skill)
        start = table_row(load(os.path.join(REF, "tool-map.md")), "Start a task, QA or review chat")[2]
        self.assertIn("⏸ WAITING on <lead>", start)

    def test_plan_is_approved_in_its_task_chat(self):
        skill = " ".join((load(os.path.join(REPO, "skills", "zoho-command-center", "SKILL.md")) +
                          load(os.path.join(REF, "how-we-talk.md"))).split())  # 2.11.0: moved there unchanged
        self.assertIn("approves only the briefs, never a task's plan", skill)
        self.assertIn("with the plan itself", skill)

    def test_briefs_carry_checks_required(self):
        text = load(os.path.join(REF, "command-center.md"))
        self.assertGreaterEqual(text.count("\"Checks required:\""), 2)


if __name__ == "__main__":
    unittest.main()
