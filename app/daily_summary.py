import json
from pathlib import Path
from datetime import datetime, timezone

PERFORMANCE = Path("app/logs/product_performance.json")
AUTOPILOT = Path("app/logs/autopilot_run.json")
PRIORITY = Path("app/logs/autopilot_priority_queue.json")
OUT = Path("app/logs/daily_summary.txt")

performance = json.loads(PERFORMANCE.read_text(encoding="utf-8-sig")) if PERFORMANCE.exists() else {}
autopilot = json.loads(AUTOPILOT.read_text(encoding="utf-8-sig")) if AUTOPILOT.exists() else {}
priority = json.loads(PRIORITY.read_text(encoding="utf-8-sig")) if PRIORITY.exists() else {}

summary = []
summary.append("AICommerce Daily Autopilot Summary")
summary.append("=" * 40)
summary.append("Created at: " + datetime.now(timezone.utc).isoformat())
summary.append("")

summary.append("Top products:")
for product_id, data in sorted(performance.items(), key=lambda x: x[1].get("score", 0), reverse=True)[:10]:
    summary.append(
        f"- {product_id}: "
        f"score={data.get('score',0)}, "
        f"sales={data.get('sales',0)}, "
        f"clicks={data.get('clicks',0)}, "
        f"published={data.get('published',0)}"
    )

summary.append("")
summary.append("Next test priorities:")
for item in priority.get("queue", [])[:5]:
    summary.append(
        f"- #{item.get('priority')} {item.get('sku')}: "
        f"score={item.get('exploration_score')}, "
        f"action={item.get('action')}"
    )

if not priority.get("queue"):
    summary.append("- No priority queue found")

summary.append("")
summary.append("Last autopilot steps:")
for step in autopilot.get("steps", []):
    summary.append(f"- {step.get('name')}: {step.get('status', 'OK' if step.get('returncode') == 0 else 'ERROR')}")

OUT.write_text("\n".join(summary), encoding="utf-8")
print("Daily summary created:", OUT)
print("\n".join(summary))
