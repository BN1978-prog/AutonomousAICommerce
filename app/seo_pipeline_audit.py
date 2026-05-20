import json
from pathlib import Path

REGISTRY=Path("app/logs/imported_skus.json")
OUT=Path("app/logs/seo_pipeline_audit.json")

data=json.loads(REGISTRY.read_text(encoding="utf-8"))

total=len(data)
seo_applied=0
push_completed=0
pushed_5_channels=0

items=[]

for sku,item in data.items():

    channels=item.get("seo_push_channels") or []

    row={
        "sku":sku,
        "seo_applied":item.get("seo_applied") is True,
        "seo_push_completed":item.get("seo_push_completed") is True,
        "channels":channels,
        "channel_count":len(channels),
        "title":item.get("seo_title") or item.get("title")
    }

    if row["seo_applied"]:
        seo_applied+=1

    if row["seo_push_completed"]:
        push_completed+=1

    if len(channels)==5:
        pushed_5_channels+=1

    items.append(row)

report={
    "total_skus":total,
    "seo_applied":seo_applied,
    "push_completed":push_completed,
    "pushed_5_channels":pushed_5_channels,
    "items":items
}

OUT.write_text(
    json.dumps(report,indent=2),
    encoding="utf-8"
)

print("TOTAL:",total)
print("SEO APPLIED:",seo_applied)
print("PUSH COMPLETED:",push_completed)
print("PUSHED 5 CHANNELS:",pushed_5_channels)
