import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/autopilot_schedule_readiness.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

dashboard = read_json("app/logs/system_status_dashboard.json")
recovery = read_json("app/logs/recovery_report.json")
alerts = read_json("app/logs/alerts.json")
backup = read_json("app/logs/backup_report.json")

checks = {
    "system_healthy": dashboard.get("system_status") == "HEALTHY",
    "safe_to_continue": dashboard.get("safe_to_continue") is True,
    "recovery_ok": recovery.get("status") == "RECOVERY_OK",
    "no_critical_alerts": alerts.get("critical_count", 0) == 0,
    "backup_ok": backup.get("status") == "BACKUP_OK",
    "live_money_spending_false": dashboard.get("live_money_spending") is False
}

missing = [k for k, v in checks.items() if not v]

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "checks": checks,
    "missing_requirements": missing,
    "recommended_schedule": {
        "health_check": "hourly",
        "daily_report": "daily",
        "backup": "after_successful_autopilot_run",
        "roi_update": "after_real_sales_detected"
    },
    "status": "AUTOPILOT_SCHEDULE_READY" if not missing else "AUTOPILOT_SCHEDULE_NOT_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
