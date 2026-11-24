"""SessionStart hook (zcc-managed: zoho-command-center setup): injects the project's ai-handoff-summary.md.

    python zcc_session_start.py --tool antigravity|codex
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zcc_hooklib as lib  # noqa: E402

if __name__ == "__main__":
    lib.run(lambda tool, payload: lib.session_start_answer(tool, lib.session_start_message(payload)))
