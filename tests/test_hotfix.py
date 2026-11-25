"""2.10.1 hotfix: Antigravity hooks always answer with a decision, and the install re-enables the guard."""
import json
import os
import subprocess
import sys
import tempfile
import unittest

from zcc_testlib import HOOKS, PY, REPO, load, load_module, run_main, save

ag = load_module("ag_install_hotfix", "antigravity/install.py")


class InstallReenablesTest(unittest.TestCase):
    def test_a_disabled_guard_comes_back_on(self):
        with tempfile.TemporaryDirectory() as home:
            hooks_path = os.path.join(home, ".gemini", "config", "hooks.json")
            save(hooks_path, json.dumps({"zcc-secrets-guard": {"enabled": False, "PreToolUse": []},
                                         "other": {"enabled": False, "Stop": []}}))
            code, out = run_main(ag, ["--home", home, "--python", PY])
            self.assertEqual(code, 0)
            self.assertIn("re-enable zcc-secrets-guard", out)
            hooks = json.loads(load(hooks_path))
            self.assertNotIn("enabled", hooks["zcc-secrets-guard"])
            self.assertEqual(hooks["other"]["enabled"], False)  # someone else's hook stays as it was


class SelfTestHookAnswersTest(unittest.TestCase):
    def answer(self, tool, event):
        out = subprocess.run([sys.executable, os.path.join(HOOKS, "zcc_hook_log.py"), "--tool", tool],
                             input=json.dumps({"hookEventName": event, "hook_event_name": event}),
                             capture_output=True, text=True, timeout=30)
        return out.stdout.strip()

    def test_antigravity_gets_a_decision_never_an_empty_answer(self):
        self.assertEqual(json.loads(self.answer("antigravity", "PreToolUse"))["decision"], "ask")
        self.assertEqual(json.loads(self.answer("antigravity", "Stop"))["decision"], "stop")
        self.assertEqual(self.answer("codex", "PreToolUse"), "")
        self.assertEqual(self.answer("codex", "Stop"), "{}")


class GateSendsBackOnceTest(unittest.TestCase):
    """Seen with the real agy, 25 Nov 2026: a second Stop in the same turn came with continuationActive false and
    executionNum 1, and the model's honest "Checks: not checked" was sent back again."""

    def gate(self, root, message, **extra):
        transcript = os.path.join(root, "t.jsonl")
        save(transcript, json.dumps({"type": "PLANNER_RESPONSE", "content": message}))
        payload = {"hookEventName": "Stop", "workspacePaths": [root], "cwd": root, "transcriptPath": transcript,
                   "continuationActive": False, "executionNum": 0}
        payload.update(extra)
        out = subprocess.run([sys.executable, os.path.join(HOOKS, "zcc_evidence_gate.py"), "--tool", "antigravity"],
                             input=json.dumps(payload), capture_output=True, text=True, timeout=30)
        return json.loads(out.stdout)["decision"]

    def test_second_stop_of_a_turn_passes(self):
        with tempfile.TemporaryDirectory() as root:
            msg = "DONE: TEST-1 report\nChecks: home page 200"
            self.assertEqual(self.gate(root, msg), "continue")
            self.assertEqual(self.gate(root, msg, executionNum=1), "stop")

    def test_not_checked_is_an_honest_answer(self):
        with tempfile.TemporaryDirectory() as root:
            os.makedirs(os.path.join(root, "tasks", "TEST-1"))
            self.assertEqual(self.gate(root, "DONE: TEST-1 report\nChecks: not checked"), "stop")
            self.assertEqual(self.gate(root, "DONE: TEST-1 report\nChecks: home page 200 (not checked)"), "stop")
            save(os.path.join(root, "tasks", "TEST-1", "brief.md"), "Checks required: visual\n")
            self.assertEqual(self.gate(root, "DONE: TEST-1 report\nChecks: visual (not checked)"), "stop")
            self.assertEqual(self.gate(root, "DONE: TEST-1 report\nChecks: not checked"), "continue")


class ReportStyleTest(unittest.TestCase):
    def test_once_per_state_change_and_short_plan_ready(self):
        ref = os.path.join(REPO, "skills", "zoho-command-center", "references")
        tool_map = " ".join(load(os.path.join(ref, "tool-map.md")).split())
        self.assertIn("**Report once per state change**", tool_map)
        self.assertIn("at most 8 lines (what, where, backup, check, rollback) plus the options as a numbered list",
                      tool_map)
        cc = " ".join(load(os.path.join(ref, "command-center.md")).split())
        self.assertIn("Show PLAN READY in at most 8 lines", cc)
        self.assertIn("once per state change", " ".join(load(os.path.join(REPO, "shared", "hard-rules.md")).split()))


class SmokeScriptTest(unittest.TestCase):
    def test_the_smoke_script_is_opt_in(self):
        text = load(os.path.join(REPO, "shared", "agy_smoke.py"))
        self.assertIn("--run", text)
        out = subprocess.run([sys.executable, os.path.join(REPO, "shared", "agy_smoke.py")], capture_output=True,
                             text=True, timeout=30)
        self.assertNotEqual(out.returncode, 0)  # without --run it only explains itself
        self.assertIn("--run", out.stdout + out.stderr)


if __name__ == "__main__":
    unittest.main()
