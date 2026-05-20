import json
from pathlib import Path
from datetime import datetime, timezone

GATE = Path("app/logs/arbitrage_safety_gate.json")
OUT = Path("app/logs/arbitrage_execution_plan.json")

items = json.loads(GATE.read_text(encoding="utf-8")) if GATE.exists() else []

plan = []

for item in items:
    if not item.get("allowed"):
        plan.append({
            "sku": item.get("sku"),
            "status": "blocked",
            "reasons": item.get("reasons", [])
        })
        continue

    plan.append({
        "sku": item.get("sku"),
        "status": "ready_for_cross_market_execution",
        "steps": [
            "confirm_active_listing",
            "monitor_order",
            "on_paid_order_run_fulfillment_guard",
            "purchase_from_source_channel",
            "push_tracking_to_sales_channels",
            "record_profit"
        ],
        "estimated_profit": item.get("estimated_profit"),
        "source_channel": item.get("source_channel"),
        "created_at": datetime.now(timezone.utc).isoformat()
    })

OUT.write_text(
    json.dumps(plan, indent=2),
    encoding="utf-8"
)

print("ARBITRAGE EXECUTION PLAN:", len(plan))

for x in plan:
    print(x["sku"], "=>", x["status"])
