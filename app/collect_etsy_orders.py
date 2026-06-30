import json
import os
import requests
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv(override=True)

OUT = Path("app/logs/etsy_orders.json")

api_base = os.getenv("ETSY_API_BASE", "https://openapi.etsy.com/v3/application").rstrip("/")
api_key = os.getenv("ETSY_API_KEY") or os.getenv("ETSY_CLIENT_ID")
token = os.getenv("ETSY_ACCESS_TOKEN")
shop_id = os.getenv("ETSY_SHOP_ID")

if not api_key or not token or not shop_id:
    print("ETSY ORDERS: missing config")
    OUT.write_text("[]", encoding="utf-8")
    raise SystemExit

headers = {
    "x-api-key": api_key,
    "Authorization": "Bearer " + token
}

url = f"{api_base}/shops/{shop_id}/receipts"

r = requests.get(
    url,
    headers=headers,
    params={
        "limit": 50,
        "was_paid": "true",
        "was_shipped": "false"
    },
    timeout=30
)

print("STATUS:", r.status_code)

if r.status_code not in [200, 201]:
    print(r.text[:1000])
    OUT.write_text("[]", encoding="utf-8")
    raise SystemExit

data = r.json()
receipts = data.get("results", []) if isinstance(data, dict) else []

orders = []

for receipt in receipts:
    receipt_id = receipt.get("receipt_id")

    txs = receipt.get("transactions") or []
    for item in txs:
        sku = item.get("sku") or item.get("product_data", {}).get("sku")

        if not sku:
            continue

        price_data = item.get("price") or {}
        amount = price_data.get("amount", 0)
        divisor = price_data.get("divisor", 100)
        sale_price = float(amount or 0) / float(divisor or 100)

        orders.append({
            "order_id": str(receipt_id),
            "channel_order_name": str(receipt_id),
            "channel": "etsy",
            "sku": sku,
            "quantity": int(item.get("quantity", 1) or 1),
            "paid": bool(receipt.get("was_paid")),
            "sale_price": sale_price,
            "shipping_address": {
                "name": receipt.get("name"),
                "address1": receipt.get("first_line"),
                "address2": receipt.get("second_line"),
                "city": receipt.get("city"),
                "province": receipt.get("state"),
                "zip": receipt.get("zip"),
                "country_code": receipt.get("country_iso"),
            },
            "raw": {
                "receipt_id": receipt_id,
                "transaction_id": item.get("transaction_id"),
                "was_paid": receipt.get("was_paid"),
                "was_shipped": receipt.get("was_shipped")
            },
            "collected_at": datetime.now(timezone.utc).isoformat()
        })

OUT.write_text(json.dumps(orders, indent=2, ensure_ascii=False), encoding="utf-8")

print("ETSY ORDERS:", len(orders))
print("REPORT:", OUT)
