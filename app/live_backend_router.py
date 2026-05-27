import json
from pathlib import Path
from datetime import datetime, timezone

GATE = Path("app/logs/live_spend_permission_gate.json")
OUT = Path("app/logs/live_backend_router.json")

gate = json.loads(GATE.read_text(encoding="utf-8"))

routes = []

for item in gate.get("approved_campaigns", []):
    if item.get("live_launch_permission"):
        routes.append({
            "sku": item["sku"],
            "budget": item["requested_budget"],
            "meta_route": "READY",
            "google_route": "READY",
            "execution_mode": "LIVE_BACKEND_READY_NOT_SENT",
            "real_money_spent": 0
        })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "routes": routes,
    "routes_count": len(routes),
    "status": "LIVE_BACKEND_ROUTER_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

print(json.dumps(report, indent=2))
