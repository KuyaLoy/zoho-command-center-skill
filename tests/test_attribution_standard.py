"""2.12.1: Vocalise early names the company form attribution standard and the agency footer badge, as plan
defaults that point to the build skill (no copy)."""
import os
import unittest

from zcc_testlib import REPO

HOW = os.path.join(REPO, "skills", "zoho-command-center", "references", "how-we-talk.md")


def section(text, title):
    start = text.index("## " + title)
    end = text.find("\n## ", start + 1)
    return text[start:end if end != -1 else None]


class AttributionStandardTest(unittest.TestCase):
    def setUp(self):
        with open(HOW, encoding="utf-8") as f:
            self.vocalise = " ".join(section(f.read(), "Vocalise early").split())

    def test_standard_named(self):
        for phrase in ("company standard", "11 labelled attribution fields", "form layout default",
                       "bridge plugin", "agency badge with its link", "asked to hide it",
                       "convert-to-wordpress 0.12.0 or later", "no copy"):
            self.assertIn(phrase, self.vocalise)

    def test_defaults_not_additions(self):
        self.assertIn("defaults in every website plan, not additions to approve", self.vocalise)


if __name__ == "__main__":
    unittest.main()
