import json
from pathlib import Path
from datetime import datetime, timezone

REG = Path("app/logs/meta_campaign_registry.json")
OUT = Path("app/logs/meta_adset_live_creator.json")

data = json.loads(REG.read_text(encoding="utf-8")) if REG.exists() else {}

adsets = []

for c in data.get("campaigns", []):
    adsets.append({
        "sku": c.get("sku"),
        "campaign_name": c.get("campaign_name"),
        "meta_campaign_id": c.get("meta_campaign_id"),
        "adset_name": f"{c.get('campaign_name')}_ADSET",
        "daily_budget": 500,
        "billing_event": "IMPRESSIONS",
        "optimization_goal": "LINK_CLICKS",
        "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
        "destination_type": "WEBSITE",
        "status": "PAUSED",
        "mode": "payload_only_no_api_call"
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "mode": "meta_adset_payload_only",
    "adsets_created": len(adsets),
    "adsets": adsets,
    "live_api_call_enabled": False,
    "status": "meta_adset_payloads_ready" if adsets else "no_meta_campaigns"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
