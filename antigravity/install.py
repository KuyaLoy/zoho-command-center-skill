"""Install the zoho-command-center setup into Antigravity's global config (~/.gemini/config).

    python antigravity/install.py --dry-run     show what would change, change nothing
    python antigravity/install.py               install or update (safe to run again)
    python antigravity/install.py --uninstall   remove only what this script installed

What it installs (each file carries the marker "zcc-managed"):
    rules/zcc-hard-rules.md                      the always-on hard rules
    agents/task-worker.md, agents/wp-qa.md       the task worker and the read-only QA agent
    hooks/zcc/*.py and three entries in hooks.json
        SessionStart (handoff brief), PreToolUse (no secrets in .md), Stop (the evidence gate)

It never overwrites or deletes a file it did not install: a file at one of its paths without the marker stops the
install before anything changes. hooks.json keeps every other hook; a backup (hooks.json.bak) is written first.
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "shared"))
import setup_lib as lib  # noqa: E402

MARKER = lib.MARKER
RULE_LIMIT = 24000  # bytes per rule file (Antigravity truncates above it)
FILES = {
    os.path.join(HERE, "rules", "zcc-hard-rules.md"): "rules/zcc-hard-rules.md",
    os.path.join(HERE, "agents", "task-worker.md"): "agents/task-worker.md",
    os.path.join(HERE, "agents", "wp-qa.md"): "agents/wp-qa.md",
}
FILES.update({os.path.join(lib.HOOKS, f): "hooks/zcc/" + f for f in lib.HOOK_FILES})
WRITE_TOOLS = "write_file|edit_file|write_to_file|replace_file_content|multi_replace_file_content"
HOOK_KEYS = ("zcc-session-start", "zcc-secrets-guard", "zcc-evidence-gate")


def hook_entries(py):
    def cmd(script):  # Antigravity runs hooks in the folder of hooks.json, so a relative path works
        return "%s hooks/zcc/%s --tool antigravity" % (py, script)
    return {
        "zcc-session-start": {"SessionStart": [{"type": "command", "command": cmd("zcc_session_start.py"),
                                                "timeout": 10}]},
        "zcc-secrets-guard": {"PreToolUse": [{"matcher": WRITE_TOOLS, "hooks": [
            {"type": "command", "command": cmd("zcc_secrets_guard.py"), "timeout": 10}]}]},
        "zcc-evidence-gate": {"Stop": [{"type": "command", "command": cmd("zcc_evidence_gate.py"), "timeout": 20}]},
    }


def install(config, dry, py):
    for src, dst in FILES.items():
        if dst.startswith("rules/") and len(lib.read(src).encode("utf-8")) > RULE_LIMIT:
            raise SystemExit("ERROR: %s is over %d bytes" % (src, RULE_LIMIT))
    plan, conflicts = lib.plan_files([(src, os.path.join(config, dst)) for src, dst in FILES.items()])
    hooks_path = os.path.join(config, "hooks.json")
    try:
        hooks = lib.load_json(hooks_path)
    except ValueError as e:
        conflicts.append("%s (%s)" % (hooks_path, e))
        hooks = {}
    if conflicts:
        return lib.stopped(conflicts)
    new_hooks = dict(hooks)
    new_hooks.update(hook_entries(py))
    state = "unchanged" if new_hooks == hooks else ("update" if hooks else "add")
    lib.apply_files(plan, dry)
    print("%-9s %s (entries %s; hooks run with: %s)" % (state, os.path.normpath(hooks_path), ", ".join(HOOK_KEYS), py))
    if state != "unchanged":
        lib.save_json(hooks_path, new_hooks, dry)
    print("Dry run: nothing changed." if dry else "Done. Restart Antigravity (or open a new conversation) to load it.")
    return 0


def uninstall(config, dry):
    lib.remove_files([os.path.join(config, dst) for dst in FILES.values()], dry)
    hooks_path = os.path.join(config, "hooks.json")
    try:
        hooks = lib.load_json(hooks_path)
    except ValueError as e:
        print("kept      %s (%s)" % (hooks_path, e))
        return 0
    if any(k in hooks for k in HOOK_KEYS):
        print("update    %s (remove entries %s)" % (os.path.normpath(hooks_path), ", ".join(HOOK_KEYS)))
        lib.save_json(hooks_path, {k: v for k, v in hooks.items() if k not in HOOK_KEYS}, dry)
    print("Dry run: nothing changed." if dry else "Done.")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Install the zoho-command-center setup into Antigravity.")
    ap.add_argument("--dry-run", action="store_true", help="show what would change, change nothing")
    ap.add_argument("--uninstall", action="store_true", help="remove only what this script installed")
    ap.add_argument("--home", default=os.path.expanduser("~"), help="home folder (default: yours); for tests")
    ap.add_argument("--python", help="command the hooks run Python with (default: found on this machine)")
    a = ap.parse_args(argv)
    config = os.path.join(a.home, ".gemini", "config")
    if a.uninstall:
        return uninstall(config, a.dry_run)
    return install(config, a.dry_run, a.python or lib.python_command())


if __name__ == "__main__":
    sys.exit(main())
