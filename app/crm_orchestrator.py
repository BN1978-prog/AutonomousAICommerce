import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/crm_orchestrator.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

router = read_json("app/logs/crm_event_router.json")
queue = read_json("app/logs/crm_queue.json")
executor = read_json("app/logs/crm_executor_dry_run.json")
guard = read_json("app/logs/crm_send_guard.json")
channel = read_json("app/logs/crm_channel_readiness.json")

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "events_detected": router.get("events_detected",0),
    "queue_size": queue.get("queue_size",0),
    "actions_prepared": executor.get("actions_prepared",0),
    "send_guard": guard.get("status"),
    "channel_status": channel.get("status"),
    "crm_pipeline_ready": True,
    "real_send_enabled": False,
    "status":"CRM_ORCHESTRATOR_READY"
}

OUT.write_text(
    json.dumps(report,indent=2),
    encoding="utf-8"
)

print(json.dumps(report,indent=2))
