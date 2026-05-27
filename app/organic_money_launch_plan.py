import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/organic_money_launch_plan.json")

top_products = [
    {
        "sku": "CJJJCWMY00923",
        "title": "Eco-Friendly Cat Scratcher Toy",
        "supplier": "CJ Dropshipping",
        "target_channels": ["shopify", "woocommerce", "ebay"],
        "mode": "dropshipping_no_inventory_purchase",
        "status": "READY_TO_LIST"
    },
    {
        "sku": "PET-BOWL-001",
        "title": "Non-slip silicone pet feeding bowl",
        "supplier": "CJ Dropshipping",
        "target_channels": ["shopify", "woocommerce", "ebay"],
        "mode": "dropshipping_no_inventory_purchase",
        "status": "READY_TO_LIST"
    }
]

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "launch_type": "ORGANIC_DROPSHIPPING_MONEY_LAUNCH",
    "paid_ads_enabled": False,
    "live_money_spending": False,
    "purchase_rule": "buy_from_supplier_only_after_customer_paid_order",
    "products_count": len(top_products),
    "products": top_products,
    "status": "ORGANIC_MONEY_LAUNCH_PLAN_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
