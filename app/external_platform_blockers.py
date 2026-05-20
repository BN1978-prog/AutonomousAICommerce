import json
from pathlib import Path
from datetime import datetime, timezone

META_REG = Path("app/logs/meta_campaign_registry.json")
META_RESULT = Path("app/logs/meta_campaign_live_result.json")
GOOGLE_RESULT = Path("app/logs/google_campaign_live_result.json")
OUT = Path("app/logs/external_platform_blockers.json")

def load(path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}

meta_reg = load(META_REG)
meta_result = load(META_RESULT)
google_result = load(GOOGLE_RESULT)

blockers = []
ready = []

if meta_reg.get("campaigns_registered", 0) > 0:
    ready.append({
        "platform": "meta_ads",
        "status": "ready_paused_campaigns_created",
        "campaigns": meta_reg.get("campaigns_registered", 0),
        "spend_enabled": False
    })
else:
    blockers.append({
        "platform": "meta_ads",
        "status": "not_ready",
        "reason": meta_result.get("status", "no_meta_campaign_registry")
    })

google_text = json.dumps(google_result)

if google_result.get("status") == "blocked":
    blockers.append({
        "platform": "google_ads",
        "status": "blocked_external_platform_permission",
        "reason": "DEVELOPER_TOKEN_NOT_APPROVED_OR_TEST_ONLY",
        "action_required": "apply_for_google_ads_api_basic_or_standard_access_or_use_test_account"
    })
elif "DEVELOPER_TOKEN_NOT_APPROVED" in google_text:
    blockers.append({
        "platform": "google_ads",
        "status": "blocked_external_platform_permission",
        "reason": "DEVELOPER_TOKEN_NOT_APPROVED",
        "action_required": "apply_for_google_ads_api_basic_or_standard_access"
    })
elif google_result.get("created", 0) > 0:
    ready.append({
        "platform": "google_ads",
        "status": "ready_paused_campaigns_created",
        "campaigns": google_result.get("created", 0),
        "spend_enabled": False
    })
else:
    blockers.append({
        "platform": "google_ads",
        "status": "not_ready_or_not_attempted",
        "reason": google_result.get("status", "no_google_result")
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "ready_platforms": ready,
    "blockers": blockers,
    "ready_count": len(ready),
    "blocker_count": len(blockers),
    "status": "external_blockers_present" if blockers else "all_external_platforms_ready"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
