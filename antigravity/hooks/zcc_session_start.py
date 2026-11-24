"""SessionStart hook (zcc-managed: zoho-command-center antigravity setup).

Reads the project's ai-handoff-summary.md and injects it at the start of every new conversation, so the chat starts
from the handoff brief instead of guessing. Prints {} (no change) when there is no summary or anything goes wrong:
a hook must never break the conversation.
"""
import json
import os
import sys

MAX_CHARS = 12000


def find_summary(payload):
    paths = list(payload.get("workspacePaths") or [])
    if payload.get("cwd"):
        paths.append(payload["cwd"])
    for base in paths:
        p = os.path.join(base, "ai-handoff-summary.md")
        if os.path.isfile(p):
            return p
    return None


def main():
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        payload = {}
    path = find_summary(payload)
    if not path:
        print("{}")
        return
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS] + "\n[cut at %d characters: read the file for the rest]" % MAX_CHARS
    msg = (
        "Start of session (zoho-command-center hook). This project's handoff brief, %s, is below: read it first, "
        "then open the zoho-command-center skill (and handoff) before anything else.\n\n%s" % (path, text)
    )
    print(json.dumps({"injectSteps": [{"systemMessage": {"systemMessage": msg}}]}))


if __name__ == "__main__":
    try:
        main()
    except Exception:  # never break the session
        print("{}")
