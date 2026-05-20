import json
from pathlib import Path
from datetime import datetime, timezone

REPORT = Path("app/logs/opportunities/global_arbitrage_report.json")
LIMITS = Path("app/logs/opportunities/global_execution_limits.json")
OUT = Path("app/logs/opportunities/global_execution_plan.json")

report = json.loads(REPORT.read_text(encoding="utf-8"))
limits = json.loads(LIMITS.read_text(encoding="utf-8"))

plans = []
blocked = []

for x in report.get("top_opportunities", []):
    margin = float(x.get("margin_percent", 0))
    profit = float(x.get("net_profit", 0))

    if margin < limits["min_margin_percent"]:
        blocked.append({**x, "reason": "margin_too_low"})
        continue

    if profit < limits["min_net_profit"]:
        blocked.append({**x, "reason": "profit_too_low"})
        continue

    plans.append({
        "sku": x["sku"],
        "title": x["title"],
        "source_market": x["source_market"],
        "target_market": x["target_market"],
        "source_cost": x["source_cost"],
        "target_price": x["target_price"],
        "net_profit": x["net_profit"],
        "margin_percent": x["margin_percent"],
        "action": "prepare_listing_test",
        "auto_purchase": False,
        "purchase_rule": "only_after_real_paid_order",
        "status": "ready_for_safe_listing_test"
    })

plans = plans[:limits["max_test_listings_per_run"]]

out = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "mode": limits["mode"],
    "plans_created": len(plans),
    "blocked": blocked,
    "plans": plans,
    "status": "execution_plan_ready" if plans else "no_safe_plans"
}

OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
print(json.dumps(out, indent=2))
