"""The hook self-test script and the Agent Skills spec check."""
import json
import os
import subprocess
import sys
import tempfile
import unittest

from zcc_testlib import PY, REPO, load, load_module, run_main, save

st = load_module("hook_selftest", "shared/hook_selftest.py")
spec = load_module("skill_spec", ".github/scripts/skill-spec.py")


class SelfTestTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = self.tmp.name
        self.env = os.environ.pop("CODEX_HOME", None)

    def tearDown(self):
        if self.env is not None:
            os.environ["CODEX_HOME"] = self.env
        self.tmp.cleanup()

    def run_st(self, *argv):
        return run_main(st, list(argv) + ["--home", self.home])

    def fire(self, tool, event):
        _, hooks_path, script = st.paths(tool, self.home)
        hooks = json.loads(load(hooks_path))
        cmd_hooks = hooks["zcc-selftest"] if tool == "antigravity" else hooks["hooks"]
        self.assertIn(event, cmd_hooks)
        payload = {"hookEventName": event} if tool == "antigravity" else {"hook_event_name": event}
        out = subprocess.run([sys.executable, script, "--tool", tool, "--log", st.log_path(self.home)],
                             input=json.dumps(payload), capture_output=True, text=True, timeout=30)
        return out.stdout.strip()

    def test_install_fire_report_remove(self):
        for tool in ("antigravity", "codex"):
            self.assertEqual(self.run_st("install", "--tool", tool, "--python", PY)[0], 0)
        self.assertEqual(self.fire("antigravity", "SessionStart"), "{}")
        self.assertEqual(self.fire("codex", "PreToolUse"), "")
        self.assertEqual(self.fire("codex", "Stop"), "{}")
        _, out = self.run_st("report")
        self.assertRegex(out, r"antigravity\s+SessionStart\s+fired")
        self.assertRegex(out, r"antigravity\s+Stop\s+NOT fired")
        self.assertRegex(out, r"codex\s+Stop\s+fired")
        for tool in ("antigravity", "codex"):
            self.assertEqual(self.run_st("remove", "--tool", tool, "--clear-log")[0], 0)
            _, hooks_path, script = st.paths(tool, self.home)
            self.assertFalse(os.path.exists(script))
            self.assertNotIn("zcc-selftest", load(hooks_path))
        self.assertFalse(os.path.exists(st.log_path(self.home)))

    def test_keeps_the_real_hooks(self):
        save(os.path.join(self.home, ".codex", "hooks.json"),
             json.dumps({"hooks": {"Stop": [{"hooks": [{"type": "command", "command": "echo mine"}]}]}}))
        self.run_st("install", "--tool", "codex", "--python", PY)
        self.run_st("remove", "--tool", "codex")
        hooks = json.loads(load(os.path.join(self.home, ".codex", "hooks.json")))
        self.assertEqual(hooks["hooks"]["Stop"], [{"hooks": [{"type": "command", "command": "echo mine"}]}])


class SpecTest(unittest.TestCase):
    def test_the_repo_skill_matches_the_spec(self):
        self.assertEqual(spec.main(REPO), 0)

    def test_a_bad_skill_fails(self):
        with tempfile.TemporaryDirectory() as d:
            save(os.path.join(d, "skills", "good-name", "SKILL.md"), "---\nname: other\ndescription: x\n---\nbody\n")
            self.assertEqual(spec.main(d), 1)


if __name__ == "__main__":
    unittest.main()
