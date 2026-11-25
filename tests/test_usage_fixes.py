"""2.11.0 usage fixes: settings copied in at install, one rules copy in Antigravity."""
import os
import re
import subprocess
import tempfile
import unittest

from zcc_testlib import PY, REPO, load, load_module, run_main, save

ag = load_module("ag_install_usage", "antigravity/install.py")
cx = load_module("cx_install_usage", "codex/install.py")
CLAUDE_MD = """# Global rules

## Something else
- not copied

## Zoho Command Center settings (read by the zoho-command-center skill)

- Lead: Alex Example (approves plans)
- Zoho portal: https://projects.example.com/portal/example
- Reply language: English

## Browser tabs
- not copied either
"""


class SettingsCopiedTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = self.tmp.name
        self.claude_md = os.path.join(self.home, ".claude", "CLAUDE.md")
        self.gemini = os.path.join(self.home, ".gemini", "GEMINI.md")
        self.agents = os.path.join(self.home, ".codex", "AGENTS.md")

    def tearDown(self):
        self.tmp.cleanup()

    def install_both(self):
        _, ag_out = run_main(ag, ["--home", self.home, "--python", PY])
        _, cx_out = run_main(cx, ["--codex-home", os.path.join(self.home, ".codex"), "--python", PY])
        return ag_out, cx_out

    def test_the_settings_block_goes_into_both_managed_blocks(self):
        save(self.claude_md, CLAUDE_MD)
        ag_out, cx_out = self.install_both()
        for path in (self.gemini, self.agents):
            text = load(path)
            self.assertIn("- Lead: Alex Example (approves plans)", text, path)
            self.assertIn("Settings (copied from `~/.claude/CLAUDE.md` at install", text, path)
            self.assertNotIn("not copied", text, path)
            self.assertNotIn("Settings: the \"Zoho Command Center settings\" block", text, path)
        for out in (ag_out, cx_out):
            self.assertIn("copied the \"Zoho Command Center settings\" block (3 lines)", out)
            self.assertNotIn("Alex Example", out)  # the settings are never printed

    def test_a_rerun_copies_changes(self):
        save(self.claude_md, CLAUDE_MD)
        self.install_both()
        save(self.claude_md, CLAUDE_MD.replace("Reply language: English", "Reply language: Spanish"))
        self.install_both()
        self.assertIn("Reply language: Spanish", load(self.gemini))
        self.assertIn("Reply language: Spanish", load(self.agents))
        self.assertEqual(load(self.gemini).count("zcc-managed:start"), 1)

    def test_no_claude_md_keeps_the_pointer_line(self):
        ag_out, cx_out = self.install_both()
        for path in (self.gemini, self.agents):
            self.assertIn("Settings: the \"Zoho Command Center settings\" block in `~/.claude/CLAUDE.md`", load(path))
        self.assertIn("no \"Zoho Command Center settings\" block", ag_out)
        self.assertIn("no \"Zoho Command Center settings\" block", cx_out)

    def test_the_repository_never_holds_a_settings_block(self):
        tracked = subprocess.run(["git", "ls-files"], cwd=REPO, capture_output=True, text=True).stdout.split()
        copied = re.compile(r"Settings \(copied from[^\n]*\n- ")  # a filled-in block, as the installers write it
        for rel in tracked:
            if rel.endswith((".md", ".py", ".toml", ".json")) and os.path.isfile(os.path.join(REPO, rel)):
                self.assertIsNone(copied.search(load(os.path.join(REPO, rel))), rel)


class OneRulesCopyTest(unittest.TestCase):
    def test_old_rules_file_removed_and_gemini_block_is_the_copy(self):
        with tempfile.TemporaryDirectory() as home:
            old = os.path.join(home, ".gemini", "config", "rules", "zcc-hard-rules.md")
            save(old, load(os.path.join(REPO, "antigravity", "rules", "zcc-hard-rules.md")))
            other = os.path.join(home, ".gemini", "config", "rules", "someone.md")
            save(other, "---\ntrigger: always_on\n---\nmine")
            code, out = run_main(ag, ["--home", home, "--python", PY])
            self.assertEqual(code, 0)
            self.assertFalse(os.path.exists(old))
            self.assertTrue(os.path.exists(other))
            self.assertIn("one rules copy now", out)
            self.assertIn("1. Before each phase", load(os.path.join(home, ".gemini", "GEMINI.md")))

    def test_a_foreign_file_at_the_old_path_stays(self):
        with tempfile.TemporaryDirectory() as home:
            old = os.path.join(home, ".gemini", "config", "rules", "zcc-hard-rules.md")
            save(old, "someone else's rules")
            code, out = run_main(ag, ["--home", home, "--python", PY])
            self.assertEqual(code, 0)
            self.assertEqual(load(old), "someone else's rules")


if __name__ == "__main__":
    unittest.main()
