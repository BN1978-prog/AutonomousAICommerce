import json
from pathlib import Path

CATALOG = Path("app/logs/product_catalog.json")
PERFORMANCE = Path("app/logs/product_performance.json")

catalog = json.loads(CATALOG.read_text(encoding="utf-8-sig"))
performance = json.loads(PERFORMANCE.read_text(encoding="utf-8-sig"))

added = 0

for p in catalog:
    product_id = p["id"]
    if product_id not in performance:
        performance[product_id] = {
            "published": 0,
            "clicks": 0,
            "sales": 0,
            "score": 0
        }
        added += 1

PERFORMANCE.write_text(json.dumps(performance, indent=2), encoding="utf-8")

print("Performance synced")
print("Added products:", added)
print("Total products:", len(performance))
