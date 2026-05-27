import json, os
from pathlib import Path
from datetime import datetime, timezone

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "channel":"etsy",
    "autopilot_enabled": True,
    "listing_publish": False,
    "inventory_sync": False,
    "order_sync": False
}

if os.getenv("ETSY_ACCESS_TOKEN"):
    report["listing_publish"]=True
    report["inventory_sync"]=True
    report["order_sync"]=True
    report["status"]="ETSY_ACTIVE"
else:
    report["status"]="ETSY_WAITING_APPROVAL"

Path("app/logs/etsy_autopilot.json").write_text(
    json.dumps(report,indent=2),
    encoding="utf-8"
)

print(json.dumps(report,indent=2))
