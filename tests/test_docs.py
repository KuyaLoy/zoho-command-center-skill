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
            self.assertEqual(len(row), 5, action)
            self.assertTrue(all(row), action)
        row = table_row(text, "Take over as Command Center")
        for tool, cell in zip(("Claude", "Antigravity", "Codex"), row[1:4]):
            self.assertIn("Active Command Center: " + tool, cell)

    def test_hard_rules_name_the_holder(self):
        for rel in ("antigravity/rules/zcc-hard-rules.md", "codex/AGENTS-block.md"):
            self.assertIn("Active Command Center", load(os.path.join(REPO, rel)), rel)


if __name__ == "__main__":
    unittest.main()
