import os
import requests

SHOP = os.getenv("SHOPIFY_STORE_URL") or os.getenv("SHOPIFY_SHOP_DOMAIN") or os.getenv("SHOPIFY_SHOP")
TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN") or os.getenv("SHOPIFY_ADMIN_TOKEN")
API_VERSION = os.getenv("SHOPIFY_API_VERSION", "2025-01")

BAD_KEYWORDS = [
    "Hair Growth",
    "High-borosilicate",
    "LIVE TEST PRODUCT",
    "Mock Real Supplier Product"
]

headers = {
    "X-Shopify-Access-Token": TOKEN,
    "Content-Type": "application/json"
}

products_url = f"https://{SHOP}/admin/api/{API_VERSION}/products.json?limit=250"
r = requests.get(products_url, headers=headers, timeout=30)
r.raise_for_status()

products = r.json().get("products", [])

for p in products:
    title = p.get("title", "")
    if any(k.lower() in title.lower() for k in BAD_KEYWORDS):
        product_id = p["id"]
        url = f"https://{SHOP}/admin/api/{API_VERSION}/products/{product_id}.json"
        d = requests.delete(url, headers=headers, timeout=30)
        print("DELETED", product_id, d.status_code, title)

print("Done")
