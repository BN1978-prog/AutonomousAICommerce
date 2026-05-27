import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/budget_mode_detector.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

balance_data = read_json("app/logs/available_balance.json")
balance = float(balance_data.get("available_balance", 0))

if balance >= 1000:
    mode = "FULL_AUTOPILOT"
    max_daily_spend = 100
elif balance >= 250:
    mode = "SCALE_TESTING"
    max_daily_spend = 20
elif balance >= 100:
    mode = "MICRO_BUDGET"
    max_daily_spend = 5
else:
    mode = "ORGANIC_ONLY"
    max_daily_spend = 0

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "currency": "GBP",
    "available_balance": balance,
    "mode": mode,
    "max_daily_spend_gbp": max_daily_spend,
    "paid_ads_allowed": max_daily_spend > 0,
    "status": "BUDGET_MODE_DETECTED"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
