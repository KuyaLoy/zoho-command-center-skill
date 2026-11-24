"""Tests for the Antigravity setup: python -m unittest discover -s antigravity/tests (from the repo root)."""
import contextlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import install  # noqa: E402

PY = '"%s"' % sys.executable


def run_install(home, *extra):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = install.main(["--home", home, "--python", PY, *extra])
    return code, out.getvalue()


def hook(name, payload):
    raw = payload if isinstance(payload, str) else json.dumps(payload)
    out = subprocess.run([sys.executable, os.path.join(ROOT, "hooks", name)], input=raw, capture_output=True,
                         text=True, timeout=30)
    return json.loads(out.stdout)


def load(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def save(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def frontmatter(path):
    text = load(path)
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    return dict(line.split(": ", 1) for line in m.group(1).splitlines())


class InstallTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = self.tmp.name
        self.config = os.path.join(self.home, ".gemini", "config")

    def tearDown(self):
        self.tmp.cleanup()

    def path(self, rel):
        return os.path.join(self.config, rel)

    def test_dry_run_changes_nothing(self):
        code, out = run_install(self.home, "--dry-run")
        self.assertEqual(code, 0)
        self.assertIn("Dry run", out)
        self.assertFalse(os.path.exists(self.config))

    def test_install_is_idempotent_and_keeps_other_hooks(self):
        os.makedirs(self.config)
        save(self.path("hooks.json"), json.dumps({"other-hook": {"Stop": []}}))
        self.assertEqual(run_install(self.home)[0], 0)
        for rel in install.FILES.values():
            self.assertTrue(os.path.isfile(self.path(rel)), rel)
        hooks = json.loads(load(self.path("hooks.json")))
        self.assertIn("other-hook", hooks)
        for k in install.HOOK_KEYS:
            self.assertIn(k, hooks)
        self.assertTrue(os.path.isfile(self.path("hooks.json.bak")))
        code, out = run_install(self.home)
        self.assertEqual(code, 0)
        self.assertNotIn("add ", out)
        self.assertNotIn("update ", out)

    def test_foreign_file_stops_install_before_any_change(self):
        os.makedirs(self.path("rules"))
        save(self.path("rules/zcc-hard-rules.md"), "someone else's rule")
        code, out = run_install(self.home)
        self.assertEqual(code, 2)
        self.assertIn("STOPPED", out)
        self.assertEqual(load(self.path("rules/zcc-hard-rules.md")), "someone else's rule")
        self.assertFalse(os.path.exists(self.path("agents")))
        self.assertFalse(os.path.exists(self.path("hooks.json")))

    def test_uninstall_removes_only_its_own(self):
        run_install(self.home)
        save(self.path("rules/other.md"), "other")
        hooks = json.loads(load(self.path("hooks.json")))
        hooks["other-hook"] = {"Stop": []}
        save(self.path("hooks.json"), json.dumps(hooks))
        self.assertEqual(run_install(self.home, "--uninstall")[0], 0)
        for rel in install.FILES.values():
            self.assertFalse(os.path.exists(self.path(rel)), rel)
        self.assertTrue(os.path.isfile(self.path("rules/other.md")))
        self.assertEqual(list(json.loads(load(self.path("hooks.json")))), ["other-hook"])


class FilesTest(unittest.TestCase):
    def test_rule_is_always_on_and_small(self):
        p = os.path.join(ROOT, "rules", "zcc-hard-rules.md")
        self.assertEqual(frontmatter(p)["trigger"], "always_on")
        self.assertLess(os.path.getsize(p), install.RULE_LIMIT)

    def test_qa_agent_has_no_write_tools(self):
        fm = frontmatter(os.path.join(ROOT, "agents", "wp-qa.md"))
        tools = fm["tools"].strip("[]").replace(" ", "").split(",")
        for t in ("edit_file", "write_file", "write_to_file", "replace_file_content"):
            self.assertNotIn(t, tools)
        self.assertEqual(fm["mainAgent"], "false")

    def test_task_worker_opens_the_skills(self):
        fm = frontmatter(os.path.join(ROOT, "agents", "task-worker.md"))
        for s in ("zoho-command-center", "handoff", "convert-to-wordpress", "figma-to-wordpress"):
            self.assertIn(s, fm["skills"])

    def test_every_file_has_the_marker(self):
        for src in install.FILES:
            self.assertIn(install.MARKER, load(os.path.join(ROOT, src)), src)


class HooksTest(unittest.TestCase):
    def guard(self, args, name="write_file"):
        return hook("zcc_secrets_guard.py", {"toolCall": {"name": name, "args": args}})

    def test_denies_a_password_in_markdown(self):
        r = self.guard({"Path": "d:\site\tasks\T1\notes.md", "Content": "Admin password: Hunter2xyz!"})
        self.assertEqual(r["decision"], "deny")

    def test_denies_json_encoded_args_as_the_app_sends_them(self):
        r = self.guard({"Path": json.dumps("d:\site\handoff.md"), "Replacement": json.dumps("api_key=abcd1234efgh")},
                       name="edit_file")
        self.assertEqual(r["decision"], "deny")

    def test_denies_a_raw_token(self):
        r = self.guard({"Path": "report.md", "Content": "token ghp_" + "a" * 36})
        self.assertEqual(r["decision"], "deny")

    def test_allows_placeholders_and_plain_words(self):
        self.assertEqual(self.guard({"Path": "notes.md", "Content": "password: <in wp-config.php>"}), {})
        self.assertEqual(self.guard({"Path": "notes.md", "Content": "Never write the password here."}), {})

    def test_ignores_non_markdown_files(self):
        self.assertEqual(self.guard({"Path": "wp-config.php", "Content": "define('DB_PASSWORD', 'Hunter2xyz');"}), {})

    def test_bad_input_never_blocks(self):
        self.assertEqual(hook("zcc_secrets_guard.py", "not json"), {})

    def test_session_start_injects_the_summary(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(hook("zcc_session_start.py", {"workspacePaths": [d]}), {})
            with open(os.path.join(d, "ai-handoff-summary.md"), "w", encoding="utf-8") as f:
                f.write("# Summary\nNext: plan T1")
            r = hook("zcc_session_start.py", {"workspacePaths": [d]})
            msg = r["injectSteps"][0]["systemMessage"]["systemMessage"]
            self.assertIn("Next: plan T1", msg)
            self.assertIn("zoho-command-center", msg)


if __name__ == "__main__":
    unittest.main()
