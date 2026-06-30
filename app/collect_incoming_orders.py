
import json
from pathlib import Path
from datetime import datetime, timezone

SOURCES = [
    ("shopify", Path("app/logs/shopify_orders.json")),
    ("woocommerce", Path("app/logs/woocommerce_orders.json")),
    ("ebay", Path("app/logs/ebay_orders.json")),
    ("etsy", Path("app/logs/etsy_orders.json")),
]

OUT = Path("app/logs/incoming_orders.json")
REPORT = Path("app/logs/collect_incoming_orders.json")

orders = []
seen = set()

for channel, path in SOURCES:
    if not path.exists():
        continue

    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        data = []

    if isinstance(data, dict):
        data = data.get("orders", [])

    for order in data:
        if not isinstance(order, dict):
            continue

        if not order.get("paid"):
            continue

        sku = order.get("sku")
        order_id = str(order.get("order_id") or order.get("id") or "")
        key = f"{channel}:{order_id}:{sku}"

        if not sku or not order_id or key in seen:
            continue

        seen.add(key)

        orders.append({
            "order_id": order_id,
            "channel_order_name": order.get("channel_order_name") or order.get("name"),
            "channel": order.get("channel") or channel,
            "sku": sku,
            "quantity": int(order.get("quantity", 1) or 1),
            "paid": True,
            "sale_price": float(order.get("sale_price", 0) or 0),
            "shipping_address": order.get("shipping_address") or {},
            "raw": order.get("raw", {}),
            "collected_at": order.get("collected_at") or datetime.now(timezone.utc).isoformat(),
            "incoming_collected_at": datetime.now(timezone.utc).isoformat()
        })

OUT.write_text(json.dumps(orders, indent=2, ensure_ascii=False), encoding="utf-8")

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "status": "INCOMING_ORDERS_COLLECTED",
    "orders": len(orders),
    "sources": [str(p) for _, p in SOURCES],
    "output": str(OUT)
}

REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
