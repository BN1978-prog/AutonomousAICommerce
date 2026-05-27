import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/budget_controller.json")

LIMITS = {
    "max_total_daily_spend": 10,
    "max_campaign_daily_spend": 5,
    "stop_if_negative_roi": True,
    "stop_if_no_sales_after_hours": 24
}

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

dashboard = read_json("app/logs/system_status_dashboard.json")
sales = read_json("app/logs/real_sales_mode.json")
control = read_json("app/logs/global_commerce_control_panel.json")

live_spend = dashboard.get("live_money_spending") is True
has_sales = sales.get("has_real_sales") is True
safe_to_continue = dashboard.get("safe_to_continue") is True

blocked = []

if not safe_to_continue:
    blocked.append("system_not_safe_to_continue")

if live_spend:
    blocked.append("live_money_spending_enabled_requires_budget_watch")

if not has_sales:
    blocked.append("no_real_sales_yet_keep_test_budget_only")

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "limits": LIMITS,
    "live_money_spending": live_spend,
    "has_real_sales": has_sales,
    "safe_to_continue": safe_to_continue,
    "blocked": blocked,
    "budget_status": "BUDGET_SAFE_MODE",
    "activation_allowed": False,
    "reason": "safe_budget_guard_active_until_owner_confirms"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
