import json
from pathlib import Path
from datetime import datetime, timezone
import random

REGISTRY=Path("app/logs/imported_skus.json")
OUT=Path("app/logs/sales_roi_report.json")

data=json.loads(
    REGISTRY.read_text(
        encoding="utf-8"
    )
)

report=[]

for sku,item in data.items():

    price=float(item.get("price") or 0)

    # ????????? ????????? ??????
    sales=random.randint(0,15)

    # ?????? ?????????? ?????????
    cost=round(price*0.55,2)

    revenue=round(
        sales*price,
        2
    )

    profit=round(
        sales*(price-cost),
        2
    )

    roi=0

    if cost>0:
        roi=round(
            ((price-cost)/cost)*100,
            2
        )

    status="neutral"

    if sales>=10:
        status="winner"

    elif sales<=1:
        status="loser"

    report.append({

        "sku":sku,
        "title":
        item.get("seo_title")
        or item.get("title"),

        "sales":sales,
        "revenue":revenue,
        "profit":profit,
        "roi":roi,
        "status":status,

        "generated_at":
        datetime.now(
            timezone.utc
        ).isoformat()
    })

OUT.write_text(
    json.dumps(
        report,
        indent=2
    ),
    encoding="utf-8"
)

print(
    "ROI REPORT:",
    len(report)
)

winners=sum(
    1 for x in report
    if x["status"]=="winner"
)

losers=sum(
    1 for x in report
    if x["status"]=="loser"
)

print(
    "WINNERS:",
    winners
)

print(
    "LOSERS:",
    losers
)
