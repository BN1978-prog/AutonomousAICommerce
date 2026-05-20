import json
from pathlib import Path

IMPORTS = Path("app/logs/imported_skus.json")
OUT = Path("app/logs/roi_report.json")

data = json.loads(IMPORTS.read_text(encoding="utf-8"))

rows = []

for sku, meta in data.items():
    price = float(meta.get("last_price") or 0)
    cost = float(meta.get("last_cost") or 0)
    sales = int(meta.get("sales") or 0)

    revenue = round(price * sales, 2)
    profit = round((price - cost) * sales, 2)

    rows.append({
        "sku": sku,
        "channel": "shopify_ebay",
        "price": price,
        "cost": cost,
        "sales": sales,
        "revenue": revenue,
        "profit": profit,
        "ebay_status": meta.get("ebay_status"),
        "shopify_product_id": meta.get("product_id")
    })

OUT.write_text(json.dumps(rows, indent=2), encoding="utf-8")

print("=== ROI REPORT ===")
print("SKUS:", len(rows))
print("TOTAL SALES:", sum(x["sales"] for x in rows))
print("TOTAL REVENUE:", round(sum(x["revenue"] for x in rows), 2))
print("TOTAL PROFIT:", round(sum(x["profit"] for x in rows), 2))

print("\nTOP PROFIT:")
for r in sorted(rows, key=lambda x: x["profit"], reverse=True)[:10]:
    print(r["sku"], "profit=", r["profit"], "revenue=", r["revenue"], "sales=", r["sales"])
