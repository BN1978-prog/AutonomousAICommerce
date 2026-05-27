import os
import requests

SHOP = os.getenv("SHOPIFY_SHOP") or os.getenv("SHOPIFY_SHOP_DOMAIN")
TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN") or os.getenv("SHOPIFY_ADMIN_TOKEN")

PRODUCT_ID_TO_DELETE = 10658215493974

url = f"https://{SHOP}/admin/api/2025-01/products/{PRODUCT_ID_TO_DELETE}.json"

r = requests.delete(
    url,
    headers={"X-Shopify-Access-Token": TOKEN},
    timeout=60
)

print("STATUS:", r.status_code)
print(r.text)
