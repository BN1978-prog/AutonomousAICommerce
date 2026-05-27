import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/woocommerce_live_publish_guard.json")
CONFIRM = Path("app/CONFIRM_WOOCOMMERCE_LIVE_PUBLISH.txt")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

publisher = read_json("app/logs/woocommerce_listing_publisher.json")
confirmed = CONFIRM.exists()

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "actions_seen": publisher.get("actions_seen", 0),
    "confirmation_file_exists": confirmed,
    "live_publish_allowed": confirmed,
    "status": "WOOCOMMERCE_LIVE_PUBLISH_ALLOWED" if confirmed else "WOOCOMMERCE_LIVE_PUBLISH_BLOCKED_BY_GUARD"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
