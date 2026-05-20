import json
from pathlib import Path
from datetime import datetime, timezone

REGISTRY=Path("app/logs/imported_skus.json")
OUT=Path("app/logs/seo_repush_required.json")

data=json.loads(REGISTRY.read_text(encoding="utf-8"))

items=[]

for sku,item in data.items():
    if item.get("seo_quality_fixed") is True:
        items.append({
            "sku":sku,
            "title":item.get("seo_title"),
            "channels":item.get("seo_push_channels",[]),
            "reason":"seo_quality_fixed_after_push",
            "created_at":datetime.now(timezone.utc).isoformat()
        })

OUT.write_text(json.dumps(items,indent=2),encoding="utf-8")

print("REPUSH REQUIRED:",len(items))
