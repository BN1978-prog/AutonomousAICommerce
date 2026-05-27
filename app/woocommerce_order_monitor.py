import json
import os
from pathlib import Path
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv(override=True)

OUT = Path("app/logs/woocommerce_order_monitor.json")

wc_url = os.getenv("WOOCOMMERCE_URL","").rstrip("/")
ck = os.getenv("WOOCOMMERCE_CONSUMER_KEY","")
cs = os.getenv("WOOCOMMERCE_CONSUMER_SECRET","")

try:
    r = requests.get(
        f"{wc_url}/wp-json/wc/v3/orders",
        auth=(ck, cs),
        params={"per_page":10},
        timeout=30
    )

    data = r.json() if r.status_code == 200 else []

    orders = []

    for o in data:
        orders.append({
            "id": o.get("id"),
            "status": o.get("status"),
            "total": o.get("total"),
            "currency": o.get("currency")
        })

    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "orders_found": len(orders),
        "orders": orders,
        "status": "WOOCOMMERCE_ORDER_MONITOR_OK"
    }

except Exception as e:
    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "error": str(e),
        "status": "WOOCOMMERCE_ORDER_MONITOR_ERROR"
    }

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
