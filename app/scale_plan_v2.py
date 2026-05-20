import json
from pathlib import Path

PLAN=Path("app/logs/scale_plan.json")
OUT=Path("app/logs/scale_plan_v2.json")

data=json.loads(
    PLAN.read_text(
        encoding="utf-8"
    )
)

new=[]

for item in data:

    score=item["score"]

    if score>=80:
        budget=2.0
        priority="critical"

    elif score>=60:
        budget=1.5
        priority="high"

    else:
        budget=1.2
        priority="medium"

    item["budget_multiplier"]=budget
    item["priority"]=priority

    new.append(item)

OUT.write_text(
    json.dumps(
        new,
        indent=2
    ),
    encoding="utf-8"
)

print("UPDATED:",len(new))

print(
    "CRITICAL:",
    sum(
        1 for x in new
        if x["priority"]=="critical"
    )
)
