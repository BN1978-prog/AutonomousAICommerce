import json
import os
from pathlib import Path
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv(override=True)

OUT = Path("app/logs/woocommerce_draft_enrichment_result.json")

wc_url = os.getenv("WOOCOMMERCE_URL", "").rstrip("/")
ck = os.getenv("WOOCOMMERCE_CONSUMER_KEY", "")
cs = os.getenv("WOOCOMMERCE_CONSUMER_SECRET", "")

products = [
    {
        "id": 17,
        "sku": "CJJJCWMY00923",
        "payload": {
            "categories": [{"name": "Pet Supplies"}],
            "tags": [{"name": "cats"}, {"name": "pet toys"}, {"name": "organic launch"}],
            "manage_stock": True,
            "stock_quantity": 10,
            "stock_status": "instock",
            "status": "draft"
        }
    },
    {
        "id": 18,
        "sku": "PET-BOWL-001",
        "payload": {
            "categories": [{"name": "Pet Supplies"}],
            "tags": [{"name": "pet bowl"}, {"name": "cats"}, {"name": "dogs"}, {"name": "organic launch"}],
            "manage_stock": True,
            "stock_quantity": 10,
            "stock_status": "instock",
            "status": "draft"
        }
    }
]

results = []

if not (wc_url and ck and cs):
    status = "BLOCKED_WOOCOMMERCE_CONFIG_MISSING"
else:
    status = "WOOCOMMERCE_DRAFT_ENRICHMENT_ATTEMPTED"

    for product in products:
        try:
            r = requests.put(
                f"{wc_url}/wp-json/wc/v3/products/{product['id']}",
                auth=(ck, cs),
                json=product["payload"],
                timeout=30
            )

            try:
                data = r.json()
            except:
                data = {"raw": r.text}

            results.append({
                "id": product["id"],
                "sku": product["sku"],
                "status_code": r.status_code,
                "ok": r.status_code in [200, 201],
                "response_status": data.get("status"),
                "categories": data.get("categories"),
                "tags": data.get("tags"),
                "stock_status": data.get("stock_status"),
                "stock_quantity": data.get("stock_quantity")
            })

        except Exception as e:
            results.append({
                "id": product["id"],
                "sku": product["sku"],
                "ok": False,
                "error": str(e)
            })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "products_attempted": len(products),
    "results": results,
    "status": status
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
