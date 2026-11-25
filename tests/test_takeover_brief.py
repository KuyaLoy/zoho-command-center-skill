"""2.11.1: the takeover brief from an old Command Center's own files (a fixture project)."""
import os
import tempfile
import unittest

from zcc_testlib import load_module, save

tb = load_module("takeover_brief", "skills/zoho-command-center/scripts/takeover_brief.py")

HANDOFF = """# Handoff: example-shop

## Project rules
- Mode: Command Center
- Active Command Center: Claude since 2026-11-20 09:00 (chat: local_abc)

## Changes Made
- 2026-11-18: ABC1-T5 footer links fixed and verified (DONE).
- 2026-11-20: ABC1-T7 shipping page copy changed on staging; waiting on the client's OK.

## Task chats
| Task | Source / status | Site or repo | Chat (tool: name / id) | Size | Phase | Waiting on | Plan / notes |
|---|---|---|---|---|---|---|---|
| ABC1-T5 Footer | Zoho: Closed | example.com | Claude: abc1-t5 / local_1 | S | ARCHIVED | nobody | tasks/ABC1-T5/plan.md |
| ABC1-T7 Shipping | Zoho: Development | example.com | Claude: abc1-t7 / local_2 | M | IMPLEMENTING | the client's OK | tasks/ABC1-T7/plan.md |
| ABC1-T9 Speed | Zoho: Open | example.com | Claude: abc1-t9 / local_3 | M | PLAN READY | lead go | tasks/ABC1-T9/plan.md |

## Next Steps
- 2026-11-20: wait for the client on ABC1-T7.
"""
EOD_OLD = "# EOD 2026-11-19\n- 10:05 ABC1-T6 menu fix DONE, verified on live.\n"
EOD_NEW = "# EOD 2026-11-21\n- 14:30 ABC1-T9 plan ready, waiting on the lead's go.\n- 16:10 ABC1-T7 PART DONE: copy on staging.\n"
SUMMARY = "# AI handoff summary\nStatus: ACTIVE\n\n## Next action\n- Lead's go on ABC1-T9's plan.\n"


class TakeoverBriefTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.p = self.tmp.name
        save(os.path.join(self.p, "handoff.md"), HANDOFF)
        save(os.path.join(self.p, "eod", "2026-11-19.md"), EOD_OLD)
        save(os.path.join(self.p, "eod", "2026-11-21.md"), EOD_NEW)
        save(os.path.join(self.p, "ai-handoff-summary.md"), SUMMARY)

    def tearDown(self):
        self.tmp.cleanup()

    def test_ten_lines_in_order_with_the_last_two_jobs(self):
        lines = tb.brief(self.p)
        self.assertLessEqual(len(lines), 10)
        self.assertTrue(lines[0].startswith("Project: example-shop"))
        self.assertIn("holder Claude since 2026-11-20 09:00", lines[0])
        self.assertEqual(lines[1], "Last jobs:")
        self.assertTrue(lines[2].startswith("- 2026-11-21 16:10 ABC1-T7 PART DONE"), lines[2])
        self.assertTrue(lines[3].startswith("- 2026-11-21 14:30 ABC1-T9 plan ready"), lines[3])
        self.assertEqual(lines[4], "Open now:")
        self.assertIn("- ABC1-T7 Shipping: IMPLEMENTING; waiting on the client's OK", lines)
        self.assertIn("- ABC1-T9 Speed: PLAN READY; waiting on lead go", lines)
        self.assertFalse(any("ABC1-T5 Footer" in l for l in lines))  # archived
        self.assertEqual(lines[-1], "Next: Lead's go on ABC1-T9's plan.")
        self.assertTrue(all(len(l) <= 120 for l in lines))

    def test_changes_made_count_when_eod_is_older(self):
        os.remove(os.path.join(self.p, "eod", "2026-11-21.md"))
        lines = tb.brief(self.p)
        self.assertTrue(lines[2].startswith("- 2026-11-20 ABC1-T7 shipping page copy"), lines[2])
        self.assertTrue(lines[3].startswith("- 2026-11-19 10:05 ABC1-T6 menu fix DONE"), lines[3])

    def test_many_open_tasks_still_fit_in_10_lines(self):
        rows = "".join("| T%d | Zoho | example.com | Claude: t / x | S | IMPLEMENTING | lead | p |\n" % i
                       for i in range(12))
        save(os.path.join(self.p, "handoff.md"), HANDOFF.replace("\n## Next Steps", rows + "\n## Next Steps"))
        lines = tb.brief(self.p)
        self.assertEqual(len(lines), 10)
        self.assertTrue(lines[-2].startswith("- and ") and lines[-2].endswith("more on the board"), lines[-2])
        self.assertTrue(lines[-1].startswith("Next: "))

    def test_an_old_layout_says_what_is_missing(self):
        save(os.path.join(self.p, "handoff.md"), "# Handoff: old\n\n## Project rules\n- Mode: Command Center\n")
        for name in os.listdir(os.path.join(self.p, "eod")):
            os.remove(os.path.join(self.p, "eod", name))
        os.remove(os.path.join(self.p, "ai-handoff-summary.md"))
        lines = tb.brief(self.p)
        self.assertIn("holder none yet (write it)", lines[0])
        self.assertIn("- unverified (no eod/ files or Changes Made)", lines)
        self.assertIn("- none on the board", lines)
        self.assertEqual(lines[-1], "Next: unverified")

    def test_no_handoff_means_set_up(self):
        with tempfile.TemporaryDirectory() as empty:
            self.assertEqual(tb.main([empty]), 1)


if __name__ == "__main__":
    unittest.main()
