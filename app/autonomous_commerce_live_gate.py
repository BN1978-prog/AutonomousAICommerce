
import json
from pathlib import Path
from datetime import datetime, timezone

CONFIG = Path("app/logs/autonomous_commerce_live_gate.json")
QUEUE = Path("app/logs/supplier_purchase_queue.json")
OUT = Path("app/logs/autonomous_commerce_live_gate_report.json")

default_config = {
    "live_mode": False,
    "cj_live_purchase_enabled": False,
    "shopify_fulfillment_live_enabled": False,
    "max_supplier_cost_per_order": 50,
    "max_daily_supplier_spend": 100,
    "min_margin_percent": 25,
    "allowed_channels": ["shopify"],
    "require_paid_order": True,
    "require_tracking_for_fulfillment": True
}

config = json.loads(CONFIG.read_text(encoding="utf-8-sig")) if CONFIG.exists() else default_config
queue = json.loads(QUEUE.read_text(encoding="utf-8-sig")) if QUEUE.exists() else []

approved = []
blocked = []
daily_spend = 0.0

for item in queue:
    supplier_cost = float(item.get("supplier_cost") or 0)
    margin = float(item.get("margin_percent") or 0)
    channel = item.get("channel")

    reasons = []

    if not config.get("live_mode"):
        reasons.append("global_live_mode_disabled")

    if not config.get("cj_live_purchase_enabled"):
        reasons.append("cj_live_purchase_disabled")

    if channel not in config.get("allowed_channels", []):
        reasons.append("channel_not_allowed")

    if supplier_cost <= 0:
        reasons.append("missing_supplier_cost")

    if supplier_cost > float(config.get("max_supplier_cost_per_order", 0)):
        reasons.append("supplier_cost_above_limit")

    if margin < float(config.get("min_margin_percent", 0)):
        reasons.append("margin_below_limit")

    if daily_spend + supplier_cost > float(config.get("max_daily_supplier_spend", 0)):
        reasons.append("daily_supplier_spend_limit_reached")

    if reasons:
        blocked.append({
            "order_id": item.get("order_id"),
            "sku": item.get("sku"),
            "supplier_cost": supplier_cost,
            "margin_percent": margin,
            "reasons": reasons
        })
        continue

    daily_spend += supplier_cost
    approved.append({
        "order_id": item.get("order_id"),
        "sku": item.get("sku"),
        "supplier_cost": supplier_cost,
        "margin_percent": margin,
        "status": "approved_for_live_cj_purchase"
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "status": "LIVE_GATE_CHECKED",
    "config": config,
    "queue_seen": len(queue),
    "approved": approved,
    "blocked": blocked,
    "approved_count": len(approved),
    "blocked_count": len(blocked),
    "approved_daily_spend": round(daily_spend, 2)
}

OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(report, indent=2, ensure_ascii=False))
