import json
import os
from pathlib import Path
from datetime import datetime, timezone
import requests

EXEC = Path("app/logs/meta_live_execution_result.json")
OUT = Path("app/logs/meta_adset_builder_result.json")

# load .env
env_path = Path(".env")
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8-sig").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip()

ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
AD_ACCOUNT_ID = os.getenv("META_AD_ACCOUNT_ID")
PIXEL_ID = os.getenv("META_PIXEL_ID")
API_VERSION = os.getenv("META_API_VERSION", "v22.0")

data = json.loads(EXEC.read_text(encoding="utf-8"))

results=[]

for item in data.get("results",[]):

    if item.get("http_status") != 200:
        continue

    campaign_response = json.loads(item["response"])
    campaign_id = campaign_response["id"]

    account_id = AD_ACCOUNT_ID
    if not account_id.startswith("act_"):
        account_id = f"act_{account_id}"

    payload = {
        "name": f"{item['campaign_name']}_ADSET",
        "campaign_id": campaign_id,
        "billing_event": "IMPRESSIONS",
        "optimization_goal": "OFFSITE_CONVERSIONS",
        "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
        "daily_budget": "2500",
        "status": "PAUSED",
        "targeting": json.dumps({
            "geo_locations": {
                "countries": ["US"]
            }
        }),
        "promoted_object": json.dumps({
            "pixel_id": PIXEL_ID,
            "custom_event_type": "PURCHASE"
        }),
        "access_token": ACCESS_TOKEN
    }

    url = f"https://graph.facebook.com/{API_VERSION}/{account_id}/adsets"

    r = requests.post(url, data=payload, timeout=30)

    results.append({
        "campaign_id": campaign_id,
        "http_status": r.status_code,
        "response": r.text,
        "requested_status": "PAUSED",
        "real_money_spent": 0
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "results": results,
    "status": "META_ADSET_BUILDER_PAUSED_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

print(json.dumps(report, indent=2))
