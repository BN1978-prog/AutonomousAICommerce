import json
from pathlib import Path
from datetime import datetime, timezone

ADSETS = Path("app/logs/meta_adset_live_creator.json")
PLAN = Path("app/logs/opportunities/global_execution_plan.json")
OUT = Path("app/logs/meta_creative_live_creator.json")

adsets = json.loads(ADSETS.read_text(encoding="utf-8")) if ADSETS.exists() else {}
plan = json.loads(PLAN.read_text(encoding="utf-8")) if PLAN.exists() else {}

plans_by_sku = {p.get("sku"): p for p in plan.get("plans", [])}

creatives = []

for a in adsets.get("adsets", []):
    sku = a.get("sku")
    p = plans_by_sku.get(sku, {})

    creatives.append({
        "sku": sku,
        "title": p.get("title") or a.get("campaign_name"),
        "adset_name": a.get("adset_name"),
        "meta_campaign_id": a.get("meta_campaign_id"),
        "creative_name": f"{sku}_CREATIVE",
        "primary_text": f"Discover {p.get('title', 'this product')} today.",
        "headline": p.get("title") or "Shop Now",
        "description": "Limited test campaign for product demand validation.",
        "call_to_action": "SHOP_NOW",
        "destination_url": "https://aicommerce-test-store-2.myshopify.com",
        "status": "READY_PAYLOAD_ONLY",
        "mode": "payload_only_no_api_call"
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "mode": "meta_creative_payload_only",
    "creatives_created": len(creatives),
    "creatives": creatives,
    "live_api_call_enabled": False,
    "status": "meta_creative_payloads_ready" if creatives else "no_creatives"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
