from dotenv import load_dotenv
load_dotenv(override=True)

import json, requests
from pathlib import Path
from app.channels.shopify_config import ShopifyConfig

store = ShopifyConfig.get_store().replace("https://","").replace("http://","").rstrip("/")
token = ShopifyConfig.get_token()

headers = {"X-Shopify-Access-Token": token}

imports_path = Path("app/logs/imported_skus.json")
imports = json.loads(imports_path.read_text(encoding="utf-8"))

url = f"https://{store}/admin/api/2024-01/orders.json?status=any&limit=250"
r = requests.get(url, headers=headers, timeout=30)

print("STATUS:", r.status_code)

if r.status_code != 200:
    print(r.text[:1000])
    raise SystemExit

orders = r.json().get("orders", [])
print("ORDERS:", len(orders))

for meta in imports.values():
    meta["shopify_sales"] = 0
    meta["sales"] = int(meta.get("ebay_sales") or 0)

for order in orders:
    for item in order.get("line_items", []):
        sku = item.get("sku")
        qty = int(item.get("quantity") or 0)

        if sku in imports:
            imports[sku]["shopify_sales"] = imports[sku].get("shopify_sales", 0) + qty
            imports[sku]["sales"] = imports[sku].get("sales", 0) + qty

imports_path.write_text(json.dumps(imports, indent=2), encoding="utf-8")

print("SHOPIFY SALES SYNCED")
