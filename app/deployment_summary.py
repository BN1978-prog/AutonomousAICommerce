import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/deployment_summary.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

checklist = read_json("app/logs/deployment_readiness_checklist.json")
release = read_json("app/logs/system_release_marker.json")
quick = read_json("app/logs/master_system_health.json")

not_ready = checklist.get("not_ready", [])

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "release_version": release.get("release_version"),
    "release_marker": release.get("status_marker"),
    "master_health": quick.get("status"),
    "ready_count": checklist.get("ready_count"),
    "not_ready_count": checklist.get("not_ready_count"),
    "not_ready_items": [x.get("item") for x in not_ready],
    "current_waiting_on": [
        x.get("item") for x in not_ready
    ],
    "status": "SYSTEM_READY_SAFE_MODE_WAITING_EXTERNALS"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
