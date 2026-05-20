import json
from pathlib import Path
from datetime import datetime, timezone

REGISTRY=Path("app/logs/imported_skus.json")
FEEDBACK=Path("app/logs/hunter_feedback.json")
OUT=Path("app/logs/hunter_registry_sync.json")

registry=json.loads(
    REGISTRY.read_text(
        encoding="utf-8"
    )
)

feedback=json.loads(
    FEEDBACK.read_text(
        encoding="utf-8"
    )
)

blocked_words={
    "glass",
    "tea",
    "microneedle",
    "hair growth",
    "flowers"
}

results=[]

for row in feedback:

    sku=row["sku"]

    if sku not in registry:
        continue

    title=(row["title"] or "").lower()

    excluded=False

    if any(x in title for x in blocked_words):
        registry[sku]["hunter_excluded"]=True
        registry[sku]["hunter_decision"]="exclude"
        excluded=True

    else:
        registry[sku]["hunter_score"]=row["hunter_score"]
        registry[sku]["hunter_decision"]=row["decision"]

    registry[sku]["hunter_updated_at"]=(
        datetime.now(
            timezone.utc
        ).isoformat()
    )

    results.append({
        "sku":sku,
        "decision":
            registry[sku].get(
                "hunter_decision"
            ),
        "excluded":excluded
    })

REGISTRY.write_text(
    json.dumps(
        registry,
        indent=2
    ),
    encoding="utf-8"
)

OUT.write_text(
    json.dumps(
        results,
        indent=2
    ),
    encoding="utf-8"
)

print(
    "SYNCED:",
    len(results)
)

print(
    "EXCLUDED:",
    sum(
        1 for x in results
        if x["excluded"]
    )
)
