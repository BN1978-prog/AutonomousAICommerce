import json
from pathlib import Path
from datetime import datetime, timezone

REGISTRY=Path("app/logs/imported_skus.json")
OUT=Path("app/logs/click_tracking_state.json")

registry=json.loads(
    REGISTRY.read_text(
        encoding="utf-8"
    )
)

items=[]

for sku,data in registry.items():

    if data.get("pipeline_active",True) is False:
        continue

    items.append({
        "sku":sku,
        "impressions":0,
        "clicks":0,
        "ctr":0,
        "add_to_cart":0,
        "orders":0,
        "revenue":0,
        "roi":None
    })

report={
    "created_at":datetime.now(
        timezone.utc
    ).isoformat(),
    "sku_count":len(items),
    "items":items
}

OUT.write_text(
    json.dumps(
        report,
        indent=2
    ),
    encoding="utf-8"
)

print(
    "TRACKED SKU:",
    len(items)
)
