import json
from pathlib import Path
from datetime import datetime, timezone

CFG = Path("app/config/auto_spend_guardrails.json")
REPORT = Path("app/logs/live_execution_report.json")
OUT = Path("app/logs/live_mode_final_lock.json")

cfg = json.loads(CFG.read_text(encoding="utf-8"))
report = json.loads(REPORT.read_text(encoding="utf-8"))

live_mode_allowed = (
    cfg.get("allow_live_spending") is True
    and cfg.get("emergency_stop") is False
    and report.get("approved_count", 0) > 0
    and report.get("real_money_spent", 0) == 0
)

result = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "allow_live_spending": cfg.get("allow_live_spending"),
    "emergency_stop": cfg.get("emergency_stop"),
    "approved_count": report.get("approved_count", 0),
    "total_daily_budget_ready": report.get("total_daily_budget_ready", 0),
    "live_mode_allowed": live_mode_allowed,
    "next_action": "READY_FOR_REAL_API_EXECUTION" if live_mode_allowed else "BLOCKED",
    "real_money_spent": 0,
    "status": "LIVE_MODE_FINAL_LOCK_READY"
}

OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")

print(json.dumps(result, indent=2))
