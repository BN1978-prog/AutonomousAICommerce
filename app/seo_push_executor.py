import json
from pathlib import Path
from datetime import datetime, timezone

PLAN = Path("app/logs/seo_push_plan.json")
OUT = Path("app/logs/seo_push_results.json")

plan = json.loads(PLAN.read_text(encoding="utf-8")) if PLAN.exists() else []

results = []

for item in plan:
    sku = item.get("sku")
    live_push = item.get("live_push") is True

    for channel in item.get("channels", []):
        if not live_push:
            results.append({
                "sku": sku,
                "channel": channel,
                "ok": True,
                "pushed": False,
                "reason": "dry_run_live_push_false",
                "title": item.get("title"),
                "checked_at": datetime.now(timezone.utc).isoformat()
            })
            continue

        results.append({
            "sku": sku,
            "channel": channel,
            "ok": False,
            "pushed": False,
            "reason": "live_push_not_implemented_yet",
            "checked_at": datetime.now(timezone.utc).isoformat()
        })

OUT.write_text(
    json.dumps(results, indent=2),
    encoding="utf-8"
)

print("SEO PUSH RESULTS:", len(results))

for r in results:
    print(
        r["sku"],
        r["channel"],
        "pushed=",
        r["pushed"],
        "reason=",
        r["reason"]
    )
