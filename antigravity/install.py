"""Install the zoho-command-center setup into Antigravity's global config (~/.gemini/config).

    python antigravity/install.py --dry-run     show what would change, change nothing
    python antigravity/install.py               install or update (safe to run again)
    python antigravity/install.py --uninstall   remove only what this script installed

What it installs (each file carries the marker "zcc-managed"):
    rules/zcc-hard-rules.md                      the always-on hard rules
    agents/task-worker.md, agents/wp-qa.md       the task worker and the read-only QA agent
    hooks/zcc/*.py and two entries in hooks.json SessionStart (handoff brief) and PreToolUse (no secrets in .md)

It never overwrites or deletes a file it did not install: a file at one of its paths without the marker stops the
install before anything changes. hooks.json keeps every other hook; a backup (hooks.json.bak) is written first.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

MARKER = "zcc-managed"
HERE = os.path.dirname(os.path.abspath(__file__))
RULE_LIMIT = 24000  # bytes per rule file (Antigravity truncates above it)
FILES = {
    "rules/zcc-hard-rules.md": "rules/zcc-hard-rules.md",
    "agents/task-worker.md": "agents/task-worker.md",
    "agents/wp-qa.md": "agents/wp-qa.md",
    "hooks/zcc_session_start.py": "hooks/zcc/zcc_session_start.py",
    "hooks/zcc_secrets_guard.py": "hooks/zcc/zcc_secrets_guard.py",
}
WRITE_TOOLS = "write_file|edit_file|write_to_file|replace_file_content|multi_replace_file_content"
HOOK_KEYS = ("zcc-session-start", "zcc-secrets-guard")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def python_command():
    """The shortest command that runs Python 3 here (a bare name avoids quoting a path with spaces)."""
    names = ["python", "py"] if os.name == "nt" else ["python3", "python"]
    for name in names:
        exe = shutil.which(name)
        if not exe or "WindowsApps" in exe:  # skip the Microsoft Store stub
            continue
        args = [name, "-3"] if name == "py" else [name]
        try:
            out = subprocess.run(args + ["-c", "import sys;print(sys.version_info[0])"], capture_output=True,
                                 text=True, timeout=20)
        except (OSError, subprocess.SubprocessError):
            continue
        if out.returncode == 0 and out.stdout.strip() == "3":
            return " ".join(args)
    return '"%s"' % sys.executable


def hook_entries(py):
    return {
        "zcc-session-start": {
            "SessionStart": [{"type": "command", "command": py + " hooks/zcc/zcc_session_start.py", "timeout": 10}],
        },
        "zcc-secrets-guard": {
            "PreToolUse": [{
                "matcher": WRITE_TOOLS,
                "hooks": [{"type": "command", "command": py + " hooks/zcc/zcc_secrets_guard.py", "timeout": 10}],
            }],
        },
    }


def load_hooks(path):
    if not os.path.exists(path):
        return {}
    data = json.loads(read(path))
    if not isinstance(data, dict):
        raise ValueError("hooks.json is not a JSON object")
    return data


def install(config, dry, py):
    plan, conflicts = [], []
    for src_rel, dst_rel in FILES.items():
        src, dst = os.path.join(HERE, src_rel), os.path.normpath(os.path.join(config, dst_rel))
        new = read(src)
        if MARKER not in new:
            raise SystemExit("ERROR: %s has no %s marker" % (src_rel, MARKER))
        if dst_rel.startswith("rules/") and len(new.encode("utf-8")) > RULE_LIMIT:
            raise SystemExit("ERROR: %s is over %d bytes" % (src_rel, RULE_LIMIT))
        if os.path.lexists(dst):
            if os.path.isdir(dst) or os.path.islink(dst) or MARKER not in read(dst):
                conflicts.append(dst)
                continue
            plan.append((dst, new, "unchanged" if read(dst) == new else "update"))
        else:
            plan.append((dst, new, "add"))
    hooks_path = os.path.join(config, "hooks.json")
    try:
        hooks = load_hooks(hooks_path)
    except ValueError as e:
        conflicts.append("%s (%s)" % (hooks_path, e))
        hooks = {}
    if conflicts:
        print("STOPPED, nothing changed. Not installed by this script (no %s marker), so left alone:" % MARKER)
        for c in conflicts:
            print("  " + c)
        return 2
    new_hooks = dict(hooks)
    new_hooks.update(hook_entries(py))
    hooks_state = "unchanged" if new_hooks == hooks else ("update" if hooks else "add")
    for dst, new, state in plan:
        print("%-9s %s" % (state, dst))
        if not dry and state != "unchanged":
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst, "w", encoding="utf-8", newline="\n") as f:
                f.write(new)
    print("%-9s %s (entries %s; hooks run with: %s)" % (hooks_state, hooks_path, ", ".join(HOOK_KEYS), py))
    if not dry and hooks_state != "unchanged":
        os.makedirs(config, exist_ok=True)
        if os.path.exists(hooks_path):
            shutil.copyfile(hooks_path, hooks_path + ".bak")
        with open(hooks_path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(new_hooks, f, indent=2, ensure_ascii=False)
            f.write("\n")
    print("Dry run: nothing changed." if dry else "Done. Restart Antigravity (or open a new conversation) to load it.")
    return 0


def uninstall(config, dry):
    for dst_rel in FILES.values():
        dst = os.path.normpath(os.path.join(config, dst_rel))
        if not os.path.lexists(dst):
            continue
        if os.path.isdir(dst) or os.path.islink(dst) or MARKER not in read(dst):
            print("kept      %s (not installed by this script)" % dst)
            continue
        print("remove    %s" % dst)
        if not dry:
            os.remove(dst)
    hook_dir = os.path.join(config, "hooks", "zcc")
    if not dry and os.path.isdir(hook_dir) and not os.listdir(hook_dir):
        os.rmdir(hook_dir)
    hooks_path = os.path.join(config, "hooks.json")
    try:
        hooks = load_hooks(hooks_path)
    except ValueError as e:
        print("kept      %s (%s)" % (hooks_path, e))
        return 0
    if any(k in hooks for k in HOOK_KEYS):
        print("update    %s (remove entries %s)" % (hooks_path, ", ".join(HOOK_KEYS)))
        if not dry:
            shutil.copyfile(hooks_path, hooks_path + ".bak")
            for k in HOOK_KEYS:
                hooks.pop(k, None)
            with open(hooks_path, "w", encoding="utf-8", newline="\n") as f:
                json.dump(hooks, f, indent=2, ensure_ascii=False)
                f.write("\n")
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
    return install(config, a.dry_run, a.python or python_command())


if __name__ == "__main__":
    sys.exit(main())
