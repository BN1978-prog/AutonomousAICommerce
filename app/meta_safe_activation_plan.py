import json
from pathlib import Path
from datetime import datetime, timezone

CONTROL = Path("app/logs/global_commerce_control_panel.json")
REG = Path("app/logs/meta_campaign_registry.json")
OUT = Path("app/logs/meta_safe_activation_plan.json")

control = json.loads(CONTROL.read_text(encoding="utf-8")) if CONTROL.exists() else {}
reg = json.loads(REG.read_text(encoding="utf-8")) if REG.exists() else {}

plans = []
blocked = []

for c in reg.get("campaigns", []):
    if c.get("status") != "PAUSED":
        blocked.append({**c, "reason": "campaign_not_paused"})
        continue

    plans.append({
        "sku": c.get("sku"),
        "campaign_name": c.get("campaign_name"),
        "meta_campaign_id": c.get("meta_campaign_id"),
        "current_status": "PAUSED",
        "recommended_next_status": "ACTIVE",
        "max_daily_budget_usd": 5,
        "max_test_duration_hours": 24,
        "auto_stop_rules": [
            "stop_if_spend_reaches_5_usd",
            "stop_if_no_sales_after_24_hours",
            "stop_if_negative_roi_detected"
        ],
        "activation_allowed_now": False,
        "reason": "manual_owner_activation_required"
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "mode": "safe_activation_planning_only",
    "plans_created": len(plans),
    "blocked": blocked,
    "plans": plans,
    "live_money_spending": False,
    "status": "META_SAFE_ACTIVATION_PLAN_READY" if plans else "NO_META_CAMPAIGNS_TO_ACTIVATE"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
