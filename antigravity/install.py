"""Install the zoho-command-center setup into Antigravity's global config (~/.gemini/config).

    python antigravity/install.py --dry-run     show what would change, change nothing
    python antigravity/install.py               install or update (safe to run again)
    python antigravity/install.py --uninstall   remove only what this script installed
    add --with-chrome (opt-in) to also add the chrome-devtools MCP server, so Antigravity drives the lead's own Chrome

What it installs (each file carries the marker "zcc-managed"):
    ~/.gemini/GEMINI.md: the hard rules and the lead's Command Center settings (copied from ~/.claude/CLAUDE.md at
        install, local only) as one marked block; the rest of the file is kept. Antigravity and T3 Code load it always,
        so this is the only copy (2.11.0 removes the old rules/zcc-hard-rules.md this script installed)
    agents/task-worker.md, agents/wp-qa.md       the task worker and the read-only QA agent
    hooks/zcc/*.py and three entries in hooks.json
        SessionStart (handoff brief), PreToolUse (no secrets in .md), Stop (the evidence gate)

It never overwrites or deletes a file it did not install: a file at one of its paths without the marker stops the
install before anything changes. hooks.json keeps every other hook; a backup (hooks.json.bak) is written first.
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "shared"))
import setup_lib as lib  # noqa: E402

MARKER = lib.MARKER
RULE_LIMIT = 24000  # bytes per rule file (Antigravity truncates above it)
OLD_RULES = "rules/zcc-hard-rules.md"  # installed up to 2.10.2; the GEMINI.md block is the one copy now
FILES = {
    os.path.join(HERE, "agents", "task-worker.md"): "agents/task-worker.md",
    os.path.join(HERE, "agents", "wp-qa.md"): "agents/wp-qa.md",
}
FILES.update({os.path.join(lib.HOOKS, f): "hooks/zcc/" + f for f in lib.HOOK_FILES})
WRITE_TOOLS = "write_file|edit_file|write_to_file|replace_file_content|multi_replace_file_content"
HOOK_KEYS = ("zcc-session-start", "zcc-secrets-guard", "zcc-evidence-gate")
CHROME_KEY = "chrome-devtools"
CHROME_SERVER = {"command": "npx", "args": ["-y", "chrome-devtools-mcp@latest", "--autoConnect"]}


def with_chrome(config, dry, remove=False):
    """Add (or remove) the chrome-devtools MCP server in mcp_config.json. It names only that one entry: never
    prints, changes or removes any other server (their settings can hold keys)."""
    path = os.path.join(config, "mcp_config.json")
    try:
        data = lib.load_json(path)
    except ValueError as e:
        print("kept      %s (%s); add the chrome-devtools server by hand" % (os.path.normpath(path), e))
        return 1
    servers = data.get("mcpServers")
    if servers is not None and not isinstance(servers, dict):
        print("kept      %s (mcpServers is not an object)" % os.path.normpath(path))
        return 1
    servers = dict(servers or {})
    current = servers.get(CHROME_KEY)
    if remove:
        if current == CHROME_SERVER:
            del servers[CHROME_KEY]
            print("update    %s (remove the %s server)" % (os.path.normpath(path), CHROME_KEY))
            lib.save_json(path, dict(data, mcpServers=servers), dry)
        elif current is not None:
            print("kept      %s server in %s (not the one this script adds)" % (CHROME_KEY, os.path.normpath(path)))
        return 0
    if current == CHROME_SERVER:
        print("unchanged %s (%s server)" % (os.path.normpath(path), CHROME_KEY))
        return 0
    if current is not None:
        print("kept      %s server in %s: it is set differently, so it stays as it is" % (CHROME_KEY,
                                                                                         os.path.normpath(path)))
        return 0
    servers[CHROME_KEY] = CHROME_SERVER
    print("%-9s %s (%s server: the lead's Chrome; other servers untouched)" % ("update" if data else "add",
                                                                              os.path.normpath(path), CHROME_KEY))
    lib.save_json(path, dict(data, mcpServers=servers), dry)
    if not dry:
        print("Chrome: open chrome://inspect/#remote-debugging, turn on \"Allow remote debugging for this browser "
              "instance\" (Chrome 144 or later), then start a new conversation.")
    return 0


RULES = os.path.join(HERE, "rules", "zcc-hard-rules.md")  # generated from shared/hard-rules.md; the block's source


def gemini_block(settings=None):
    """The hard rules (the rule file without its frontmatter), with the lead's settings when given, as a marked
    block for ~/.gemini/GEMINI.md."""
    body = re.sub(r"\A---\n.*?\n---\n", "", lib.read(RULES), flags=re.S).strip("\n")
    body = lib.rules_with_settings(body, settings)
    return ("<!-- zcc-managed:start (zoho-command-center Antigravity setup; the install script replaces this block) "
            "-->\n%s\n<!-- zcc-managed:end -->\n" % body)


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


def remove_old_rules(config, dry):
    """The rules file this script installed before 2.11.0 (only that marked file; a foreign one stays)."""
    old = os.path.normpath(os.path.join(config, OLD_RULES))
    if os.path.lexists(old):
        if lib.ours(old):
            print("remove    %s (one rules copy now: the GEMINI.md block)" % old)
            if not dry:
                os.remove(old)
        else:
            print("kept      %s (not installed by this script)" % old)


def install(config, dry, py, claude_md=None):
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
    new_hooks.update(hook_entries(py))  # fresh entries: an "enabled": false someone set on them goes
    state = "unchanged" if new_hooks == hooks else ("update" if hooks else "add")
    lib.apply_files(plan, dry)
    print("%-9s %s (entries %s; hooks run with: %s)" % (state, os.path.normpath(hooks_path), ", ".join(HOOK_KEYS), py))
    for key in HOOK_KEYS:
        if isinstance(hooks.get(key), dict) and hooks[key].get("enabled") is False:
            print("re-enable %s (it was \"enabled\": false; 2.10.1 fixes the empty answer that blocked writes)" % key)
    if state != "unchanged":
        lib.save_json(hooks_path, new_hooks, dry)
    remove_old_rules(config, dry)
    settings = lib.settings_block(claude_md)
    lib.say_settings(settings, claude_md)
    size = lib.update_block(os.path.join(os.path.dirname(config), "GEMINI.md"), gemini_block(settings), dry,
                            "the zcc-managed block: hard rules and settings, the one copy Antigravity and T3 load")
    if size > RULE_LIMIT:
        print("WARNING: GEMINI.md is over %d bytes: Antigravity cuts it there." % RULE_LIMIT)
    print("Dry run: nothing changed." if dry else "Done. Restart Antigravity (or open a new conversation) to load it.")
    return 0


def uninstall(config, dry):
    lib.remove_files([os.path.join(config, dst) for dst in FILES.values()], dry)
    remove_old_rules(config, dry)
    hooks_path = os.path.join(config, "hooks.json")
    try:
        hooks = lib.load_json(hooks_path)
    except ValueError as e:
        print("kept      %s (%s)" % (hooks_path, e))
        return 0
    if any(k in hooks for k in HOOK_KEYS):
        print("update    %s (remove entries %s)" % (os.path.normpath(hooks_path), ", ".join(HOOK_KEYS)))
        lib.save_json(hooks_path, {k: v for k, v in hooks.items() if k not in HOOK_KEYS}, dry)
    gemini = os.path.join(os.path.dirname(config), "GEMINI.md")
    if os.path.exists(gemini):
        lib.update_block(gemini, None, dry, "remove the zcc-managed block")
    print("Dry run: nothing changed." if dry else "Done.")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Install the zoho-command-center setup into Antigravity.")
    ap.add_argument("--dry-run", action="store_true", help="show what would change, change nothing")
    ap.add_argument("--uninstall", action="store_true", help="remove only what this script installed")
    ap.add_argument("--home", default=os.path.expanduser("~"), help="home folder (default: yours); for tests")
    ap.add_argument("--python", help="command the hooks run Python with (default: found on this machine)")
    ap.add_argument("--claude-md", help="the CLAUDE.md to copy the settings block from (default: ~/.claude/CLAUDE.md)")
    ap.add_argument("--with-chrome", action="store_true",
                    help="also add the chrome-devtools MCP server (Antigravity drives your own Chrome)")
    a = ap.parse_args(argv)
    config = os.path.join(a.home, ".gemini", "config")
    if a.uninstall:
        code = uninstall(config, a.dry_run)
        return code or (with_chrome(config, a.dry_run, remove=True) if a.with_chrome else 0)
    claude_md = a.claude_md or os.path.join(a.home, ".claude", "CLAUDE.md")
    code = install(config, a.dry_run, a.python or lib.python_command(), claude_md)
    if code == 0 and a.with_chrome:
        code = with_chrome(config, a.dry_run)
    return code


if __name__ == "__main__":
    sys.exit(main())
