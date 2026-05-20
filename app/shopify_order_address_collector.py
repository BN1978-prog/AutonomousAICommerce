import json, os, requests
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

OUT = Path("app/logs/shopify_order_address_collector.json")
ORDERS_OUT = Path("app/logs/shopify_order_addresses.json")

shop = (
    os.getenv("SHOPIFY_STORE_URL","")
    .replace("https://","")
    .replace("http://","")
    .strip("/")
)

token = (
    os.getenv("SHOPIFY_ADMIN_TOKEN")
    or os.getenv("SHOPIFY_ACCESS_TOKEN")
    or ""
).strip()

api_version = os.getenv("SHOPIFY_API_VERSION","2025-01").strip() or "2025-01"

result = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "ok": False,
    "shop": shop,
    "orders_seen": 0,
    "addresses_collected": 0,
    "orders": [],
    "status": "not_run"
}

try:
    if not shop or not token:
        result["status"] = "missing_shopify_env"
    else:
        url = f"https://{shop}/admin/api/{api_version}/orders.json"
        params = {
            "status": "open",
            "financial_status": "paid",
            "limit": 50
        }
        headers = {
            "X-Shopify-Access-Token": token,
            "Content-Type": "application/json"
        }

        r = requests.get(url, headers=headers, params=params, timeout=30)
        result["status_code"] = r.status_code

        if r.status_code != 200:
            result["status"] = "shopify_api_error"
            result["response"] = r.text[:2000]
        else:
            data = r.json()
            orders = data.get("orders", [])
            result["orders_seen"] = len(orders)

            collected = []

            for o in orders:
                shipping = o.get("shipping_address") or {}
                line_items = o.get("line_items") or []

                skus = []
                for li in line_items:
                    sku = li.get("sku")
                    if sku:
                        skus.append({
                            "sku": sku,
                            "quantity": li.get("quantity", 1),
                            "title": li.get("title")
                        })

                address = {
                    "order_id": str(o.get("id")),
                    "order_name": o.get("name"),
                    "email": o.get("email"),
                    "financial_status": o.get("financial_status"),
                    "fulfillment_status": o.get("fulfillment_status"),
                    "currency": o.get("currency"),
                    "total_price": o.get("total_price"),
                    "skus": skus,
                    "shipping_address": {
                        "firstName": shipping.get("first_name"),
                        "lastName": shipping.get("last_name"),
                        "address1": shipping.get("address1"),
                        "address2": shipping.get("address2"),
                        "city": shipping.get("city"),
                        "province": shipping.get("province"),
                        "countryCode": shipping.get("country_code"),
                        "zip": shipping.get("zip"),
                        "phone": shipping.get("phone") or o.get("phone") or "0000000000"
                    }
                }

                collected.append(address)

            ORDERS_OUT.write_text(
                json.dumps(collected, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )

            result["ok"] = True
            result["addresses_collected"] = len(collected)
            result["orders"] = collected
            result["status"] = "addresses_collected" if collected else "no_paid_open_orders"

except Exception as e:
    result["status"] = "exception"
    result["error"] = str(e)

OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(result, indent=2, ensure_ascii=False))
