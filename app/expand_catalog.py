import json
from pathlib import Path
from datetime import datetime, timezone

CATALOG = Path("app/logs/product_catalog.json")

new_products = [
    {
        "id":"pet_water_fountain",
        "name":"automatic pet water fountain",
        "category":"pet hydration",
        "angle":"keeps water fresh and encourages pets to drink more",
        "hashtags":"#petwater #catcare #dogcare #petproducts",
        "url":"https://aicommerce-test-store-2.myshopify.com"
    },
    {
        "id":"pet_bed",
        "name":"soft pet bed",
        "category":"pet comfort",
        "angle":"gives cats and dogs a cozy place to rest",
        "hashtags":"#petbed #petcomfort #doglife #catlife",
        "url":"https://aicommerce-test-store-2.myshopify.com"
    }
]

catalog = json.loads(CATALOG.read_text(encoding="utf-8-sig"))

existing = {x["id"] for x in catalog}

added = 0
for p in new_products:
    if p["id"] not in existing:
        catalog.append(p)
        added += 1

CATALOG.write_text(
    json.dumps(catalog, indent=2),
    encoding="utf-8"
)

print("Catalog updated")
print("Added:", added)
print("Total:", len(catalog))
print("Time:", datetime.now(timezone.utc).isoformat())
