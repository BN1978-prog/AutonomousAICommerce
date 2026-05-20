import json
from pathlib import Path
from datetime import datetime, timezone

REGISTRY=Path("app/logs/imported_skus.json")
OUT=Path("app/logs/seo_mass_push_plan.json")

data=json.loads(REGISTRY.read_text(encoding="utf-8"))

plan=[]

for sku,item in data.items():

    if item.get("seo_applied") is not True:
        continue

    channels=[]

    if item.get("product_id"):
        channels.append("shopify")

    if item.get("ebay_status")=="published":
        channels.append("ebay")

    channels.append("woocommerce")
    channels.append("meta_feed")
    channels.append("google_feed")

    plan.append({
        "sku":sku,
        "product_id":item.get("product_id"),
        "title":item.get("seo_title") or item.get("title"),
        "description":item.get("seo_description") or item.get("description"),
        "tags":item.get("seo_tags") or item.get("tags"),
        "channels":channels,
        "status":"ready_to_push",
        "live_push":False,
        "created_at":datetime.now(timezone.utc).isoformat()
    })

OUT.write_text(
    json.dumps(plan,indent=2),
    encoding="utf-8"
)

print("SEO MASS PUSH PLAN:",len(plan))

for x in plan:
    print(x["sku"], "=>", ", ".join(x["channels"]))
