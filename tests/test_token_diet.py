"""2.12.0 (token diet): Command Center briefs in about 8 lines, checks are one pass/fail list, no self-check lines,
read-only helper work runs as a background subagent, and Command Center moves to a fresh chat instead of clearing."""
import os
import re
import unittest

from zcc_testlib import REPO, load, load_module

SKILL_DIR = os.path.join(REPO, "skills", "zoho-command-center")
REF = os.path.join(SKILL_DIR, "references")
lib = load_module("zcc_hooklib", os.path.join("shared", "hooks", "zcc_hooklib.py"))


def flat(path):
    return " ".join(load(path).split())


def row(text, action):
    line = next(l for l in text.splitlines() if l.startswith("| " + action))
    return [c.strip() for c in re.split(r"(?<!\\)\|", line)[1:-1]]


class BriefTemplateTest(unittest.TestCase):
    def setUp(self):
        self.text = load(os.path.join(REF, "brief.md"))
        self.block = re.search(r"```markdown\n(.*?)```", self.text, re.S).group(1)

    def test_about_eight_lines_and_every_part(self):
        lines = [l for l in self.block.splitlines() if l.strip() and not l.startswith(">")]
        self.assertLessEqual(len(lines), 10, lines)
        for part in ("Goal and why:", "Quality bar:", "Tools and facts:", "Freedom:", "Checks required:",
                     "Where it goes:", "Goal in one line:", "follow its Worker rules"):
            self.assertIn(part, self.block)
        self.assertTrue(self.block.lstrip().startswith("> "), "the lead's words are quoted once at the top")

    def test_the_evidence_gate_reads_its_checks_line(self):
        sample = self.block.replace("<check>, <check>, <check>", "home 200, LCP under 2.5 s, form email received")
        names = [n for m in lib.REQUIRED_LINE.finditer(sample) for n in lib.split_names(m.group(1))]
        self.assertEqual(names, ["home 200", "LCP under 2.5 s", "form email received"])

    def test_no_restated_worker_rules_and_the_checks_list_format(self):
        self.assertIn("Never restate rules the worker already loads", self.text)
        self.assertIn("Pass|Fail | line | evidence", self.text)
        self.assertNotIn("until the lead says go", self.block)

    def test_step_2_points_to_it(self):
        cc = flat(os.path.join(REF, "command-center.md"))
        self.assertIn("a brief of about 8 lines in the shape of `brief.md`", cc)
        self.assertIn("Never restate rules the worker already loads", cc)
        self.assertIn("brief.md", flat(os.path.join(SKILL_DIR, "SKILL.md")))


class NoSelfCheckLinesTest(unittest.TestCase):
    PHRASES = ("verify each", "prove working", "done and verified", "verify the brief's key facts",
               "self-check", "verification that proves", "prove every item", "how you verified it",
               "make one spot check yourself")

    def test_gone_from_skill_and_references(self):
        for name in ["SKILL.md"] + ["references/" + f for f in os.listdir(REF)]:
            text = flat(os.path.join(SKILL_DIR, name)).lower()
            for phrase in self.PHRASES:
                self.assertNotIn(phrase, text, (name, phrase))

    def test_hard_rule_2_names_the_pass_fail_line(self):
        self.assertIn('a "Pass|Fail" line and a "## <check>" section', flat(os.path.join(REPO, "shared",
                                                                                          "hard-rules.md")))


class ChatChoiceAndMoveTest(unittest.TestCase):
    def test_chat_or_subagent(self):
        skill = flat(os.path.join(SKILL_DIR, "SKILL.md"))
        cc = flat(os.path.join(REF, "command-center.md"))
        self.assertIn("**Chat or subagent**", skill)
        self.assertIn("a background subagent for read-only work", skill)
        for words in ("a background subagent of yours for read-only work", "a QA second read",
                      "A new task or a release always starts in a fresh chat"):
            self.assertIn(words, cc)
        self.assertNotIn("never a hidden background subagent", cc)
        cells = row(load(os.path.join(REF, "tool-map.md")), "Read-only helper")
        self.assertEqual(len(cells), 6)
        self.assertTrue(all(cells))

    def test_command_center_moves_never_clears_itself(self):
        cc = flat(os.path.join(REF, "command-center.md"))
        self.assertIn("Move to a fresh chat at milestones; never clear yourself", cc)
        self.assertNotIn("Reset yourself only when it is safe", cc)
        self.assertIn('"Command Center moved: send your stops to <its id>"', cc)
        tool_map = load(os.path.join(REF, "tool-map.md"))
        self.assertFalse(any(l.startswith("| Reset Command Center") for l in tool_map.splitlines()))
        cells = row(tool_map, "Move Command Center to a fresh chat")
        self.assertEqual(len(cells), 6)
        self.assertIn('never `clear_session` "self"', cells[1])
        for cell in cells[1:]:
            self.assertIn("take over", cell)

    def test_effort_by_need(self):  # 2.13.0 replaced "high by default" (test_effort_lean.py has the rest)
        self.assertIn("| M | everything else: the usual task | medium", load(os.path.join(SKILL_DIR, "SKILL.md")))


if __name__ == "__main__":
    unittest.main()
