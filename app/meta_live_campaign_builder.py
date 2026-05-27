import json
from pathlib import Path
from datetime import datetime, timezone

ROUTER = Path("app/logs/live_backend_router.json")
OUT = Path("app/logs/meta_live_campaign_payloads.json")

router = json.loads(ROUTER.read_text(encoding="utf-8"))

payloads = []

for route in router.get("routes", []):
    if route.get("meta_route") == "READY":
        sku = route["sku"]
        budget = route["budget"]

        payloads.append({
            "sku": sku,
            "platform": "meta",
            "campaign_name": f"AICommerce_AUTO_{sku}",
            "daily_budget": budget,
            "status": "PAUSED",
            "objective": "OUTCOME_SALES",
            "optimization_goal": "PURCHASE",
            "execution_mode": "PAYLOAD_READY_NOT_SENT",
            "real_money_spent": 0
        })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "payloads_created": len(payloads),
    "payloads": payloads,
    "status": "META_LIVE_CAMPAIGN_PAYLOADS_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

print(json.dumps(report, indent=2))
