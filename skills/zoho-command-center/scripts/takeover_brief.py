"""Draft the takeover brief (command-center.md step 1) from a project's own files, in at most 10 lines.

    python <this skill's folder>/scripts/takeover_brief.py <project folder>

Reads handoff.md (title, Mode and holder lines, the "## Task chats" board, "## Changes Made"), the newest files in
eod/ and ai-handoff-summary.md ("## Next action"). Writes nothing. The brief is a draft: Command Center re-checks each
open task (files, site, Zoho by its link) before it reports, and anything the files do not say is "unverified".
"""
import glob
import os
import re
import sys

MAX_LINES = 10
WIDTH = 118


def read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def section(text, name):
    m = re.search(r"^## " + re.escape(name) + r"\b.*$", text, re.M)
    if not m:
        return ""
    rest = text[m.end():]
    nxt = re.search(r"^## ", rest, re.M)
    return rest[:nxt.start()] if nxt else rest


def bullets(text):
    out, cur = [], None
    for line in text.splitlines():
        if re.match(r"^\s*[-*] ", line):
            if cur:
                out.append(cur)
            cur = re.sub(r"^\s*[-*] ", "", line).strip()
        elif cur is not None and line.startswith("  ") and line.strip():
            cur += " " + line.strip()
        elif not line.strip() and cur:
            out.append(cur)
            cur = None
    if cur:
        out.append(cur)
    return out


def short(text, width=WIDTH):
    text = " ".join(text.split())
    return text if len(text) <= width else text[:width - 3].rstrip() + "..."


def board_rows(handoff):
    rows = []
    for line in section(handoff, "Task chats").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 7 or set(cells[0]) <= set("-: ") or cells[0].lower() == "task":
            continue
        rows.append(cells)
    return rows


def last_jobs(project, handoff):
    """(date, text) of the newest finished or stopped jobs: eod/ lines first, then handoff.md's Changes Made."""
    jobs = []
    for path in sorted(glob.glob(os.path.join(project, "eod", "*.md"))):
        date = os.path.splitext(os.path.basename(path))[0]
        for b in bullets(read(path)):
            jobs.append((date, b))
    for b in bullets(section(handoff, "Changes Made")):
        m = re.match(r"^(\d{4}-\d{2}-\d{2})\b[\s:,-]*(.*)$", b)
        jobs.append((m.group(1), m.group(2)) if m else ("undated", b))
    dated = [j for j in jobs if j[0] != "undated"]
    dated.sort(key=lambda j: j[0])  # stable: within a day, file order
    seen, out = set(), []
    for date, text in reversed(dated):
        key = text.lower()[:60]
        if key in seen:
            continue
        seen.add(key)
        out.append((date, text))
        if len(out) == 2:
            break
    return out


def brief(project):
    handoff = read(os.path.join(project, "handoff.md"))
    summary = read(os.path.join(project, "ai-handoff-summary.md"))
    title = re.search(r"^# (?:Handoff:\s*)?(.+)$", handoff, re.M)
    name = title.group(1).strip() if title else os.path.basename(os.path.abspath(project))
    mode = re.search(r"Mode:\s*([^\n]+)", handoff)
    holder = re.search(r"Active Command Center:\s*([^\n]+)", handoff)
    rows = board_rows(handoff)
    site = rows[-1][2] if rows else "unverified"
    lines = [short("Project: %s; site %s; mode %s; holder %s" % (
        name, site, mode.group(1).strip() if mode else "unverified",
        holder.group(1).strip() if holder else "none yet (write it)"))]
    lines.append("Last jobs:")
    jobs = last_jobs(project, handoff)
    lines += [short("- %s %s" % j) for j in jobs] or ["- unverified (no eod/ files or Changes Made)"]
    open_rows = [r for r in rows if not re.search(r"\b(DONE|ARCHIVED)\b", r[5] + " " + r[1], re.I)]
    lines.append("Open now:")
    room = MAX_LINES - len(lines) - 1
    shown = open_rows[:room - 1] if len(open_rows) > room else open_rows
    lines += [short("- %s: %s; waiting on %s" % (r[0], r[5] or "unverified", r[6] or "unverified")) for r in shown]
    if len(open_rows) > len(shown):
        lines.append("- and %d more on the board" % (len(open_rows) - len(shown)))
    if not open_rows:
        lines.append("- none on the board")
    nxt = bullets(section(summary, "Next action")) or bullets(section(handoff, "Next Steps"))[-1:]
    lines.append(short("Next: " + (nxt[0] if nxt else "unverified")))
    return lines[:MAX_LINES]


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    project = argv[0] if argv else "."
    if not os.path.isfile(os.path.join(project, "handoff.md")):
        print("No handoff.md in %s: not an existing Command Center (set it up instead)." % project)
        return 1
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    print("\n".join(brief(project)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
