import json
from pathlib import Path
from datetime import datetime, timezone

REGISTRY = Path("app/logs/live_campaign_registry.json")
GATE = Path("app/logs/live_spend_permission_gate.json")
CFG = Path("app/config/auto_spend_guardrails.json")
OUT = Path("app/logs/live_api_execution_gate.json")

registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
gate = json.loads(GATE.read_text(encoding="utf-8"))
cfg = json.loads(CFG.read_text(encoding="utf-8"))

approved = []

for item in registry.get("campaigns", []):
    can_execute = (
        item.get("ready_for_live_api") is True
        and gate.get("final_spend_permission") is True
        and not cfg.get("emergency_stop", True)
        and cfg.get("allow_live_spending") is True
    )

    approved.append({
        "sku": item["sku"],
        "platform": item["platform"],
        "campaign_name": item["campaign_name"],
        "daily_budget": item["daily_budget"],
        "can_execute_live_api": can_execute,
        "execution_mode": "LIVE_API_READY_DRY_RUN" if can_execute else "BLOCKED",
        "real_money_spent": 0
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "approved_live_api_actions": approved,
    "approved_count": len([x for x in approved if x["can_execute_live_api"]]),
    "real_money_spent": 0,
    "status": "LIVE_API_EXECUTION_GATE_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

print(json.dumps(report, indent=2))
