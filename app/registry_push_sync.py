import json
from pathlib import Path
from datetime import datetime, timezone

REGISTRY=Path("app/logs/imported_skus.json")
EXECUTION=Path("app/logs/seo_mass_push_execution.json")

registry=json.loads(REGISTRY.read_text(encoding="utf-8"))
execution=json.loads(EXECUTION.read_text(encoding="utf-8"))

by_sku={}

for row in execution:
    if row.get("ok") is not True:
        continue

    if row.get("pushed") is not True:
        continue

    sku=row["sku"]
    channel=row["channel"]

    by_sku.setdefault(sku,[])
    if channel not in by_sku[sku]:
        by_sku[sku].append(channel)

for sku,channels in by_sku.items():
    if sku not in registry:
        continue

    registry[sku]["seo_push_completed"]=True
    registry[sku]["seo_push_channels"]=channels
    registry[sku]["seo_push_completed_at"]=datetime.now(timezone.utc).isoformat()

REGISTRY.write_text(json.dumps(registry,indent=2),encoding="utf-8")

print("UPDATED SKU:",len(by_sku))
