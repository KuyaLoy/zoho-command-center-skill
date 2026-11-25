"""Self-test hook (zcc-managed: zoho-command-center hook self-test): logs that an event fired, decides nothing.

    python zcc_hook_log.py --tool antigravity|codex --log <file>
"""
import datetime
import json
import sys


def main():
    argv = sys.argv[1:]
    tool = argv[argv.index("--tool") + 1] if "--tool" in argv else "antigravity"
    log = argv[argv.index("--log") + 1] if "--log" in argv else None
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        payload = {}
    event = payload.get("hookEventName") or payload.get("hook_event_name") or "unknown"
    if log:
        with open(log, "a", encoding="utf-8") as f:
            f.write("%s\t%s\t%s\n" % (datetime.datetime.now().isoformat(timespec="seconds"), tool, event))
    print(answer(tool, event))


def answer(tool, event):
    """A neutral answer: Antigravity needs a decision on every PreToolUse (an empty answer counts as deny, learned
    25 Nov 2026), so the test hook asks; Codex wants JSON only from Stop, nothing from the others."""
    if tool == "antigravity":
        if event == "PreToolUse":
            return json.dumps({"decision": "ask", "reason": "zcc hook self-test (log only)"})
        if event == "Stop":
            return json.dumps({"decision": "stop"})
        return json.dumps({"injectSteps": []})
    return "{}" if event == "Stop" else ""


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print(json.dumps({"decision": "ask", "reason": "zcc hook self-test error"}))
