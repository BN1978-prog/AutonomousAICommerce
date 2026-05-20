import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/global_arbitrage_candidates.json")

candidates = [
    {
        "product": "Eco-Friendly Cat Scratcher Toy",
        "sku": "CJJJCWMY00923",
        "buy_from": "cjdropshipping",
        "buy_price": 16.34,
        "sell_to": "shopify",
        "sell_price": 39.99,
        "shipping_cost": 0.00,
        "platform_fee_percent": 3,
        "risk_reserve_percent": 8
    },
    {
        "product": "Non-slip silicone pet feeding bowl",
        "sku": "PET-BOWL-001",
        "buy_from": "cjdropshipping",
        "buy_price": 4.50,
        "sell_to": "shopify",
        "sell_price": 16.99,
        "shipping_cost": 0.00,
        "platform_fee_percent": 3,
        "risk_reserve_percent": 8
    }
]

items = []

for c in candidates:
    sell = float(c["sell_price"])
    buy = float(c["buy_price"])
    shipping = float(c["shipping_cost"])
    fee = sell * float(c["platform_fee_percent"]) / 100
    risk = sell * float(c["risk_reserve_percent"]) / 100
    profit = sell - buy - shipping - fee - risk
    margin = (profit / sell) * 100 if sell else 0

    decision = "candidate" if margin >= 30 and profit >= 5 else "reject"

    items.append({
        **c,
        "platform_fee": round(fee, 2),
        "risk_reserve": round(risk, 2),
        "net_profit": round(profit, 2),
        "margin_percent": round(margin, 2),
        "decision": decision
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "mode": "multi_market_scan_safe",
    "markets_scanned": ["cjdropshipping", "shopify"],
    "items_seen": len(items),
    "candidates": len([x for x in items if x["decision"] == "candidate"]),
    "items": items,
    "status": "ok"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
