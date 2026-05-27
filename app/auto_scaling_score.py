from app.alert_dispatcher import notify
import json
from pathlib import Path
from datetime import datetime, timezone

SRC = Path("app/logs/daily_summary.txt")
OUT = Path("app/logs/auto_scaling_score.json")

rules = {
    "min_score_for_scale_candidate": 50,
    "min_sales_for_scale_candidate": 3,
    "min_clicks_for_scale_candidate": 20
}

candidates = []

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

        scale_candidate = (
            score >= rules["min_score_for_scale_candidate"]
            and sales >= rules["min_sales_for_scale_candidate"]
            and clicks >= rules["min_clicks_for_scale_candidate"]
        )

        candidates.append({
            "sku": sku,
            "score": score,
            "sales": sales,
            "clicks": clicks,
            "scale_candidate": scale_candidate,
            "recommended_action": "PREPARE_SCALING_REVIEW" if scale_candidate else "KEEP_TESTING"
        })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "rules": rules,
    "candidates": candidates,
    "scale_ready": [x for x in candidates if x["scale_candidate"]],
    "live_money_spending": False,
    "status": "AUTO_SCALING_SCORE_READY_SAFE_MODE"
}

try:
    for item in report["scale_ready"]:

        payload = (
            f"Product: {item['sku']}\n"
            f"Score: {item['score']}\n"
            f"Sales: {item['sales']}\n"
            f"Clicks: {item['clicks']}\n\n"
            f"Recommended: PREPARE_SCALING_REVIEW"
        )

        notify("SCALE_CANDIDATE", payload)

        print(f"SCALE ALERT SENT: {item['sku']}")

except Exception as e:
    print("scale alert skipped:", e)


OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

print(json.dumps(report, indent=2))
