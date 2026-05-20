import json
from pathlib import Path
from datetime import datetime, timezone

REGISTRY=Path("app/logs/imported_skus.json")
SCORES=Path("app/logs/dynamic_product_score.json")
OUT=Path("app/logs/dynamic_score_sync.json")

registry=json.loads(REGISTRY.read_text(encoding="utf-8"))
scores=json.loads(SCORES.read_text(encoding="utf-8"))

updated=0

for row in scores:

    sku=row["sku"]

    if sku not in registry:
        continue

    score=row["dynamic_score"]

    registry[sku]["dynamic_score"]=score

    if score>=100:
        tier="A"

    elif score>=70:
        tier="B"

    elif score>=40:
        tier="C"

    else:
        tier="D"

    registry[sku]["product_tier"]=tier
    registry[sku]["dynamic_updated_at"]=(
        datetime.now(timezone.utc).isoformat()
    )

    updated+=1

REGISTRY.write_text(
    json.dumps(registry,indent=2),
    encoding="utf-8"
)

Path(OUT).write_text(
    json.dumps(
        {
            "updated":updated,
            "tiers":{
                "A":"score>=100",
                "B":"70-99",
                "C":"40-69",
                "D":"<40"
            }
        },
        indent=2
    ),
    encoding="utf-8"
)

print("UPDATED:",updated)
