import json
from pathlib import Path
from datetime import datetime, timezone

SRC = Path("app/logs/spend_history_tracker.json")
OUT = Path("app/logs/negative_roi_auto_pause.json")

data = json.loads(SRC.read_text(encoding="utf-8"))

pause_actions = []

for item in data.get("history", []):
    should_pause = item["rolling_roi_percent"] < 0

    pause_actions.append({
        "sku": item["sku"],
        "rolling_roi_percent": item["rolling_roi_percent"],
        "health": item["health"],
        "should_pause": should_pause,
        "action": "AUTO_PAUSE_CAMPAIGN" if should_pause else "KEEP_RUNNING"
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "pause_actions": pause_actions,
    "auto_pause_enabled": True,
    "status": "NEGATIVE_ROI_AUTO_PAUSE_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

print(json.dumps(report, indent=2))
