import json
from pathlib import Path
from datetime import datetime, timezone

CANDIDATES = Path("app/logs/market_arbitrage_candidates.json")
OUT = Path("app/logs/arbitrage_decisions.json")

items = json.loads(CANDIDATES.read_text(encoding="utf-8")) if CANDIDATES.exists() else []

decisions = []

for item in items:
    actions = []

    if item.get("decision") == "publish":
        actions.append({
            "type": "cross_market_publish",
            "confidence": "medium",
            "reason": "Estimated profit is above arbitrage threshold.",
            "target_channel": item.get("target_channel"),
            "target_price": item.get("target_price")
        })

    elif item.get("decision") == "watch":
        actions.append({
            "type": "watch_arbitrage",
            "confidence": "low",
            "reason": "Estimated profit is too low for safe resale."
        })

    decisions.append({
        "sku": item.get("sku"),
        "source_channel": item.get("source_channel"),
        "source_price": item.get("source_price"),
        "estimated_profit": item.get("estimated_profit"),
        "actions": actions,
        "decided_at": datetime.now(timezone.utc).isoformat()
    })

OUT.write_text(
    json.dumps(decisions, indent=2),
    encoding="utf-8"
)

print("ARBITRAGE DECISIONS:", len(decisions))

for d in decisions:
    print(
        d["sku"],
        "=>",
        ", ".join(a["type"] for a in d["actions"])
    )
