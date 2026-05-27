import json
from pathlib import Path
from datetime import datetime, timezone

METRICS = Path("app/logs/manual_channel_metrics.json")

data=json.loads(
    METRICS.read_text(
        encoding="utf-8-sig"
    )
)

channel="instagram"

data[channel]["clicks"] += 1

data["updated_at"]=datetime.now(
    timezone.utc
).isoformat()

METRICS.write_text(
    json.dumps(data,indent=2),
    encoding="utf-8"
)

print(json.dumps(data,indent=2))
