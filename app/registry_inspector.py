import json
from pathlib import Path

IMPORTS = Path("app/logs/imported_skus.json")

data = json.loads(
    IMPORTS.read_text(encoding="utf-8")
)

for sku, item in list(data.items())[:10]:

    print("="*50)
    print("SKU:", sku)

    for k,v in item.items():
        print(f"{k}: {v}")
