import json
from pathlib import Path

PERFORMANCE = Path("app/logs/product_performance.json")
PUBLISHED = Path("app/logs/published_posts.json")
AUTOPILOT = Path("app/logs/autopilot_run.json")

performance = json.loads(PERFORMANCE.read_text(encoding="utf-8-sig"))
published = json.loads(PUBLISHED.read_text(encoding="utf-8-sig")) if PUBLISHED.exists() else []
autopilot = json.loads(AUTOPILOT.read_text(encoding="utf-8-sig")) if AUTOPILOT.exists() else {}

print("=== AICommerce Autopilot Report ===")
print()

print("Products ranking:")
for product_id, data in sorted(performance.items(), key=lambda x: x[1].get("score", 0), reverse=True):
    print(
        f"- {product_id}: "
        f"score={data.get('score',0)}, "
        f"sales={data.get('sales',0)}, "
        f"clicks={data.get('clicks',0)}, "
        f"published={data.get('published',0)}"
    )

print()
print("Published posts:", len(published))

if published:
    last = published[-1]
    print("Last post ID:", last.get("post_id"))
    print("Last post preview:", last.get("text_preview"))

print()
print("Last autopilot mode:", autopilot.get("mode"))
print("Last autopilot time:", autopilot.get("created_at"))

print()
print("Last steps:")
for step in autopilot.get("steps", []):
    status = step.get("status","OK" if step.get("returncode")==0 else "ERROR")
    print(f"- {step.get('name')}: {status}")


print()
print("Exploration v2:")
try:
    exp_path = Path("app/logs/exploration_v2.json")
    if exp_path.exists():
        exp = json.loads(exp_path.read_text(encoding="utf-8-sig"))
        print("Status:", exp.get("status"))
        print("Cooldown count:", exp.get("cooldown_count"))
        print("Top exploration candidates:")
        for item in exp.get("top_candidates", [])[:5]:
            print(
                "- "
                + str(item.get("id") or item.get("product_id") or item.get("sku") or item.get("title"))
                + ": exploration_score="
                + str(item.get("exploration_score"))
                + ", boost="
                + str(item.get("exploration_boost"))
                + ", cooldown="
                + str(item.get("cooldown"))
            )
    else:
        print("No exploration_v2.json found")
except Exception as e:
    print("Exploration v2 report error:", e)
