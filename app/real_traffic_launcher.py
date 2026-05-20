import json
from pathlib import Path
from datetime import datetime, timezone

EXEC_PLAN = Path("app/logs/opportunities/global_execution_plan.json")
OUT = Path("app/logs/real_traffic_launcher.json")

plan = json.loads(EXEC_PLAN.read_text(encoding="utf-8")) if EXEC_PLAN.exists() else {}

campaigns = []

for p in plan.get("plans", []):
    campaigns.append({
        "sku": p.get("sku"),
        "title": p.get("title"),
        "target_market": p.get("target_market"),
        "margin_percent": p.get("margin_percent"),
        "net_profit": p.get("net_profit"),
        "daily_test_budget": 5,
        "channels": ["google_ads", "meta_ads"],
        "mode": "draft_campaign_only_no_spend",
        "status": "ready_for_manual_campaign_review"
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "mode": "safe_campaign_draft_from_execution_plan",
    "campaigns_created": len(campaigns),
    "campaigns": campaigns,
    "spend_enabled": False,
    "reason": "draft_only_until_auto_ad_spend_enabled",
    "status": "campaign_drafts_ready" if campaigns else "no_campaign_candidates"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
