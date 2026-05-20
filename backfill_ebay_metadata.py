import json
from pathlib import Path

imports_path = Path("app/logs/imported_skus.json")
ebay_path = Path("app/logs/ebay_published_skus.json")

imports = json.loads(imports_path.read_text(encoding="utf-8"))
ebay = json.loads(ebay_path.read_text(encoding="utf-8"))

count = 0

for sku, meta in ebay.items():
    if sku not in imports:
        continue

    if meta.get("status") == "published":
        imports[sku]["ebay_status"] = "published"
        imports[sku]["ebay_offer_id"] = meta.get("offer_id")
        imports[sku]["ebay_listing_id"] = meta.get("listing_id")
        count += 1

imports_path.write_text(json.dumps(imports, indent=2), encoding="utf-8")

print("BACKFILLED:", count)
