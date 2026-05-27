import json
from pathlib import Path
from datetime import datetime, timezone

VALIDATOR = Path("app/logs/emergency_stop_validator.json")
EXECUTOR = Path("app/logs/auto_spend_executor.json")
OUT = Path("app/logs/live_spend_permission_gate.json")

validator = json.loads(VALIDATOR.read_text(encoding="utf-8"))
executor = json.loads(EXECUTOR.read_text(encoding="utf-8"))

approved_campaigns = []

for item in executor.get("executions", []):
    allowed = (
        validator.get("final_spend_permission") is True
        and item.get("execution_allowed") is True
        and item.get("next_action") == "PREPARE_LIVE_CAMPAIGN"
    )

    approved_campaigns.append({
        "sku": item["sku"],
        "requested_budget": item["requested_budget"],
        "live_launch_permission": allowed,
        "next_action": "READY_FOR_LIVE_BACKEND" if allowed else "BLOCKED"
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "final_spend_permission": validator.get("final_spend_permission"),
    "approved_campaigns": approved_campaigns,
    "real_money_spent": 0,
    "status": "LIVE_SPEND_PERMISSION_GATE_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

print(json.dumps(report, indent=2))
