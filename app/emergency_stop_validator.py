import json
from pathlib import Path
from datetime import datetime, timezone

CFG = Path("app/config/auto_spend_guardrails.json")
EXECUTOR = Path("app/logs/auto_spend_executor.json")
BUDGET = Path("app/logs/hourly_budget_monitor.json")
OUT = Path("app/logs/emergency_stop_validator.json")

cfg = json.loads(CFG.read_text(encoding="utf-8"))
executor = json.loads(EXECUTOR.read_text(encoding="utf-8"))
budget = json.loads(BUDGET.read_text(encoding="utf-8"))

emergency_stop = cfg.get("emergency_stop", True)

blocked = emergency_stop or not budget.get("budget_ok", False)

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "emergency_stop": emergency_stop,
    "budget_ok": budget.get("budget_ok", False),
    "planned_daily_spend": executor.get("planned_daily_spend", 0),
    "final_spend_permission": not blocked,
    "action": "ALLOW_LIMITED_SPEND" if not blocked else "BLOCK_ALL_SPEND",
    "status": "EMERGENCY_STOP_VALIDATOR_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

print(json.dumps(report, indent=2))
