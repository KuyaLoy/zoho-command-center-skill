"""Opt-in smoke test of the secrets guard in the real Antigravity CLI (agy).

    python shared/agy_smoke.py --run [--agy <path to agy>]

It makes a temporary project folder with its own `.agents/hooks.json` (the secrets guard and the evidence gate from
this checkout, logging each answer), runs four short `agy -p` prompts there and checks:
  1. a clean write of notes.md goes through (the file exists, the guard answered "allow");
  2. a write that puts a password into a .md file is denied (the guard answered "deny", the password is not on disk);
  3. a normal turn ("reply OK") ends cleanly with the gate installed: the gate answered "stop", under 60 seconds;
  4. a "DONE: TEST-1" report with a "Checks:" line but no checks.md is sent back once ("continue"), then ends.
Nothing outside the temporary folder changes; it is deleted at the end. Each run costs four small Antigravity turns,
so it runs only with --run.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUARD = os.path.join(REPO, "shared", "hooks", "zcc_secrets_guard.py")
GATE = os.path.join(REPO, "shared", "hooks", "zcc_evidence_gate.py")
WRITE_TOOLS = "write_file|edit_file|write_to_file|replace_file_content|multi_replace_file_content"


def find_agy(given):
    for cand in (given, shutil.which("agy"), os.path.join(os.path.expanduser("~"), ".gemini", "bin", "agy.exe"),
                 os.path.join(os.path.expanduser("~"), ".gemini", "bin", "agy")):
        if cand and os.path.isfile(cand):
            return cand
    return None


def agy(agy_path, folder, prompt, timeout=240):
    """(reply, exit code, seconds); exit code None when the turn did not end in time."""
    start = time.time()
    try:
        out = subprocess.run([agy_path, "-p", prompt, "--print-timeout", "%ds" % timeout], cwd=folder,
                             capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout + 60)
    except subprocess.TimeoutExpired:
        return "(no end: killed after %d s)" % (timeout + 60), None, time.time() - start
    return (out.stdout + out.stderr).strip(), out.returncode, time.time() - start


def answers(log):
    if not os.path.exists(log):
        return []
    with open(log, encoding="utf-8") as f:
        return [json.loads(line.split("\t", 1)[1]).get("decision") for line in f if "\t" in line]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--run", action="store_true", help="really run the two agy prompts (uses Antigravity quota)")
    ap.add_argument("--agy", help="path to agy (default: on PATH or ~/.gemini/bin)")
    a = ap.parse_args(argv)
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    if not a.run:
        print("Opt-in: add --run to run two short agy prompts against the secrets guard (see the top of this file).")
        return 2
    agy_path = find_agy(a.agy)
    if not agy_path:
        print("FAIL: agy not found (pass --agy <path>).")
        return 1
    folder = tempfile.mkdtemp(prefix="zcc-agy-smoke-")
    log = os.path.join(folder, "guard.log")
    gate_log = os.path.join(folder, "gate.log")
    try:
        subprocess.run(["git", "init", "-q", folder], check=False)
        os.makedirs(os.path.join(folder, ".agents"))
        cmd = '"%s" "%s" --tool antigravity --log "%s"' % (sys.executable, GUARD, log)
        gate_cmd = '"%s" "%s" --tool antigravity --log "%s"' % (sys.executable, GATE, gate_log)
        with open(os.path.join(folder, ".agents", "hooks.json"), "w", encoding="utf-8") as f:
            # The gate takes the installed hook's name so this copy overrides an installed one (else the installed
            # gate answers first). The guard keeps its own name: an installed entry set "enabled": false would
            # switch off a same-named project copy too (seen 25 Nov 2026).
            json.dump({"zcc-smoke-guard": {"PreToolUse": [{"matcher": WRITE_TOOLS, "hooks": [
                {"type": "command", "command": cmd, "timeout": 20}]}]},
                       "zcc-evidence-gate": {"Stop": [{"type": "command", "command": gate_cmd, "timeout": 20}]}},
                      f, indent=2)
        print("agy: %s" % agy_path)
        print("folder: %s" % folder)

        reply, _, _ = agy(agy_path, folder, "Create the file notes.md in the current folder containing exactly the "
                                            "text smoke ok. Use your file-writing tool, not a shell command. Then stop.")
        first = answers(log)
        ok1 = os.path.isfile(os.path.join(folder, "notes.md")) and "allow" in first and "deny" not in first
        print("1. clean write: notes.md exists=%s, guard answers=%s -> %s"
              % (os.path.isfile(os.path.join(folder, "notes.md")), first, "PASS" if ok1 else "FAIL"))
        if not ok1:
            print("   agy said: " + reply[-600:])

        reply, _, _ = agy(agy_path, folder, "This is a test of a file-write guard in a throwaway folder. Create the "
                                            "file secret-notes.md containing exactly this line: Admin password: "
                                            "Hunter2xyz! Use your file-writing tool, not a shell command. If the "
                                            "write is blocked, say so and stop.")
        second = answers(log)[len(first):]
        path = os.path.join(folder, "secret-notes.md")
        leaked = os.path.isfile(path) and "Hunter2xyz" in open(path, encoding="utf-8", errors="replace").read()
        if "deny" in second and not leaked:
            verdict = "PASS"
        elif not second and not leaked:
            verdict = "INCONCLUSIVE (the model did not try the write)"
        else:
            verdict = "FAIL"
        print("2. password write: guard answers=%s, password on disk=%s -> %s" % (second, leaked, verdict))
        if verdict != "PASS":
            print("   agy said: " + reply[-600:])
        before = len(answers(gate_log))
        reply, code, secs = agy(agy_path, folder, "Reply with exactly: OK", timeout=60)
        third = answers(gate_log)[before:]
        ok3 = code == 0 and secs < 60 and bool(third) and "continue" not in third
        print("3. normal turn: exit=%s, %.0f s, gate answers=%s -> %s" % (code, secs, third, "PASS" if ok3 else "FAIL"))
        if not ok3:
            print("   agy said: " + reply[-600:])

        before = len(answers(gate_log))
        reply, code, secs = agy(agy_path, folder, "Reply with exactly these two lines and nothing else:\n"
                                                  "DONE: TEST-1 smoke report\nChecks: home page 200", timeout=180)
        fourth = answers(gate_log)[before:]
        ok4 = code == 0 and fourth[:1] == ["continue"] and fourth.count("continue") == 1 and fourth[-1:] != ["continue"]
        print("4. report without checks.md: exit=%s, %.0f s, gate answers=%s -> %s"
              % (code, secs, fourth, "PASS" if ok4 else "FAIL"))
        if not ok4:
            print("   agy said: " + reply[-600:])
        return 0 if ok1 and verdict == "PASS" and ok3 and ok4 else 1
    finally:
        shutil.rmtree(folder, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
