import json
from pathlib import Path

ORDERS = Path("app/logs/incoming_orders.json")
QUEUE = Path("app/logs/supplier_purchase_queue.json")
ATTEMPTS = Path("app/logs/cj_purchase_attempts.json")
TRACKING = Path("app/logs/tracking_updates.json")
OUT = Path("app/logs/fulfillment_status_report.json")

def load(path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []

orders = load(ORDERS)
queue = load(QUEUE)
attempts = load(ATTEMPTS)
tracking = load(TRACKING)

report = {
    "orders_received": len(orders),
    "ready_for_supplier_purchase": len(queue),
    "cj_purchase_attempts": len(attempts),
    "waiting_for_tracking": len([
        x for x in tracking
        if x.get("status") == "waiting_for_supplier_tracking"
    ]),
    "tracking_ready_to_push": len([
        x for x in tracking
        if x.get("tracking_number")
        and x.get("channel_update_status") == "pending"
    ])
}

OUT.write_text(
    json.dumps(report, indent=2),
    encoding="utf-8"
)

print("=== FULFILLMENT STATUS ===")
for k,v in report.items():
    print(k + ":", v)
