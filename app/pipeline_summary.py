import json
from pathlib import Path

imports = Path("app/logs/imported_skus.json")

data = json.loads(
    imports.read_text(encoding="utf-8")
)

created=0
updated=0
published=0

for sku,meta in data.items():

    status = str(meta.get("status",""))
    update_status = str(meta.get("last_update_status",""))

    if "draft" in status or "imported" in status:
        created += 1

    if update_status=="updated":
        updated += 1

    if meta.get("ebay_listing_id") or meta.get("ebay_status") == "published":
        published += 1

print("=== PIPELINE SUMMARY ===")
print("CREATED:",created)
print("UPDATED:",updated)
print("EBAY PUBLISHED:",published)
