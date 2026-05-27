import json
import os
from pathlib import Path
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv(override=True)

OUT = Path("app/logs/woocommerce_publish_result.json")
CONFIRM = Path("app/CONFIRM_WOOCOMMERCE_FINAL_PUBLISH.txt")

wc_url = os.getenv("WOOCOMMERCE_URL", "").rstrip("/")
ck = os.getenv("WOOCOMMERCE_CONSUMER_KEY", "")
cs = os.getenv("WOOCOMMERCE_CONSUMER_SECRET", "")

product_ids = [17, 18]
results = []

if not CONFIRM.exists():
    status = "BLOCKED_FINAL_CONFIRMATION_MISSING"
elif not (wc_url and ck and cs):
    status = "BLOCKED_WOOCOMMERCE_CONFIG_MISSING"
else:
    status = "WOOCOMMERCE_FINAL_PUBLISH_ATTEMPTED"

    for pid in product_ids:
        r = requests.put(
            f"{wc_url}/wp-json/wc/v3/products/{pid}",
            auth=(ck, cs),
            json={"status": "publish"},
            timeout=30
        )

        try:
            data = r.json()
        except:
            data = {"raw": r.text}

        results.append({
            "id": pid,
            "status_code": r.status_code,
            "ok": r.status_code in [200, 201],
            "product_status": data.get("status"),
            "name": data.get("name"),
            "sku": data.get("sku"),
            "permalink": data.get("permalink")
        })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "confirmation_file_exists": CONFIRM.exists(),
    "products_attempted": len(product_ids),
    "results": results,
    "status": status
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
