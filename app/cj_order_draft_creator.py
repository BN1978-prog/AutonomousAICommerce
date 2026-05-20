import json
from pathlib import Path
from datetime import datetime, timezone

QUEUE=Path("app/logs/supplier_purchase_queue.json")
OUT=Path("app/logs/cj_order_drafts.json")
REPORT=Path("app/logs/cj_order_draft_creator.json")

queue=json.loads(QUEUE.read_text(encoding="utf-8")) if QUEUE.exists() else []

drafts=[]
skipped=[]

for item in queue:
    if item.get("status")!="queued_for_supplier_purchase":
        skipped.append({
            "order_id":item.get("order_id"),
            "sku":item.get("sku"),
            "reason":"not_queued_for_supplier_purchase"
        })
        continue

    draft={
        "created_at":datetime.now(timezone.utc).isoformat(),
        "supplier":"cjdropshipping",
        "mode":"draft_only_no_api_call",
        "payType":3,
        "order_id":item.get("order_id"),
        "sku":item.get("sku"),
        "quantity":item.get("quantity",1),
        "sale_price":item.get("sale_price"),
        "supplier_cost":item.get("supplier_cost"),
        "margin_percent":item.get("margin_percent"),
        "status":"draft_ready_waiting_cj_order_mapping",
        "needs_mapping":[
            "CJ productId / variantId",
            "customer shipping address",
            "shipping method",
            "CJ createOrderV3 field mapping"
        ]
    }

    drafts.append(draft)

OUT.write_text(json.dumps(drafts,indent=2),encoding="utf-8")

report={
    "created_at":datetime.now(timezone.utc).isoformat(),
    "queue_size":len(queue),
    "drafts_created":len(drafts),
    "skipped":skipped,
    "status":"idle_no_queue" if not queue else "drafts_created",
    "output_file":str(OUT)
}

REPORT.write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps(report,indent=2))
