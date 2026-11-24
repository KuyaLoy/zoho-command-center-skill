"""T3 Code support: the hard rules as a marked block in ~/.gemini/GEMINI.md (2.9.1)."""
import os
import tempfile
import unittest

from zcc_testlib import PY, REPO, load, load_module, run_main, save

ag = load_module("ag_install_t3", "antigravity/install.py")
POINTER = "# My global rules\n\nRead my CLAUDE.md first.\n"


class GeminiBlockTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = self.tmp.name
        self.gemini = os.path.join(self.home, ".gemini", "GEMINI.md")

    def tearDown(self):
        self.tmp.cleanup()

    def install(self, *extra):
        return run_main(ag, ["--home", self.home, "--python", PY, *extra])

    def test_dry_run_writes_no_block(self):
        save(self.gemini, POINTER)
        self.install("--dry-run")
        self.assertEqual(load(self.gemini), POINTER)

    def test_adds_the_block_and_keeps_the_pointer(self):
        save(self.gemini, POINTER)
        self.assertEqual(self.install()[0], 0)
        text = load(self.gemini)
        self.assertTrue(text.startswith(POINTER.rstrip("\n")))
        self.assertEqual(text.count("<!-- zcc-managed:start"), 1)
        self.assertIn("open the skill section you need", text)
        self.assertIn("Active Command Center", text)
        self.assertNotIn("trigger: always_on", text)  # the frontmatter stays in the rule file only
        self.assertLess(len(text.encode("utf-8")), ag.RULE_LIMIT)
        self.assertEqual(load(self.gemini + ".bak"), POINTER)

    def test_is_idempotent(self):
        save(self.gemini, POINTER)
        self.install()
        first = load(self.gemini)
        code, out = self.install()
        self.assertEqual(load(self.gemini), first)
        self.assertIn("unchanged", out)
        self.assertNotIn("add ", out)

    def test_creates_the_file_when_missing(self):
        self.install()
        self.assertTrue(load(self.gemini).startswith("<!-- zcc-managed:start"))

    def test_uninstall_removes_only_the_block(self):
        save(self.gemini, POINTER)
        self.install()
        self.assertEqual(self.install("--uninstall")[0], 0)
        self.assertEqual(load(self.gemini).strip(), POINTER.strip())

    def test_the_block_matches_the_rule_file(self):
        block = ag.gemini_block()
        rules = load(os.path.join(REPO, "antigravity", "rules", "zcc-hard-rules.md"))
        body = rules.split("\n---\n", 1)[1].strip()
        self.assertIn(body, block)


class ToolMapTest(unittest.TestCase):
    def test_t3_code_section(self):
        text = load(os.path.join(REPO, "skills", "zoho-command-center", "references", "tool-map.md"))
        self.assertIn("## T3 Code", text)
        for word in ("GEMINI.md", "New worktree", "/hooks", "stable"):
            self.assertIn(word, text.split("## T3 Code", 1)[1])


if __name__ == "__main__":
    unittest.main()
