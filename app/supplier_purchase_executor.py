import json
from pathlib import Path
from datetime import datetime, timezone

QUEUE=Path("app/logs/supplier_purchase_queue.json")
OUT=Path("app/logs/supplier_purchase_executor.json")

queue=json.loads(QUEUE.read_text(encoding="utf-8")) if QUEUE.exists() else []

processed=[]
waiting=[]

for item in queue:
    if item.get("status")=="queued_for_supplier_purchase":
        waiting.append({
            "order_id":item.get("order_id"),
            "sku":item.get("sku"),
            "quantity":item.get("quantity",1),
            "status":"waiting_supplier_api_connection"
        })

report={
    "created_at":datetime.now(timezone.utc).isoformat(),
    "queue_size":len(queue),
    "waiting_supplier_api":len(waiting),
    "processed":processed,
    "waiting":waiting,
    "status":"waiting_supplier_api_connection" if waiting else "idle_no_purchase_queue"
}

OUT.write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps(report,indent=2))
