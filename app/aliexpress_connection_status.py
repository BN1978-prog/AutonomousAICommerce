import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/aliexpress_connection_status.json")

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "channel": "aliexpress",
    "ready": False,
    "missing": [
        "ALIEXPRESS_APP_KEY",
        "ALIEXPRESS_APP_SECRET",
        "ALIEXPRESS_ACCESS_TOKEN",
        "ALIEXPRESS_REFRESH_TOKEN"
    ],
    "external_blocker": True,
    "status": "ALIEXPRESS_DEVELOPER_ACCESS_NOT_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
