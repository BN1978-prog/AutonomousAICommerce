import json
from pathlib import Path
from datetime import datetime, timezone

TRACKING = Path("app/logs/tracking_updates.json")
OUT = Path("app/logs/tracking_push_results.json")

items = json.loads(TRACKING.read_text(encoding="utf-8")) if TRACKING.exists() else []

results = []

for item in items:

    if not item.get("tracking_number"):
        results.append({
            "order_id": item.get("order_id"),
            "sku": item.get("sku"),
            "ok": True,
            "skipped": True,
            "reason": "tracking_number_missing"
        })
        continue

    if item.get("channel_update_status") != "pending":
        results.append({
            "order_id": item.get("order_id"),
            "sku": item.get("sku"),
            "ok": True,
            "skipped": True,
            "reason": "already_processed_or_not_pending"
        })
        continue

    results.append({
        "order_id": item.get("order_id"),
        "sku": item.get("sku"),
        "ok": False,
        "skipped": False,
        "reason": "live_channel_tracking_push_not_enabled_yet",
        "tracking_number": item.get("tracking_number"),
        "carrier": item.get("carrier"),
        "attempted_at": datetime.now(timezone.utc).isoformat()
    })

OUT.write_text(
    json.dumps(results, indent=2),
    encoding="utf-8"
)

print("TRACKING PUSH RESULTS:", len(results))
for r in results:
    print(r.get("order_id"), r.get("reason"))
