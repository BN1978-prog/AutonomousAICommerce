import json
from pathlib import Path
from datetime import datetime, timezone

ACT = Path("app/logs/meta_activation_executor.json")
SALES = Path("app/logs/real_sales_mode.json")
OUT = Path("app/logs/meta_auto_stop_monitor.json")

activation = json.loads(ACT.read_text(encoding="utf-8")) if ACT.exists() else {}
sales = json.loads(SALES.read_text(encoding="utf-8")) if SALES.exists() else {}

checks = []

for item in activation.get("actions", []):
    checks.append({
        "sku": item.get("sku"),
        "campaign_name": item.get("campaign_name"),
        "meta_campaign_id": item.get("meta_campaign_id"),
        "rules": [
            "stop_if_spend_reaches_5_usd",
            "stop_if_no_sales_after_24_hours",
            "stop_if_negative_roi_detected"
        ],
        "current_sales_mode": sales.get("mode"),
        "has_real_sales": sales.get("has_real_sales"),
        "action": "monitor_only_no_api_call",
        "status": "ready_to_monitor_when_campaign_active"
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "mode": "meta_auto_stop_monitor_safe_read",
    "active_campaigns_seen": len(activation.get("actions", [])),
    "checks": checks,
    "live_api_call_enabled": False,
    "status": "idle_no_active_meta_campaigns" if not checks else "monitoring_ready"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
