import json
from pathlib import Path
from datetime import datetime, timezone

PLAN = Path("app/logs/publish_execution_plan.json")
OUT = Path("app/logs/action_executor.json")

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "actions_created": 0,
    "actions": [],
    "status": "NO_PLAN"
}

if PLAN.exists():

    data=json.loads(
        PLAN.read_text(encoding="utf-8-sig")
    )

    actions=[]

    for item in data.get("execution_plan",[]):

        sku=item.get("sku")

        for action in item.get("actions",[]):

            actions.append({
                "sku":sku,
                "action":action,
                "status":"scheduled"
            })

    report={
        "created_at": datetime.now(timezone.utc).isoformat(),
        "actions_created":len(actions),
        "actions":actions,
        "status":"ACTION_EXECUTOR_READY"
    }

OUT.write_text(
    json.dumps(report,indent=2),
    encoding="utf-8"
)

print(json.dumps(report,indent=2))
