import json
from pathlib import Path
from datetime import datetime, timezone

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "sales_mode": "DROPSHIPPING_PRELAUNCH",
    "inventory_purchase_required": False,
    "supplier": "CJ_DROPSHIPPING",
    "channels": [
        "shopify",
        "ebay",
        "woocommerce"
    ],
    "paid_ads_enabled": False,
    "traffic_source": "organic",
    "status": "READY_FOR_FIRST_PRODUCTS"
}

Path("app/logs/sales_mode.json").write_text(
    json.dumps(report, indent=2),
    encoding="utf-8"
)

print(json.dumps(report, indent=2))
