import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/system_release_marker.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

master = read_json("app/logs/master_system_health.json")
dashboard = read_json("app/logs/system_status_dashboard.json")
niche = read_json("app/logs/niche_exclusion_summary.json")

release = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "release_name": "AIC_SAFE_AUTOPILOT_CORE",
    "release_version": "v1.1-safe-pet-niche",
    "system_status": dashboard.get("system_status"),
    "production_readiness": dashboard.get("production_readiness"),
    "status": dashboard.get("status"),
    "master_health": master.get("status"),
    "live_money_spending": dashboard.get("live_money_spending"),
    "pet_niche_status": niche.get("status"),
    "pet_niche_excluded_skus": niche.get("excluded_skus", []),
    "external_blockers": dashboard.get("external_blockers", []),
    "notes": [
        "Core commerce system stable",
        "Token self-healing enabled",
        "CRM safe draft mode enabled",
        "Budget guard enabled",
        "Recovery and backup enabled",
        "Meta funnel paused",
        "Google waiting Basic Access",
        "Amazon pending verification",
        "Pet niche filter enabled",
        "Non-pet SKUs excluded from automation"
    ],
    "status_marker": "STABLE_SAFE_RELEASE_PET_NICHE_PROTECTED"
}

OUT.write_text(json.dumps(release, indent=2), encoding="utf-8")
print(json.dumps(release, indent=2))
