import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/supplier_fallback_engine.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

cj = read_json("app/logs/cj_supplier_readiness.json")

suppliers = [
    {
        "name":"cjdropshipping",
        "priority":1,
        "ready": cj.get("ok") is True,
        "status": cj.get("status")
    },
    {
        "name":"aliexpress",
        "priority":2,
        "ready": False,
        "status":"not_connected_yet"
    },
    {
        "name":"amazon",
        "priority":3,
        "ready": False,
        "status":"waiting_sp_api_verification"
    },
    {
        "name":"ebay",
        "priority":4,
        "ready": True,
        "status":"fallback_market_available"
    }
]

active = [s for s in suppliers if s["ready"]]

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "suppliers": suppliers,
    "active_suppliers": active,
    "primary_supplier": active[0]["name"] if active else None,
    "fallback_available": len(active) > 1,
    "status": "SUPPLIER_FALLBACK_READY" if active else "NO_SUPPLIER_AVAILABLE"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
