import json
from pathlib import Path
from datetime import datetime, timezone

IMPORTS = Path("app/logs/imported_skus.json")
OUT = Path("app/logs/conversion_watch.json")

data = json.loads(IMPORTS.read_text(encoding="utf-8"))

now = datetime.now(timezone.utc)
report=[]

for sku,meta in data.items():

    created=meta.get("created_at")
    if not created:
        continue

    age=(now-datetime.fromisoformat(created)).days

    sales=int(meta.get("sales",0) or 0)
    score=int(meta.get("last_score",0) or 0)

    action="watch"

    if sales>0:
        action="scale"

    elif age>=14 and sales==0:
        action="consider_disable"

    elif score>=80:
        action="promote"

    report.append({
        "sku":sku,
        "days_live":age,
        "sales":sales,
        "score":score,
        "price":meta.get("last_price"),
        "recommended_action":action
    })

OUT.write_text(
    json.dumps(report,indent=2),
    encoding="utf-8"
)

print("WATCH ITEMS:",len(report))
print("REPORT:",OUT)
