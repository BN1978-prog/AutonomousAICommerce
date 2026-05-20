import json
from pathlib import Path

TRACKING = Path("app/logs/tracking_updates.json")

items = json.loads(TRACKING.read_text(encoding="utf-8"))

for item in items:
    if item.get("order_id") == "TEST-ORDER-001":
        item["tracking_number"] = "TESTTRACK123456"
        item["carrier"] = "CJPacket"
        item["status"] = "tracking_received"
        item["channel_update_status"] = "pending"

TRACKING.write_text(
    json.dumps(items, indent=2),
    encoding="utf-8"
)

print("test tracking added")
