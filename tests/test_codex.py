"""Codex setup: install script and files."""
import json
import os
import tempfile
import tomllib
import unittest

from zcc_testlib import PY, REPO, load, load_module, run_main, save

cx = load_module("cx_install", "codex/install.py")


class InstallTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = os.path.join(self.tmp.name, ".codex")

    def tearDown(self):
        self.tmp.cleanup()

    def path(self, rel):
        return os.path.join(self.home, rel)

    def install(self, *extra):
        return run_main(cx, ["--codex-home", self.home, "--python", PY, *extra])

    def test_dry_run_changes_nothing(self):
        code, out = self.install("--dry-run")
        self.assertEqual(code, 0)
        self.assertIn("Dry run", out)
        self.assertFalse(os.path.exists(self.home))

    def test_install_keeps_the_rest_and_is_idempotent(self):
        save(self.path("AGENTS.md"), "# My rules\nKeep me.\n")
        other = {"type": "command", "command": "echo other"}
        save(self.path("hooks.json"), json.dumps({"hooks": {"Stop": [{"hooks": [other]}]}}))
        code, out = self.install()
        self.assertEqual(code, 0)
        self.assertIn("/hooks", out)
        agents = load(self.path("AGENTS.md"))
        self.assertTrue(agents.startswith("# My rules\nKeep me.\n"))
        self.assertEqual(agents.count("zcc-managed:start"), 1)
        hooks = json.loads(load(self.path("hooks.json")))["hooks"]
        self.assertEqual(len(hooks["Stop"]), 2)
        self.assertEqual(hooks["Stop"][0]["hooks"][0], other)
        self.assertIn("zcc_evidence_gate.py", hooks["Stop"][1]["hooks"][0]["command"])
        self.assertIn("--tool codex", hooks["PreToolUse"][0]["hooks"][0]["command"])
        self.assertIn("apply_patch", hooks["PreToolUse"][0]["matcher"])
        for rel in cx.FILES.values():
            self.assertTrue(os.path.isfile(self.path(rel)), rel)
        code, out = self.install()
        self.assertNotIn("add ", out)
        self.assertNotIn("update ", out)
        self.assertEqual(load(self.path("AGENTS.md")).count("zcc-managed:start"), 1)
        self.assertEqual(len(json.loads(load(self.path("hooks.json")))["hooks"]["Stop"]), 2)

    def test_foreign_agent_file_stops_install(self):
        save(self.path("agents/zcc-reviewer.toml"), 'name = "mine"\n')
        code, out = self.install()
        self.assertEqual(code, 2)
        self.assertFalse(os.path.exists(self.path("AGENTS.md")))
        self.assertFalse(os.path.exists(self.path("hooks.json")))

    def test_uninstall_removes_only_its_own(self):
        save(self.path("AGENTS.md"), "# My rules\n")
        self.install()
        self.assertEqual(self.install("--uninstall")[0], 0)
        self.assertEqual(load(self.path("AGENTS.md")).strip(), "# My rules")
        for rel in cx.FILES.values():
            self.assertFalse(os.path.exists(self.path(rel)), rel)
        self.assertEqual(json.loads(load(self.path("hooks.json")))["hooks"], {})


class FilesTest(unittest.TestCase):
    def test_agent_files_are_valid_toml_with_the_required_keys(self):
        for name in ("zcc-task-worker.toml", "zcc-reviewer.toml"):
            data = tomllib.loads(load(os.path.join(REPO, "codex", "agents", name)))
            for key in ("name", "description", "developer_instructions"):
                self.assertTrue(data.get(key), (name, key))
            self.assertNotIn("model", data, name)  # the lead's model
            self.assertNotIn("sandbox_mode", data, name)  # an agent cannot set its own sandbox

    def test_agents_block_is_marked_and_small(self):
        block = load(os.path.join(REPO, "codex", "AGENTS-block.md"))
        self.assertTrue(block.startswith("<!-- zcc-managed:start"))
        self.assertTrue(block.rstrip().endswith("<!-- zcc-managed:end -->"))
        self.assertLess(len(block.encode("utf-8")), 8 * 1024)
        for word in ("$zoho-command-center", "checks.md", "codex -s read-only"):
            self.assertIn(word, block)


if __name__ == "__main__":
    unittest.main()
