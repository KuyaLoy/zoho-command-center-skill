"""Shared helpers for the install scripts in antigravity/ and codex/ (not installed anywhere).

Every file the scripts install carries the marker "zcc-managed". A file at one of their paths without it is someone
else's: the install stops before any change, and an uninstall leaves it alone.
"""
import json
import os
import re
import shutil
import subprocess
import sys

MARKER = "zcc-managed"
SHARED = os.path.dirname(os.path.abspath(__file__))
HOOKS = os.path.join(SHARED, "hooks")
HOOK_FILES = ["zcc_hooklib.py", "zcc_session_start.py", "zcc_secrets_guard.py", "zcc_evidence_gate.py"]


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def ours(path):
    return os.path.isfile(path) and not os.path.islink(path) and MARKER in read(path)


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


def plan_files(pairs):
    """pairs: [(source path, destination path)] -> (plan [(dst, text, state)], conflicts [dst])."""
    plan, conflicts = [], []
    for src, dst in pairs:
        text = read(src)
        if MARKER not in text:
            raise SystemExit("ERROR: %s has no %s marker" % (src, MARKER))
        dst = os.path.normpath(dst)
        if os.path.lexists(dst):
            if not ours(dst):
                conflicts.append(dst)
                continue
            plan.append((dst, text, "unchanged" if read(dst) == text else "update"))
        else:
            plan.append((dst, text, "add"))
    return plan, conflicts


def apply_files(plan, dry):
    for dst, text, state in plan:
        print("%-9s %s" % (state, dst))
        if not dry and state != "unchanged":
            write(dst, text)


def remove_files(paths, dry):
    for dst in paths:
        dst = os.path.normpath(dst)
        if not os.path.lexists(dst):
            continue
        if not ours(dst):
            print("kept      %s (not installed by this script)" % dst)
            continue
        print("remove    %s" % dst)
        if not dry:
            os.remove(dst)
    for d in sorted({os.path.dirname(os.path.normpath(p)) for p in paths}, reverse=True):
        if not dry and os.path.isdir(d) and not os.listdir(d) and os.path.basename(d) in ("zcc", "zcc-selftest"):
            os.rmdir(d)


BLOCK = re.compile(r"<!-- zcc-managed:start.*?<!-- zcc-managed:end -->\n?", re.S)


def with_block(current, block):
    """current text with its marked zcc-managed block replaced by block (None: removed); other text kept."""
    rest = BLOCK.sub("", current)
    if block is None:
        return rest
    return (rest.rstrip("\n") + "\n\n" if rest.strip() else "") + block


def update_block(path, block, dry, label):
    """Write (or with block None remove) the marked block in a text file; returns the new size in bytes."""
    current = read(path) if os.path.exists(path) else ""
    new = with_block(current, block)
    if new == current:
        state = "unchanged"
    elif block is None:
        state = "update"
    else:
        state = "update" if current else "add"
    if block is not None or new != current:
        print("%-9s %s (%s)" % (state, os.path.normpath(path), label))
    if state != "unchanged" and not dry:
        if current:
            write(path + ".bak", current)
        write(path, new)
    return len(new.encode("utf-8"))


SETTINGS_HEAD = re.compile(r"^## Zoho Command Center settings\b.*$", re.M)
SETTINGS_LINE = re.compile(r"^Settings: .*$", re.M)


def settings_block(claude_md):
    """The lead's "## Zoho Command Center settings" section of CLAUDE.md (heading excluded), or None. Read at install
    time only and written only into the lead's own local files, never into this repository."""
    if not claude_md or not os.path.isfile(claude_md):
        return None
    text = read(claude_md)
    m = SETTINGS_HEAD.search(text)
    if not m:
        return None
    rest = text[m.end():]
    nxt = re.search(r"^## ", rest, re.M)
    body = (rest[:nxt.start()] if nxt else rest).strip("\n")
    return body or None


def rules_with_settings(rules, settings):
    """The rules text with its "Settings:" line replaced by the copied settings (2.11.0: no CLAUDE.md read per chat).
    No settings: the line stays, pointing at CLAUDE.md."""
    if not settings:
        return rules
    head = ("Settings (copied from `~/.claude/CLAUDE.md` at install; open that file only for a rule not covered "
            "here):\n")
    return SETTINGS_LINE.sub(lambda m: head + settings, rules, count=1)


def say_settings(settings, claude_md):
    if settings:
        print("settings  copied the \"Zoho Command Center settings\" block (%d lines) from %s; re-run after you change it"
              % (len(settings.splitlines()), os.path.normpath(claude_md)))
    else:
        print("settings  no \"Zoho Command Center settings\" block in %s: the rules keep pointing to that file"
              % os.path.normpath(claude_md or "~/.claude/CLAUDE.md"))


def load_json(path):
    if not os.path.exists(path):
        return {}
    data = json.loads(read(path))
    if not isinstance(data, dict):
        raise ValueError("not a JSON object")
    return data


def save_json(path, data, dry):
    if dry:
        return
    if os.path.exists(path):
        shutil.copyfile(path, path + ".bak")
    write(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def stopped(conflicts):
    print("STOPPED, nothing changed. Not installed by this script (no %s marker), so left alone:" % MARKER)
    for c in conflicts:
        print("  " + c)
    return 2
