import json
from pathlib import Path
from datetime import datetime, timezone

IN = Path("app/logs/campaign_executor.json")
GUARD = Path("app/logs/live_ads_guard.json")
CONFIRM = Path("app/logs/CONFIRM_LIVE_ADS_LAUNCH.json")
OUT = Path("app/logs/ad_campaign_executor.json")

data = json.loads(IN.read_text(encoding="utf-8")) if IN.exists() else {}
guard = json.loads(GUARD.read_text(encoding="utf-8")) if GUARD.exists() else {}

live_enabled = bool(guard.get("live_ads_launch_enabled", False))
require_confirm = bool(guard.get("require_final_confirmation_file", True))
confirm_exists = CONFIRM.exists()

actions = []
blocked = []

for c in data.get("campaigns", []):
    if not c.get("spend_enabled"):
        blocked.append({**c, "reason": "spend_not_enabled"})
        continue

    if not live_enabled:
        blocked.append({**c, "reason": "live_ads_launch_disabled_by_guard"})
        continue

    if require_confirm and not confirm_exists:
        blocked.append({**c, "reason": "missing_final_confirmation_file"})
        continue

    actions.append({
        "created_at": datetime.now(timezone.utc).isoformat(),
        "sku": c.get("sku"),
        "title": c.get("title"),
        "channels": c.get("channels", []),
        "daily_budget": c.get("daily_test_budget", 0),
        "action": "would_call_live_ads_api",
        "mode": "guard_passed_but_api_call_not_implemented",
        "status": "ready_for_real_google_meta_api_code"
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "mode": "guarded_live_ads_executor",
    "live_ads_launch_enabled": live_enabled,
    "confirmation_file_exists": confirm_exists,
    "actions_ready": len(actions),
    "blocked": blocked,
    "actions": actions,
    "status": "blocked_by_guard" if blocked and not actions else "ready_for_live_api_code"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
