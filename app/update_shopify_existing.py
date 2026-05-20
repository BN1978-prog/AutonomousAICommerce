from dotenv import load_dotenv
load_dotenv(override=True)

import os, json, requests
from pathlib import Path

from app.suppliers.real_supplier import fetch_real_supplier_products
from app.suppliers.normalize_product import normalize_supplier_product
from app.suppliers.ai_product_score import score_product
from app.pricing_ai import dynamic_price
from app.channels.shopify_config import ShopifyConfig

IMPORTS = Path("app/logs/imported_skus.json")

shop_url = "https://" + ShopifyConfig.get_store().strip().replace("https://","").replace("http://","").rstrip("/")
token = ShopifyConfig.get_token()

headers = {
    "X-Shopify-Access-Token": token,
    "Content-Type": "application/json"
}

imports = json.loads(IMPORTS.read_text(encoding="utf-8"))
products = fetch_real_supplier_products()

updated = 0

for raw in products:
    try:
        normalized = normalize_supplier_product(raw)
    except Exception:
        continue

    sku = normalized.get("sku")

    if sku not in imports:
        continue

    meta = imports[sku]
    product_id = meta.get("product_id")

    if not product_id:
        continue

    score = score_product(normalized)
    pricing = dynamic_price(normalized.get("cost", 0), score.get("score", 50))
    normalized["price"] = pricing["price"]

    payload = {
        "product": {
            "id": product_id,
            "title": normalized["title"],
            "body_html": normalized["description"],
            "vendor": normalized.get("vendor", "CJdropshipping"),
            "tags": normalized.get("seo_tags", "CJdropshipping, ai-selected, draft-review"),
            "variants": [
                {
                    "sku": sku,
                    "price": str(normalized["price"]),
                    "inventory_quantity": int(normalized.get("inventory", 1))
                }
            ]
        }
    }

    url = f"{shop_url}/admin/api/2024-01/products/{product_id}.json"
    r = requests.put(url, headers=headers, json=payload, timeout=30)

    print("SKU:", sku)
    print("STATUS:", r.status_code)
    print("PRICE:", normalized["price"])
    print("SCORE:", score["score"])

    if r.status_code in [200, 201]:
        updated += 1
        meta["last_update_status"] = "updated"
        meta["last_price"] = normalized["price"]
        meta["last_score"] = score["score"]
    else:
        print(r.text[:1000])
        meta["last_update_status"] = "failed"

IMPORTS.write_text(json.dumps(imports, indent=2), encoding="utf-8")

print("UPDATED:", updated)
