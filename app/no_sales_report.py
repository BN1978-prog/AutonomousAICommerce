import json
from pathlib import Path

IMPORTS = Path("app/logs/imported_skus.json")
REPORT = Path("app/logs/no_sales_report.json")

imports = json.loads(IMPORTS.read_text(encoding="utf-8"))

items = []

for sku, data in imports.items():
    sales = int(data.get("sales", 0) or 0)

    if sales == 0:
        items.append({
            "sku": sku,
            "status": data.get("status"),
            "score": data.get("last_score"),
            "price": data.get("last_price"),
            "source": data.get("source"),
            "ebay_status": data.get("ebay_status"),
            "product_id": data.get("product_id")
        })

REPORT.write_text(
    json.dumps(items, indent=2),
    encoding="utf-8"
)

print("NO SALES SKUS:", len(items))
print("REPORT:", REPORT)
