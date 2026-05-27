import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/crm_final_gate.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

summary = read_json("app/logs/crm_readiness_summary.json")
queue = read_json("app/logs/crm_queue.json")
guard = read_json("app/logs/crm_send_guard.json")

checks = {
    "provider_connected": summary.get("channel_status") == "CRM_CHANNEL_READY",
    "smtp_real_config": summary.get("smtp_status") == "SMTP_CONFIG_READY",
    "owner_confirmed": guard.get("owner_confirmation_file_exists") is True,
    "queue_has_items": queue.get("queue_size", 0) > 0
}

missing = [k for k, v in checks.items() if not v]

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "checks": checks,
    "missing": missing,
    "send_allowed": False,
    "status": "CRM_FINAL_GATE_BLOCKED" if missing else "CRM_FINAL_GATE_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
