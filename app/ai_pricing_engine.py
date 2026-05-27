import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/ai_pricing_engine.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

opportunities = read_json("app/logs/global_arbitrage_engine.json")

items = opportunities.get("top_opportunities", [])

pricing = []

for item in items:
    source_cost = float(item.get("source_cost", 0) or 0)
    current_price = float(item.get("target_price", 0) or 0)
    current_profit = float(item.get("net_profit", 0) or 0)
    margin = float(item.get("margin_percent", 0) or 0)

    min_profit = 10
    min_margin = 35

    recommended_price = current_price

    if margin > 55:
        recommended_price = round(current_price * 0.97, 2)

    elif margin < min_margin or current_profit < min_profit:
        recommended_price = round(current_price * 1.08, 2)

    pricing.append({
        "sku": item.get("sku"),
        "title": item.get("title"),
        "source_cost": source_cost,
        "current_price": current_price,
        "current_profit": current_profit,
        "current_margin_percent": margin,
        "recommended_price": recommended_price,
        "min_profit_required": min_profit,
        "min_margin_required": min_margin,
        "action": "hold_price" if recommended_price == current_price else "adjust_price_recommended",
        "auto_apply": False
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "items_seen": len(items),
    "pricing_recommendations": pricing,
    "auto_apply_enabled": False,
    "status": "AI_PRICING_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
