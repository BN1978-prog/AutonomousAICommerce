import json
from pathlib import Path
from datetime import datetime, timezone

Q = Path("app/logs/autopilot_priority_queue.json")
OUT = Path("app/logs/publish_execution_plan.json")

data=json.loads(Q.read_text(encoding="utf-8"))

actions=[]

for item in data.get("queue",[])[:3]:

    actions.append({
        "sku": item["sku"],
        "priority": item["priority"],
        "actions":[
            "increase_social_posts",
            "increase_testing_frequency",
            "consider_campaign_candidate"
        ]
    })

report={
    "created_at":datetime.now(timezone.utc).isoformat(),
    "items_selected":len(actions),
    "execution_plan":actions,
    "status":"PUBLISH_EXECUTION_PLAN_READY"
}

OUT.write_text(
    json.dumps(report,indent=2),
    encoding="utf-8"
)

print(json.dumps(report,indent=2))
