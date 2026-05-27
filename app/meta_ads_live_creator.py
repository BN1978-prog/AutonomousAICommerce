import json
from pathlib import Path
from datetime import datetime, timezone

CREATIVES = Path("app/logs/meta_creative_live_creator.json")
OUT = Path("app/logs/meta_ads_live_creator.json")

data = json.loads(CREATIVES.read_text(encoding="utf-8")) if CREATIVES.exists() else {}

ads = []

for c in data.get("creatives", []):
    ads.append({
        "sku": c.get("sku"),
        "ad_name": f"{c.get('sku')}_AD",
        "adset_name": c.get("adset_name"),
        "creative_name": c.get("creative_name"),
        "headline": c.get("headline"),
        "primary_text": c.get("primary_text"),
        "destination_url": c.get("destination_url"),
        "status": "PAUSED",
        "mode": "payload_only_no_api_call"
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "mode": "meta_ads_payload_only",
    "ads_created": len(ads),
    "ads": ads,
    "live_api_call_enabled": False,
    "status": "meta_ads_payloads_ready" if ads else "no_ads"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
