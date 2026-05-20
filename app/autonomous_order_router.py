import json
from pathlib import Path
from datetime import datetime, timezone

ORDERS=Path("app/logs/incoming_orders.json")
LIMITS=Path("app/logs/autonomy_limits.json")
QUEUE=Path("app/logs/supplier_purchase_queue.json")
OUT=Path("app/logs/autonomous_order_router.json")

orders=json.loads(ORDERS.read_text(encoding="utf-8")) if ORDERS.exists() else []
limits=json.loads(LIMITS.read_text(encoding="utf-8")) if LIMITS.exists() else {}
queue=json.loads(QUEUE.read_text(encoding="utf-8")) if QUEUE.exists() else []

max_order_cost=limits.get("max_order_cost",50)
min_margin=limits.get("min_margin_percent",25)

created=[]
skipped=[]

for order in orders:
    if not order.get("paid", False):
        skipped.append({"order":order.get("id"),"reason":"not_paid"})
        continue

    sku=order.get("sku")
    sale_price=float(order.get("sale_price",0))
    supplier_cost=float(order.get("supplier_cost",0))

    if supplier_cost<=0:
        skipped.append({"order":order.get("id"),"sku":sku,"reason":"missing_supplier_cost"})
        continue

    margin=((sale_price-supplier_cost)/sale_price)*100 if sale_price else 0

    if supplier_cost>max_order_cost:
        skipped.append({"order":order.get("id"),"sku":sku,"reason":"supplier_cost_above_limit"})
        continue

    if margin<min_margin:
        skipped.append({"order":order.get("id"),"sku":sku,"reason":"margin_below_limit","margin":round(margin,2)})
        continue

    item={
        "created_at":datetime.now(timezone.utc).isoformat(),
        "order_id":order.get("id"),
        "sku":sku,
        "quantity":order.get("quantity",1),
        "sale_price":sale_price,
        "supplier_cost":supplier_cost,
        "margin_percent":round(margin,2),
        "status":"queued_for_supplier_purchase",
        "requires_supplier_api":True
    }

    queue.append(item)
    created.append(item)

QUEUE.write_text(json.dumps(queue,indent=2),encoding="utf-8")

report={
    "created_at":datetime.now(timezone.utc).isoformat(),
    "orders_seen":len(orders),
    "queued":len(created),
    "skipped":skipped,
    "queue_size":len(queue),
    "status":"ready_waiting_orders" if not orders else "processed_orders"
}

OUT.write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps(report,indent=2))
