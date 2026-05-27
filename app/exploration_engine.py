import json, random
from pathlib import Path

DECISIONS = Path("app/logs/autopilot_decisions.json")

d = json.loads(DECISIONS.read_text(encoding="utf-8-sig"))

top = [x for x in d if x["action"]=="scale"]
new = [x for x in d if x["score"]==0]

selected = []

selected.extend(top[:2])

if new:
    selected.extend(random.sample(
        new,
        min(3, len(new))
    ))

print("=== Exploration Picks ===")

for x in selected:
    print(
        f"{x['product_id']} | "
        f"score={x['score']} | "
        f"action={x['action']}"
    )

Path("app/logs/exploration_candidates.json").write_text(
    json.dumps(selected, indent=2),
    encoding="utf-8"
)
