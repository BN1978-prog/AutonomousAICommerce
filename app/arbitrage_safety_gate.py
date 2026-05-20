import json
from pathlib import Path

IMPORTS = Path("app/logs/imported_skus.json")
DECISIONS = Path("app/logs/arbitrage_decisions.json")
OUT = Path("app/logs/arbitrage_safety_gate.json")

imports = json.loads(IMPORTS.read_text(encoding="utf-8")) if IMPORTS.exists() else {}
decisions = json.loads(DECISIONS.read_text(encoding="utf-8")) if DECISIONS.exists() else []

results = []

MIN_PROFIT = 5.00

for d in decisions:
    sku = d.get("sku")
    meta = imports.get(sku, {})

    allowed = True
    reasons = []

    profit = float(d.get("estimated_profit", 0) or 0)
    source = d.get("source_channel")

    if profit < MIN_PROFIT:
        allowed = False
        reasons.append("profit_below_threshold")

    if not source:
        allowed = False
        reasons.append("missing_source_channel")

    if not meta.get("product_id"):
        allowed = False
        reasons.append("missing_shopify_product")

    if meta.get("ebay_status") != "published":
        allowed = False
        reasons.append("missing_ebay_publish")

    if meta.get("risk") in ["high", "blocked"]:
        allowed = False
        reasons.append("risk_blocked")

    action_types = [
        a.get("type")
        for a in d.get("actions", [])
    ]

    if "cross_market_publish" not in action_types:
        allowed = False
        reasons.append("not_publish_decision")

    results.append({
        "sku": sku,
        "allowed": allowed,
        "estimated_profit": profit,
        "source_channel": source,
        "reasons": reasons,
        "action": "approve_arbitrage" if allowed else "block_or_watch"
    })

OUT.write_text(
    json.dumps(results, indent=2),
    encoding="utf-8"
)

print("ARBITRAGE SAFETY RESULTS:", len(results))

for r in results:
    print(
        r["sku"],
        "allowed=",
        r["allowed"],
        "profit=",
        r["estimated_profit"],
        "reasons=",
        ",".join(r["reasons"])
    )
