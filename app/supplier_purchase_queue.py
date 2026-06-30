
import json
from pathlib import Path
from datetime import datetime, timezone

ORDERS = Path("app/logs/incoming_orders.json")
IMPORTS = Path("app/logs/imported_skus.json")
QUEUE = Path("app/logs/supplier_purchase_queue.json")
REPORT = Path("app/logs/supplier_purchase_queue_report.json")

from app.fulfillment_guard import check_fulfillment_allowed
from app.order_processing_ledger import is_stage_done, mark_stage

def to_float(v, default=0.0):
    try:
        return float(v or default)
    except Exception:
        return default

orders = json.loads(ORDERS.read_text(encoding="utf-8-sig")) if ORDERS.exists() else []
imports = json.loads(IMPORTS.read_text(encoding="utf-8-sig")) if IMPORTS.exists() else {}

queue = []
skipped = []

for order in orders:
    sku = order.get("sku")
    order_id = order.get("order_id")
    channel = order.get("channel")
    product = imports.get(sku, {})

    if is_stage_done(order_id, sku, channel, "supplier_queue_created"):
        skipped.append({
            "order_id": order_id,
            "sku": sku,
            "reason": "already_queued_in_ledger"
        })
        continue

    if not product:
        skipped.append({
            "order_id": order_id,
            "sku": sku,
            "reason": "sku_not_found_in_imported_skus"
        })
        continue

    guard = check_fulfillment_allowed(order, product)

    if not guard.get("allowed"):
        skipped.append({
            "order_id": order_id,
            "sku": sku,
            "reason": guard.get("reason") or "fulfillment_guard_blocked",
            "guard": guard
        })
        continue

    sale_price = to_float(order.get("sale_price"))
    supplier_cost = to_float(product.get("supplier_cost"))
    shipping_cost = to_float(product.get("shipping_cost"))
    estimated_profit = round(sale_price - supplier_cost - shipping_cost, 2)
    margin_percent = round((estimated_profit / sale_price) * 100, 2) if sale_price else 0

    row = {
        "order_id": order_id,
        "channel_order_name": order.get("channel_order_name"),
        "channel": channel,
        "sku": sku,
        "quantity": int(order.get("quantity", 1) or 1),

        "supplier": product.get("supplier") or "cj",
        "cj_product_id": product.get("cj_product_id"),
        "cj_variant_id": product.get("cj_variant_id"),
        "supplier_product_id": product.get("supplier_product_id") or product.get("cj_product_id"),
        "supplier_variant_id": product.get("supplier_variant_id") or product.get("cj_variant_id"),

        "sale_price": sale_price,
        "supplier_cost": supplier_cost,
        "shipping_cost": shipping_cost,
        "estimated_profit": estimated_profit,
        "margin_percent": margin_percent,

        "shipping_address": order.get("shipping_address"),
        "status": "ready_for_supplier_purchase",
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    queue.append(row)
    mark_stage(order_id, sku, channel, "supplier_queue_created", row)

QUEUE.write_text(json.dumps(queue, indent=2, ensure_ascii=False), encoding="utf-8")

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "status": "SUPPLIER_PURCHASE_QUEUE_BUILT",
    "orders_seen": len(orders),
    "queued": len(queue),
    "skipped": skipped,
    "output": str(QUEUE)
}

REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

print("SUPPLIER PURCHASE QUEUE:", len(queue))
print(json.dumps(report, indent=2, ensure_ascii=False))
