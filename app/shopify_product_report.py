import os
import json
from pathlib import Path
from datetime import datetime, timezone
import requests

SHOPIFY_SHOP = (
    os.getenv("SHOPIFY_SHOP")
    or os.getenv("SHOPIFY_STORE")
    or os.getenv("SHOPIFY_STORE_URL")
    or ""
).replace("https://", "").replace("http://", "").rstrip("/")

SHOPIFY_TOKEN = (
    os.getenv("SHOPIFY_ACCESS_TOKEN")
    or os.getenv("SHOPIFY_ADMIN_TOKEN")
    or os.getenv("SHOPIFY_TOKEN")
    or ""
)

if not SHOPIFY_SHOP or not SHOPIFY_TOKEN:
    raise SystemExit(
        "Missing Shopify credentials. Need SHOPIFY_SHOP and SHOPIFY_ACCESS_TOKEN."
    )

url = f"https://{SHOPIFY_SHOP}/admin/api/2024-10/products.json?limit=20"

r = requests.get(
    url,
    headers={
        "X-Shopify-Access-Token": SHOPIFY_TOKEN,
        "Content-Type": "application/json",
    },
    timeout=60,
)

if r.status_code != 200:
    raise SystemExit(f"Shopify API failed {r.status_code}: {r.text}")

products = r.json().get("products", [])

items = []
for p in products:
    items.append({
        "id": p.get("id"),
        "title": p.get("title"),
        "status": p.get("status"),
        "vendor": p.get("vendor"),
        "product_type": p.get("product_type"),
        "variants": len(p.get("variants", [])),
        "images": len(p.get("images", [])),
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "shop": SHOPIFY_SHOP,
    "products_returned": len(items),
    "items": items,
    "status": "SHOPIFY_PRODUCT_REPORT_READY",
}

Path("app/logs").mkdir(parents=True, exist_ok=True)
Path("app/logs/shopify_product_report.json").write_text(
    json.dumps(report, indent=2, ensure_ascii=False),
    encoding="utf-8",
)

print(json.dumps(report, indent=2, ensure_ascii=False))
