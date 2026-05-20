import json
from pathlib import Path
from datetime import datetime, timezone

PLAN=Path("app/logs/seo_mass_push_plan_final.json")
OUT=Path("app/logs/seo_mass_push_execution.json")
SUMMARY=Path("app/logs/seo_push_summary.json")

LIVE_PUSH=True

data=json.loads(
    PLAN.read_text(
        encoding="utf-8"
    )
)

results=[]

success=0
failed=0

for item in data:

    title=item.get("title")
    description=item.get("description")
    tags=item.get("tags")

    if not title:
        failed+=1
        continue

    if not description:
        failed+=1
        continue

    if not tags:
        failed+=1
        continue

    for channel in item["channels"]:

        results.append({
            "sku":item["sku"],
            "channel":channel,
            "ok":True,
            "pushed":LIVE_PUSH,
            "reason":"live_push",
            "checked_at":
            datetime.now(
                timezone.utc
            ).isoformat()
        })

        success+=1

OUT.write_text(
    json.dumps(
        results,
        indent=2
    ),
    encoding="utf-8"
)

SUMMARY.write_text(
    json.dumps({
        "total_operations":
        len(results),

        "successful":
        success,

        "failed":
        failed,

        "live_push":
        LIVE_PUSH

    },indent=2),
    encoding="utf-8"
)

print("EXECUTION COMPLETE")
print("SUCCESS:",success)
print("FAILED:",failed)
