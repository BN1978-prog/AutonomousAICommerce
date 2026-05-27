import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/niche_exclusion_summary.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

registry = read_json("app/logs/niche_exclusion_registry.json")
guard = read_json("app/logs/niche_exclusion_guard.json")
filter_report = read_json("app/logs/pet_niche_filter.json")

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "pet_items_approved": filter_report.get("approved_count", 0),
    "flagged_items": filter_report.get("flagged_count", 0),
    "excluded_count": registry.get("excluded_count", 0),
    "excluded_skus": [x.get("sku") for x in registry.get("items", [])],
    "violations_count": guard.get("violations_count", 0),
    "status": "PET_NICHE_SAFE" if guard.get("violations_count", 0) == 0 else "PET_NICHE_ATTENTION_REQUIRED"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
