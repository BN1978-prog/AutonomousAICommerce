import json
from pathlib import Path

PERFORMANCE=Path("app/logs/product_performance.json")

performance=json.loads(
    PERFORMANCE.read_text(
        encoding="utf-8-sig"
    )
)

decisions=[]

for product_id,data in performance.items():

    score=data.get("score",0)
    sales=data.get("sales",0)
    clicks=data.get("clicks",0)
    published=data.get("published",0)

    action="keep_testing"
    reason="Not enough data yet"

    if sales>=3 and score>=50:

        if published>=16:
            action="pause"
            reason="Hard limit reached"

        elif published>=8:
            action="cooldown"
            reason="Reduce frequency"

        else:
            action="scale"
            reason="Strong sales and high score"

    elif clicks>=10 and sales==0:
        action="test_new_angle"
        reason="Clicks exist but no sales yet"

    decisions.append({
        "product_id":product_id,
        "action":action,
        "reason":reason,
        "score":score,
        "sales":sales,
        "clicks":clicks,
        "published":published
    })

Path(
    "app/logs/autopilot_decisions.json"
).write_text(
    json.dumps(
        decisions,
        indent=2
    ),
    encoding="utf-8"
)

print("=== Autopilot Decisions ===")

for d in decisions:
    print(
        f"{d['product_id']}: "
        f"{d['action']} "
        f"(published={d['published']})"
    )

