import json
from pathlib import Path

HUNTER=Path("app/logs/hunter_promoted.json")
IMPORTS=Path("app/logs/imported_skus.json")

hunter=json.loads(HUNTER.read_text(encoding="utf-8"))

imports={}
if IMPORTS.exists():
    imports=json.loads(IMPORTS.read_text(encoding="utf-8"))

added=0

for item in hunter:

    sku=item["sku"]

    if sku in imports:
        continue

    imports[sku]={
        "status":"hunter_imported",
        "last_score":round(item["score"]*100),
        "last_price":item["price"],
        "source":"ai_hunter"
    }

    added+=1

IMPORTS.write_text(
    json.dumps(imports,indent=2),
    encoding="utf-8"
)

print("HUNTER IMPORTED:",added)
