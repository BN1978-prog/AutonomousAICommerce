import json
from pathlib import Path
from datetime import datetime, timezone

SOURCES = [
    ("shopify", Path("app/logs/shopify_orders.json")),
    ("ebay", Path("app/logs/ebay_orders.json")),
    ("woocommerce", Path("app/logs/woocommerce_orders.json")),
]

OUT = Path("app/logs/incoming_orders.json")

orders = []

for channel, path in SOURCES:
    if not path.exists():
        continue

    data = json.loads(path.read_text(encoding="utf-8"))

    if isinstance(data, dict):
        data = data.get("orders", [])

    for o in data:
        sku = o.get("sku")
        if not sku and o.get("line_items"):
            sku = o["line_items"][0].get("sku")

        if not sku:
            continue

        orders.append({
            "order_id": str(o.get("order_id") or o.get("id")),
            "channel": channel,
            "sku": sku,
            "quantity": int(o.get("quantity", 1) or 1),
            "paid": bool(o.get("paid", False) or o.get("financial_status") == "paid"),
            "sale_price": float(o.get("sale_price", 0) or o.get("total_price", 0) or 0),
            "shipping_address": o.get("shipping_address") or {},
            "raw": o,
            "collected_at": datetime.now(timezone.utc).isoformat()
        })

OUT.write_text(
    json.dumps(orders, indent=2),
    encoding="utf-8"
)

print("INCOMING ORDERS:", len(orders))
print("REPORT:", OUT)
