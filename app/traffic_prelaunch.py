import json
from pathlib import Path
from datetime import datetime, timezone

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "traffic_mode": "ORGANIC_PRELAUNCH",
    "paid_ads_enabled": False,
    "daily_budget": 0,
    "sources": [
        "SEO",
        "Shopify catalog indexing",
        "eBay listings",
        "Meta organic pages",
        "CJ product sync"
    ],
    "status": "TRAFFIC_PRELAUNCH_ACTIVE"
}

Path("app/logs/traffic_prelaunch.json").write_text(
    json.dumps(report, indent=2),
    encoding="utf-8"
)

print(json.dumps(report, indent=2))
