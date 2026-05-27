import os, json, requests
from pathlib import Path

ENV = Path(".env")
for line in ENV.read_text(encoding="utf-8-sig").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k, v = line.split("=", 1)
        os.environ[k.strip()] = v.strip()

shop = os.getenv("SHOPIFY_SHOP_DOMAIN") or os.getenv("SHOPIFY_STORE_URL")
token = os.getenv("SHOPIFY_ADMIN_TOKEN") or os.getenv("SHOPIFY_ACCESS_TOKEN")
version = os.getenv("SHOPIFY_API_VERSION", "2025-01")

url = f"https://{shop}/admin/api/{version}/products.json?limit=50"

r = requests.get(
    url,
    headers={
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json"
    },
    timeout=30
)

print("Status:", r.status_code)

data = r.json()
products = data.get("products", [])

catalog = []

for p in products:
    handle = p.get("handle") or str(p.get("id"))
    title = p.get("title") or handle
    product_url = f"https://{shop}/products/{handle}"

    catalog.append({
        "id": handle.replace("-", "_"),
        "name": title,
        "category": p.get("product_type") or "shopify product",
        "angle": "is available now in our store",
        "hashtags": "#petproducts #petcare #shopping #onlinestore",
        "url": product_url
    })

Path("app/logs/product_catalog.json").write_text(
    json.dumps(catalog, indent=2),
    encoding="utf-8"
)

print("Imported Shopify products:", len(catalog))
for item in catalog:
    print("-", item["id"], "|", item["name"])
