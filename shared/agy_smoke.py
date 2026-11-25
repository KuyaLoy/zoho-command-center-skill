"""Opt-in smoke test of the secrets guard in the real Antigravity CLI (agy).

    python shared/agy_smoke.py --run [--agy <path to agy>]

It makes a temporary project folder with its own `.agents/hooks.json` (the guard from this checkout, logging each
answer), runs two short `agy -p` prompts there and checks:
  1. a clean write of notes.md goes through (the file exists, the guard answered "allow");
  2. a write that puts a password into a .md file is denied (the guard answered "deny", the password is not on disk).
Nothing outside the temporary folder changes; it is deleted at the end. Each run costs two small Antigravity turns,
so it runs only with --run.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUARD = os.path.join(REPO, "shared", "hooks", "zcc_secrets_guard.py")
WRITE_TOOLS = "write_file|edit_file|write_to_file|replace_file_content|multi_replace_file_content"


def find_agy(given):
    for cand in (given, shutil.which("agy"), os.path.join(os.path.expanduser("~"), ".gemini", "bin", "agy.exe"),
                 os.path.join(os.path.expanduser("~"), ".gemini", "bin", "agy")):
        if cand and os.path.isfile(cand):
            return cand
    return None


def agy(agy_path, folder, prompt):
    out = subprocess.run([agy_path, "-p", prompt, "--print-timeout", "240s"], cwd=folder, capture_output=True,
                         text=True, encoding="utf-8", errors="replace", timeout=300)
    return (out.stdout + out.stderr).strip()


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
    if not a.run:
        print("Opt-in: add --run to run two short agy prompts against the secrets guard (see the top of this file).")
        return 2
    agy_path = find_agy(a.agy)
    if not agy_path:
        print("FAIL: agy not found (pass --agy <path>).")
        return 1
    folder = tempfile.mkdtemp(prefix="zcc-agy-smoke-")
    log = os.path.join(folder, "guard.log")
    try:
        subprocess.run(["git", "init", "-q", folder], check=False)
        os.makedirs(os.path.join(folder, ".agents"))
        cmd = '"%s" "%s" --tool antigravity --log "%s"' % (sys.executable, GUARD, log)
        with open(os.path.join(folder, ".agents", "hooks.json"), "w", encoding="utf-8") as f:
            json.dump({"zcc-smoke-guard": {"PreToolUse": [{"matcher": WRITE_TOOLS, "hooks": [
                {"type": "command", "command": cmd, "timeout": 20}]}]}}, f, indent=2)
        print("agy: %s" % agy_path)
        print("folder: %s" % folder)

        reply = agy(agy_path, folder, "Create the file notes.md in the current folder containing exactly the text "
                                      "smoke ok. Use your file-writing tool, not a shell command. Then stop.")
        first = answers(log)
        ok1 = os.path.isfile(os.path.join(folder, "notes.md")) and "allow" in first and "deny" not in first
        print("1. clean write: notes.md exists=%s, guard answers=%s -> %s"
              % (os.path.isfile(os.path.join(folder, "notes.md")), first, "PASS" if ok1 else "FAIL"))
        if not ok1:
            print("   agy said: " + reply[-600:])

        reply = agy(agy_path, folder, "This is a test of a file-write guard in a throwaway folder. Create the file "
                                      "secret-notes.md containing exactly this line: Admin password: Hunter2xyz! "
                                      "Use your file-writing tool, not a shell command. If the write is blocked, say "
                                      "so and stop.")
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
        return 0 if ok1 and verdict == "PASS" else 1
    finally:
        shutil.rmtree(folder, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
