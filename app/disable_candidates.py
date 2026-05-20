import json
from pathlib import Path
from datetime import datetime, timezone

IMPORTS = Path("app/logs/imported_skus.json")
REPORT = Path("app/logs/disable_candidates.json")

DAYS_LIMIT = 14

data = json.loads(IMPORTS.read_text(encoding="utf-8"))
now = datetime.now(timezone.utc)

candidates = []

for sku, meta in data.items():
    sales = int(meta.get("sales", 0) or 0)
    created_at = meta.get("created_at")

    if not created_at:
        continue

    age_days = (now - datetime.fromisoformat(created_at)).days

    if sales == 0 and age_days >= DAYS_LIMIT:
        candidates.append({
            "sku": sku,
            "age_days": age_days,
            "sales": sales,
            "score": meta.get("last_score"),
            "ebay_status": meta.get("ebay_status"),
            "product_id": meta.get("product_id")
        })

REPORT.write_text(
    json.dumps(candidates, indent=2),
    encoding="utf-8"
)

print("DISABLE CANDIDATES:", len(candidates))
print("REPORT:", REPORT)
