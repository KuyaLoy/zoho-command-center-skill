"""Antigravity setup: install script and files."""
import json
import os
import tempfile
import unittest

from zcc_testlib import PY, REPO, frontmatter, load, load_module, run_main, save

ag = load_module("ag_install", "antigravity/install.py")


class InstallTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = self.tmp.name
        self.config = os.path.join(self.home, ".gemini", "config")

    def tearDown(self):
        self.tmp.cleanup()

    def path(self, rel):
        return os.path.join(self.config, rel)

    def install(self, *extra):
        return run_main(ag, ["--home", self.home, "--python", PY, *extra])

    def test_dry_run_changes_nothing(self):
        code, out = self.install("--dry-run")
        self.assertEqual(code, 0)
        self.assertIn("Dry run", out)
        self.assertFalse(os.path.exists(self.config))

    def test_install_is_idempotent_and_keeps_other_hooks(self):
        save(self.path("hooks.json"), json.dumps({"other-hook": {"Stop": []}}))
        self.assertEqual(self.install()[0], 0)
        for rel in ag.FILES.values():
            self.assertTrue(os.path.isfile(self.path(rel)), rel)
        hooks = json.loads(load(self.path("hooks.json")))
        self.assertIn("other-hook", hooks)
        for k in ag.HOOK_KEYS:
            self.assertIn(k, hooks)
        self.assertIn("--tool antigravity", hooks["zcc-evidence-gate"]["Stop"][0]["command"])
        self.assertTrue(os.path.isfile(self.path("hooks.json.bak")))
        code, out = self.install()
        self.assertEqual(code, 0)
        self.assertNotIn("add ", out)
        self.assertNotIn("update ", out)

    def test_foreign_file_stops_install_before_any_change(self):
        save(self.path("agents/wp-qa.md"), "someone else's agent")
        code, out = self.install()
        self.assertEqual(code, 2)
        self.assertIn("STOPPED", out)
        self.assertEqual(load(self.path("agents/wp-qa.md")), "someone else's agent")
        self.assertFalse(os.path.exists(self.path("agents/task-worker.md")))
        self.assertFalse(os.path.exists(self.path("hooks.json")))

    def test_uninstall_removes_only_its_own(self):
        self.install()
        save(self.path("rules/other.md"), "other")
        hooks = json.loads(load(self.path("hooks.json")))
        hooks["other-hook"] = {"Stop": []}
        save(self.path("hooks.json"), json.dumps(hooks))
        self.assertEqual(self.install("--uninstall")[0], 0)
        for rel in ag.FILES.values():
            self.assertFalse(os.path.exists(self.path(rel)), rel)
        self.assertFalse(os.path.exists(self.path("hooks/zcc")))
        self.assertTrue(os.path.isfile(self.path("rules/other.md")))
        self.assertEqual(list(json.loads(load(self.path("hooks.json")))), ["other-hook"])


class FilesTest(unittest.TestCase):
    def test_rule_is_always_on_and_small(self):
        p = os.path.join(REPO, "antigravity", "rules", "zcc-hard-rules.md")
        self.assertEqual(frontmatter(p)["trigger"], "always_on")
        self.assertLess(os.path.getsize(p), ag.RULE_LIMIT)
        self.assertIn("checks.md", load(p))

    def test_qa_agent_is_read_only(self):
        fm = frontmatter(os.path.join(REPO, "antigravity", "agents", "wp-qa.md"))
        tools = fm["tools"].strip("[]").replace(" ", "").split(",")
        for t in ("edit_file", "write_file", "write_to_file", "replace_file_content"):
            self.assertNotIn(t, tools)
        self.assertEqual(fm["mainAgent"], "false")
        self.assertEqual(fm["commandExecutionPolicy"], "sandbox")
        self.assertIn("webview_browser", tools)

    def test_agents_use_known_tools_and_the_leads_model(self):
        known = {"read_file", "edit_file", "write_file", "run_command", "manage_task", "update_steps", "update_focus",
                 "send_message", "manage_subagents", "invoke_subagent", "webview_browser"}
        for name in ("task-worker.md", "wp-qa.md"):
            fm = frontmatter(os.path.join(REPO, "antigravity", "agents", name))
            tools = set(fm["tools"].strip("[]").replace(" ", "").split(","))
            self.assertLessEqual(tools, known, name)
            self.assertIn("update_steps", tools, name)
            self.assertEqual(fm["model"], "inherit", name)

    def test_task_worker_opens_the_skills(self):
        fm = frontmatter(os.path.join(REPO, "antigravity", "agents", "task-worker.md"))
        for s in ("zoho-command-center", "handoff", "convert-to-wordpress", "figma-to-wordpress"):
            self.assertIn(s, fm["skills"])

    def test_every_file_has_the_marker(self):
        for src in ag.FILES:
            self.assertIn(ag.MARKER, load(src), src)


if __name__ == "__main__":
    unittest.main()
