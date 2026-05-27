import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/customer_analytics.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

sales = read_json("app/logs/real_sales_mode.json")
orders = read_json("app/logs/shopify_order_address_collector.json")

orders_list = orders.get("orders", [])

customers = {}

for order in orders_list:
    email = order.get("email") or "unknown"

    if email not in customers:
        customers[email] = {
            "email": email,
            "orders": 0,
            "estimated_ltv": 0,
            "status": "new_customer"
        }

    customers[email]["orders"] += 1

for email, data in customers.items():
    if data["orders"] > 1:
        data["status"] = "repeat_customer"

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "customers_seen": len(customers),
    "orders_seen": orders.get("orders_seen", 0),
    "has_real_sales": sales.get("has_real_sales"),
    "total_revenue": sales.get("total_revenue", 0),
    "customers": list(customers.values()),
    "metrics": {
        "repeat_customers": len([c for c in customers.values() if c["status"] == "repeat_customer"]),
        "new_customers": len([c for c in customers.values() if c["status"] == "new_customer"]),
        "estimated_ltv_total": sum(c["estimated_ltv"] for c in customers.values())
    },
    "status": "CUSTOMER_ANALYTICS_WAITING_FOR_SALES" if not customers else "CUSTOMER_ANALYTICS_ACTIVE"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
