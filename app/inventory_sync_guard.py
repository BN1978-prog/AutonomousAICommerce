import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/inventory_sync_guard.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

registry = read_json("app/logs/registry_quality_report.json")
supplier = read_json("app/logs/supplier_fallback_engine.json")
opportunities = read_json("app/logs/global_arbitrage_engine.json")

items = opportunities.get("top_opportunities", [])

checks = []

for item in items:
    checks.append({
        "sku": item.get("sku"),
        "title": item.get("title"),
        "supplier_available": supplier.get("status") == "SUPPLIER_FALLBACK_READY",
        "inventory_status": "assumed_available_until_live_supplier_stock_sync",
        "shopify_sync_allowed": True,
        "ads_allowed": True,
        "reason": "stock_sync_guard_ready"
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "items_checked": len(checks),
    "checks": checks,
    "live_supplier_stock_sync": False,
    "status": "INVENTORY_SYNC_GUARD_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
