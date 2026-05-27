import json
from pathlib import Path
from datetime import datetime, timezone

DECISIONS = Path("app/logs/auto_launch_decisions.json")
CFG = Path("app/config/auto_spend_guardrails.json")
OUT = Path("app/logs/auto_spend_executor.json")

decisions = json.loads(DECISIONS.read_text(encoding="utf-8"))
cfg = json.loads(CFG.read_text(encoding="utf-8"))

executions = []
spent_today_planned = 0

for item in decisions.get("decisions", []):
    budget = item["recommended_daily_budget"]

    allowed = (
        item["auto_launch_approved"]
        and cfg["allow_live_spending"]
        and not cfg["emergency_stop"]
        and budget <= cfg["max_campaign_budget"]
        and spent_today_planned + budget <= cfg["max_daily_global_budget"]
    )

    executions.append({
        "sku": item["sku"],
        "requested_budget": budget,
        "execution_allowed": allowed,
        "execution_mode": "DRY_RUN_EXECUTION",
        "next_action": "PREPARE_LIVE_CAMPAIGN" if allowed else "BLOCKED_BY_GUARDRAILS",
        "real_money_spent": 0
    })

    if allowed:
        spent_today_planned += budget

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "mode": "LIMITED_AUTO_SPEND_EXECUTOR",
    "emergency_stop": cfg["emergency_stop"],
    "planned_daily_spend": spent_today_planned,
    "max_daily_global_budget": cfg["max_daily_global_budget"],
    "executions": executions,
    "real_money_spent": 0,
    "status": "AUTO_SPEND_EXECUTOR_READY_DRY_RUN"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

print(json.dumps(report, indent=2))
