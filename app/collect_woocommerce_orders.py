import json
import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv(override=True)

OUT = Path("app/logs/woocommerce_orders.json")

store = (
    os.getenv("WOOCOMMERCE_URL")
    or os.getenv("WOOCOMMERCE_STORE_URL")
    or ""
).strip().rstrip("/")

key = (
    os.getenv("WOOCOMMERCE_KEY")
    or os.getenv("WOOCOMMERCE_CONSUMER_KEY")
    or ""
).strip()

secret = (
    os.getenv("WOOCOMMERCE_SECRET")
    or os.getenv("WOOCOMMERCE_CONSUMER_SECRET")
    or ""
).strip()

if not store or not key or not secret:
    print("WOOCOMMERCE ORDERS: missing config")
    OUT.write_text("[]", encoding="utf-8")
    raise SystemExit

r = requests.get(
    f"{store}/wp-json/wc/v3/orders",
    auth=(key, secret),
    params={
        "status": "processing",
        "per_page": 50
    },
    timeout=30
)

print("STATUS:", r.status_code)

if r.status_code not in [200, 201]:
    print(r.text[:1000])
    OUT.write_text("[]", encoding="utf-8")
    raise SystemExit

raw_orders = r.json()

orders = []

for o in raw_orders:
    shipping = o.get("shipping") or {}

    for item in o.get("line_items", []):
        sku = item.get("sku")

        if not sku:
            continue

        orders.append({
            "order_id": str(o.get("id")),
            "channel_order_name": o.get("number"),
            "channel": "woocommerce",
            "sku": sku,
            "quantity": int(item.get("quantity", 1) or 1),
            "paid": bool(o.get("date_paid")),
            "sale_price": float(item.get("total", 0) or 0),
            "shipping_address": {
                "name": (shipping.get("first_name","") + " " + shipping.get("last_name","")).strip(),
                "address1": shipping.get("address_1"),
                "address2": shipping.get("address_2"),
                "city": shipping.get("city"),
                "postal_code": shipping.get("postcode"),
                "country": shipping.get("country"),
                "phone": shipping.get("phone")
            },
            "raw": {
                "order_id": o.get("id"),
                "number": o.get("number"),
                "status": o.get("status"),
                "date_created": o.get("date_created"),
                "line_item_id": item.get("id")
            },
            "collected_at": datetime.now(timezone.utc).isoformat()
        })

OUT.write_text(
    json.dumps(orders, indent=2),
    encoding="utf-8"
)

print("WOOCOMMERCE ORDERS:", len(orders))
print("REPORT:", OUT)
