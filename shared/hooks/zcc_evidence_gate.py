"""Stop hook (zcc-managed: zoho-command-center setup): the evidence gate.

A DONE, PART DONE, READY FOR QA, QA 0 or QA REPORT message must list its checks in a "Checks:" line, and each check
needs a "## <check>" section with a code block (the command and its output) in tasks/<TASK-ID>/checks.md, a QA file
or the message itself. Otherwise the chat is sent back once (Antigravity: continue; Codex: block) to run them.

    python zcc_evidence_gate.py --tool antigravity|codex
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zcc_hooklib as lib  # noqa: E402

if __name__ == "__main__":
    lib.run(lib.gate_answer)
