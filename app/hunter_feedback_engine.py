import json
from pathlib import Path

ROI=Path("app/logs/sales_roi_report.json")
OUT=Path("app/logs/hunter_feedback.json")

data=json.loads(
    ROI.read_text(
        encoding="utf-8"
    )
)

feedback=[]

for item in data:

    score=0

    sales=item["sales"]
    roi=item["roi"]

    if sales>=10:
        score+=50

    elif sales>=5:
        score+=25

    if roi>=80:
        score+=30

    if item["status"]=="winner":
        decision="boost"

    elif item["status"]=="loser":
        decision="reduce"

    else:
        decision="hold"

    feedback.append({

        "sku":item["sku"],
        "title":item["title"],
        "hunter_score":score,
        "decision":decision
    })

OUT.write_text(
    json.dumps(
        feedback,
        indent=2
    ),
    encoding="utf-8"
)

print(
    "FEEDBACK GENERATED:",
    len(feedback)
)

print(
    "BOOST:",
    sum(
        1 for x in feedback
        if x["decision"]=="boost"
    )
)

print(
    "REDUCE:",
    sum(
        1 for x in feedback
        if x["decision"]=="reduce"
    )
)
