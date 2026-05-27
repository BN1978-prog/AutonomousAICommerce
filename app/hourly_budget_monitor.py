import json
from pathlib import Path
from datetime import datetime, timezone

EXECUTOR = Path("app/logs/auto_spend_executor.json")
CFG = Path("app/config/auto_spend_guardrails.json")
OUT = Path("app/logs/hourly_budget_monitor.json")

executor = json.loads(EXECUTOR.read_text(encoding="utf-8"))
cfg = json.loads(CFG.read_text(encoding="utf-8"))

planned = executor.get("planned_daily_spend", 0)
limit = cfg.get("max_daily_global_budget", 0)

utilization = round((planned / limit) * 100, 2) if limit else 0

budget_ok = (
    not cfg.get("emergency_stop", True)
    and planned <= limit
)

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "planned_daily_spend": planned,
    "max_daily_global_budget": limit,
    "budget_utilization_percent": utilization,
    "emergency_stop": cfg.get("emergency_stop", True),
    "budget_ok": budget_ok,
    "action": "CONTINUE" if budget_ok else "STOP_ALL_SPEND",
    "status": "HOURLY_BUDGET_MONITOR_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

print(json.dumps(report, indent=2))
