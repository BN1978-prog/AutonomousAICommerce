import json
import os
from pathlib import Path
from datetime import datetime, timezone

CFG = Path("app/config/auto_spend_guardrails.json")
LOCK = Path("app/logs/live_mode_final_lock.json")
GOOGLE = Path("app/logs/google_live_campaign_payloads.json")
OUT = Path("app/logs/google_live_execution_result.json")

# load .env
env_path = Path(".env")
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8-sig").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip()

cfg = json.loads(CFG.read_text(encoding="utf-8"))
lock = json.loads(LOCK.read_text(encoding="utf-8"))
google = json.loads(GOOGLE.read_text(encoding="utf-8"))

required = [
    "GOOGLE_ADS_DEVELOPER_TOKEN",
    "GOOGLE_ADS_CLIENT_ID",
    "GOOGLE_ADS_CLIENT_SECRET",
    "GOOGLE_ADS_REFRESH_TOKEN",
    "GOOGLE_ADS_CUSTOMER_ID"
]

missing = [x for x in required if not os.getenv(x)]

real_execution_enabled = (
    cfg.get("allow_live_spending") is True
    and cfg.get("emergency_stop") is False
    and lock.get("live_mode_allowed") is True
    and not missing
)

results = []

for item in google.get("payloads", []):
    results.append({
        "sku": item["sku"],
        "platform": "google",
        "campaign_name": item["campaign_name"],
        "requested_status": "PAUSED",
        "real_api_called": False,
        "reason": "google_ads_api_payload_ready_but_sdk_call_not_enabled_yet",
        "credentials_ready": not missing,
        "missing_credentials": missing,
        "real_money_spent": 0
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "real_execution_enabled": bool(real_execution_enabled),
    "campaigns_checked": len(results),
    "results": results,
    "real_money_spent": 0,
    "status": "GOOGLE_LIVE_EXECUTOR_PAUSED_ONLY_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

print(json.dumps(report, indent=2))
