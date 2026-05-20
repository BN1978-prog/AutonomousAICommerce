import json
from pathlib import Path

REGISTRY=Path("app/logs/imported_skus.json")
OUT=Path("app/logs/hunter_action_plan.json")

data=json.loads(REGISTRY.read_text(encoding="utf-8"))

actions=[]

for sku,item in data.items():

    decision=item.get("hunter_decision")

    if decision=="boost":
        action="increase_budget_and_priority"

    elif decision=="reduce":
        action="reduce_visibility_or_pause_testing"

    elif decision=="exclude":
        action="remove_from_pet_pipeline"

    else:
        action="keep_monitoring"

    actions.append({
        "sku":sku,
        "decision":decision,
        "action":action,
        "title":item.get("seo_title") or item.get("title")
    })

OUT.write_text(json.dumps(actions,indent=2),encoding="utf-8")

print("ACTION PLAN:",len(actions))
print("BOOST:",sum(1 for x in actions if x["decision"]=="boost"))
print("REDUCE:",sum(1 for x in actions if x["decision"]=="reduce"))
print("EXCLUDE:",sum(1 for x in actions if x["decision"]=="exclude"))
