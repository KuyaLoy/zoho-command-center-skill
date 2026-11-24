"""Shared code for the zoho-command-center hooks (zcc-managed: zoho-command-center setup).

Each hook script runs as `python <script> --tool antigravity|codex`, reads the event as JSON on stdin and prints the
answer in that tool's format. Any error inside a hook means "no decision": a hook must never break the session.
"""
import json
import os
import re
import sys

SUMMARY_LIMIT = 12000

# ---------------------------------------------------------------- input and output


def tool_arg(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if "--tool" in argv and argv.index("--tool") + 1 < len(argv):
        return argv[argv.index("--tool") + 1]
    return "antigravity"


def read_payload():
    raw = sys.stdin.read()
    try:
        data = json.loads(raw or "{}")
    except ValueError:
        return {}
    return data if isinstance(data, dict) else {}


def emit(obj):
    if obj is not None:
        print(json.dumps(obj, ensure_ascii=False))


def workspace_dirs(payload):
    dirs = list(payload.get("workspacePaths") or [])
    if payload.get("cwd"):
        dirs.append(payload["cwd"])
    return [d for d in dirs if isinstance(d, str) and d]


# ---------------------------------------------------------------- session start


def find_summary(payload):
    for base in workspace_dirs(payload):
        p = os.path.join(base, "ai-handoff-summary.md")
        if os.path.isfile(p):
            return p
    return None


def session_start_message(payload):
    path = find_summary(payload)
    if not path:
        return None
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    if len(text) > SUMMARY_LIMIT:
        text = text[:SUMMARY_LIMIT] + "\n[cut at %d characters: read the file for the rest]" % SUMMARY_LIMIT
    return ("Start of session (zoho-command-center hook). This project's handoff brief, %s, is below: read it first, "
            "then open the zoho-command-center skill (and handoff) before anything else.\n\n%s" % (path, text))


def session_start_answer(tool, msg):
    if msg is None:
        return {} if tool == "antigravity" else None
    if tool == "codex":
        return {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": msg}}
    return {"injectSteps": [{"systemMessage": {"systemMessage": msg}}]}


# ---------------------------------------------------------------- secrets in .md files

PLACEHOLDER = re.compile(
    r"^(<[^>]*>|\*+|x{3,}|\.{3}|redacted|hidden|none|null|changeme|example|your[_-]?\w*|\$\{?\w+\}?)$", re.I)
ASSIGNED = re.compile(
    r"(?i)\b(pass(word|wd)?|pwd|api[_-]?key|secret|token|auth[_-]?key|private[_-]?key|client[_-]?secret|"
    r"write[_-]?key|access[_-]?key)\b\s*[:=]\s*[`'\"]?([^\s`'\"<>]{6,})")
RAW = [
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),               # AWS access key id
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),      # GitHub tokens
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),           # API secret keys
    re.compile(r"\bxox[abpr]-[A-Za-z0-9-]{10,}\b"),     # Slack tokens
    re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{20,}"),  # bearer tokens
]
MD_PATH = re.compile(r"[^\s'\"<>|;&]+\.(?:md|markdown)\b", re.I)


def find_secret(text):
    for m in ASSIGNED.finditer(text):
        if not PLACEHOLDER.match(m.group(3)):
            return m.group(1)
    for rx in RAW:
        if rx.search(text):
            return "a key or token"
    return None


def strings(value):
    """Every string inside a tool call's arguments (Antigravity may send them JSON-encoded)."""
    if isinstance(value, dict):
        for v in value.values():
            yield from strings(v)
    elif isinstance(value, list):
        for v in value:
            yield from strings(v)
    elif isinstance(value, str):
        s = value
        if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
            try:
                s = json.loads(s)
            except ValueError:
                pass
        if isinstance(s, str):
            yield s


def md_writes(tool, payload):
    """(markdown path, text written to it) pairs for this tool call."""
    if tool == "codex":
        name = payload.get("tool_name") or ""
        tin = payload.get("tool_input") or {}
        cmd = tin.get("command") if isinstance(tin, dict) else tin
        if isinstance(cmd, list):
            cmd = " ".join(str(c) for c in cmd)
        if not isinstance(cmd, str):
            return []
        if "apply_patch" in name or "*** Begin Patch" in cmd:
            out, path, added = [], None, []
            for line in cmd.splitlines():
                m = re.match(r"\*\*\* (?:Add|Update) File: (.+)$", line)
                if m or line.startswith("*** End Patch"):
                    if path and re.search(r"\.(md|markdown)$", path, re.I):
                        out.append((path, "\n".join(added)))
                    path, added = (m.group(1).strip() if m else None), []
                elif path and line.startswith("+"):
                    added.append(line[1:])
            if path and re.search(r"\.(md|markdown)$", path, re.I):
                out.append((path, "\n".join(added)))
            return out
        # a shell command that writes into a .md file (redirect, tee, Out-File, Set-Content, Add-Content)
        if re.search(r">>?|\btee\b|Out-File|Set-Content|Add-Content", cmd, re.I):
            paths = MD_PATH.findall(cmd)
            return [(paths[0], cmd)] if paths else []
        return []
    args = (payload.get("toolCall") or {}).get("args") or {}
    values = list(strings(args))
    targets = [v.strip() for v in values if re.search(r"\.(md|markdown)$", v.strip(), re.I) and len(v) < 1000]
    if not targets:
        return []
    return [(targets[0], "\n".join(v for v in values if v.strip() not in targets))]


def secrets_answer(tool, payload):
    for path, text in md_writes(tool, payload):
        kind = find_secret(text)
        if kind:
            reason = ("Blocked by the zoho-command-center secrets guard: this write puts %s into %s. Never write "
                      "secrets into .md files: name where the value is kept instead (for example \"in wp-config.php\" "
                      "or \"in the password manager\")." % (kind, path))
            if tool == "codex":
                return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                               "permissionDecisionReason": reason}}
            return {"decision": "deny", "reason": reason}
    return {} if tool == "antigravity" else None


# ---------------------------------------------------------------- the evidence gate

REPORT = re.compile(r"^[\W_]*(DONE|PART DONE|READY FOR QA|QA 0|QA REPORT)\s*:\s*([A-Za-z0-9][\w.-]*)", re.M)
CHECKS_LINE = re.compile(r"^[\W_]*Checks?\s*:\s*(.+)$", re.M | re.I)
SECTION = re.compile(r"^##+\s+(.+?)\s*$", re.M)
FENCE = re.compile(r"```[^\n]*\n(.*?)```", re.S)


def last_message(tool, payload):
    if tool == "codex":
        return payload.get("last_assistant_message") or ""
    path = payload.get("transcriptPath")
    if not path or not os.path.isfile(path):
        return ""
    with open(path, encoding="utf-8", errors="replace") as f:
        lines = f.read().splitlines()
    for line in reversed(lines):
        try:
            step = json.loads(line)
        except ValueError:
            continue
        if isinstance(step, dict) and step.get("type") == "PLANNER_RESPONSE" and step.get("content"):
            return step["content"]
    return ""


def evidence(text):
    """{check name (lower): True when its section has a code block with a command and its output}."""
    found = {}
    heads = list(SECTION.finditer(text))
    for i, h in enumerate(heads):
        body = text[h.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        ok = any(len([ln for ln in block.splitlines() if ln.strip()]) >= 2 for block in FENCE.findall(body))
        name = h.group(1).strip().strip("`*").lower()
        found[name] = found.get(name, False) or ok
    return found


def task_dir(payload, task_id):
    for base in workspace_dirs(payload):
        d = os.path.abspath(base)
        for _ in range(6):
            cand = os.path.join(d, "tasks", task_id)
            if os.path.isdir(cand):
                return cand
            parent = os.path.dirname(d)
            if parent == d:
                break
            d = parent
    return None


def evidence_sources(folder):
    texts = []
    if folder:
        for rel in ("checks.md", os.path.join("qa", "checks.md")):
            p = os.path.join(folder, rel)
            if os.path.isfile(p):
                with open(p, encoding="utf-8", errors="replace") as f:
                    texts.append(f.read())
        qa = os.path.join(folder, "qa")
        if os.path.isdir(qa):
            for name in sorted(os.listdir(qa)):
                if name.startswith("qa-") and name.endswith(".md"):
                    with open(os.path.join(qa, name), encoding="utf-8", errors="replace") as f:
                        texts.append(f.read())
    return texts


def gate_problem(tool, payload):
    """None when the stop may go ahead, else the reason to send the chat back."""
    if payload.get("stop_hook_active") or payload.get("continuationActive"):
        return None  # one push back per turn, so the gate can never loop
    msg = last_message(tool, payload)
    m = REPORT.search(msg or "")
    if not m:
        return None
    kind, task_id = m.group(1), m.group(2)
    folder = task_dir(payload, task_id)
    where = os.path.join("tasks", task_id, "checks.md")
    cl = CHECKS_LINE.search(msg)
    if not cl:
        return ("Evidence gate (zoho-command-center): your %s for %s has no \"Checks:\" line. Name every check you ran "
                "in one line \"Checks: <check>, <check>\", with each one under \"## <check>\" in %s (a code block with "
                "the command and its output), then send the report again." % (kind, task_id, where))
    names = [n.strip().strip("`*.").strip() for n in re.split(r"[,;]", cl.group(1)) if n.strip()]
    found = {}
    for text in evidence_sources(folder) + [msg]:
        for k, v in evidence(text).items():
            found[k] = found.get(k, False) or v
    missing = [n for n in names if not found.get(n.lower())]
    if not missing:
        return None
    return ("Evidence gate (zoho-command-center): your %s for %s names checks with no command output in %s: %s. Run "
            "each one now, paste the command and its output in a code block under \"## <check>\" there, then send "
            "the report again. A check you did not run is reported as \"not checked\"." %
            (kind, task_id, where, ", ".join(missing)))


def gate_answer(tool, payload):
    reason = gate_problem(tool, payload)
    if reason is None:
        return {}
    if tool == "codex":
        return {"decision": "block", "reason": reason}
    return {"decision": "continue", "reason": reason}


# ---------------------------------------------------------------- runner


def run(answer_fn, tool=None):
    tool = tool or tool_arg()
    try:
        emit(answer_fn(tool, read_payload()))
    except Exception:  # never break or block the session on the hook's own error
        emit({} if tool == "antigravity" else None)
