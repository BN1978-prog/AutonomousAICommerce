import json
from pathlib import Path
from datetime import datetime, timezone

SRC = Path("app/logs/live_execution_consolidated.json")
OUT = Path("app/logs/live_spend_audit_ledger.jsonl")

data = json.loads(SRC.read_text(encoding="utf-8"))

entry = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "event": "LIVE_EXECUTION_AUDIT",
    "total_campaigns_checked": data.get("total_campaigns_checked", 0),
    "real_api_calls": data.get("real_api_calls", 0),
    "real_money_spent": data.get("real_money_spent", 0),
    "status": data.get("status"),
    "results": data.get("results", [])
}

with OUT.open("a", encoding="utf-8") as f:
    f.write(json.dumps(entry) + "\n")

print(json.dumps({
    "ledger": str(OUT),
    "event": entry["event"],
    "real_api_calls": entry["real_api_calls"],
    "real_money_spent": entry["real_money_spent"],
    "status": "LIVE_SPEND_AUDIT_LEDGER_UPDATED"
}, indent=2))
