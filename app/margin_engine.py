import json
from pathlib import Path
from datetime import datetime, timezone

IN = Path("app/logs/global_arbitrage_candidates.json")
OUT = Path("app/logs/opportunities/margin_report.json")
OUT.parent.mkdir(parents=True, exist_ok=True)

data = json.loads(IN.read_text(encoding="utf-8")) if IN.exists() else {"items": []}

items = []

for x in data.get("items", []):
    sell = float(x.get("sell_price", x.get("target_price", 0)))
    buy = float(x.get("buy_price", x.get("source_cost", 0)))
    shipping = float(x.get("shipping_cost", 0))
    fee = float(x.get("platform_fee", sell * 0.03))
    risk = float(x.get("risk_reserve", sell * 0.08))

    profit = sell - buy - shipping - fee - risk
    margin = (profit / sell) * 100 if sell else 0

    items.append({
        "sku": x.get("sku"),
        "title": x.get("product") or x.get("title"),
        "source_market": x.get("buy_from") or x.get("source_market"),
        "source_cost": buy,
        "shipping_cost": shipping,
        "target_market": x.get("sell_to") or x.get("target_market"),
        "target_price": sell,
        "platform_fee": round(fee, 2),
        "risk_reserve": round(risk, 2),
        "net_profit": round(profit, 2),
        "margin_percent": round(margin, 2),
        "decision": "candidate" if margin >= 25 and profit >= 5 else "reject"
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "mode": "margin_from_multi_market_candidates",
    "items_seen": len(items),
    "candidates": len([x for x in items if x["decision"] == "candidate"]),
    "items": items,
    "status": "ok"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
