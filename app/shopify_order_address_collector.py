import json
import os
import requests
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv(override=True)

OUT = Path("app/logs/shopify_order_address_collector.json")
ORDERS_OUT = Path("app/logs/shopify_order_addresses.json")

shop = (
    os.getenv("SHOPIFY_SHOP_DOMAIN")
    or os.getenv("SHOPIFY_STORE_URL")
    or os.getenv("SHOPIFY_DOMAIN")
    or "aicommerce-test-store-2.myshopify.com"
).strip()

if shop.startswith("https://"):
    shop = shop.replace("https://", "").strip("/")

if shop.startswith("http://"):
    shop = shop.replace("http://", "").strip("/")

if not shop.endswith(".myshopify.com"):
    shop = shop + ".myshopify.com"

token = (
    os.getenv("SHOPIFY_ACCESS_TOKEN")
    or os.getenv("SHOPIFY_ADMIN_TOKEN")
    or os.getenv("SHOPIFY_ADMIN_API_TOKEN")
)

api_version = os.getenv("SHOPIFY_API_VERSION", "2025-01").strip() or "2025-01"

result = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "ok": False,
    "shop": shop,
    "orders_seen": 0,
    "addresses_collected": 0,
    "orders": [],
    "status": None
}

try:
    if not shop or not token:
        result["status"] = "missing_shopify_env"
    else:
        url = f"https://{shop}/admin/api/{api_version}/orders.json"

        r = requests.get(
            url,
            headers={
                "X-Shopify-Access-Token": token,
                "Content-Type": "application/json"
            },
            params={
                "status": "any",
                "limit": 50
            },
            timeout=30
        )

        result["status_code"] = r.status_code

        if r.status_code == 200:
            data = r.json()
            orders = data.get("orders", [])

            collected = []

            for order in orders:
                address = order.get("shipping_address") or order.get("billing_address")

                if address:
                    collected.append({
                        "order_id": order.get("id"),
                        "order_name": order.get("name"),
                        "email": order.get("email"),
                        "address": address
                    })

            result["ok"] = True
            result["orders_seen"] = len(orders)
            result["addresses_collected"] = len(collected)
            result["orders"] = collected
            result["status"] = "success"

            ORDERS_OUT.write_text(
                json.dumps(collected, indent=2),
                encoding="utf-8"
            )

        else:
            result["status"] = "shopify_api_error"
            result["response"] = r.text[:500]

except Exception as e:
    result["status"] = "exception"
    result["error"] = str(e)

OUT.write_text(
    json.dumps(result, indent=2),
    encoding="utf-8"
)

print(json.dumps(result, indent=2))
