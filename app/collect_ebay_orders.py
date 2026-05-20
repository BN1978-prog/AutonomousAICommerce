import json
import requests
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv(override=True)

from app.channels.ebay_gateway import ebay_headers, ebay_config

OUT = Path("app/logs/ebay_orders.json")

try:
    h = ebay_headers()
    cfg = ebay_config()

    print("EBAY ORDERS REQUEST START")

    r = requests.get(
        cfg["api_base"] + "/sell/fulfillment/v1/order",
        headers=h["headers"],
        params={"limit": 20},
        timeout=(5, 15)
    )

    print("STATUS:", r.status_code)

    if r.status_code not in [200, 201]:
        print(r.text[:1000])
        OUT.write_text("[]", encoding="utf-8")
        raise SystemExit

    data = r.json()
    raw_orders = data.get("orders", [])

    orders = []

    for o in raw_orders:
        for item in o.get("lineItems", []):
            sku = item.get("sku")
            if not sku:
                continue

            orders.append({
                "order_id": str(o.get("orderId")),
                "channel": "ebay",
                "sku": sku,
                "quantity": int(item.get("quantity", 1) or 1),
                "paid": o.get("orderPaymentStatus") == "PAID",
                "sale_price": float(item.get("lineItemCost", {}).get("value", 0) or 0),
                "shipping_address": {},
                "raw": {
                    "order_id": o.get("orderId"),
                    "order_status": o.get("orderStatus"),
                    "payment_status": o.get("orderPaymentStatus")
                },
                "collected_at": datetime.now(timezone.utc).isoformat()
            })

    OUT.write_text(json.dumps(orders, indent=2), encoding="utf-8")

    print("EBAY ORDERS:", len(orders))
    print("REPORT:", OUT)

except requests.exceptions.Timeout:
    print("EBAY ORDERS TIMEOUT")
    OUT.write_text("[]", encoding="utf-8")

except Exception as e:
    print("EBAY ORDERS ERROR:", str(e))
    OUT.write_text("[]", encoding="utf-8")
