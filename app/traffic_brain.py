import json
from pathlib import Path

PROMO = Path("app/logs/promotion_candidates.json")
ARBITRAGE = Path("app/logs/arbitrage_safety_gate.json")
OUT = Path("app/logs/traffic_candidates.json")

promo = json.loads(
    PROMO.read_text(encoding="utf-8")
) if PROMO.exists() else []

arb = json.loads(
    ARBITRAGE.read_text(encoding="utf-8")
) if ARBITRAGE.exists() else []

arb_ok = {
    x["sku"]
    for x in arb
    if x.get("allowed")
}

candidates=[]

for item in promo:

    sku=item.get("sku")

    score=float(
        item.get("score",0)
        or 0
    )

    priority="low"

    if sku in arb_ok:
        priority="high"

    elif score>=90:
        priority="medium"

    candidates.append({
        "sku":sku,
        "score":score,
        "priority":priority,
        "traffic_actions":[
            "seo",
            "meta_ads",
            "google_ads",
            "social_post"
        ] if priority=="high" else [
            "seo",
            "social_post"
        ]
    })

candidates=sorted(
    candidates,
    key=lambda x:(
        x["priority"]=="high",
        x["score"]
    ),
    reverse=True
)

OUT.write_text(
    json.dumps(
        candidates,
        indent=2
    ),
    encoding="utf-8"
)

print(
    "TRAFFIC CANDIDATES:",
    len(candidates)
)

for c in candidates:
    print(
        c["sku"],
        "priority=",
        c["priority"]
    )

print(
    "REPORT:",
    OUT
)
