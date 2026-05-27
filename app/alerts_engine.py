import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/alerts.json")

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
blockers = read_json("app/logs/external_blockers_monitor.json")
daily = read_json("app/logs/daily_report.json")

alerts = []

if dashboard.get("system_status") != "HEALTHY":
    alerts.append({
        "level": "critical",
        "type": "system_health",
        "message": "System is not HEALTHY"
    })

if dashboard.get("safe_to_continue") is not True:
    alerts.append({
        "level": "critical",
        "type": "safe_to_continue",
        "message": "System is not safe to continue"
    })

if dashboard.get("live_money_spending") is True:
    alerts.append({
        "level": "critical",
        "type": "live_money_spending",
        "message": "Live money spending is enabled"
    })

if recovery.get("critical_changes_count", 0) > 0:
    alerts.append({
        "level": "critical",
        "type": "recovery",
        "message": "Critical recovery changes detected",
        "details": recovery.get("critical_changes", [])
    })

for b in blockers.get("blockers", []):
    if b.get("reason") == "owner_safety_guard":
        alerts.append({
            "level": "info",
            "type": "owner_safety_guard",
            "platform": b.get("platform"),
            "message": "Owner safety guard is active"
        })
    else:
        alerts.append({
            "level": "warning",
            "type": "external_blocker",
            "platform": b.get("platform"),
            "message": b.get("reason"),
            "action_required": b.get("action_required")
        })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "alerts_count": len(alerts),
    "critical_count": len([a for a in alerts if a.get("level") == "critical"]),
    "warning_count": len([a for a in alerts if a.get("level") == "warning"]),
    "info_count": len([a for a in alerts if a.get("level") == "info"]),
    "alerts": alerts,
    "status": "ALERTS_OK" if not [a for a in alerts if a.get("level") == "critical"] else "CRITICAL_ALERTS_PRESENT"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
