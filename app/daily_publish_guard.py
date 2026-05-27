import json
from pathlib import Path
from datetime import datetime, timezone

LOCK = Path("app/logs/daily_publish_lock.json")

today = datetime.now(timezone.utc).date().isoformat()

if LOCK.exists():
    data = json.loads(LOCK.read_text(encoding="utf-8-sig"))
else:
    data = {}

if data.get("last_publish_date") == today:
    print("Daily publish already done:", today)
    raise SystemExit(10)

data["last_publish_date"] = today
LOCK.write_text(json.dumps(data, indent=2), encoding="utf-8")

print("Daily publish allowed:", today)
