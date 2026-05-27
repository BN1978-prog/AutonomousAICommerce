import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/crm_executor_dry_run.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

queue = read_json("app/logs/crm_queue.json")
guard = read_json("app/logs/crm_send_guard.json")
channel = read_json("app/logs/crm_channel_readiness.json")

actions = []

for item in queue.get("queue", []):
    actions.append({
        "flow": item.get("flow"),
        "event": item.get("event"),
        "subject": item.get("subject"),
        "status": "dry_run_not_sent",
        "reason": "crm_send_guard_active"
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "queue_size": queue.get("queue_size", 0),
    "actions_prepared": len(actions),
    "actions": actions,
    "send_guard_status": guard.get("status"),
    "channel_status": channel.get("status"),
    "real_send_enabled": False,
    "status": "CRM_EXECUTOR_DRY_RUN_OK"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
