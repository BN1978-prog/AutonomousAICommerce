import os, requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(override=True)

api_base = os.getenv("ETSY_API_BASE", "https://openapi.etsy.com/v3/application").rstrip("/")
api_key = os.getenv("ETSY_API_KEY") or os.getenv("ETSY_CLIENT_ID")
token = os.getenv("ETSY_ACCESS_TOKEN")
shop_id = os.getenv("ETSY_SHOP_ID")

headers = {
    "x-api-key": api_key,
    "Authorization": "Bearer " + token
}

paths = [
    f"{api_base}/shops/{shop_id}/readiness-state",
    f"{api_base}/shops/{shop_id}/readiness-states",
    f"{api_base}/shops/{shop_id}/listing-readiness-states"
]

for url in paths:
    r = requests.get(url, headers=headers, timeout=30)
    print("URL:", url)
    print("STATUS:", r.status_code)
    print(r.text[:2000])
    print("-" * 60)

Path("app/logs/etsy_readiness_states_checked.txt").write_text(
    "checked",
    encoding="utf-8"
)
