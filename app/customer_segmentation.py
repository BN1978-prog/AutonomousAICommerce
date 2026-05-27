import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/customer_segmentation.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

analytics = read_json("app/logs/customer_analytics.json")

customers = analytics.get("customers", [])

segments = {
    "new_customers": [],
    "repeat_customers": [],
    "high_value_customers": [],
    "inactive_customers": []
}

for customer in customers:
    orders = customer.get("orders", 0)
    ltv = customer.get("estimated_ltv", 0)

    if orders <= 1:
        segments["new_customers"].append(customer)

    if orders > 1:
        segments["repeat_customers"].append(customer)

    if ltv >= 100:
        segments["high_value_customers"].append(customer)

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "customers_seen": len(customers),
    "segments": {
        "new_customers": len(segments["new_customers"]),
        "repeat_customers": len(segments["repeat_customers"]),
        "high_value_customers": len(segments["high_value_customers"]),
        "inactive_customers": len(segments["inactive_customers"])
    },
    "segment_details": segments,
    "recommended_actions": [
        {
            "segment": "new_customers",
            "action": "send_welcome_flow"
        },
        {
            "segment": "repeat_customers",
            "action": "send_loyalty_offer"
        },
        {
            "segment": "high_value_customers",
            "action": "protect_with_priority_support"
        },
        {
            "segment": "inactive_customers",
            "action": "send_win_back_flow"
        }
    ],
    "status": "CUSTOMER_SEGMENTATION_WAITING_FOR_SALES" if not customers else "CUSTOMER_SEGMENTATION_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
