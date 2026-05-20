import json
from pathlib import Path

IN=Path("app/logs/real_sales_report.json")
OUT=Path("app/logs/real_sales_report_filtered.json")

d=json.loads(
    IN.read_text(
        encoding="utf-8"
    )
)

items=[
    x for x in d["items"]
    if x["total_quantity"]>0
]

report={
    "created_at":d["created_at"],
    "sku_count":len(items),
    "total_quantity":sum(
        x["total_quantity"]
        for x in items
    ),
    "total_revenue":round(
        sum(
            x["total_revenue"]
            for x in items
        ),
        2
    ),
    "items":items
}

OUT.write_text(
    json.dumps(
        report,
        indent=2
    ),
    encoding="utf-8"
)

print(
    "ACTIVE SALES SKU:",
    report["sku_count"]
)
