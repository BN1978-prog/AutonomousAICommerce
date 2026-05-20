import json
from pathlib import Path
from datetime import datetime, timezone

FILES = {
    "final": "app/logs/final_system_checkpoint.json",
    "ads": "app/logs/ad_campaign_executor.json",
    "orders": "app/logs/real_sales_mode.json",
    "queue": "app/logs/supplier_purchase_executor.json",
    "arb": "app/logs/opportunities/global_execution_plan.json",
    "external": "app/logs/external_platform_blockers.json",
}

def load(path):
    p = Path(path)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}

data = {k: load(v) for k, v in FILES.items()}

external = data["external"]
ready_platforms = external.get("ready_platforms", [])
blockers = external.get("blockers", [])

def platform_status(name):
    for r in ready_platforms:
        if r.get("platform") == name:
            return r.get("status")
    for b in blockers:
        if b.get("platform") == name:
            return b.get("status") + ":" + b.get("reason", "")
    return "unknown"

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "system_status": data["final"].get("status"),
    "safe_to_continue": data["final"].get("safe_to_continue"),
    "arbitrage_plans": data["arb"].get("plans_created", 0),
    "ad_actions_ready": data["ads"].get("actions_ready", 0),
    "meta_status": platform_status("meta_ads"),
    "google_status": platform_status("google_ads"),
    "external_ready_count": external.get("ready_count", 0),
    "external_blocker_count": external.get("blocker_count", 0),
    "external_blockers": blockers,
    "real_sales_mode": data["orders"].get("mode"),
    "has_real_sales": data["orders"].get("has_real_sales"),
    "purchase_queue_size": data["queue"].get("queue_size"),
    "live_money_spending": False,
    "next_required_action": "wait_for_real_sales_or_resolve_external_platform_blockers",
    "status": "GLOBAL_COMMERCE_READY_WITH_EXTERNAL_BLOCKERS" if blockers else "GLOBAL_COMMERCE_READY_SAFE_MODE"
}

Path("app/logs/global_commerce_control_panel.json").write_text(
    json.dumps(report, indent=2), encoding="utf-8"
)

print(json.dumps(report, indent=2))
