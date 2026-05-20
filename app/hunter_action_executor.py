import json
from pathlib import Path
from datetime import datetime, timezone

REGISTRY=Path("app/logs/imported_skus.json")
PLAN=Path("app/logs/hunter_action_plan.json")
OUT=Path("app/logs/hunter_action_execution.json")

registry=json.loads(REGISTRY.read_text(encoding="utf-8"))
plan=json.loads(PLAN.read_text(encoding="utf-8"))

results=[]

for row in plan:

    sku=row["sku"]
    action=row["action"]

    if sku not in registry:
        continue

    if action=="increase_budget_and_priority":
        registry[sku]["priority_level"]="high"
        registry[sku]["budget_multiplier"]=1.5

    elif action=="reduce_visibility_or_pause_testing":
        registry[sku]["priority_level"]="low"
        registry[sku]["budget_multiplier"]=0.5

    elif action=="remove_from_pet_pipeline":
        registry[sku]["pipeline_active"]=False

    else:
        registry[sku]["priority_level"]="normal"
        registry[sku]["budget_multiplier"]=1.0

    registry[sku]["action_executed_at"]=(
        datetime.now(timezone.utc).isoformat()
    )

    results.append({
        "sku":sku,
        "action":action,
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

print("EXECUTED:",len(results))
