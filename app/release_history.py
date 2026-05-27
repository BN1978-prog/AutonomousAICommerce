import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/release_history.json")
MARKER = Path("app/logs/system_release_marker.json")

def read_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except:
        return default

history = read_json(OUT, {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "releases": []
})

marker = read_json(MARKER, {})

entry = {
    "recorded_at": datetime.now(timezone.utc).isoformat(),
    "release_version": marker.get("release_version"),
    "release_name": marker.get("release_name"),
    "status_marker": marker.get("status_marker"),
    "master_health": marker.get("master_health"),
    "pet_niche_status": marker.get("pet_niche_status"),
    "live_money_spending": marker.get("live_money_spending")
}

history["releases"].append(entry)
history["latest"] = entry
history["releases_count"] = len(history["releases"])
history["status"] = "RELEASE_HISTORY_UPDATED"

OUT.write_text(json.dumps(history, indent=2), encoding="utf-8")
print(json.dumps(history, indent=2))
