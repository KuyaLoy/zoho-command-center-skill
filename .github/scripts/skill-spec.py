"""Agent Skills spec check (agentskills.io), run by the check workflow on every pull request.

    python .github/scripts/skill-spec.py
Each skills/<name>/SKILL.md: frontmatter name equals the folder name (lowercase letters, digits and hyphens, at most
64 characters), a description of 1 to 1,024 characters, and fewer than 500 lines.
"""
import glob
import os
import re
import sys


def check(path):
    errors = []
    folder = os.path.basename(os.path.dirname(path))
    with open(path, encoding="utf-8") as f:
        text = f.read()
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return ["%s: no frontmatter" % path]
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip("'\"")
    name, desc = fm.get("name", ""), fm.get("description", "")
    if name != folder:
        errors.append("%s: name %r is not the folder name %r" % (path, name, folder))
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
        errors.append("%s: name %r must be lowercase letters, digits and hyphens, at most 64" % (path, name))
    if not 1 <= len(desc) <= 1024:
        errors.append("%s: description is %d characters (1 to 1,024)" % (path, len(desc)))
    lines = text.count("\n")
    if lines >= 500:
        errors.append("%s: %d lines (under 500)" % (path, lines))
    return errors


def main(root="."):
    paths = sorted(glob.glob(os.path.join(root, "skills", "*", "SKILL.md")))
    errors = [e for p in paths for e in check(p)]
    for e in errors:
        print("::error::" + e)
    if not paths:
        print("::error::no skills/*/SKILL.md found")
        return 1
    if not errors:
        print("OK: %d skill(s) match the Agent Skills spec." % len(paths))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
