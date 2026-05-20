import json
from pathlib import Path
from datetime import datetime, timezone

ATTEMPTS = Path("app/logs/cj_purchase_attempts.json")
TRACKING = Path("app/logs/tracking_updates.json")

attempts = json.loads(ATTEMPTS.read_text(encoding="utf-8")) if ATTEMPTS.exists() else []

updates = []

for item in attempts:
    payload = item.get("payload", {})

    if item.get("status") != "prepared_not_purchased":
        continue

    updates.append({
        "order_id": payload.get("order_id"),
        "sku": payload.get("sku"),
        "supplier": "cj",
        "tracking_number": None,
        "carrier": None,
        "status": "waiting_for_supplier_tracking",
        "channel_update_status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat()
    })

TRACKING.write_text(
    json.dumps(updates, indent=2),
    encoding="utf-8"
)

print("TRACKING WATCH ITEMS:", len(updates))
print("REPORT:", TRACKING)
