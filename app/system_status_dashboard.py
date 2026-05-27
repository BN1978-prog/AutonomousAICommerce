import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/system_status_dashboard.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

production = read_json("app/logs/production_readiness_report.json")
blockers = read_json("app/logs/external_blockers_monitor.json")
healer = read_json("app/logs/channel_self_healer.json")
control = read_json("app/logs/global_commerce_control_panel.json")

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "system_status": production.get("system_status"),
    "production_readiness": production.get("production_readiness"),
    "safe_to_continue": production.get("safe_to_continue"),
    "live_money_spending": production.get("live_money_spending"),
    "channel_self_healer": healer.get("status"),
    "external_blockers_count": blockers.get("blockers_count"),
    "external_blockers": blockers.get("blockers", []),
    "meta_funnel": production.get("meta_funnel"),
    "meta_activation": production.get("meta_activation"),
    "google_status": production.get("google_status"),
    "real_sales_mode": control.get("real_sales_mode"),
    "purchase_queue_size": control.get("purchase_queue_size"),
    "status": production.get("status")
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
