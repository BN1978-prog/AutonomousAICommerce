import json
from pathlib import Path
from datetime import datetime, timezone
from app.alert_dispatcher import notify

SRC = Path("app/logs/live_api_execution_gate.json")
OUT = Path("app/logs/live_execution_report.json")

data = json.loads(SRC.read_text(encoding="utf-8"))

approved = [
    x for x in data.get("approved_live_api_actions", [])
    if x.get("can_execute_live_api")
]

total_budget = sum(x["daily_budget"] for x in approved)

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "approved_count": len(approved),
    "total_daily_budget_ready": total_budget,
    "approved_actions": approved,
    "real_money_spent": 0,
    "status": "LIVE_EXECUTION_REPORT_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

try:
    lines = [
        "Live API dry-run ready",
        f"Approved campaigns: {len(approved)}",
        f"Total daily budget ready: ${total_budget}",
        "Real money spent: $0",
        ""
    ]

    for item in approved:
        lines.append(
            f"{item['platform'].upper()} | {item['sku']} | ${item['daily_budget']}/day"
        )

    notify("CEO_DASHBOARD", "\n".join(lines))

    print("LIVE EXECUTION REPORT ALERT SENT")

except Exception as e:
    print("live execution alert skipped:", e)

print(json.dumps(report, indent=2))
