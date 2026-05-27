import json
from pathlib import Path
from datetime import datetime, timezone

SRC = Path("app/logs/campaign_executor.json")
OUT = Path("app/logs/meta_campaign_registry.json")

data = json.loads(SRC.read_text(encoding="utf-8-sig"))
campaigns = []

for c in data.get("campaigns", []):
    if "meta_ads" not in c.get("channels", []):
        continue

    campaigns.append({
        "sku": c.get("sku"),
        "name": "AICommerce Meta Test - " + c.get("title", c.get("sku")),
        "title": c.get("title"),
        "objective": "OUTCOME_TRAFFIC",
        "daily_budget": c.get("daily_test_budget", 5),
        "status": "PAUSED",
        "spend_enabled": False,
        "mode": "paused_payload_only",
        "source": "campaign_executor"
    })

OUT.write_text(json.dumps({
    "created_at": datetime.now(timezone.utc).isoformat(),
    "campaigns_registered": len(campaigns),
    "campaigns": campaigns,
    "status": "meta_campaigns_registered" if campaigns else "no_campaigns_registered"
}, indent=2), encoding="utf-8")

print("Meta campaigns registered:", len(campaigns))
