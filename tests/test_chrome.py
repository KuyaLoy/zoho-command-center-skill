"""2.10.2: Antigravity drives the lead's Chrome through the chrome-devtools MCP (opt-in install, browser rules)."""
import json
import os
import tempfile
import unittest

from zcc_testlib import PY, REPO, load, load_module, run_main, save

ag = load_module("ag_install_chrome", "antigravity/install.py")
OTHER = {"command": "npx", "args": ["-y", "some-server"], "env": {"SOME_TOKEN": "tok-secret-123456"}}


class WithChromeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = self.tmp.name
        self.mcp = os.path.join(self.home, ".gemini", "config", "mcp_config.json")

    def tearDown(self):
        self.tmp.cleanup()

    def install(self, *extra):
        return run_main(ag, ["--home", self.home, "--python", PY, *extra])

    def servers(self):
        return json.loads(load(self.mcp))["mcpServers"]

    def test_not_added_without_the_flag(self):
        self.install()
        self.assertFalse(os.path.exists(self.mcp))

    def test_adds_keeps_others_and_never_prints_them(self):
        save(self.mcp, json.dumps({"mcpServers": {"github": OTHER}, "other": 1}))
        code, out = self.install("--with-chrome")
        self.assertEqual(code, 0)
        self.assertEqual(self.servers()["chrome-devtools"], ag.CHROME_SERVER)
        self.assertEqual(self.servers()["github"], OTHER)
        self.assertEqual(json.loads(load(self.mcp))["other"], 1)
        self.assertTrue(os.path.isfile(self.mcp + ".bak"))
        for secret in ("github", "some-server", "SOME_TOKEN", "tok-secret"):
            self.assertNotIn(secret, out)
        self.assertIn("chrome://inspect/#remote-debugging", out)

    def test_is_idempotent(self):
        self.install("--with-chrome")
        first = load(self.mcp)
        code, out = self.install("--with-chrome")
        self.assertEqual(load(self.mcp), first)
        self.assertIn("unchanged", out)

    def test_keeps_an_entry_set_differently(self):
        mine = {"command": "node", "args": ["my-chrome-mcp.js"]}
        save(self.mcp, json.dumps({"mcpServers": {"chrome-devtools": mine}}))
        code, out = self.install("--with-chrome")
        self.assertEqual(code, 0)
        self.assertEqual(self.servers()["chrome-devtools"], mine)
        self.assertIn("stays as it is", out)

    def test_dry_run_and_uninstall(self):
        save(self.mcp, json.dumps({"mcpServers": {"github": OTHER}}))
        self.install("--with-chrome", "--dry-run")
        self.assertNotIn("chrome-devtools", self.servers())
        self.install("--with-chrome")
        self.install("--uninstall", "--with-chrome")
        self.assertEqual(self.servers(), {"github": OTHER})

    def test_a_broken_config_is_left_alone(self):
        save(self.mcp, "{not json")
        code, out = self.install("--with-chrome")
        self.assertEqual(code, 1)
        self.assertEqual(load(self.mcp), "{not json")


class BrowserRulesTest(unittest.TestCase):
    def test_tool_map_and_hard_rules(self):
        tool_map = " ".join(load(os.path.join(REPO, "skills", "zoho-command-center", "references",
                                              "tool-map.md")).split())
        for words in ("## Browser rules", "List the open pages first", "act only on the task's own tabs",
                      "Never read or type a password", "`chrome-devtools` MCP (`list_pages`",
                      "the built-in browser pane only when that MCP is unavailable"):
            self.assertIn(words, tool_map)
        rules = " ".join(load(os.path.join(REPO, "shared", "hard-rules.md")).split())
        self.assertIn("list the pages first, act only on the task's own tabs, sign-ins stay the lead's", rules)
        readme = " ".join(load(os.path.join(REPO, "README.md")).split())
        self.assertIn("work-only Chrome profile", readme)


if __name__ == "__main__":
    unittest.main()
