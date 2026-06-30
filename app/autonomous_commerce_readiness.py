
import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/autonomous_commerce_readiness.json")

FILES = {
    "live_gate_config": Path("app/logs/autonomous_commerce_live_gate.json"),
    "live_gate_report": Path("app/logs/autonomous_commerce_live_gate_report.json"),
    "fulfillment_runner": Path("app/logs/autonomous_fulfillment_runner.json"),
    "commerce_runner": Path("app/logs/autonomous_commerce_runner.json"),
    "universal_publisher": Path("app/logs/universal_publisher.json"),
    "incoming_orders": Path("app/logs/incoming_orders.json"),
    "supplier_queue": Path("app/logs/supplier_purchase_queue.json"),
    "order_ledger": Path("app/logs/order_processing_ledger.json"),
}

REQUIRED_ORDER_STAGES = [
    "supplier_queue_created",
    "cj_order_draft_created",
    "cj_payload_created",
    "cj_purchase_attempted",
    "tracking_watch_created",
    "shopify_fulfillment_synced",
]

def read_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return default

def stage_done(order, stage):
    return bool(order.get("stages", {}).get(stage, {}).get("done"))

live_config = read_json(FILES["live_gate_config"], {})
live_report = read_json(FILES["live_gate_report"], {})
fulfillment_runner = read_json(FILES["fulfillment_runner"], {})
commerce_runner = read_json(FILES["commerce_runner"], {})
publisher = read_json(FILES["universal_publisher"], {})
incoming = read_json(FILES["incoming_orders"], [])
queue = read_json(FILES["supplier_queue"], [])
ledger = read_json(FILES["order_ledger"], {"orders": {}})

checks = []

def add_check(name, ok, status, details=None):
    checks.append({
        "name": name,
        "ok": bool(ok),
        "status": status,
        "details": details or {}
    })

orders = ledger.get("orders", {}) if isinstance(ledger, dict) else {}

order_stage_reports = []

for key, order in orders.items():
    stages = {
        stage: stage_done(order, stage)
        for stage in REQUIRED_ORDER_STAGES
    }

    complete = all(stages.values())

    order_stage_reports.append({
        "key": key,
        "order_id": order.get("order_id"),
        "sku": order.get("sku"),
        "channel": order.get("channel"),
        "complete": complete,
        "stages": stages,
        "missing_stages": [s for s, done in stages.items() if not done]
    })

complete_orders = [x for x in order_stage_reports if x["complete"]]
incomplete_orders = [x for x in order_stage_reports if not x["complete"]]

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
    "supplier_queue",
    isinstance(queue, list),
    "ready",
    {"queue_size": len(queue)}
)

add_check(
    "live_gate_configured",
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
    "fulfillment_runner",
    fulfillment_runner.get("status") == "AUTONOMOUS_FULFILLMENT_RUN_COMPLETED",
    fulfillment_runner.get("status", "missing"),
    {
        "errors": len(fulfillment_runner.get("errors", [])) if isinstance(fulfillment_runner, dict) else None
    }
)

add_check(
    "commerce_runner",
    commerce_runner.get("status") == "AUTONOMOUS_COMMERCE_RUN_COMPLETED",
    commerce_runner.get("status", "missing"),
    {
        "errors": len(commerce_runner.get("errors", [])) if isinstance(commerce_runner, dict) else None
    }
)

add_check(
    "order_processing_ledger",
    isinstance(orders, dict),
    "ready",
    {
        "orders_in_ledger": len(orders),
        "complete_orders": len(complete_orders),
        "incomplete_orders": len(incomplete_orders)
    }
)

live_mode = bool(live_config.get("live_mode"))
cj_live = bool(live_config.get("cj_live_purchase_enabled"))
fulfillment_live = bool(live_config.get("shopify_fulfillment_live_enabled"))

blocking_items = [x for x in checks if not x["ok"]]

if live_mode and cj_live and fulfillment_live:
    mode_status = "FULL_LIVE_AUTONOMY_ENABLED"
elif live_mode or cj_live or fulfillment_live:
    mode_status = "PARTIAL_LIVE_AUTONOMY"
else:
    mode_status = "SAFE_AUTONOMY_DRY_RUN_GATED"

if complete_orders and not blocking_items:
    lifecycle_status = "FULL_ORDER_LIFECYCLE_VERIFIED"
elif orders:
    lifecycle_status = "ORDER_LIFECYCLE_PARTIALLY_VERIFIED"
else:
    lifecycle_status = "WAITING_FOR_FIRST_ORDER"

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "status": mode_status,
    "lifecycle_status": lifecycle_status,
    "autonomous_without_manual_steps": len(blocking_items) == 0,
    "live_mode": live_mode,
    "cj_live_purchase_enabled": cj_live,
    "shopify_fulfillment_live_enabled": fulfillment_live,
    "checks": checks,
    "blocking_items": blocking_items,
    "order_lifecycle": {
        "required_stages": REQUIRED_ORDER_STAGES,
        "orders": order_stage_reports,
        "complete_orders": len(complete_orders),
        "incomplete_orders": len(incomplete_orders)
    },
    "summary": {
        "incoming_orders": len(incoming),
        "supplier_queue": len(queue),
        "orders_in_ledger": len(orders),
        "complete_order_lifecycles": len(complete_orders),
        "live_gate_approved": live_report.get("approved_count", 0),
        "live_gate_blocked": live_report.get("blocked_count", 0)
    },
    "note": "System is autonomous by design. Real supplier spend remains controlled by autonomous_commerce_live_gate."
}

OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(report, indent=2, ensure_ascii=False))
