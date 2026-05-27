import json
import os
from pathlib import Path
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv(override=True)

OUT = Path("app/logs/woocommerce_category_fix_result.json")

wc_url = os.getenv("WOOCOMMERCE_URL", "").rstrip("/")
ck = os.getenv("WOOCOMMERCE_CONSUMER_KEY", "")
cs = os.getenv("WOOCOMMERCE_CONSUMER_SECRET", "")

products = [17, 18]
category_name = "Pet Supplies"

results = []

try:
    # 1. Find existing category
    r = requests.get(
        f"{wc_url}/wp-json/wc/v3/products/categories",
        auth=(ck, cs),
        params={"search": category_name},
        timeout=30
    )
    cats = r.json() if r.status_code == 200 else []

    category_id = None
    for c in cats:
        if c.get("name", "").lower() == category_name.lower():
            category_id = c.get("id")
            break

    # 2. Create category if missing
    if not category_id:
        cr = requests.post(
            f"{wc_url}/wp-json/wc/v3/products/categories",
            auth=(ck, cs),
            json={"name": category_name},
            timeout=30
        )
        cdata = cr.json()
        category_id = cdata.get("id")
        results.append({
            "action": "create_category",
            "status_code": cr.status_code,
            "category_id": category_id,
            "response": cdata
        })
    else:
        results.append({
            "action": "category_exists",
            "category_id": category_id
        })

    # 3. Assign category to products
    for pid in products:
        ur = requests.put(
            f"{wc_url}/wp-json/wc/v3/products/{pid}",
            auth=(ck, cs),
            json={"categories": [{"id": category_id}], "status": "draft"},
            timeout=30
        )
        udata = ur.json()
        results.append({
            "action": "assign_category",
            "product_id": pid,
            "status_code": ur.status_code,
            "ok": ur.status_code in [200, 201],
            "categories": udata.get("categories")
        })

    status = "WOOCOMMERCE_CATEGORY_FIX_ATTEMPTED"

except Exception as e:
    status = "WOOCOMMERCE_CATEGORY_FIX_ERROR"
    results.append({"error": str(e)})

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "category_name": category_name,
    "results": results,
    "status": status
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
