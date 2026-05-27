import json
from pathlib import Path
from datetime import datetime, timezone

META = Path("app/logs/meta_live_campaign_payloads.json")
GOOGLE = Path("app/logs/google_live_campaign_payloads.json")
OUT = Path("app/logs/live_campaign_registry.json")

meta = json.loads(META.read_text(encoding="utf-8")) if META.exists() else {}
google = json.loads(GOOGLE.read_text(encoding="utf-8")) if GOOGLE.exists() else {}

campaigns = []

for item in meta.get("payloads", []):
    campaigns.append({
        "sku": item["sku"],
        "platform": "meta",
        "campaign_name": item["campaign_name"],
        "daily_budget": item["daily_budget"],
        "status": item["status"],
        "execution_mode": item["execution_mode"],
        "ready_for_live_api": item["execution_mode"] == "PAYLOAD_READY_NOT_SENT",
        "real_money_spent": 0
    })

for item in google.get("payloads", []):
    campaigns.append({
        "sku": item["sku"],
        "platform": "google",
        "campaign_name": item["campaign_name"],
        "daily_budget": item["daily_budget"],
        "status": item["status"],
        "execution_mode": item["execution_mode"],
        "ready_for_live_api": item["execution_mode"] == "PAYLOAD_READY_NOT_SENT",
        "real_money_spent": 0
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "campaigns_count": len(campaigns),
    "campaigns": campaigns,
    "ready_for_live_api_count": len([x for x in campaigns if x["ready_for_live_api"]]),
    "real_money_spent": 0,
    "status": "LIVE_CAMPAIGN_REGISTRY_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

print(json.dumps(report, indent=2))
