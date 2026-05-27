import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/crm_queue.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

router = read_json("app/logs/crm_event_router.json")
drafts = read_json("app/logs/crm_draft_outbox.json")
guard = read_json("app/logs/crm_send_guard.json")

draft_map = {
    d.get("flow"): d
    for d in drafts.get("drafts", [])
}

queue = []

for event in router.get("events", []):
    flow = event.get("flow")

    if flow in draft_map and event.get("status") == "ready_to_queue":
        queue.append({
            "event": event.get("event"),
            "flow": flow,
            "subject": draft_map[flow].get("subject"),
            "body": draft_map[flow].get("body"),
            "status": "queued_draft_only",
            "send_enabled": False
        })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "queue_size": len(queue),
    "queue": queue,
    "send_guard_status": guard.get("status"),
    "send_allowed": False,
    "status": "CRM_QUEUE_READY" if queue else "CRM_QUEUE_EMPTY_WAITING_EVENTS"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
