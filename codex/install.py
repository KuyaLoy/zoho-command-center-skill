"""Install the zoho-command-center setup into Codex (~/.codex, or $CODEX_HOME).

    python codex/install.py --dry-run     show what would change, change nothing
    python codex/install.py               install or update (safe to run again)
    python codex/install.py --uninstall   remove only what this script installed

What it installs (each piece carries the marker "zcc-managed"):
    AGENTS.md                      a marked block with the hard rules (the rest of the file is kept)
    agents/zcc-task-worker.toml    the task worker subagent (name "zcc-task-worker")
    agents/zcc-reviewer.toml       the QA subagent, read-only by its rule (name "zcc-reviewer")
    hooks/zcc/*.py and three groups in hooks.json
        SessionStart (handoff brief), PreToolUse (no secrets in .md), Stop (the evidence gate)

Codex runs a new or changed hook only after you trust it once: run `codex`, open /hooks and trust the three "zcc:"
hooks. It never overwrites or deletes a file it did not install; hooks.json and AGENTS.md get a .bak first.
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "shared"))
import setup_lib as lib  # noqa: E402

MARKER = lib.MARKER
AGENTS_LIMIT = 32 * 1024  # project_doc_max_bytes default: Codex stops reading AGENTS.md files past it
FILES = {
    os.path.join(HERE, "agents", "zcc-task-worker.toml"): "agents/zcc-task-worker.toml",
    os.path.join(HERE, "agents", "zcc-reviewer.toml"): "agents/zcc-reviewer.toml",
}
FILES.update({os.path.join(lib.HOOKS, f): "hooks/zcc/" + f for f in lib.HOOK_FILES})
WRITE_TOOLS = "apply_patch|Bash|shell|Edit|Write"
SCRIPTS = ("zcc_session_start.py", "zcc_secrets_guard.py", "zcc_evidence_gate.py")


def hook_groups(py, codex_home):
    def handler(script, status, timeout, **extra):
        path = os.path.join(codex_home, "hooks", "zcc", script)
        h = {"type": "command", "command": '%s "%s" --tool codex' % (py, path), "timeout": timeout,
             "statusMessage": "zcc: " + status}
        h.update(extra)
        return h
    return {
        "SessionStart": {"matcher": "startup|resume|clear|compact",
                         "hooks": [handler("zcc_session_start.py", "handoff brief", 10, additionalContextLimit=2000)]},
        "PreToolUse": {"matcher": WRITE_TOOLS, "hooks": [handler("zcc_secrets_guard.py", "no secrets in .md", 10)]},
        "Stop": {"hooks": [handler("zcc_evidence_gate.py", "evidence gate", 20)]},
    }


def is_ours(group):
    for h in group.get("hooks", []) if isinstance(group, dict) else []:
        if str(h.get("statusMessage", "")).startswith("zcc:") or any(s in str(h.get("command", "")) for s in SCRIPTS):
            return True
    return False


def merged_hooks(hooks, py, codex_home):
    data = {k: v for k, v in hooks.items()}
    events = dict(data.get("hooks") or {})
    for event in list(events):
        events[event] = [g for g in events[event] if not is_ours(g)]
        if not events[event]:
            del events[event]
    if py is not None:
        for event, group in hook_groups(py, codex_home).items():
            events.setdefault(event, []).append(group)
    data["hooks"] = events
    return data


def agents_md(current, block):
    return lib.with_block(current, block)


def install(home, dry, py):
    plan, conflicts = lib.plan_files([(src, os.path.join(home, dst)) for src, dst in FILES.items()])
    hooks_path = os.path.join(home, "hooks.json")
    try:
        hooks = lib.load_json(hooks_path)
    except ValueError as e:
        conflicts.append("%s (%s)" % (hooks_path, e))
        hooks = {}
    if conflicts:
        return lib.stopped(conflicts)
    lib.apply_files(plan, dry)

    agents_path = os.path.join(home, "AGENTS.md")
    current = lib.read(agents_path) if os.path.exists(agents_path) else ""
    new = agents_md(current, lib.read(os.path.join(HERE, "AGENTS-block.md")))
    state = "unchanged" if new == current else ("update" if current else "add")
    print("%-9s %s (the zcc-managed block; %d bytes of %d)" % (state, os.path.normpath(agents_path),
                                                              len(new.encode("utf-8")), AGENTS_LIMIT))
    if len(new.encode("utf-8")) > AGENTS_LIMIT:
        print("WARNING: AGENTS.md is over 32 KiB: Codex may not read all of it (project_doc_max_bytes).")
    if state != "unchanged" and not dry:
        if current:
            lib.write(agents_path + ".bak", current)
        lib.write(agents_path, new)

    new_hooks = merged_hooks(hooks, py, home)
    state = "unchanged" if new_hooks == hooks else ("update" if hooks else "add")
    print("%-9s %s (SessionStart, PreToolUse, Stop groups marked \"zcc:\"; hooks run with: %s)"
          % (state, os.path.normpath(hooks_path), py))
    if state != "unchanged":
        lib.save_json(hooks_path, new_hooks, dry)
    if dry:
        print("Dry run: nothing changed.")
    else:
        print("Done. Next: run `codex`, open /hooks and trust the three \"zcc:\" hooks (Codex skips a hook until "
              "you trust it, and again after it changes).")
    return 0


def uninstall(home, dry):
    lib.remove_files([os.path.join(home, dst) for dst in FILES.values()], dry)
    agents_path = os.path.join(home, "AGENTS.md")
    if os.path.exists(agents_path):
        current = lib.read(agents_path)
        new = agents_md(current, None)
        if new != current:
            print("update    %s (remove the zcc-managed block)" % os.path.normpath(agents_path))
            if not dry:
                lib.write(agents_path + ".bak", current)
                lib.write(agents_path, new)
    hooks_path = os.path.join(home, "hooks.json")
    try:
        hooks = lib.load_json(hooks_path)
    except ValueError as e:
        print("kept      %s (%s)" % (hooks_path, e))
        return 0
    new_hooks = merged_hooks(hooks, None, home)
    if hooks and new_hooks != hooks:
        print("update    %s (remove the \"zcc:\" groups)" % os.path.normpath(hooks_path))
        lib.save_json(hooks_path, new_hooks, dry)
    print("Dry run: nothing changed." if dry else "Done.")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Install the zoho-command-center setup into Codex.")
    ap.add_argument("--dry-run", action="store_true", help="show what would change, change nothing")
    ap.add_argument("--uninstall", action="store_true", help="remove only what this script installed")
    ap.add_argument("--codex-home", default=os.environ.get("CODEX_HOME") or os.path.join(os.path.expanduser("~"),
                    ".codex"), help="Codex home (default: $CODEX_HOME or ~/.codex); for tests")
    ap.add_argument("--python", help="command the hooks run Python with (default: found on this machine)")
    a = ap.parse_args(argv)
    if a.uninstall:
        return uninstall(a.codex_home, a.dry_run)
    return install(a.codex_home, a.dry_run, a.python or lib.python_command())


if __name__ == "__main__":
    sys.exit(main())
