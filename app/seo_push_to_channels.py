import json
from pathlib import Path
from datetime import datetime, timezone

IMPORTS = Path("app/logs/imported_skus.json")
OUT = Path("app/logs/seo_push_plan.json")

data = json.loads(IMPORTS.read_text(encoding="utf-8"))

plan = []

for sku, meta in data.items():
    if meta.get("seo_auto_applied") is not True:
        continue

    channels = []

    if meta.get("product_id"):
        channels.append("shopify")

    if meta.get("ebay_status") == "published":
        channels.append("ebay")

    channels.append("woocommerce")
    channels.append("meta_feed")
    channels.append("google_feed")

    plan.append({
        "sku": sku,
        "title": meta.get("title"),
        "description": meta.get("description"),
        "tags": meta.get("tags"),
        "channels": channels,
        "status": "ready_to_push",
        "live_push": False,
        "created_at": datetime.now(timezone.utc).isoformat()
    })

OUT.write_text(
    json.dumps(plan, indent=2),
    encoding="utf-8"
)

print("SEO PUSH PLAN:", len(plan))

for x in plan:
    print(x["sku"], "=>", ", ".join(x["channels"]))
