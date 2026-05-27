import json
import os
from pathlib import Path
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv(override=True)

OUT = Path("app/logs/woocommerce_image_gap_report.json")

wc_url = os.getenv("WOOCOMMERCE_URL", "").rstrip("/")
ck = os.getenv("WOOCOMMERCE_CONSUMER_KEY", "")
cs = os.getenv("WOOCOMMERCE_CONSUMER_SECRET", "")

product_ids = [17, 18]
items = []

for pid in product_ids:
    r = requests.get(
        f"{wc_url}/wp-json/wc/v3/products/{pid}",
        auth=(ck, cs),
        timeout=30
    )
    data = r.json()

    images = data.get("images", [])

    items.append({
        "id": pid,
        "name": data.get("name"),
        "sku": data.get("sku"),
        "status": data.get("status"),
        "images_count": len(images),
        "needs_images": len(images) == 0
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "products_checked": len(items),
    "items_needing_images": [x for x in items if x["needs_images"]],
    "items": items,
    "status": "WOOCOMMERCE_IMAGE_GAP_REPORT_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
