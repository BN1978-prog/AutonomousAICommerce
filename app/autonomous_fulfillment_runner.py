
import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/autonomous_fulfillment_runner.json")

STEPS = [
    ("autonomous_runtime_mode", "python -m app.autonomous_runtime_mode"),
    ("collect_shopify_orders", "python -m app.collect_shopify_orders"),
    ("collect_woocommerce_orders", "python -m app.collect_woocommerce_orders"),
    ("collect_ebay_orders", "python -m app.collect_ebay_orders"),
    ("collect_etsy_orders", "python -m app.collect_etsy_orders"),
    ("collect_incoming_orders", "python -m app.collect_incoming_orders"),
    ("supplier_purchase_queue", "python -m app.supplier_purchase_queue"),
    ("cj_order_draft_creator", "python -m app.cj_order_draft_creator"),
    ("cj_payload_builder", "python -m app.cj_payload_builder"),
    ("cj_customer_address_validator", "python -m app.cj_customer_address_validator"),
    ("autonomous_commerce_live_gate", "python -m app.autonomous_commerce_live_gate"),
    ("cj_purchase_executor", "python -m app.cj_purchase_executor"),
    ("tracking_sync", "python -m app.tracking_sync"),
    ("shopify_fulfillment_sync", "python -m app.shopify_fulfillment_sync"),
]

results = []

for name, command in STEPS:
    p = subprocess.run(command, shell=True, capture_output=True, text=True)

    results.append({
        "name": name,
        "command": command,
        "returncode": p.returncode,
        "status": "OK" if p.returncode == 0 else "ERROR",
        "stdout": p.stdout,
        "stderr": p.stderr
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "status": "AUTONOMOUS_FULFILLMENT_RUN_COMPLETED",
    "steps": results,
    "errors": [x for x in results if x["status"] != "OK"],
    "note": "Autonomous paid-order fulfillment pipeline. Live CJ purchase is controlled by autonomous_commerce_live_gate."
}

OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(report, indent=2, ensure_ascii=False))
