import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/product_quality_filter.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

scores = read_json("app/logs/dynamic_product_score.json")
tiers = read_json("app/logs/tier_summary.json")
opportunities = read_json("app/logs/global_arbitrage_engine.json")

items = opportunities.get("top_opportunities", [])

approved = []
blocked = []

for item in items:
    margin = float(item.get("margin_percent", 0) or 0)
    profit = float(item.get("net_profit", 0) or 0)
    title = str(item.get("title", "")).lower()

    reasons = []

    if margin < 35:
        reasons.append("margin_below_35_percent")

    if profit < 10:
        reasons.append("net_profit_below_10")

    risky_words = [
        "medical",
        "medicine",
        "cure",
        "treatment",
        "drug",
        "hair growth",
        "weight loss",
        "supplement"
    ]

    for word in risky_words:
        if word in title:
            reasons.append("possible_policy_risk_keyword_" + word.replace(" ", "_"))

    if reasons:
        blocked.append({
            "sku": item.get("sku"),
            "title": item.get("title"),
            "reasons": reasons,
            "status": "blocked_by_quality_filter"
        })
    else:
        approved.append({
            "sku": item.get("sku"),
            "title": item.get("title"),
            "margin_percent": margin,
            "net_profit": profit,
            "status": "approved_for_safe_test"
        })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "items_seen": len(items),
    "approved_count": len(approved),
    "blocked_count": len(blocked),
    "approved": approved,
    "blocked": blocked,
    "status": "PRODUCT_QUALITY_FILTER_OK"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
