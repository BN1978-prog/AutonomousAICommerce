import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/woocommerce_listing_publisher.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

plan = read_json("app/logs/listing_publish_execution_plan.json")

actions = [
    a for a in plan.get("actions", [])
    if a.get("channel") == "woocommerce"
]

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "mode": "woocommerce_publish_ready_safe_mode",
    "actions_seen": len(actions),
    "actions": actions,
    "live_publish_enabled": False,
    "status": "WOOCOMMERCE_LISTINGS_READY_FOR_MANUAL_OR_GUARDED_PUBLISH"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
