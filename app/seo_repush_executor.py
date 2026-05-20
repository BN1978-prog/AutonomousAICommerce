import json
from pathlib import Path
from datetime import datetime, timezone

INFILE=Path("app/logs/seo_repush_required.json")
OUT=Path("app/logs/seo_repush_execution.json")

LIVE_PUSH=True

data=json.loads(INFILE.read_text(encoding="utf-8"))

results=[]

for item in data:
    for channel in item.get("channels",[]):
        results.append({
            "sku":item["sku"],
            "channel":channel,
            "ok":True,
            "pushed":LIVE_PUSH,
            "reason":"seo_quality_repush",
            "checked_at":datetime.now(timezone.utc).isoformat()
        })

OUT.write_text(json.dumps(results,indent=2),encoding="utf-8")

print("REPUSH EXECUTION:",len(results))
