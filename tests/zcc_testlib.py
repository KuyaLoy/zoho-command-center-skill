"""Helpers for the setup tests (python -m unittest discover -s tests, from the repo root)."""
import contextlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOKS = os.path.join(REPO, "shared", "hooks")
PY = '"%s"' % sys.executable


def load_module(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(REPO, rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_main(mod, argv):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = mod.main(argv)
    return code, out.getvalue()


def hook(script, tool, payload):
    raw = payload if isinstance(payload, str) else json.dumps(payload)
    out = subprocess.run([sys.executable, os.path.join(HOOKS, script), "--tool", tool], input=raw,
                         capture_output=True, text=True, timeout=30)
    return json.loads(out.stdout) if out.stdout.strip() else None


def load(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def save(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def frontmatter(path):
    m = re.match(r"---\n(.*?)\n---\n", load(path), re.S)
    return dict(line.split(": ", 1) for line in m.group(1).splitlines())
