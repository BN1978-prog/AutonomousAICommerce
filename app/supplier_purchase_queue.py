import json
from pathlib import Path
from datetime import datetime, timezone

ORDERS = Path("app/logs/incoming_orders.json")
IMPORTS = Path("app/logs/imported_skus.json")
QUEUE = Path("app/logs/supplier_purchase_queue.json")

from app.fulfillment_guard import check_fulfillment_allowed

orders = json.loads(ORDERS.read_text(encoding="utf-8")) if ORDERS.exists() else []
imports = json.loads(IMPORTS.read_text(encoding="utf-8")) if IMPORTS.exists() else {}

queue = []

for order in orders:
    sku = order.get("sku")
    product = imports.get(sku, {})

    guard = check_fulfillment_allowed(order, product)

    if not guard.get("allowed"):
        continue

    queue.append({
        "order_id": order.get("order_id"),
        "channel": order.get("channel"),
        "sku": sku,
        "quantity": int(order.get("quantity", 1) or 1),
        "supplier": product.get("supplier") or "cj",
        "shipping_address": order.get("shipping_address"),
        "estimated_profit": guard.get("estimated_profit"),
        "status": "ready_for_supplier_purchase",
        "created_at": datetime.now(timezone.utc).isoformat()
    })

QUEUE.write_text(
    json.dumps(queue, indent=2),
    encoding="utf-8"
)

print("SUPPLIER PURCHASE QUEUE:", len(queue))
print("REPORT:", QUEUE)
