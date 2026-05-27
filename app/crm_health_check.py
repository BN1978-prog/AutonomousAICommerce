import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/crm_health_check.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

crm = read_json("app/logs/crm_automation_status.json")
messages = read_json("app/logs/crm_message_generator.json")
queue = read_json("app/logs/crm_queue.json")
guard = read_json("app/logs/crm_send_guard.json")
channel = read_json("app/logs/crm_channel_readiness.json")
orchestrator = read_json("app/logs/crm_orchestrator.json")

checks = {
    "crm_flows_ready": crm.get("status") == "CRM_AUTOMATION_READY",
    "messages_ready": messages.get("status") == "CRM_MESSAGES_READY_DRAFT_ONLY",
    "queue_layer_ready": queue.get("status") in ["CRM_QUEUE_READY", "CRM_QUEUE_EMPTY_WAITING_EVENTS"],
    "send_guard_active": guard.get("status") == "CRM_SEND_BLOCKED_BY_GUARD",
    "orchestrator_ready": orchestrator.get("status") == "CRM_ORCHESTRATOR_READY"
}

missing = [k for k, v in checks.items() if not v]

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "checks": checks,
    "missing": missing,
    "channel_status": channel.get("status"),
    "real_send_enabled": False,
    "status": "CRM_HEALTHY_SAFE_MODE" if not missing else "CRM_HEALTH_ATTENTION_REQUIRED"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
