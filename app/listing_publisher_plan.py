import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/listing_publisher_plan.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

launch = read_json("app/logs/organic_money_launch_plan.json")

publish_actions = []

for product in launch.get("products", []):
    for channel in product.get("target_channels", []):
        publish_actions.append({
            "sku": product.get("sku"),
            "title": product.get("title"),
            "channel": channel,
            "action": "prepare_listing",
            "mode": "safe_publish_plan_no_supplier_purchase",
            "paid_ads_enabled": False,
            "supplier_purchase_allowed": False,
            "status": "READY_FOR_CHANNEL_LISTING"
        })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "products_seen": len(launch.get("products", [])),
    "publish_actions_count": len(publish_actions),
    "publish_actions": publish_actions,
    "status": "LISTING_PUBLISHER_PLAN_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
