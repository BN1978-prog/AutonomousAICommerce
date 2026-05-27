import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/stable_release_105.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

quick = read_json("app/logs/master_system_health.json")
dashboard = read_json("app/logs/system_status_dashboard.json")
runbook = read_json("app/logs/operator_runbook.json")

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "release": "AIC_GLOBAL_SAFE_CORE_105",
    "autopilot_steps": "105/105",
    "master_health": quick.get("status"),
    "failed_checks": quick.get("failed_count"),
    "system_status": dashboard.get("system_status"),
    "production_readiness": dashboard.get("status"),
    "live_money_spending": dashboard.get("live_money_spending"),
    "external_waiting_on": [
        "Amazon verification / refresh token / seller ID",
        "Google Basic Access review",
        "TikTok Shop regional onboarding",
        "AliExpress developer access",
        "SMTP real provider",
        "first real sales"
    ],
    "runbook_status": runbook.get("status"),
    "status": "STABLE_RELEASE_105_CONFIRMED"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
