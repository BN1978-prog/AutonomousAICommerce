import json
from pathlib import Path
from datetime import datetime, timezone

PAYLOADS=Path("app/logs/cj_order_payloads.json")
OUT=Path("app/logs/cj_customer_address_validator.json")

payloads=json.loads(PAYLOADS.read_text(encoding="utf-8")) if PAYLOADS.exists() else []

ready=[]
blocked=[]

required=[
    "firstName",
    "lastName",
    "address1",
    "city",
    "province",
    "countryCode",
    "zip",
    "phone"
]

for p in payloads:
    address=p.get("shipping_address") or {}
    missing=[k for k in required if not address.get(k)]

    if missing:
        blocked.append({
            "order_id":p.get("order_id"),
            "status":"blocked_missing_customer_shipping_address",
            "missing":missing
        })
    else:
        ready.append({
            "order_id":p.get("order_id"),
            "status":"ready_for_cj_create_order"
        })

report={
    "created_at":datetime.now(timezone.utc).isoformat(),
    "payloads_seen":len(payloads),
    "ready_for_cj":len(ready),
    "blocked":blocked,
    "ready":ready,
    "status":"ready_for_cj_create_order" if ready else "blocked_waiting_customer_address"
}

OUT.write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps(report,indent=2))
