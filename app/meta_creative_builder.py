import json
import os
from pathlib import Path
from datetime import datetime, timezone
import requests

ADSET = Path("app/logs/meta_adset_builder_result.json")
OUT = Path("app/logs/meta_creative_builder_result.json")

env_path = Path(".env")
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8-sig").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip()

ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
AD_ACCOUNT_ID = os.getenv("META_AD_ACCOUNT_ID")
PAGE_ID = os.getenv("META_PAGE_ID")
PRODUCT_URL = os.getenv("SHOPIFY_PRODUCT_URL")
API_VERSION = os.getenv("META_API_VERSION", "v22.0")

missing = [k for k,v in {
    "META_ACCESS_TOKEN": ACCESS_TOKEN,
    "META_AD_ACCOUNT_ID": AD_ACCOUNT_ID,
    "META_PAGE_ID": PAGE_ID,
    "SHOPIFY_PRODUCT_URL": PRODUCT_URL
}.items() if not v]

data = json.loads(ADSET.read_text(encoding="utf-8"))
results=[]

account_id = AD_ACCOUNT_ID or ""
if account_id and not account_id.startswith("act_"):
    account_id = f"act_{account_id}"

for item in data.get("results",[]):
    if item.get("http_status") != 200:
        continue

    if missing:
        results.append({
            "real_api_called": False,
            "missing": missing,
            "real_money_spent": 0
        })
        continue

    payload = {
        "name": "AICommerce_CREATIVE_non_slip_silicone_pet_feeding_bowl",
        "object_story_spec": json.dumps({
            "page_id": PAGE_ID,
            "link_data": {
                "link": PRODUCT_URL,
                "message": "Keep pet feeding clean and simple with a non-slip silicone feeding bowl.",
                "name": "Non-slip Silicone Pet Feeding Bowl",
                "description": "Practical, easy to use, and selected for pet owners.",
                "call_to_action": {
                    "type": "SHOP_NOW",
                    "value": {
                        "link": PRODUCT_URL
                    }
                }
            }
        }),
        "access_token": ACCESS_TOKEN
    }

    url = f"https://graph.facebook.com/{API_VERSION}/{account_id}/adcreatives"
    r = requests.post(url, data=payload, timeout=30)

    results.append({
        "http_status": r.status_code,
        "response": r.text,
        "real_api_called": True,
        "real_money_spent": 0
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "missing": missing,
    "results": results,
    "status": "META_CREATIVE_BUILDER_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
