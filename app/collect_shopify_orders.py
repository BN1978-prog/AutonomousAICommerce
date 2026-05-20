import json
import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv(override=True)

OUT = Path("app/logs/shopify_orders.json")

store = (
    os.getenv("SHOPIFY_STORE_URL") or ""
).strip().replace("https://","").replace("http://","").rstrip("/")

token = (
    os.getenv("SHOPIFY_ADMIN_TOKEN")
    or os.getenv("SHOPIFY_ACCESS_TOKEN")
    or ""
).strip()

api_version = os.getenv("SHOPIFY_API_VERSION", "2024-01")

if not store or not token:
    print("SHOPIFY ORDERS: missing config")
    OUT.write_text("[]", encoding="utf-8")
    raise SystemExit

r = requests.get(
    f"https://{store}/admin/api/{api_version}/orders.json",
    headers={
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json"
    },
    params={
        "status": "open",
        "financial_status": "paid",
        "limit": 50
    },
    timeout=30
)

print("STATUS:", r.status_code)

if r.status_code != 200:
    print(r.text[:1000])
    OUT.write_text("[]", encoding="utf-8")
    raise SystemExit

raw_orders = r.json().get("orders", [])

orders = []

for o in raw_orders:
    shipping = o.get("shipping_address") or {}

    for item in o.get("line_items", []):
        sku = item.get("sku")

        if not sku:
            continue

        orders.append({
            "order_id": str(o.get("id")),
            "channel_order_name": o.get("name"),
            "channel": "shopify",
            "sku": sku,
            "quantity": int(item.get("quantity", 1) or 1),
            "paid": o.get("financial_status") == "paid",
            "sale_price": float(item.get("price", 0) or 0),
            "shipping_address": shipping,
            "raw": {
                "order_id": o.get("id"),
                "name": o.get("name"),
                "created_at": o.get("created_at"),
                "line_item_id": item.get("id"),
                "fulfillment_status": o.get("fulfillment_status")
            },
            "collected_at": datetime.now(timezone.utc).isoformat()
        })

OUT.write_text(
    json.dumps(orders, indent=2),
    encoding="utf-8"
)

print("SHOPIFY ORDERS:", len(orders))
print("REPORT:", OUT)
