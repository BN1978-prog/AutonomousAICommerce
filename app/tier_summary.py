import json
from pathlib import Path

REGISTRY=Path("app/logs/imported_skus.json")
OUT=Path("app/logs/tier_summary.json")

data=json.loads(
    REGISTRY.read_text(
        encoding="utf-8"
    )
)

summary={
    "A":[],
    "B":[],
    "C":[],
    "D":[]
}

for sku,item in data.items():

    tier=item.get("product_tier","D")

    row={
        "sku":sku,
        "title":item.get("seo_title") or item.get("title"),
        "dynamic_score":item.get("dynamic_score"),
        "hunter_decision":item.get("hunter_decision"),
        "pipeline_active":item.get("pipeline_active",True)
    }

    summary.setdefault(tier,[])
    summary[tier].append(row)

for tier in summary:
    summary[tier]=sorted(
        summary[tier],
        key=lambda x:x.get("dynamic_score") or 0,
        reverse=True
    )

report={
    "counts":{
        "A":len(summary["A"]),
        "B":len(summary["B"]),
        "C":len(summary["C"]),
        "D":len(summary["D"])
    },
    "actions":{
        "A":"scale_aggressively",
        "B":"growth_test",
        "C":"monitor",
        "D":"pause_or_remove"
    },
    "tiers":summary
}

OUT.write_text(
    json.dumps(report,indent=2),
    encoding="utf-8"
)

print("A:",len(summary["A"]))
print("B:",len(summary["B"]))
print("C:",len(summary["C"]))
print("D:",len(summary["D"]))
