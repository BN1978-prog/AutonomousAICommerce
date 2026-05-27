import os
import base64
import requests
from pathlib import Path

SHOP = os.getenv("SHOPIFY_SHOP") or os.getenv("SHOPIFY_SHOP_DOMAIN")
TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN") or os.getenv("SHOPIFY_ADMIN_TOKEN")

PRODUCT_ID = 10657934934358
IMAGE_PATH = Path("app/assets/product_images/dog_socks.jpg")

if not SHOP:
    raise SystemExit("Missing SHOPIFY_SHOP / SHOPIFY_SHOP_DOMAIN")

if not TOKEN:
    raise SystemExit("Missing SHOPIFY_ACCESS_TOKEN / SHOPIFY_ADMIN_TOKEN")

if not IMAGE_PATH.exists():
    raise SystemExit(f"Image not found: {IMAGE_PATH}")

image_b64 = base64.b64encode(IMAGE_PATH.read_bytes()).decode("utf-8")

url = f"https://{SHOP}/admin/api/2025-01/products/{PRODUCT_ID}.json"

payload = {
    "product": {
        "id": PRODUCT_ID,
        "status": "active",
        "images": [
            {
                "attachment": image_b64,
                "filename": IMAGE_PATH.name
            }
        ]
    }
}

r = requests.put(
    url,
    headers={
        "X-Shopify-Access-Token": TOKEN,
        "Content-Type": "application/json"
    },
    json=payload,
    timeout=90
)

print("STATUS:", r.status_code)
print(r.text[:1000])
