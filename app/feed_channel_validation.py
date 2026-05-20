import json
from pathlib import Path
from datetime import datetime, timezone

REGISTRY=Path("app/logs/imported_skus.json")
GOOGLE=Path("app/logs/google_feed_seo.json")
META=Path("app/logs/meta_feed_seo.json")
OUT=Path("app/logs/feed_channel_validation.json")

registry=json.loads(REGISTRY.read_text(encoding="utf-8"))

required=[
    "sku",
    "title",
    "description",
    "price",
    "image",
    "product_url"
]

def load_json(path):
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))

feeds={
    "google_feed":load_json(GOOGLE),
    "meta_feed":load_json(META)
}

active_skus={
    sku for sku,item in registry.items()
    if item.get("pipeline_active",True) is True
    and item.get("hunter_decision")!="exclude"
}

report=[]

for feed_name,items in feeds.items():

    feed_skus={x.get("sku") for x in items}
    missing_skus=sorted(list(active_skus-feed_skus))

    bad_items=[]

    for item in items:
        missing=[
            field for field in required
            if item.get(field) in [None,"",[]]
        ]

        if missing:
            bad_items.append({
                "sku":item.get("sku"),
                "missing":missing
            })

    ok=len(missing_skus)==0 and len(bad_items)==0

    report.append({
        "feed":feed_name,
        "ok":ok,
        "items_in_feed":len(items),
        "active_skus_expected":len(active_skus),
        "missing_skus":missing_skus,
        "bad_items":bad_items,
        "checked_at":datetime.now(timezone.utc).isoformat()
    })

OUT.write_text(
    json.dumps(report,indent=2),
    encoding="utf-8"
)

for r in report:
    print(
        r["feed"],
        "ok=",
        r["ok"],
        "items=",
        r["items_in_feed"],
        "expected=",
        r["active_skus_expected"],
        "missing=",
        len(r["missing_skus"]),
        "bad=",
        len(r["bad_items"])
    )
