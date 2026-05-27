import json
from pathlib import Path
from datetime import datetime, timezone

SRC = Path("app/logs/daily_summary.txt")
OUT = Path("app/logs/product_guardrails.json")

rules = {
    "min_clicks_before_judgement": 20,
    "max_sales_for_loser": 0,
    "max_score_for_loser": 5
}

items = []

text = SRC.read_text(encoding="utf-8") if SRC.exists() else ""

for line in text.splitlines():
    if line.startswith("- ") and "score=" in line:
        sku = line.split(":")[0].replace("- ","").strip()

        try:
            score = int(line.split("score=")[1].split(",")[0])
            sales = int(line.split("sales=")[1].split(",")[0])
            clicks = int(line.split("clicks=")[1].split(",")[0])
        except Exception:
            continue

        loser = (
            clicks >= rules["min_clicks_before_judgement"]
            and sales <= rules["max_sales_for_loser"]
            and score <= rules["max_score_for_loser"]
        )

        items.append({
            "sku": sku,
            "score": score,
            "sales": sales,
            "clicks": clicks,
            "guardrail_status": "STOP_TESTING" if loser else "CONTINUE",
            "reason": "enough_clicks_no_sales_low_score" if loser else "not_loser"
        })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "rules": rules,
    "items": items,
    "stop_testing": [x for x in items if x["guardrail_status"] == "STOP_TESTING"],
    "live_money_spending": False,
    "status": "PRODUCT_GUARDRAILS_READY_SAFE_MODE"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

print(json.dumps(report, indent=2))
