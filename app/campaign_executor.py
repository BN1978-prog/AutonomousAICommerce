import json
from pathlib import Path
from datetime import datetime, timezone

IN = Path("app/logs/real_traffic_launcher.json")
LIMITS = Path("app/logs/ad_spend_limits.json")
OUT = Path("app/logs/campaign_executor.json")

data = json.loads(IN.read_text(encoding="utf-8")) if IN.exists() else {}
limits = json.loads(LIMITS.read_text(encoding="utf-8")) if LIMITS.exists() else {
    "auto_ad_spend_enabled": False,
    "max_daily_campaign_budget": 5,
    "allowed_channels": ["google_ads", "meta_ads"],
    "require_margin_percent": 35,
    "require_net_profit": 10
}

approved = []
blocked = []

auto_spend = bool(limits.get("auto_ad_spend_enabled", False))

for c in data.get("campaigns", []):
    budget = float(c.get("daily_test_budget", 0))
    margin = float(c.get("margin_percent", 0))
    profit = float(c.get("net_profit", 0))
    channels = c.get("channels", [])

    if budget > float(limits.get("max_daily_campaign_budget", 5)):
        blocked.append({**c, "reason": "daily_budget_above_safe_limit"})
        continue

    if margin < float(limits.get("require_margin_percent", 35)):
        blocked.append({**c, "reason": "margin_below_safe_limit"})
        continue

    if profit < float(limits.get("require_net_profit", 10)):
        blocked.append({**c, "reason": "profit_below_safe_limit"})
        continue

    if any(ch not in limits.get("allowed_channels", []) for ch in channels):
        blocked.append({**c, "reason": "channel_not_allowed"})
        continue

    approved.append({
        **c,
        "spend_enabled": auto_spend,
        "executor_mode": "auto_launch_allowed_by_limits" if auto_spend else "manual_launch_required",
        "status": "ready_for_auto_launch" if auto_spend else "approved_for_manual_launch"
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "mode": "campaign_executor_with_limits",
    "auto_ad_spend_enabled": auto_spend,
    "approved": len(approved),
    "blocked": blocked,
    "campaigns": approved,
    "spend_enabled": auto_spend and len(approved) > 0,
    "status": "ready_for_auto_launch" if auto_spend and approved else ("approved_for_manual_launch" if approved else "no_campaigns_approved")
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
