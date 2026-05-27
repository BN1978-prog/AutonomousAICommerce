import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/crm_draft_outbox.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

messages = read_json("app/logs/crm_message_generator.json")
send_guard = read_json("app/logs/crm_send_guard.json")
channel = read_json("app/logs/crm_channel_readiness.json")

drafts = []

for template in messages.get("templates", []):
    drafts.append({
        "flow": template.get("flow"),
        "subject": template.get("subject"),
        "body": template.get("body"),
        "status": "draft_only",
        "send_enabled": False
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "drafts_created": len(drafts),
    "drafts": drafts,
    "send_allowed": send_guard.get("send_allowed") is True and channel.get("status") == "CRM_CHANNEL_READY",
    "status": "CRM_DRAFT_OUTBOX_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
