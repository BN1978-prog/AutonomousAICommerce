import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/listing_publish_validator.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

plan = read_json("app/logs/listing_publisher_plan.json")
global_channels = read_json("app/logs/global_channel_status_summary.json")

ready_channels = set(global_channels.get("env_ready_channels", []))

validated = []
blocked = []

for action in plan.get("publish_actions", []):
    channel = action.get("channel")

    if channel in ready_channels:
        validated.append({
            **action,
            "validation": "channel_ready",
            "publish_allowed": True
        })
    else:
        blocked.append({
            **action,
            "validation": "channel_not_ready",
            "publish_allowed": False
        })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "actions_seen": len(plan.get("publish_actions", [])),
    "validated_count": len(validated),
    "blocked_count": len(blocked),
    "validated": validated,
    "blocked": blocked,
    "status": "LISTING_PUBLISH_VALIDATION_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
