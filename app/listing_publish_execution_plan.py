import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/listing_publish_execution_plan.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

validated = read_json("app/logs/listing_publish_validator.json").get("validated", [])

actions = []

for item in validated:
    actions.append({
        "sku": item.get("sku"),
        "title": item.get("title"),
        "channel": item.get("channel"),
        "execution_type": "organic_listing_publish",
        "paid_ads_enabled": False,
        "supplier_purchase_allowed": False,
        "status": "READY_TO_PUBLISH_ORGANIC_LISTING"
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "actions_ready": len(actions),
    "actions": actions,
    "status": "LISTING_PUBLISH_EXECUTION_PLAN_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
