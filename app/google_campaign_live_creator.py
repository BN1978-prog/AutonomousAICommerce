import json
from pathlib import Path
from datetime import datetime, timezone

IN = Path("app/logs/ad_campaign_executor.json")
GUARD = Path("app/logs/google_api_guard.json")
OUT = Path("app/logs/google_campaign_live_creator.json")

data = json.loads(IN.read_text(encoding="utf-8")) if IN.exists() else {}
guard = json.loads(GUARD.read_text(encoding="utf-8")) if GUARD.exists() else {}

google_live_enabled = bool(guard.get("google_live_api_enabled", False))
create_paused = bool(guard.get("create_campaigns_as_paused", True))
max_campaigns = int(guard.get("max_campaigns_per_run", 2))
max_budget = float(guard.get("max_daily_budget", 5))

payloads = []
blocked = []
actions = []

for a in data.get("actions", []):
    if "google_ads" not in a.get("channels", []):
        continue

    budget = float(a.get("daily_budget", 0))

    if budget > max_budget:
        blocked.append({**a, "reason": "budget_above_google_guard_limit"})
        continue

    payload = {
        "sku": a.get("sku"),
        "title": a.get("title"),
        "channel": "google_ads",
        "daily_budget": budget,
        "campaign_name": f"AIC_TEST_{a.get('sku')}",
        "advertising_channel_type": "SEARCH",
        "status": "PAUSED" if create_paused else "ENABLED"
    }

    payloads.append({
        **payload,
        "mode": "payload_only_no_api_call" if not google_live_enabled else "would_call_google_ads_api"
    })

payloads = payloads[:max_campaigns]

if google_live_enabled:
    for p in payloads:
        actions.append({
            **p,
            "action": "would_post_to_google_ads_campaign_endpoint",
            "status": "ready_for_real_google_ads_api_post_code"
        })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "mode": "google_creator_with_api_guard",
    "google_live_api_enabled": google_live_enabled,
    "payloads_created": len(payloads),
    "payloads": payloads,
    "actions": actions,
    "blocked": blocked,
    "live_api_call_enabled": google_live_enabled,
    "status": "blocked_by_google_api_guard" if not google_live_enabled else "ready_for_real_google_ads_api_post_code"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
