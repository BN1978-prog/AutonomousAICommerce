import json
from pathlib import Path
from datetime import datetime, timezone

IN = Path("app/logs/meta_campaign_live_result.json")
OUT = Path("app/logs/meta_campaign_registry.json")

data = json.loads(IN.read_text(encoding="utf-8")) if IN.exists() else {}

items = []

for r in data.get("results", []):
    if r.get("ok") and r.get("response", {}).get("id"):
        items.append({
            "created_at": data.get("created_at"),
            "sku": r.get("sku"),
            "campaign_name": r.get("campaign_name"),
            "meta_campaign_id": r["response"]["id"],
            "status": "PAUSED",
            "spend_enabled": False,
            "source": "meta_live_api_create_paused_campaigns"
        })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "campaigns_registered": len(items),
    "campaigns": items,
    "status": "registered" if items else "no_campaigns_registered"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
