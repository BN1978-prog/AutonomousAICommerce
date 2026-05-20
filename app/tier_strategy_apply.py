import json
from pathlib import Path
from datetime import datetime, timezone

REGISTRY=Path("app/logs/imported_skus.json")
data=json.loads(REGISTRY.read_text(encoding="utf-8"))

updated=0

for sku,item in data.items():

    tier=item.get("product_tier","C")

    if tier=="A":
        item["ads_budget_multiplier"]=2.0
        item["featured_product"]=True
        item["pause_candidate"]=False

    elif tier=="B":
        item["ads_budget_multiplier"]=1.5
        item["featured_product"]=False
        item["pause_candidate"]=False

    elif tier=="C":
        item["ads_budget_multiplier"]=1.0
        item["featured_product"]=False
        item["pause_candidate"]=False

    else:
        item["ads_budget_multiplier"]=0
        item["featured_product"]=False
        item["pause_candidate"]=True

    item["tier_strategy_updated_at"]=(
        datetime.now(timezone.utc).isoformat()
    )

    updated+=1

REGISTRY.write_text(
    json.dumps(data,indent=2),
    encoding="utf-8"
)

print("UPDATED:",updated)
