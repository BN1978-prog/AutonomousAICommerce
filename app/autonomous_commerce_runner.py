
import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/autonomous_commerce_runner.json")

STEPS = [
    ("autonomous_runtime_mode", "python -m app.autonomous_runtime_mode"),

    # Product discovery / listing / publishing
    ("sku_master_enricher", "python -m app.sku_master_enricher"),
    ("cj_product_discovery_importer", "python -m app.cj_product_discovery_importer"),
    ("product_scoring_engine", "python -m app.product_scoring_engine"),
    ("seo_content_engine", "python -m app.seo_content_engine"),
    ("universal_listing_builder", "python -m app.universal_listing_builder"),
    ("marketplace_listing_optimizer", "python -m app.marketplace_listing_optimizer"),
    ("universal_publisher", "python -m app.universal_publisher"),

    # Paid-order fulfillment
    ("autonomous_fulfillment_runner", "python -m app.autonomous_fulfillment_runner"),

    # Readiness
    ("autonomous_commerce_readiness", "python -m app.autonomous_commerce_readiness"),
]

results = []

for name, command in STEPS:
    p = subprocess.run(command, shell=True, capture_output=True, text=True)

    results.append({
        "name": name,
        "command": command,
        "returncode": p.returncode,
        "status": "OK" if p.returncode == 0 else "ERROR",
        "stdout": p.stdout[-4000:],
        "stderr": p.stderr[-4000:]
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "status": "AUTONOMOUS_COMMERCE_RUN_COMPLETED",
    "steps": results,
    "errors": [x for x in results if x["status"] != "OK"],
    "note": "One-command autonomous commerce cycle: discover, score, publish, collect paid orders, gate supplier purchase, track fulfillment."
}

OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(report, indent=2, ensure_ascii=False))
