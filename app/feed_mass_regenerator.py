import json
from pathlib import Path
from datetime import datetime, timezone

REGISTRY=Path("app/logs/imported_skus.json")
GOOGLE=Path("app/logs/google_feed_seo.json")
META=Path("app/logs/meta_feed_seo.json")

data=json.loads(REGISTRY.read_text(encoding="utf-8"))

items=[]

for sku,item in data.items():

    if item.get("pipeline_active",True) is False:
        continue

    if item.get("hunter_decision")=="exclude":
        continue

    feed_item={
        "sku":sku,
        "title":item.get("seo_title") or item.get("title"),
        "description":item.get("seo_description") or item.get("description"),
        "tags":item.get("seo_tags") or item.get("tags") or [],
        "price":item.get("price"),
        "image":item.get("image"),
        "product_url":item.get("product_url"),
        "updated_at":datetime.now(timezone.utc).isoformat()
    }

    items.append(feed_item)

google_items=[]

for x in items:
    y=dict(x)
    y["feed"]="google"
    google_items.append(y)

meta_items=[]

for x in items:
    y=dict(x)
    y["feed"]="meta"
    meta_items.append(y)

GOOGLE.write_text(
    json.dumps(google_items,indent=2),
    encoding="utf-8"
)

META.write_text(
    json.dumps(meta_items,indent=2),
    encoding="utf-8"
)

print("GOOGLE FEED:",len(google_items))
print("META FEED:",len(meta_items))
