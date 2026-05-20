import json
from pathlib import Path
from datetime import datetime, timezone

CANDIDATES = Path("app/logs/traffic_candidates.json")
SEO = Path("app/logs/seo_suggestions.json")
PRICING = Path("app/logs/pricing_experiments.json")
OUT = Path("app/logs/traffic_execution_plan.json")

candidates = json.loads(CANDIDATES.read_text(encoding="utf-8")) if CANDIDATES.exists() else []
seo = json.loads(SEO.read_text(encoding="utf-8")) if SEO.exists() else []
pricing = json.loads(PRICING.read_text(encoding="utf-8")) if PRICING.exists() else []

seo_by_sku = {x.get("sku"): x for x in seo}
pricing_by_sku = {x.get("sku"): x for x in pricing}

plan = []

for item in candidates:
    sku = item.get("sku")
    priority = item.get("priority")
    actions = []

    if "seo" in item.get("traffic_actions", []):
        actions.append({
            "channel": "seo",
            "action": "apply_seo_suggestion",
            "payload": seo_by_sku.get(sku),
            "auto_apply": priority == "high"
        })

    if "social_post" in item.get("traffic_actions", []):
        actions.append({
            "channel": "social",
            "action": "create_product_post",
            "auto_apply": False
        })

    if "meta_ads" in item.get("traffic_actions", []):
        actions.append({
            "channel": "meta_ads",
            "action": "prepare_campaign",
            "daily_budget": 3.00,
            "auto_apply": False
        })

    if "google_ads" in item.get("traffic_actions", []):
        actions.append({
            "channel": "google_ads",
            "action": "prepare_campaign",
            "daily_budget": 3.00,
            "auto_apply": False
        })

    if sku in pricing_by_sku:
        actions.append({
            "channel": "pricing",
            "action": "queue_price_test",
            "payload": pricing_by_sku.get(sku),
            "auto_apply": False
        })

    plan.append({
        "sku": sku,
        "priority": priority,
        "actions": actions,
        "created_at": datetime.now(timezone.utc).isoformat()
    })

OUT.write_text(
    json.dumps(plan, indent=2),
    encoding="utf-8"
)

print("TRAFFIC EXECUTION PLAN:", len(plan))

for p in plan:
    print(p["sku"], "priority=", p["priority"])
    for a in p["actions"]:
        print(" -", a["channel"], a["action"], "auto=", a.get("auto_apply"))
