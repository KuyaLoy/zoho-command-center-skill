"""The shared hooks, in both tools' formats."""
import json
import os
import tempfile
import unittest

from zcc_testlib import hook, save

REPORT_OK = "DONE: T1 site built.\nChecks: home 200, form sends\nNext: QA — waiting on Command Center"
CHECKS = """# Checks
## home 200
```
$ curl -sI https://site.test/ | head -1
HTTP/1.1 200 OK
```
## form sends
```
$ python check_form.py
sent: 1
```
"""


class SecretsGuardTest(unittest.TestCase):
    def ag(self, args, name="write_file"):
        return hook("zcc_secrets_guard.py", "antigravity", {"toolCall": {"name": name, "args": args}})

    def cx(self, tool_name, command):
        return hook("zcc_secrets_guard.py", "codex", {"hook_event_name": "PreToolUse", "tool_name": tool_name,
                                                      "tool_input": {"command": command}})

    def test_antigravity_denies_a_password_in_markdown(self):
        r = self.ag({"Path": "d:\\site\\tasks\\T1\\notes.md", "Content": "Admin password: Hunter2xyz!"})
        self.assertEqual(r["decision"], "deny")

    def test_antigravity_json_encoded_args(self):
        r = self.ag({"Path": json.dumps("d:\\site\\handoff.md"), "Replacement": json.dumps("api_key=abcd1234efgh")},
                    name="edit_file")
        self.assertEqual(r["decision"], "deny")

    def test_antigravity_allows_placeholders_and_other_files(self):
        self.assertEqual(self.ag({"Path": "notes.md", "Content": "password: <in wp-config.php>"}), {})
        self.assertEqual(self.ag({"Path": "notes.md", "Content": "Never write the password here."}), {})
        self.assertEqual(self.ag({"Path": "wp-config.php", "Content": "define('DB_PASSWORD', 'Hunter2xyz');"}), {})

    def test_codex_denies_a_token_in_a_patch_to_markdown(self):
        patch = "*** Begin Patch\n*** Add File: tasks/T1/notes.md\n+token ghp_" + "a" * 36 + "\n*** End Patch"
        r = self.cx("apply_patch", patch)
        self.assertEqual(r["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_codex_allows_the_same_value_in_a_php_file(self):
        patch = "*** Begin Patch\n*** Update File: wp-config.php\n+define('DB_PASSWORD', 'Hunter2xyz');\n*** End Patch"
        self.assertIsNone(self.cx("apply_patch", patch))

    def test_codex_denies_a_shell_write_into_markdown(self):
        r = self.cx("Bash", "echo 'password=Hunter2xyz' >> tasks/T1/notes.md")
        self.assertEqual(r["hookSpecificOutput"]["permissionDecision"], "deny")
        self.assertIsNone(self.cx("Bash", "cat tasks/T1/notes.md"))

    def test_bad_input_never_blocks(self):
        self.assertEqual(hook("zcc_secrets_guard.py", "antigravity", "not json"), {})
        self.assertIsNone(hook("zcc_secrets_guard.py", "codex", "not json"))


class SessionStartTest(unittest.TestCase):
    def test_injects_the_summary_in_each_format(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(hook("zcc_session_start.py", "antigravity", {"workspacePaths": [d]}), {})
            self.assertIsNone(hook("zcc_session_start.py", "codex", {"cwd": d}))
            save(os.path.join(d, "ai-handoff-summary.md"), "# Summary\nNext: plan T1")
            r = hook("zcc_session_start.py", "antigravity", {"workspacePaths": [d]})
            self.assertIn("Next: plan T1", r["injectSteps"][0]["systemMessage"]["systemMessage"])
            r = hook("zcc_session_start.py", "codex", {"cwd": d, "hook_event_name": "SessionStart"})
            self.assertEqual(r["hookSpecificOutput"]["hookEventName"], "SessionStart")
            self.assertIn("Next: plan T1", r["hookSpecificOutput"]["additionalContext"])


class EvidenceGateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        os.makedirs(os.path.join(self.root, "tasks", "T1"))

    def tearDown(self):
        self.tmp.cleanup()

    def cx(self, message, **extra):
        payload = {"hook_event_name": "Stop", "cwd": self.root, "last_assistant_message": message,
                   "stop_hook_active": False}
        payload.update(extra)
        return hook("zcc_evidence_gate.py", "codex", payload)

    def ag(self, message, **extra):
        transcript = os.path.join(self.root, "transcript.jsonl")
        steps = [{"type": "PLANNER_RESPONSE", "content": "earlier"}, {"type": "GENERIC", "content": "x"},
                 {"type": "PLANNER_RESPONSE", "content": message}, {"type": "GENERIC", "content": "y"}]
        save(transcript, "\n".join(json.dumps(s) for s in steps))
        payload = {"hookEventName": "Stop", "workspacePaths": [self.root], "transcriptPath": transcript,
                   "continuationActive": False}
        payload.update(extra)
        return hook("zcc_evidence_gate.py", "antigravity", payload)

    def test_passes_when_every_check_has_output(self):
        save(os.path.join(self.root, "tasks", "T1", "checks.md"), CHECKS)
        self.assertEqual(self.cx(REPORT_OK), {})
        self.assertEqual(self.ag(REPORT_OK), {})

    def test_blocks_a_check_without_output(self):
        save(os.path.join(self.root, "tasks", "T1", "checks.md"), CHECKS.split("## form sends")[0] +
             "## form sends\nchecked, fine\n")
        r = self.cx(REPORT_OK)
        self.assertEqual(r["decision"], "block")
        self.assertIn("form sends", r["reason"])
        self.assertNotIn("home 200,", r["reason"])
        r = self.ag(REPORT_OK)
        self.assertEqual(r["decision"], "continue")

    def test_blocks_a_report_without_a_checks_line(self):
        r = self.cx("READY FOR QA: T1 staging is up.\nNext: QA — waiting on Command Center")
        self.assertEqual(r["decision"], "block")
        self.assertIn("Checks:", r["reason"])

    def test_blocks_a_report_that_leaves_out_a_required_check(self):
        save(os.path.join(self.root, "tasks", "T1", "checks.md"), CHECKS)
        save(os.path.join(self.root, "tasks", "T1", "brief.md"),
             "# Brief\nDo the thing.\nChecks required: home 200, visual at 3 widths\n")
        r = self.cx(REPORT_OK)
        self.assertEqual(r["decision"], "block")
        self.assertIn("visual at 3 widths", r["reason"])
        self.assertIn("tasks/T1/brief.md", r["reason"])
        self.assertEqual(self.ag(REPORT_OK)["decision"], "continue")

    def test_a_qa_report_follows_its_qa_brief(self):
        save(os.path.join(self.root, "tasks", "T1", "qa", "brief.md"), "Checks required: visual, speed\n")
        msg = "QA 0: T1 pass 2\nChecks: visual\n## visual\n```\n$ python shots.py\n3 widths, 0 diff\n```"
        r = self.cx(msg)
        self.assertEqual(r["decision"], "block")
        self.assertIn("speed", r["reason"])
        self.assertIn("tasks/T1/qa/brief.md", r["reason"])
        msg = msg.replace("Checks: visual", "Checks: visual, speed") + "\n## speed\n```\n$ lighthouse x\nperf 95\n```"
        self.assertEqual(self.cx(msg), {})

    def test_evidence_in_the_message_itself_counts(self):
        msg = "QA 0: T1 pass 2\nChecks: links\n## links\n```\n$ python linkcheck.py\n0 broken\n```"
        self.assertEqual(self.cx(msg), {})

    def test_ignores_other_messages_and_never_loops(self):
        self.assertEqual(self.cx("PLAN READY: T1 plan in tasks/T1/plan.md"), {})
        self.assertEqual(self.cx("DONE: T1\nChecks: home 200", stop_hook_active=True), {})
        self.assertEqual(self.ag("DONE: T1\nChecks: home 200", continuationActive=True), {})

    def test_bad_input_never_blocks(self):
        self.assertEqual(hook("zcc_evidence_gate.py", "codex", "not json"), {})
        self.assertEqual(hook("zcc_evidence_gate.py", "antigravity", "not json"), {})


if __name__ == "__main__":
    unittest.main()
