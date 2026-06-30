
import json
from pathlib import Path
from datetime import datetime, timezone

DRAFTS = Path("app/logs/cj_order_drafts.json")
OUT = Path("app/logs/cj_order_payloads.json")
REPORT = Path("app/logs/cj_payload_builder.json")

drafts = json.loads(DRAFTS.read_text(encoding="utf-8-sig")) if DRAFTS.exists() else []

def normalize_shopify_address(addr):
    addr = addr or {}

    first = addr.get("firstName") or addr.get("first_name") or ""
    last = addr.get("lastName") or addr.get("last_name") or ""
    phone = addr.get("phone") or addr.get("telephone") or "0000000000"

    return {
        "firstName": first,
        "lastName": last,
        "address1": addr.get("address1") or addr.get("address_1") or "",
        "address2": addr.get("address2") or addr.get("address_2") or "",
        "city": addr.get("city") or "",
        "province": addr.get("province") or addr.get("province_code") or addr.get("state") or "",
        "countryCode": addr.get("countryCode") or addr.get("country_code") or addr.get("country") or "",
        "zip": addr.get("zip") or addr.get("postal_code") or "",
        "phone": phone
    }

payloads = []
skipped = []

for d in drafts:
    if d.get("status") != "draft_ready_for_payload_builder":
        skipped.append({
            "sku": d.get("sku"),
            "order_id": d.get("order_id"),
            "reason": "draft_not_ready"
        })
        continue

    if not d.get("cj_variant_id"):
        skipped.append({
            "sku": d.get("sku"),
            "order_id": d.get("order_id"),
            "reason": "missing_cj_variant_id"
        })
        continue

    address = normalize_shopify_address(d.get("shipping_address"))

    payload = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "supplier": "cjdropshipping",
        "endpoint": "createOrderV3",
        "mode": "payload_only_no_api_call",
        "payType": 3,

        "order_id": d.get("order_id"),
        "channel_order_name": d.get("channel_order_name"),
        "channel": d.get("channel"),
        "sku": d.get("sku"),

        "products": [
            {
                "vid": d.get("cj_variant_id"),
                "quantity": int(d.get("quantity", 1) or 1)
            }
        ],

        "shipping_address": address,

        "financials": {
            "sale_price": d.get("sale_price"),
            "supplier_cost": d.get("supplier_cost"),
            "shipping_cost": d.get("shipping_cost"),
            "estimated_profit": d.get("estimated_profit"),
            "margin_percent": d.get("margin_percent")
        },

        "status": "payload_ready_for_address_validation"
    }

    payloads.append(payload)

OUT.write_text(json.dumps(payloads, indent=2, ensure_ascii=False), encoding="utf-8")

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "drafts_seen": len(drafts),
    "payloads_created": len(payloads),
    "skipped": skipped,
    "status": "payloads_created" if payloads else "waiting_valid_drafts",
    "output_file": str(OUT)
}

REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(report, indent=2, ensure_ascii=False))
