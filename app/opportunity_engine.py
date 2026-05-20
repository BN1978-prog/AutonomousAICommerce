import json
from pathlib import Path
from datetime import datetime, timezone

IN = Path("app/logs/opportunities/margin_report.json")
OUT = Path("app/logs/opportunities/opportunity_report.json")

data = json.loads(IN.read_text(encoding="utf-8")) if IN.exists() else {"items":[]}

opportunities = []
rejected = []

for item in data.get("items", []):
    margin = float(item.get("margin_percent", 0))
    profit = float(item.get("net_profit", 0))

    if margin >= 40 and profit >= 10:
        action = "strong_candidate_scale_test"
        priority = "A"
    elif margin >= 25 and profit >= 5:
        action = "candidate_small_test"
        priority = "B"
    else:
        action = "reject"
        priority = "D"

    record = {
        **item,
        "priority": priority,
        "recommended_action": action,
        "execution_mode": "analysis_only_no_purchase_no_listing"
    }

    if action == "reject":
        rejected.append(record)
    else:
        opportunities.append(record)

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "mode": "safe_opportunity_analysis",
    "items_seen": len(data.get("items", [])),
    "opportunities": len(opportunities),
    "rejected": len(rejected),
    "top_opportunities": opportunities,
    "rejected_items": rejected,
    "status": "opportunities_found" if opportunities else "no_opportunities"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
