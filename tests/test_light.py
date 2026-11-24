"""2.9.3: a lighter start (less loaded at session start, the same rules)."""
import os
import re
import tempfile
import unittest

from zcc_testlib import REPO, hook, load, save

SUMMARY = """# AI handoff summary: example
Updated: 2026-11-24 10:00 | By: Command Center - example
Last change: something
Status: ACTIVE

## Now
- T1 building pages
- Waiting on: the lead's go for T2

## Next action
- T1: phase 3 forms

## Verified facts
""" + "\n".join("- fact %d [verified 2026-11-24: check]" % i for i in range(200)) + """

## Key paths
- tasks/T1/
"""


class SessionStartIsLightTest(unittest.TestCase):
    def run_hook(self, tool, text):
        with tempfile.TemporaryDirectory() as d:
            save(os.path.join(d, "ai-handoff-summary.md"), text)
            r = hook("zcc_session_start.py", tool, {"cwd": d, "workspacePaths": [d]})
        if tool == "codex":
            return r["hookSpecificOutput"]["additionalContext"]
        return r["injectSteps"][0]["systemMessage"]["systemMessage"]

    def test_only_the_essentials_under_the_cap(self):
        for tool in ("codex", "antigravity"):
            msg = self.run_hook(tool, SUMMARY)
            self.assertLess(len(msg), 2000, tool)
            for kept in ("Status: ACTIVE", "## Now", "## Next action", "T1: phase 3 forms", "Waiting on: the lead"):
                self.assertIn(kept, msg, (tool, kept))
            for dropped in ("Verified facts", "fact 7", "Key paths"):
                self.assertNotIn(dropped, msg, (tool, dropped))
            self.assertIn("ai-handoff-summary.md", msg)

    def test_a_huge_now_section_is_cut(self):
        big = SUMMARY.replace("- T1 building pages", "\n".join("- line %d of work" % i for i in range(300)))
        msg = self.run_hook("codex", big)
        self.assertLess(len(msg), 2000)
        self.assertIn("[cut: read the file for the rest]", msg)

    def test_codex_context_limit_matches(self):
        self.assertIn("additionalContextLimit=2000", load(os.path.join(REPO, "codex", "install.py")))


class ShortRulesTest(unittest.TestCase):
    FILES = ("antigravity/rules/zcc-hard-rules.md", "codex/AGENTS-block.md")

    def test_all_eleven_rules_in_a_small_budget(self):
        for rel in self.FILES:
            text = load(os.path.join(REPO, rel))
            numbers = [int(n) for n in re.findall(r"^(\d+)\. ", text, re.M)]
            self.assertEqual(numbers, list(range(1, 12)), rel)
            self.assertLess(len(text.encode("utf-8")), 2100, rel)
            for word in ("checks.md", "Checks required:", "Active Command Center", "## Stops", "qa/brief.md",
                         "open the skill section you need"):
                self.assertIn(word, text, (rel, word))


class QaRunsItsOwnChecksTest(unittest.TestCase):
    def test_rule_11_says_command_center_never_runs_qa_checks(self):
        for rel in ShortRulesTest.FILES:
            text = load(os.path.join(REPO, rel))
            rule = " ".join(re.search(r"^11\. (.+?)(?=^\S)", text, re.M | re.S).group(1).split())
            self.assertIn("runs every check itself; Command Center never runs QA checks", rule, rel)

    def test_step_5_and_the_qa_brief_say_how(self):
        text = " ".join(load(os.path.join(REPO, "skills", "zoho-command-center", "references",
                                          "command-center.md")).split())
        for words in ("full-page screenshots", "one scroll has triggered the reveals", "LCP above 2.5 s",
                      "Command Center never runs QA checks", "you brief and read its report"):
            self.assertIn(words, text)
        qa = " ".join(load(os.path.join(REPO, "antigravity", "agents", "wp-qa.md")).split())
        self.assertIn("You run every check yourself", qa)


class LoadOnDemandTest(unittest.TestCase):
    def test_skill_says_what_to_open(self):
        skill = " ".join(load(os.path.join(REPO, "skills", "zoho-command-center", "SKILL.md")).split())
        self.assertIn("open only the section you need", skill)
        self.assertIn("task chats never need it", skill)
        self.assertIn("your tool's column and mode section only", skill)

    def test_takeover_reads_light(self):
        text = load(os.path.join(REPO, "skills", "zoho-command-center", "references", "command-center.md"))
        self.assertIn("Read light", text)

    def test_usage_row_for_every_tool(self):
        text = load(os.path.join(REPO, "skills", "zoho-command-center", "references", "tool-map.md"))
        row = next(l for l in text.splitlines() if l.startswith("| Keep usage low"))
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", row)[1:-1]]
        self.assertEqual(len(cells), 6)
        self.assertTrue(all(cells))


if __name__ == "__main__":
    unittest.main()
