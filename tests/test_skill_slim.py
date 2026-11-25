"""2.11.0: SKILL.md is slim (about 5,000 tokens), and no rule of 2.10.2 is lost: every bullet and paragraph of the
2.10.2 SKILL.md (tests/data/skill-2.10.2.md) is still there, word for word, in SKILL.md or a reference file."""
import glob
import os
import re
import unittest

from zcc_testlib import REPO, load

SKILL_DIR = os.path.join(REPO, "skills", "zoho-command-center")
SNAPSHOT = os.path.join(REPO, "tests", "data", "skill-2.10.2.md")
# Changed on purpose in 2.11.0 (not moved): the Files paragraph now lists the new reference files.
# 2.11.1: the Command Center role line says the holder line is a record ("the one the lead works with").
CHANGED = ("**Files** (beside this one)", "**Command Center:** anything else in a Command Center project.")


def norm(text):
    return " ".join(text.split())


def units(text):
    """Each bullet (its own lines only) and each paragraph of a SKILL.md, without frontmatter, headings, the version
    line, table rows and the generated Hard rules section."""
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    text = re.sub(r"## Hard rules \(every tool, every turn\)\n.*?(?=\n## )", "", text, flags=re.S)
    out, cur = [], []
    for line in text.split("\n"):
        starts = re.match(r"^\s*- ", line) or line.startswith("#") or line.startswith("|") or not line.strip()
        if starts and cur:
            out.append(norm(" ".join(cur)))
            cur = []
        if line.startswith("#") or line.startswith("|") or not line.strip() or line.startswith("Version:"):
            continue
        cur.append(re.sub(r"^\s*- ", "", line))
    if cur:
        out.append(norm(" ".join(cur)))
    return [u for u in out if u and not u.startswith(CHANGED)]


class SlimSkillTest(unittest.TestCase):
    def test_about_5000_tokens(self):
        size = len(load(os.path.join(SKILL_DIR, "SKILL.md")).encode("utf-8"))
        self.assertLess(size, 21000, "SKILL.md is %d bytes (about %d tokens)" % (size, size // 4))

    def test_no_rule_of_2_10_2_is_lost(self):
        union = norm(" ".join([load(os.path.join(SKILL_DIR, "SKILL.md"))] +
                              [load(p) for p in sorted(glob.glob(os.path.join(SKILL_DIR, "references", "*.md")))]))
        union = union.replace("- ", "")  # moved nested bullets lost their indent; compare the words
        lost = [u for u in units(load(SNAPSHOT)) if u.replace("- ", "") not in union]
        self.assertEqual(lost, [], "\n\n".join(u[:160] for u in lost))

    def test_every_moved_part_has_a_pointer(self):
        skill = load(os.path.join(SKILL_DIR, "SKILL.md"))
        for ref in ("task-size.md", "how-we-talk.md", "safety.md", "context-watch.md", "qa-chat.md"):
            self.assertIn(ref, skill)
            text = load(os.path.join(SKILL_DIR, "references", ref))
            for part in re.findall(r"^## (.+)$", text, re.M):
                self.assertIn(part.split(" (")[0].split(",")[0], skill + text, (ref, part))

    def test_worker_rules_and_sections_kept(self):
        skill = load(os.path.join(SKILL_DIR, "SKILL.md"))
        for heading in ("## Settings", "## Task size and effort", "## Which role am I?",
                        "## Hard rules (every tool, every turn)", "## Shared rules (both roles)",
                        "## Command Center rules (PM/TL)",
                        "## Context watch: never let a task chat hit auto-compact (learned 11 Nov 2026)",
                        "## Worker rules (task chat)"):
            self.assertIn(heading, skill)
        for words in ("Phase 1, plan, read-only", "Phase 2, work", "**Cheaper checks, with proof**",
                      "**Talk to Command Center directly at each milestone**", "Final report"):
            self.assertIn(words, skill)


if __name__ == "__main__":
    unittest.main()
