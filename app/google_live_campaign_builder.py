import json
from pathlib import Path
from datetime import datetime, timezone

ROUTER = Path("app/logs/live_backend_router.json")
OUT = Path("app/logs/google_live_campaign_payloads.json")

router = json.loads(ROUTER.read_text(encoding="utf-8"))

payloads = []

for route in router.get("routes", []):
    if route.get("google_route") == "READY":
        sku = route["sku"]
        budget = route["budget"]

        payloads.append({
            "sku": sku,
            "platform": "google",
            "campaign_name": f"AICommerce_AUTO_{sku}",
            "daily_budget": budget,
            "status": "PAUSED",
            "channel_type": "SEARCH",
            "bidding_strategy": "MAXIMIZE_CONVERSIONS",
            "execution_mode": "PAYLOAD_READY_NOT_SENT",
            "real_money_spent": 0
        })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "payloads_created": len(payloads),
    "payloads": payloads,
    "status": "GOOGLE_LIVE_CAMPAIGN_PAYLOADS_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

print(json.dumps(report, indent=2))
