import json
import os
from pathlib import Path
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv(override=True)

OUT = Path("app/logs/woocommerce_pre_publish_check.json")

wc_url = os.getenv("WOOCOMMERCE_URL", "").rstrip("/")
ck = os.getenv("WOOCOMMERCE_CONSUMER_KEY", "")
cs = os.getenv("WOOCOMMERCE_CONSUMER_SECRET", "")

product_ids = [17, 18]
results = []

for pid in product_ids:
    r = requests.get(
        f"{wc_url}/wp-json/wc/v3/products/{pid}",
        auth=(ck, cs),
        timeout=30
    )
    data = r.json()

    issues = []

    if data.get("status") != "draft":
        issues.append("not_draft")
    if not data.get("name"):
        issues.append("missing_name")
    if not data.get("regular_price"):
        issues.append("missing_price")
    if not data.get("sku"):
        issues.append("missing_sku")
    if not data.get("categories"):
        issues.append("missing_category")
    if data.get("stock_status") != "instock":
        issues.append("not_instock")
    if not data.get("images"):
        issues.append("missing_images")

    results.append({
        "id": pid,
        "name": data.get("name"),
        "sku": data.get("sku"),
        "status": data.get("status"),
        "price": data.get("regular_price"),
        "categories": data.get("categories"),
        "stock_status": data.get("stock_status"),
        "images_count": len(data.get("images", [])),
        "issues": issues,
        "publish_ready": len([x for x in issues if x != "missing_images"]) == 0
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "products_checked": len(results),
    "results": results,
    "status": "WOOCOMMERCE_PRE_PUBLISH_CHECK_COMPLETE"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
