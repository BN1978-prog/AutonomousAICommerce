import json
import os
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv(override=True)

OUT = Path("app/logs/woocommerce_real_publisher.json")
CONFIRM = Path("app/CONFIRM_WOOCOMMERCE_LIVE_PUBLISH.txt")

wc_url = os.getenv("WOOCOMMERCE_URL", "")
ck = os.getenv("WOOCOMMERCE_CONSUMER_KEY", "")
cs = os.getenv("WOOCOMMERCE_CONSUMER_SECRET", "")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

plan = read_json("app/logs/listing_publish_execution_plan.json")
actions = [a for a in plan.get("actions", []) if a.get("channel") == "woocommerce"]

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "confirmation_file_exists": CONFIRM.exists(),
    "woocommerce_config_present": bool(wc_url and ck and cs),
    "actions_seen": len(actions),
    "actions": actions,
    "live_api_call_enabled": False,
    "status": "WOOCOMMERCE_REAL_PUBLISHER_READY_GUARDED"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
