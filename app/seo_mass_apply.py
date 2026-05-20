import json
from pathlib import Path
from datetime import datetime, timezone

PLAN=Path("app/logs/traffic_execution_plan_final.json")
REGISTRY=Path("app/logs/imported_skus.json")
OUT=Path("app/logs/seo_mass_apply_results.json")

plan=json.loads(PLAN.read_text(encoding="utf-8"))
registry=json.loads(REGISTRY.read_text(encoding="utf-8"))

results=[]

for item in plan:

    sku=item["sku"]

    if sku not in registry:
        results.append({
            "sku":sku,
            "ok":False,
            "reason":"missing_registry_sku"
        })
        continue

    registry[sku]["seo_title"]=item["seo_title"]
    registry[sku]["seo_description"]=item["seo_description"]
    registry[sku]["seo_tags"]=item["seo_tags"]

    registry[sku]["seo_applied"]=True
    registry[sku]["seo_applied_at"]=datetime.now(
        timezone.utc
    ).isoformat()

    results.append({
        "sku":sku,
        "ok":True
    })

REGISTRY.write_text(
    json.dumps(registry,indent=2),
    encoding="utf-8"
)

OUT.write_text(
    json.dumps(results,indent=2),
    encoding="utf-8"
)

print(
    "SEO MASS APPLY:",
    sum(x["ok"] for x in results),
    "/",
    len(results)
)
