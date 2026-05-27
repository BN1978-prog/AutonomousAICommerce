import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/niche_exclusion_registry.json")

excluded = [
    {
        "sku": "CJYD2896648",
        "reason": "outside_pet_niche",
        "exclude_from": [
            "google_feed",
            "meta_feed",
            "ads",
            "seo",
            "ai_ranking",
            "scaling"
        ]
    },
    {
        "sku": "CJJT2896696",
        "reason": "outside_pet_niche",
        "exclude_from": [
            "google_feed",
            "meta_feed",
            "ads",
            "seo",
            "ai_ranking",
            "scaling"
        ]
    }
]

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "excluded_count": len(excluded),
    "items": excluded,
    "status": "NICHE_EXCLUSION_ACTIVE"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
