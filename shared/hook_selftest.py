"""Hook self-test: do SessionStart, PreToolUse and Stop hooks fire on this machine, in Antigravity and in Codex?

    python shared/hook_selftest.py install --tool antigravity|codex
        adds a log-only hook (it decides nothing) for the three events and prints what to do next
    python shared/hook_selftest.py report
        shows which events fired, per tool
    python shared/hook_selftest.py remove --tool antigravity|codex
        takes the test hook out again (and its log, with --clear-log)

Run it before relying on the zcc hooks: a forum report says some Antigravity hooks never fire on Windows 11. The
hooks are a second line; the always-on rules are the first.
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import setup_lib as lib  # noqa: E402

KEY = "zcc-selftest"
EVENTS = ("SessionStart", "PreToolUse", "Stop")


def paths(tool, home):
    root = os.path.join(home, ".gemini", "config") if tool == "antigravity" else \
        (os.environ.get("CODEX_HOME") or os.path.join(home, ".codex"))
    return root, os.path.join(root, "hooks.json"), os.path.join(root, "hooks", KEY, "zcc_hook_log.py")


def log_path(home):
    return os.path.join(home, ".zcc-hook-selftest.log")


def entries(tool, py, script, log):
    cmd = '%s "%s" --tool %s --log "%s"' % (py, script, tool, log)
    handler = {"type": "command", "command": cmd, "timeout": 10}
    if tool == "antigravity":
        return {KEY: {"SessionStart": [handler], "PreToolUse": [{"matcher": "*", "hooks": [handler]}],
                      "Stop": [handler]}}
    h = dict(handler, statusMessage="zcc-selftest: log only")
    return {"SessionStart": {"hooks": [h]}, "PreToolUse": {"matcher": "*", "hooks": [h]}, "Stop": {"hooks": [h]}}


def is_test(group):
    return any(str(h.get("statusMessage", "")).startswith("zcc-selftest") for h in group.get("hooks", []))


def without_test(tool, hooks):
    if tool == "antigravity":
        return {k: v for k, v in hooks.items() if k != KEY}
    data = dict(hooks)
    events = {e: [g for g in gs if not is_test(g)] for e, gs in (data.get("hooks") or {}).items()}
    data["hooks"] = {e: gs for e, gs in events.items() if gs}
    return data


def install(tool, home, py):
    root, hooks_path, script = paths(tool, home)
    plan, conflicts = lib.plan_files([(os.path.join(lib.HOOKS, "zcc_hook_log.py"), script)])
    if conflicts:
        return lib.stopped(conflicts)
    lib.apply_files(plan, False)
    hooks = without_test(tool, lib.load_json(hooks_path))
    if tool == "antigravity":
        hooks.update(entries(tool, py, script, log_path(home)))
    else:
        for event, group in entries(tool, py, script, log_path(home)).items():
            hooks.setdefault("hooks", {}).setdefault(event, []).append(group)
    lib.save_json(hooks_path, hooks, False)
    print("add       test hook in %s (log: %s)" % (os.path.normpath(hooks_path), log_path(home)))
    if tool == "antigravity":
        print("Next: open Antigravity, start a new conversation, send \"Run the command: echo zcc-selftest\", wait for "
              "the answer, then run: python shared/hook_selftest.py report")
    else:
        print("Next: run `codex` in any folder, open /hooks and trust the \"zcc-selftest\" hooks, send \"Run the command: "
              "echo zcc-selftest\", wait for the answer, exit, then run: python shared/hook_selftest.py report")
    return 0


def report(home):
    log = log_path(home)
    seen = {}
    if os.path.exists(log):
        for line in lib.read(log).splitlines():
            parts = line.split("\t")
            if len(parts) == 3:
                seen.setdefault(parts[1], {}).setdefault(parts[2], parts[0])
    if not seen:
        print("No hook has fired yet (log: %s)." % log)
    for tool in ("antigravity", "codex"):
        if tool in seen:
            for event in EVENTS:
                when = seen[tool].get(event)
                print("%-12s %-13s %s" % (tool, event, ("fired " + when) if when else "NOT fired"))
    return 0


def remove(tool, home, clear_log):
    root, hooks_path, script = paths(tool, home)
    lib.remove_files([script], False)
    if os.path.exists(hooks_path):
        hooks = lib.load_json(hooks_path)
        new = without_test(tool, hooks)
        if new != hooks:
            lib.save_json(hooks_path, new, False)
            print("update    %s (test hook removed)" % os.path.normpath(hooks_path))
    if clear_log and os.path.exists(log_path(home)):
        os.remove(log_path(home))
        print("remove    %s" % log_path(home))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check whether hooks fire in Antigravity and Codex on this machine.")
    ap.add_argument("action", choices=["install", "report", "remove"])
    ap.add_argument("--tool", choices=["antigravity", "codex"])
    ap.add_argument("--home", default=os.path.expanduser("~"), help="home folder (default: yours); for tests")
    ap.add_argument("--python", help="command the hook runs Python with (default: found on this machine)")
    ap.add_argument("--clear-log", action="store_true", help="with remove: delete the log too")
    a = ap.parse_args(argv)
    if a.action == "report":
        return report(a.home)
    if not a.tool:
        ap.error("--tool is required for %s" % a.action)
    if a.action == "install":
        return install(a.tool, a.home, a.python or lib.python_command())
    return remove(a.tool, a.home, a.clear_log)


if __name__ == "__main__":
    sys.exit(main())
