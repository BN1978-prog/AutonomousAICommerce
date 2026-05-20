import json
from pathlib import Path

ACTIONS = Path("app/logs/promotion_actions.json")
OUT = Path("app/logs/promotion_plan.md")

items = json.loads(ACTIONS.read_text(encoding="utf-8")) if ACTIONS.exists() else []

lines = []
lines.append("# Promotion Plan")
lines.append("")
lines.append("## Priority Products")
lines.append("")

for item in items:
    sku = item.get("sku")
    score = item.get("score")
    actions = item.get("actions", [])

    lines.append(f"### {sku}")
    lines.append(f"- Score: {score}")
    lines.append("- Actions:")

    for action in actions:
        lines.append(f"  - {action}")

    lines.append("")

OUT.write_text(
    "\n".join(lines),
    encoding="utf-8"
)

print("PROMOTION PLAN:", OUT)
print(OUT.read_text(encoding="utf-8"))
