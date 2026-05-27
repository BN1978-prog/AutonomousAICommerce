import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/real_sales_loop_status.json")

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
router = read_json("app/logs/autonomous_order_router.json")
drafts = read_json("app/logs/cj_order_drafts.json")
payloads = read_json("app/logs/cj_order_payloads.json")
address_validation = read_json("app/logs/cj_customer_address_validator.json")
supplier = read_json("app/logs/cj_supplier_readiness.json")

has_sales = sales.get("has_real_sales") is True
orders_seen = orders.get("orders_seen", 0) or 0
addresses_collected = orders.get("addresses_collected", 0) or 0
queue_size = router.get("queue_size", 0) or 0

checks = {
    "has_real_sales": has_sales,
    "orders_seen": orders_seen > 0,
    "addresses_collected": addresses_collected > 0,
    "supplier_ready": supplier.get("ok") is True,
    "queue_ready": queue_size > 0
}

blocked_reasons = []

if not has_sales:
    blocked_reasons.append("waiting_for_real_sales")

if orders_seen == 0:
    blocked_reasons.append("no_shopify_orders_seen")

if addresses_collected == 0:
    blocked_reasons.append("no_customer_addresses_collected")

if supplier.get("ok") is not True:
    blocked_reasons.append("supplier_not_ready")

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "checks": checks,
    "orders_seen": orders_seen,
    "addresses_collected": addresses_collected,
    "queue_size": queue_size,
    "supplier_status": supplier.get("status"),
    "blocked_reasons": blocked_reasons,
    "next_step": "wait_for_real_paid_order" if not has_sales else "create_supplier_draft",
    "status": "REAL_SALES_LOOP_WAITING" if blocked_reasons else "REAL_SALES_LOOP_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
