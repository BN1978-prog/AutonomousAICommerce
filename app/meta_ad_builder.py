import json
import os
from pathlib import Path
from datetime import datetime, timezone
import requests

ADSET = Path("app/logs/meta_adset_builder_result.json")
CREATIVE = Path("app/logs/meta_creative_builder_result.json")
OUT = Path("app/logs/meta_ad_builder_result.json")

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

adset_data = json.loads(ADSET.read_text(encoding="utf-8"))
creative_data = json.loads(CREATIVE.read_text(encoding="utf-8"))

creative_id = None

for x in creative_data.get("results", []):
    if x.get("http_status") == 200:
        creative_id = json.loads(x["response"])["id"]

results=[]

account_id = AD_ACCOUNT_ID
if not account_id.startswith("act_"):
    account_id = f"act_{account_id}"

for item in adset_data.get("results",[]):

    if item.get("http_status") != 200:
        continue

    adset_id = json.loads(item["response"])["id"]

    payload = {
        "name": "AICommerce_AD_non_slip_silicone_pet_feeding_bowl",
        "adset_id": adset_id,
        "creative": json.dumps({
            "creative_id": creative_id
        }),
        "status": "PAUSED",
        "access_token": ACCESS_TOKEN
    }

    url = f"https://graph.facebook.com/{API_VERSION}/{account_id}/ads"

    r = requests.post(url, data=payload, timeout=30)

    results.append({
        "adset_id": adset_id,
        "creative_id": creative_id,
        "http_status": r.status_code,
        "response": r.text,
        "requested_status": "PAUSED",
        "real_money_spent": 0
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "results": results,
    "status": "META_AD_BUILDER_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

print(json.dumps(report, indent=2))
