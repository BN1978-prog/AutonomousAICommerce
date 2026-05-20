import json
from pathlib import Path

sku = "REAL-MOCK-004"

files = [
    "app/logs/image_failed_skus.json",
    "app/logs/imported_skus.json",
    "app/logs/blocked_products.json",
    "app/logs/stock_state.json"
]

for f in files:
    p = Path(f)
    if not p.exists():
        continue

    data = json.loads(p.read_text(encoding="utf-8"))

    if isinstance(data, list):
        data = [
            x for x in data
            if not (
                x == sku or
                (isinstance(x,dict) and x.get("sku")==sku)
            )
        ]

    elif isinstance(data, dict):
        data.pop(sku, None)

    p.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print("cleaned:", f)

print("DONE")
