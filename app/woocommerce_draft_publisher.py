import json
import os
from pathlib import Path
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv(override=True)

OUT = Path("app/logs/woocommerce_draft_publish_result.json")
CONFIRM = Path("app/CONFIRM_WOOCOMMERCE_LIVE_PUBLISH.txt")

wc_url = os.getenv("WOOCOMMERCE_URL", "").rstrip("/")
ck = os.getenv("WOOCOMMERCE_CONSUMER_KEY", "")
cs = os.getenv("WOOCOMMERCE_CONSUMER_SECRET", "")

products = [
    {
        "name": "Eco-Friendly Cat Scratcher Toy",
        "type": "simple",
        "regular_price": "19.99",
        "description": "Eco-friendly cat scratcher toy for indoor cats. Suitable for organic dropshipping launch.",
        "short_description": "Eco-friendly cat scratcher toy.",
        "sku": "CJJJCWMY00923",
        "status": "draft"
    },
    {
        "name": "Non-slip silicone pet feeding bowl",
        "type": "simple",
        "regular_price": "14.99",
        "description": "Non-slip silicone feeding bowl for pets. Suitable for cats and small dogs.",
        "short_description": "Non-slip silicone pet feeding bowl.",
        "sku": "PET-BOWL-001",
        "status": "draft"
    }
]

results = []

if not CONFIRM.exists():
    status = "BLOCKED_CONFIRMATION_FILE_MISSING"
elif not (wc_url and ck and cs):
    status = "BLOCKED_WOOCOMMERCE_CONFIG_MISSING"
else:
    status = "WOOCOMMERCE_DRAFT_PUBLISH_ATTEMPTED"

    for product in products:
        try:
            r = requests.post(
                f"{wc_url}/wp-json/wc/v3/products",
                auth=(ck, cs),
                json=product,
                timeout=30
            )

            try:
                data = r.json()
            except:
                data = {"raw": r.text}

            results.append({
                "sku": product["sku"],
                "name": product["name"],
                "status_code": r.status_code,
                "ok": r.status_code in [200, 201],
                "response": data
            })

        except Exception as e:
            results.append({
                "sku": product["sku"],
                "name": product["name"],
                "ok": False,
                "error": str(e)
            })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "wc_url": wc_url,
    "products_attempted": len(products),
    "results": results,
    "status": status
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
