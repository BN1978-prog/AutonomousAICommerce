import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/niche_exclusion_guard.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

exclusions = read_json("app/logs/niche_exclusion_registry.json")
campaigns = read_json("app/logs/real_traffic_launcher.json")
pricing = read_json("app/logs/ai_pricing_engine.json")

excluded_skus = [
    item.get("sku")
    for item in exclusions.get("items", [])
]

violations = []

for campaign in campaigns.get("campaigns", []):
    if campaign.get("sku") in excluded_skus:
        violations.append({
            "sku": campaign.get("sku"),
            "source": "real_traffic_launcher",
            "violation": "excluded_sku_present_in_campaigns"
        })

for item in pricing.get("pricing_recommendations", []):
    if item.get("sku") in excluded_skus:
        violations.append({
            "sku": item.get("sku"),
            "source": "ai_pricing_engine",
            "violation": "excluded_sku_present_in_pricing"
        })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "excluded_skus": excluded_skus,
    "violations_count": len(violations),
    "violations": violations,
    "status": "NICHE_EXCLUSION_GUARD_OK" if not violations else "NICHE_EXCLUSION_VIOLATIONS_FOUND"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
