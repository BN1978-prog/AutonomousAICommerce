import json
from pathlib import Path
from datetime import datetime, timezone

PLAN = Path("app/logs/publish_execution_plan.json")
OUT = Path("app/logs/social_content_plan.json")

data = json.loads(PLAN.read_text(encoding="utf-8-sig")) if PLAN.exists() else {}

posts = []

for item in data.get("execution_plan", []):
    sku = item.get("sku")
    title = sku.replace("_", " ").title()

    posts.append({
        "sku": sku,
        "platforms": ["facebook", "instagram"],
        "status": "draft_ready",
        "post_text": (
            f"Looking for a useful pet product? "
            f"Check out {title}. Practical, simple and selected for pet owners."
        ),
        "cta": "Shop now",
        "mode": "draft_only_no_auto_publish"
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "posts_created": len(posts),
    "posts": posts,
    "status": "SOCIAL_CONTENT_PLAN_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
