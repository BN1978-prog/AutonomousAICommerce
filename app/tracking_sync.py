
import json
from pathlib import Path
from datetime import datetime, timezone
from app.order_processing_ledger import is_stage_done, mark_stage, load_ledger

ATTEMPTS = Path("app/logs/cj_purchase_attempts.json")
TRACKING = Path("app/logs/tracking_updates.json")
REPORT = Path("app/logs/tracking_sync_report.json")

attempts = json.loads(ATTEMPTS.read_text(encoding="utf-8-sig")) if ATTEMPTS.exists() else []
ledger = load_ledger()

for order_key, order in ledger.get("orders", {}).items():
    stage = order.get("stages", {}).get("cj_purchase_attempted", {})
    data = stage.get("data")

    if not data:
        continue

    # Ledger has the durable canonical purchase attempt.
    # If current attempts file only contains a later "skipped already" row,
    # still restore the real prepared_not_purchased attempt from ledger.
    existing_ready = any(
        isinstance(x, dict)
        and x.get("order_id") == data.get("order_id")
        and x.get("sku") == data.get("sku")
        and x.get("status") in ["prepared_not_purchased", "live_cj_api_call_not_implemented_yet"]
        for x in attempts
    )

    if not existing_ready:
        attempts.append(data)

existing = json.loads(TRACKING.read_text(encoding="utf-8-sig")) if TRACKING.exists() else []

updates = list(existing) if isinstance(existing, list) else []
created = []
skipped = []

existing_keys = {
    f"{x.get('order_id')}:{x.get('sku')}"
    for x in updates
    if isinstance(x, dict)
}

for item in attempts:
    payload = item.get("payload", {})
    order_id = item.get("order_id") or payload.get("orderNumber")
    sku = item.get("sku") or payload.get("sku")
    channel = item.get("channel") or "shopify"
    key = f"{order_id}:{sku}"

    if item.get("status") not in ["prepared_not_purchased", "live_cj_api_call_not_implemented_yet"]:
        skipped.append({
            "order_id": order_id,
            "sku": sku,
            "reason": "purchase_not_ready_for_tracking",
            "status": item.get("status")
        })
        continue

    if key in existing_keys:
        skipped.append({
            "order_id": order_id,
            "sku": sku,
            "reason": "already_exists_in_tracking_updates"
        })
        continue

    if is_stage_done(order_id, sku, channel, "tracking_watch_created"):
        skipped.append({
            "order_id": order_id,
            "sku": sku,
            "reason": "already_tracking_watch_in_ledger"
        })
        continue

    row = {
        "order_id": order_id,
        "sku": sku,
        "channel": channel,
        "supplier": "cj",
        "tracking_number": item.get("tracking_number"),
        "carrier": item.get("carrier"),
        "status": "waiting_for_supplier_tracking",
        "channel_update_status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    updates.append(row)
    created.append(row)
    mark_stage(order_id, sku, channel, "tracking_watch_created", row)

TRACKING.write_text(json.dumps(updates, indent=2, ensure_ascii=False), encoding="utf-8")

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "status": "TRACKING_SYNC_CHECKED",
    "attempts_seen": len(attempts),
    "ledger_orders_seen": len(ledger.get("orders", {})),
    "existing_tracking": len(existing) if isinstance(existing, list) else 0,
    "created": len(created),
    "total_tracking": len(updates),
    "skipped": skipped,
    "output": str(TRACKING)
}

REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

print("TRACKING WATCH ITEMS:", len(updates))
print(json.dumps(report, indent=2, ensure_ascii=False))
