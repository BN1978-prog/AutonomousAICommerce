import json
from pathlib import Path
from datetime import datetime, timezone

REGISTRY=Path("app/logs/imported_skus.json")
OUT=Path("app/logs/autonomous_loop_health.json")

data=json.loads(REGISTRY.read_text(encoding="utf-8"))

counts={
    "total":len(data),
    "tier_A":0,
    "tier_B":0,
    "tier_C":0,
    "tier_D":0,
    "featured":0,
    "pause_candidates":0,
    "pipeline_inactive":0,
    "boost":0,
    "reduce":0,
    "hold":0,
    "exclude":0
}

for sku,item in data.items():

    tier=item.get("product_tier","D")
    counts[f"tier_{tier}"]=counts.get(f"tier_{tier}",0)+1

    if item.get("featured_product") is True:
        counts["featured"]+=1

    if item.get("pause_candidate") is True:
        counts["pause_candidates"]+=1

    if item.get("pipeline_active") is False:
        counts["pipeline_inactive"]+=1

    decision=item.get("hunter_decision")
    if decision in counts:
        counts[decision]+=1

health={
    "created_at":datetime.now(timezone.utc).isoformat(),
    "system_status":"HEALTHY",
    "autonomous_loop_active":True,
    "counts":counts,
    "logic":{
        "Tier A":"scale aggressively",
        "Tier B":"growth test",
        "Tier C":"monitor",
        "Tier D":"pause or remove"
    }
}

OUT.write_text(json.dumps(health,indent=2),encoding="utf-8")

print(json.dumps(health,indent=2))
