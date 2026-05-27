import json
from pathlib import Path
from datetime import datetime, timezone

EXECUTOR = Path("app/logs/auto_spend_executor.json")
OUT = Path("app/logs/spend_history_tracker.json")

executor = json.loads(EXECUTOR.read_text(encoding="utf-8"))

history=[]

for item in executor.get("executions",[]):

    planned = item["requested_budget"]

    simulated_spend = planned
    simulated_revenue = round(planned * 4.5, 2)
    simulated_profit = round(simulated_revenue - simulated_spend, 2)

    roi = round(
        (simulated_profit / simulated_spend) * 100,
        2
    ) if simulated_spend else 0

    history.append({
        "sku": item["sku"],
        "planned_budget": planned,
        "simulated_spend": simulated_spend,
        "simulated_revenue": simulated_revenue,
        "simulated_profit": simulated_profit,
        "rolling_roi_percent": roi,
        "health": (
            "POSITIVE"
            if roi > 0 else
            "NEGATIVE"
        )
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "tracked_campaigns": len(history),
    "history": history,
    "total_simulated_spend": round(
        sum(x["simulated_spend"] for x in history),2
    ),
    "total_simulated_profit": round(
        sum(x["simulated_profit"] for x in history),2
    ),
    "status": "SPEND_HISTORY_TRACKER_READY"
}

OUT.write_text(
    json.dumps(report, indent=2),
    encoding="utf-8"
)

print(json.dumps(report, indent=2))
