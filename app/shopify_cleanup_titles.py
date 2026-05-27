import os
import requests

SHOP = os.getenv("SHOPIFY_STORE_URL") or os.getenv("SHOPIFY_SHOP_DOMAIN") or os.getenv("SHOPIFY_SHOP")
TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN") or os.getenv("SHOPIFY_ADMIN_TOKEN")
API_VERSION = os.getenv("SHOPIFY_API_VERSION", "2025-01")

RENAMES = {
    "10594986492246": "Warm Pet Blanket - Cozy Winter Cover",
    "10659785146710": "Pet Hair Remover Grooming Glove",
    "10656856244566": "Foldable Cat Tunnel Toy",
    "10595047965014": "Pet Grooming Brush for Shedding",
    "10594435596630": "Large Pet Grooming Brush",
    "10578817876310": "Durable Pet Leash for Daily Walks",
    "10598237241686": "Non-Slip Cotton Dog Socks",
    "10598252478806": "Cat Harness and Leash Set",
    "10650143490390": "Adjustable Dog Harness Vest",
    "10601382445398": "Red Reflective Pet Chest Harness"
}

headers = {
    "X-Shopify-Access-Token": TOKEN,
    "Content-Type": "application/json"
}

for product_id, title in RENAMES.items():
    url = f"https://{SHOP}/admin/api/{API_VERSION}/products/{product_id}.json"

    payload = {
        "product": {
            "id": int(product_id),
            "title": title
        }
    }

    r = requests.put(url, headers=headers, json=payload, timeout=30)
    print(product_id, r.status_code, title)

print("Done")
