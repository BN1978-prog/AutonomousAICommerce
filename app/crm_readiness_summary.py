import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/crm_readiness_summary.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

channel = read_json("app/logs/crm_channel_readiness.json")
smtp = read_json("app/logs/smtp_config_validator.json")
guard = read_json("app/logs/crm_send_guard.json")
queue = read_json("app/logs/crm_queue.json")
health = read_json("app/logs/crm_health_check.json")

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "crm_health": health.get("status"),
    "channel_status": channel.get("status"),
    "ready_providers": channel.get("ready_providers", []),
    "smtp_status": smtp.get("status"),
    "smtp_ready_for_real_send": smtp.get("smtp_ready_for_real_send"),
    "send_guard_status": guard.get("status"),
    "send_allowed": False,
    "queue_size": queue.get("queue_size", 0),
    "status": "CRM_SAFE_READY_TEMPLATE_MODE"
    if smtp.get("status") == "SMTP_CONFIG_TEMPLATE_ONLY"
    else "CRM_SAFE_READY_PROVIDER_CONNECTED"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
