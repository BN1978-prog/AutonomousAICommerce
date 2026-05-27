import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/crm_send_guard.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

messages = read_json("app/logs/crm_message_generator.json")
confirmation = Path("app/logs/OWNER_CONFIRM_CRM_SEND.json")

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "templates_ready": messages.get("templates_created", 0),
    "owner_confirmation_file_exists": confirmation.exists(),
    "send_allowed": False,
    "reason": "owner_confirmation_required",
    "status": "CRM_SEND_BLOCKED_BY_GUARD"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
