import os, json, requests
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

url = f"{api_base}/shops/{shop_id}/shipping-profiles"

r = requests.get(url, headers=headers, timeout=30)

print("STATUS:", r.status_code)
print(r.text[:2000])

Path("app/logs/etsy_shipping_profiles.json").write_text(
    r.text,
    encoding="utf-8"
)
