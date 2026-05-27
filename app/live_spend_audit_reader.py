import json
from pathlib import Path

LEDGER = Path("app/logs/live_spend_audit_ledger.jsonl")

entries = []

if LEDGER.exists():
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        if line.strip():
            entries.append(json.loads(line))

last = entries[-5:]

report = {
    "ledger_exists": LEDGER.exists(),
    "entries_count": len(entries),
    "last_entries": last,
    "status": "LIVE_SPEND_AUDIT_READER_READY"
}

print(json.dumps(report, indent=2))
