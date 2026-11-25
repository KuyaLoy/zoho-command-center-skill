"""2.11.1: one simple phrase sets up or takes over a Command Center; the takeover brief is short and fixed."""
import os
import re
import unittest

from zcc_testlib import REPO, load, load_module

ag = load_module("ag_install_trigger", "antigravity/install.py")
PHRASES = ('"set this as command center"', '"command center"', '"take over"', '"gawin mong command center"')
SKILL = os.path.join(REPO, "skills", "zoho-command-center", "SKILL.md")
CC = os.path.join(REPO, "skills", "zoho-command-center", "references", "command-center.md")


def flat(text):
    return " ".join(text.split())


class TriggerPhrasesTest(unittest.TestCase):
    def test_in_the_description(self):
        desc = re.search(r"^description: '(.*)'$", load(SKILL), re.M).group(1)
        for phrase in PHRASES:
            self.assertIn(phrase, desc)
        self.assertLessEqual(len(desc), 1024)

    def test_in_every_always_on_rule_copy(self):
        copies = {"antigravity": load(os.path.join(REPO, "antigravity", "rules", "zcc-hard-rules.md")),
                  "gemini block": ag.gemini_block(),
                  "codex": load(os.path.join(REPO, "codex", "AGENTS-block.md")),
                  "claude": load(SKILL)}
        for name, text in copies.items():
            for phrase in PHRASES:
                self.assertIn(phrase, flat(text), (name, phrase))
        self.assertIn("`$zoho-command-center`, step 1", flat(copies["codex"]))


class TakeoverBriefTest(unittest.TestCase):
    def test_step_1_sets_up_or_takes_over_from_the_phrase_alone(self):
        text = flat(load(CC))
        self.assertIn("**The lead's phrase alone is enough**", text)
        self.assertIn("An empty or new folder: set up", text)
        self.assertIn("take over at once", text)
        self.assertIn("keep all its history", text)

    def test_the_brief_template_in_order(self):
        text = flat(load(CC))
        self.assertIn("**The takeover brief**", text)
        self.assertIn("at most 10 lines, always in this order", text)
        order = [text.index(label) for label in ("- Project: name, site, mode", "- Last jobs: the last 1 or 2",
                                                 "- Open now: each open task", "- Next: one line")]
        self.assertEqual(order, sorted(order))
        self.assertIn("the newest `eod/` files and handoff.md's Changes Made", text)
        self.assertIn("4. Report the takeover brief (step 1", text)


if __name__ == "__main__":
    unittest.main()
