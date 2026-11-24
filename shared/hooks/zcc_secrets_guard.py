"""PreToolUse hook (zcc-managed: zoho-command-center setup): denies a write that puts a password, key or token into
a Markdown file. Anything else gets no decision, so the tool's own permission settings stay as they are.

    python zcc_secrets_guard.py --tool antigravity|codex
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zcc_hooklib as lib  # noqa: E402

if __name__ == "__main__":
    lib.run(lib.secrets_answer)
