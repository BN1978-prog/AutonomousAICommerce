import json
import os
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv(override=True)

QUEUE = Path("app/logs/supplier_purchase_queue.json")
OUT = Path("app/logs/cj_purchase_attempts.json")

DRY_RUN = os.getenv(
    "CJ_PURCHASE_DRY_RUN",
    "true"
).lower() == "true"

queue = []

if QUEUE.exists():
    queue = json.loads(
        QUEUE.read_text(encoding="utf-8")
    )

attempts = []

for item in queue:

    payload = {
        "supplier": "cj",
        "order_id": item.get("order_id"),
        "sku": item.get("sku"),
        "quantity": int(item.get("quantity",1)),
        "shipping_address": item.get("shipping_address"),
        "requested_at": datetime.now(
            timezone.utc
        ).isoformat()
    }

    if DRY_RUN:

        attempts.append({
            "ok": True,
            "dry_run": True,
            "status": "prepared_not_purchased",
            "payload": payload
        })

    else:

        attempts.append({
            "ok": False,
            "dry_run": False,
            "status": "live_purchase_not_enabled_yet",
            "payload": payload
        })

OUT.write_text(
    json.dumps(
        attempts,
        indent=2
    ),
    encoding="utf-8"
)

print("CJ PURCHASE ATTEMPTS:",len(attempts))
print("DRY_RUN:",DRY_RUN)
print("REPORT:",OUT)
