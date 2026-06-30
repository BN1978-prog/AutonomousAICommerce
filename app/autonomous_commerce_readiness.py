
import json
from pathlib import Path
from datetime import datetime, timezone

FILES = {
    "live_gate_config": Path("app/logs/autonomous_commerce_live_gate.json"),
    "live_gate_report": Path("app/logs/autonomous_commerce_live_gate_report.json"),
    "fulfillment_runner": Path("app/logs/autonomous_fulfillment_runner.json"),
    "cj_purchase_attempts": Path("app/logs/cj_purchase_attempts.json"),
    "tracking_updates": Path("app/logs/tracking_updates.json"),
    "shopify_fulfillment_sync": Path("app/logs/shopify_fulfillment_sync.json"),
    "universal_publisher": Path("app/logs/universal_publisher.json"),
    "incoming_orders": Path("app/logs/incoming_orders.json"),
    "supplier_queue": Path("app/logs/supplier_purchase_queue.json"),
}

OUT = Path("app/logs/autonomous_commerce_readiness.json")

def read_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return default

live_config = read_json(FILES["live_gate_config"], {})
live_report = read_json(FILES["live_gate_report"], {})
fulfillment_runner = read_json(FILES["fulfillment_runner"], {})
cj_attempts = read_json(FILES["cj_purchase_attempts"], [])
tracking = read_json(FILES["tracking_updates"], [])
shopify_fulfillment = read_json(FILES["shopify_fulfillment_sync"], {})
publisher = read_json(FILES["universal_publisher"], {})
incoming = read_json(FILES["incoming_orders"], [])
queue = read_json(FILES["supplier_queue"], [])

checks = []

def add_check(name, ok, status, details=None):
    checks.append({
        "name": name,
        "ok": bool(ok),
        "status": status,
        "details": details or {}
    })

add_check(
    "shopify_publisher",
    publisher.get("status") in ["UNIVERSAL_PUBLISHER_LIVE", "UNIVERSAL_PUBLISHER_DRY_RUN"],
    publisher.get("status", "missing"),
    {"mode": publisher.get("mode")}
)

add_check(
    "paid_order_collection",
    isinstance(incoming, list),
    "ready",
    {"incoming_orders": len(incoming)}
)

add_check(
    "supplier_purchase_queue",
    isinstance(queue, list),
    "ready",
    {"queue_size": len(queue)}
)

add_check(
    "live_gate_present",
    bool(live_config),
    "configured" if live_config else "missing",
    live_config
)

add_check(
    "live_gate_enforced",
    live_report.get("status") == "LIVE_GATE_CHECKED",
    live_report.get("status", "missing"),
    {
        "approved_count": live_report.get("approved_count"),
        "blocked_count": live_report.get("blocked_count")
    }
)

add_check(
    "cj_purchase_executor",
    isinstance(cj_attempts, list),
    "ready",
    {
        "attempts": len(cj_attempts),
        "statuses": sorted(list({x.get("status") for x in cj_attempts if isinstance(x, dict)}))
    }
)

add_check(
    "tracking_sync",
    isinstance(tracking, list),
    "ready",
    {
        "tracking_items": len(tracking),
        "waiting": sum(1 for x in tracking if isinstance(x, dict) and not x.get("tracking_number"))
    }
)

add_check(
    "shopify_fulfillment_sync",
    bool(shopify_fulfillment),
    shopify_fulfillment.get("status", "missing"),
    {
        "dry_run": shopify_fulfillment.get("dry_run"),
        "updates_seen": shopify_fulfillment.get("updates_seen")
    }
)

live_mode = bool(live_config.get("live_mode"))
cj_live = bool(live_config.get("cj_live_purchase_enabled"))
fulfillment_live = bool(live_config.get("shopify_fulfillment_live_enabled"))

if live_mode and cj_live and fulfillment_live:
    readiness = "FULL_LIVE_AUTONOMY_ENABLED"
elif live_mode or cj_live or fulfillment_live:
    readiness = "PARTIAL_LIVE_AUTONOMY"
else:
    readiness = "SAFE_AUTONOMY_DRY_RUN_GATED"

blocking_items = [x for x in checks if not x["ok"]]

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "status": readiness,
    "autonomous_without_manual_steps": len(blocking_items) == 0,
    "live_mode": live_mode,
    "cj_live_purchase_enabled": cj_live,
    "shopify_fulfillment_live_enabled": fulfillment_live,
    "checks": checks,
    "blocking_items": blocking_items,
    "summary": {
        "incoming_orders": len(incoming),
        "supplier_queue": len(queue),
        "cj_attempts": len(cj_attempts),
        "tracking_items": len(tracking),
        "live_gate_approved": live_report.get("approved_count", 0),
        "live_gate_blocked": live_report.get("blocked_count", 0)
    },
    "note": "System is designed for autonomy. Real money spend remains controlled by autonomous_commerce_live_gate."
}

OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(report, indent=2, ensure_ascii=False))
