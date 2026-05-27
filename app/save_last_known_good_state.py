import json
from pathlib import Path
from datetime import datetime, timezone

SRC = Path("app/logs/system_status_dashboard.json")
OUT = Path("app/logs/last_known_good_state.json")

data = json.loads(SRC.read_text(encoding="utf-8")) if SRC.exists() else {}

snapshot = {
    "saved_at": datetime.now(timezone.utc).isoformat(),
    "system_status": data.get("system_status"),
    "production_readiness": data.get("production_readiness"),
    "status": data.get("status"),
    "safe_to_continue": data.get("safe_to_continue"),
    "live_money_spending": data.get("live_money_spending"),
    "channel_self_healer": data.get("channel_self_healer"),
    "external_blockers_count": data.get("external_blockers_count"),
    "external_blockers": data.get("external_blockers", []),
    "meta_funnel": data.get("meta_funnel"),
    "google_status": data.get("google_status"),
    "real_sales_mode": data.get("real_sales_mode"),
    "purchase_queue_size": data.get("purchase_queue_size")
}

OUT.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
print(json.dumps(snapshot, indent=2))
