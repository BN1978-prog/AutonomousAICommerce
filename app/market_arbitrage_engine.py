import json
from pathlib import Path

IMPORTS = Path("app/logs/imported_skus.json")
OUT = Path("app/logs/market_arbitrage_candidates.json")

imports = json.loads(
    IMPORTS.read_text(encoding="utf-8")
) if IMPORTS.exists() else {}

candidates = []

for sku, item in imports.items():

    source_price = float(
        item.get("cost")
        or item.get("last_price")
        or 0
    )

    if source_price <= 0:
        continue

    estimated_shipping = float(
        item.get("shipping_cost", 2.5)
    )

    estimated_fee = round(
        source_price * 0.15,
        2
    )

    target_price = round(
        source_price * 1.8,
        2
    )

    estimated_profit = round(
        target_price
        - source_price
        - estimated_shipping
        - estimated_fee,
        2
    )

    decision = (
        "publish"
        if estimated_profit > 5
        else "watch"
    )

    candidates.append({
        "sku": sku,
        "source_channel": item.get("source") or "cj",
        "source_price": source_price,
        "target_channel": "ebay/shopify",
        "target_price": target_price,
        "shipping_cost": estimated_shipping,
        "fees": estimated_fee,
        "estimated_profit": estimated_profit,
        "decision": decision
    })

candidates = sorted(
    candidates,
    key=lambda x: x["estimated_profit"],
    reverse=True
)

OUT.write_text(
    json.dumps(candidates[:20], indent=2),
    encoding="utf-8"
)

print(
    "ARBITRAGE CANDIDATES:",
    len(candidates[:20])
)

for x in candidates[:10]:
    print(
        x["sku"],
        "profit=",
        x["estimated_profit"],
        "decision=",
        x["decision"]
    )

print("REPORT:", OUT)
