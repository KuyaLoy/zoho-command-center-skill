"""PreToolUse hook (zcc-managed: zoho-command-center antigravity setup).

Denies a file write or edit that would put a password, key or token into a Markdown file (notes, reports, plans,
handoff files). Everything else gets no decision ({}), so the app's own permission settings stay as they are.
"""
import json
import re
import sys

# A value that is clearly a placeholder, not a secret.
PLACEHOLDER = re.compile(r"^(<[^>]*>|\*+|x{3,}|\.{3}|redacted|hidden|none|null|changeme|example|your[_-]?\w*|\$\{?\w+\}?)$",
                         re.I)
ASSIGNED = re.compile(
    r"(?i)\b(pass(word|wd)?|pwd|api[_-]?key|secret|token|auth[_-]?key|private[_-]?key|client[_-]?secret|"
    r"write[_-]?key|access[_-]?key)\b\s*[:=]\s*[`'\"]?([^\s`'\"<>]{6,})"
)
RAW = [
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),               # AWS access key id
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),      # GitHub tokens
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),           # API secret keys
    re.compile(r"\bxox[abpr]-[A-Za-z0-9-]{10,}\b"),     # Slack tokens
    re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{20,}"),  # bearer tokens
]


def strings(value):
    """Every string inside the tool call's arguments (values may arrive JSON-encoded)."""
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


def find_secret(text):
    for m in ASSIGNED.finditer(text):
        if not PLACEHOLDER.match(m.group(3)):
            return m.group(1)
    for rx in RAW:
        if rx.search(text):
            return "a key or token"
    return None


def main():
    payload = json.loads(sys.stdin.read() or "{}")
    args = (payload.get("toolCall") or {}).get("args") or {}
    values = list(strings(args))
    targets = [v.strip() for v in values if re.search(r"\.(md|markdown)$", v.strip(), re.I) and len(v) < 1000]
    if not targets:
        print("{}")
        return
    for v in values:
        if v.strip() in targets:
            continue
        kind = find_secret(v)
        if kind:
            print(json.dumps({
                "decision": "deny",
                "reason": "Blocked by the zoho-command-center secrets guard: this write puts %s into %s. Never "
                          "write secrets into .md files: name where the value is kept instead (for example "
                          "\"in wp-config.php\" or \"in the password manager\")." % (kind, targets[0]),
            }))
            return
    print("{}")


if __name__ == "__main__":
    try:
        main()
    except Exception:  # never block on the guard's own error
        print("{}")
