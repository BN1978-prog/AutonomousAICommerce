
import json
from pathlib import Path
from datetime import datetime, timezone

QUEUE = Path("app/logs/supplier_purchase_queue.json")
OUT = Path("app/logs/cj_order_drafts.json")
REPORT = Path("app/logs/cj_order_draft_creator.json")

queue = json.loads(QUEUE.read_text(encoding="utf-8-sig")) if QUEUE.exists() else []

drafts = []
skipped = []

for item in queue:
    if item.get("status") not in ["queued_for_supplier_purchase", "ready_for_supplier_purchase"]:
        skipped.append({
            "order_id": item.get("order_id"),
            "sku": item.get("sku"),
            "reason": "not_ready_for_supplier_purchase"
        })
        continue

    if not item.get("cj_product_id") or not item.get("cj_variant_id"):
        skipped.append({
            "order_id": item.get("order_id"),
            "sku": item.get("sku"),
            "reason": "missing_cj_product_or_variant"
        })
        continue

    if not item.get("shipping_address"):
        skipped.append({
            "order_id": item.get("order_id"),
            "sku": item.get("sku"),
            "reason": "missing_shipping_address"
        })
        continue

    draft = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "supplier": "cjdropshipping",
        "mode": "draft_only_no_api_call",
        "payType": 3,

        "order_id": item.get("order_id"),
        "channel_order_name": item.get("channel_order_name"),
        "channel": item.get("channel"),

        "sku": item.get("sku"),
        "quantity": int(item.get("quantity", 1) or 1),

        "cj_product_id": item.get("cj_product_id"),
        "cj_variant_id": item.get("cj_variant_id"),
        "supplier_product_id": item.get("supplier_product_id"),
        "supplier_variant_id": item.get("supplier_variant_id"),

        "sale_price": item.get("sale_price"),
        "supplier_cost": item.get("supplier_cost"),
        "shipping_cost": item.get("shipping_cost"),
        "estimated_profit": item.get("estimated_profit"),
        "margin_percent": item.get("margin_percent"),

        "shipping_address": item.get("shipping_address"),

        "status": "draft_ready_for_payload_builder"
    }

    drafts.append(draft)

OUT.write_text(json.dumps(drafts, indent=2, ensure_ascii=False), encoding="utf-8")

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "queue_size": len(queue),
    "drafts_created": len(drafts),
    "skipped": skipped,
    "status": "idle_no_queue" if not queue else "drafts_created",
    "output_file": str(OUT)
}

REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(report, indent=2, ensure_ascii=False))
