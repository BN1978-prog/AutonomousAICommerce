import os
import json
import requests
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlparse

ENV = Path(".env")
IMPORTS = Path("app/logs/imported_skus.json")
OUT = Path("app/logs/shopify_registry_hydration_results.json")

def load_env_file(path):
    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and value:
            os.environ[key] = value

def normalize_shop_domain(value):
    if not value:
        return None

    value = value.strip()

    if value.startswith("http://") or value.startswith("https://"):
        return urlparse(value).netloc.rstrip("/")

    return value.replace("/", "").strip()

load_env_file(ENV)

shop_domain = normalize_shop_domain(
    os.getenv("SHOPIFY_STORE_URL")
    or os.getenv("SHOPIFY_STORE_DOMAIN")
    or os.getenv("SHOPIFY_SHOP")
)

token = (
    os.getenv("SHOPIFY_ACCESS_TOKEN")
    or os.getenv("SHOPIFY_ADMIN_TOKEN")
    or os.getenv("SHOPIFY_ADMIN_ACCESS_TOKEN")
)

api_version = os.getenv("SHOPIFY_API_VERSION", "2025-01")

print("SHOPIFY DOMAIN:", shop_domain)
print("TOKEN EXISTS:", bool(token))

if not shop_domain:
    raise SystemExit("Missing Shopify shop domain")

if not token:
    raise SystemExit("Missing Shopify token")

data = json.loads(IMPORTS.read_text(encoding="utf-8")) if IMPORTS.exists() else {}

headers = {
    "X-Shopify-Access-Token": token,
    "Content-Type": "application/json"
}

results = []

for sku, meta in data.items():
    product_id = meta.get("product_id")

    if not product_id:
        results.append({
            "sku": sku,
            "ok": False,
            "skipped": True,
            "reason": "missing_product_id"
        })
        continue

    url = f"https://{shop_domain}/admin/api/{api_version}/products/{product_id}.json"

    try:
        resp = requests.get(url, headers=headers, timeout=30)

        if resp.status_code >= 400:
            results.append({
                "sku": sku,
                "ok": False,
                "skipped": True,
                "reason": f"shopify_http_{resp.status_code}",
                "body": resp.text[:500]
            })
            continue

        product = resp.json().get("product") or {}

        variants = product.get("variants") or []
        images = product.get("images") or []

        price = variants[0].get("price") if variants else None
        image = images[0].get("src") if images else None

        handle = product.get("handle")
        product_url = f"https://{shop_domain}/products/{handle}" if handle else None

        meta["title"] = product.get("title")
        meta["description"] = product.get("body_html")
        meta["price"] = price
        meta["image"] = image
        meta["product_url"] = product_url
        meta["shopify_handle"] = handle
        meta["registry_hydrated_from_shopify"] = True
        meta["registry_hydrated_at"] = datetime.now(timezone.utc).isoformat()

        results.append({
            "sku": sku,
            "ok": True,
            "skipped": False,
            "reason": "hydrated_from_shopify",
            "title": meta.get("title"),
            "price": meta.get("price")
        })

    except Exception as e:
        results.append({
            "sku": sku,
            "ok": False,
            "skipped": True,
            "reason": "exception",
            "error": str(e)
        })

IMPORTS.write_text(json.dumps(data, indent=2), encoding="utf-8")
OUT.write_text(json.dumps(results, indent=2), encoding="utf-8")

ok_count = sum(1 for r in results if r.get("ok") is True)
fail_count = len(results) - ok_count

print("SHOPIFY REGISTRY HYDRATION RESULTS:", len(results))
print("OK:", ok_count)
print("FAILED/SKIPPED:", fail_count)

for r in results:
    print(
        r["sku"],
        "ok=",
        r["ok"],
        "skipped=",
        r["skipped"],
        "reason=",
        r["reason"],
        "title=",
        r.get("title")
    )
