
import json
import os
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv(override=True)

PAYLOADS = Path("app/logs/cj_order_payloads.json")
VALIDATION = Path("app/logs/cj_customer_address_validator.json")
OUT = Path("app/logs/cj_purchase_attempts.json")

DRY_RUN = os.getenv("CJ_PURCHASE_DRY_RUN", "true").lower() == "true"

payloads = json.loads(PAYLOADS.read_text(encoding="utf-8-sig")) if PAYLOADS.exists() else []
validation = json.loads(VALIDATION.read_text(encoding="utf-8-sig")) if VALIDATION.exists() else {}

ready_ids = {
    x.get("order_id")
    for x in validation.get("ready", [])
    if x.get("status") == "ready_for_cj_create_order"
}

attempts = []

for payload in payloads:
    order_id = payload.get("order_id")

    if order_id not in ready_ids:
        attempts.append({
            "ok": False,
            "dry_run": DRY_RUN,
            "status": "blocked_not_address_validated",
            "order_id": order_id,
            "sku": payload.get("sku")
        })
        continue

    cj_payload = {
        "payType": payload.get("payType", 3),
        "products": payload.get("products", []),
        "shippingAddress": payload.get("shipping_address", {}),
        "orderNumber": str(order_id),
        "remark": f"AICommerce {payload.get('channel')} {payload.get('channel_order_name') or ''}".strip()
    }

    if DRY_RUN:
        attempts.append({
            "ok": True,
            "dry_run": True,
            "status": "prepared_not_purchased",
            "supplier": "cj",
            "order_id": order_id,
            "sku": payload.get("sku"),
            "payload": cj_payload,
            "financials": payload.get("financials", {}),
            "prepared_at": datetime.now(timezone.utc).isoformat()
        })
    else:
        attempts.append({
            "ok": False,
            "dry_run": False,
            "status": "live_purchase_not_enabled_yet",
            "supplier": "cj",
            "order_id": order_id,
            "sku": payload.get("sku"),
            "payload": cj_payload,
            "financials": payload.get("financials", {}),
            "prepared_at": datetime.now(timezone.utc).isoformat()
        })

OUT.write_text(json.dumps(attempts, indent=2, ensure_ascii=False), encoding="utf-8")

print("CJ PURCHASE ATTEMPTS:", len(attempts))
print("DRY_RUN:", DRY_RUN)
print("REPORT:", OUT)
