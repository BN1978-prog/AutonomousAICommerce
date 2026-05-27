import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/global_channel_status_summary.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

roadmap = read_json("app/logs/global_marketplace_roadmap.json")
requirements = read_json("app/logs/global_channel_requirements_check.json")

req_by_channel = {
    c.get("channel"): c
    for c in requirements.get("channels", [])
}

summary = []

for ch in roadmap.get("channels", []):
    name = ch.get("channel")
    req = req_by_channel.get(name, {})

    summary.append({
        "channel": name,
        "type": ch.get("type"),
        "roadmap_status": ch.get("status"),
        "env_ready": req.get("ready", ch.get("status") in ["connected", "connected_paused_safe_mode"]),
        "missing": req.get("missing", []),
        "priority": ch.get("priority")
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "channels_total": len(summary),
    "env_ready_channels": [x["channel"] for x in summary if x["env_ready"]],
    "not_ready_channels": [x["channel"] for x in summary if not x["env_ready"]],
    "summary": summary,
    "status": "GLOBAL_CHANNEL_STATUS_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
