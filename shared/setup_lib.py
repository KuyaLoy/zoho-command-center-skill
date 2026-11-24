"""Shared helpers for the install scripts in antigravity/ and codex/ (not installed anywhere).

Every file the scripts install carries the marker "zcc-managed". A file at one of their paths without it is someone
else's: the install stops before any change, and an uninstall leaves it alone.
"""
import json
import os
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
