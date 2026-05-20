import json
from pathlib import Path
from datetime import datetime, timezone

DRAFTS=Path("app/logs/cj_order_drafts.json")
MAPPING=Path("app/logs/cj_product_mapping.json")
OUT=Path("app/logs/cj_order_payloads.json")
REPORT=Path("app/logs/cj_payload_builder.json")

drafts=json.loads(DRAFTS.read_text(encoding="utf-8")) if DRAFTS.exists() else []
mapping=json.loads(MAPPING.read_text(encoding="utf-8")) if MAPPING.exists() else {}

payloads=[]
skipped=[]

for d in drafts:
    sku=d.get("sku")
    m=mapping.get(sku)

    if not m:
        skipped.append({"sku":sku,"order_id":d.get("order_id"),"reason":"missing_cj_mapping"})
        continue

    if "TEMP_" in str(m) or "REAL_" in str(m):
        skipped.append({"sku":sku,"order_id":d.get("order_id"),"reason":"temporary_mapping_values"})
        continue

    payload={
        "created_at":datetime.now(timezone.utc).isoformat(),
        "supplier":"cjdropshipping",
        "endpoint":"createOrderV3",
        "mode":"payload_only_no_api_call",
        "payType":3,
        "order_id":d.get("order_id"),
        "products":[
            {
                "vid":m.get("cj_variant_id"),
                "quantity":d.get("quantity",1)
            }
        ],
        "shipping_method":m.get("shipping_method"),
        "status":"payload_ready_waiting_customer_shipping_address"
    }

    payloads.append(payload)

OUT.write_text(json.dumps(payloads,indent=2),encoding="utf-8")

report={
    "created_at":datetime.now(timezone.utc).isoformat(),
    "drafts_seen":len(drafts),
    "payloads_created":len(payloads),
    "skipped":skipped,
    "status":"payloads_created" if payloads else "waiting_valid_mapping",
    "output_file":str(OUT)
}

REPORT.write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps(report,indent=2))

