import json
import os
from pathlib import Path
from datetime import datetime, timezone
import requests

CFG = Path("app/config/auto_spend_guardrails.json")
LOCK = Path("app/logs/live_mode_final_lock.json")
META = Path("app/logs/meta_live_campaign_payloads.json")
OUT = Path("app/logs/meta_live_execution_result.json")

cfg = json.loads(CFG.read_text(encoding="utf-8"))
lock = json.loads(LOCK.read_text(encoding="utf-8"))
meta = json.loads(META.read_text(encoding="utf-8"))


# load .env
env_path = Path(".env")
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8-sig").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip()

ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
AD_ACCOUNT_ID = os.getenv("META_AD_ACCOUNT_ID")
API_VERSION = os.getenv("META_API_VERSION", "v22.0")

results = []

real_execution_enabled = (
    cfg.get("allow_live_spending") is True
    and cfg.get("emergency_stop") is False
    and lock.get("live_mode_allowed") is True
    and ACCESS_TOKEN
    and AD_ACCOUNT_ID
)

for item in meta.get("payloads", []):
    payload = {
        "name": item["campaign_name"],
        "objective": item.get("objective", "OUTCOME_SALES"),
        "status": "PAUSED",
        "special_ad_categories": "[]",
        "is_adset_budget_sharing_enabled": "false",
        "access_token": ACCESS_TOKEN
    }

    if real_execution_enabled:
        account_id = AD_ACCOUNT_ID
        if not account_id.startswith("act_"):
            account_id = f"act_{account_id}"

        url = f"https://graph.facebook.com/{API_VERSION}/{account_id}/campaigns"

        r = requests.post(url, data=payload, timeout=30)

        results.append({
            "sku": item["sku"],
            "platform": "meta",
            "campaign_name": item["campaign_name"],
            "requested_status": "PAUSED",
            "http_status": r.status_code,
            "response": r.text,
            "real_api_called": True,
            "real_money_spent": 0
        })
    else:
        results.append({
            "sku": item["sku"],
            "platform": "meta",
            "campaign_name": item["campaign_name"],
            "requested_status": "PAUSED",
            "real_api_called": False,
            "reason": "missing_credentials_or_gate_blocked",
            "real_money_spent": 0
        })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "real_execution_enabled": bool(real_execution_enabled),
    "campaigns_attempted": len(results),
    "results": results,
    "real_money_spent": 0,
    "status": "META_LIVE_EXECUTOR_PAUSED_ONLY_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

print(json.dumps(report, indent=2))
