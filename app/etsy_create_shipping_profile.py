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
    "Authorization": "Bearer " + token,
    "Content-Type": "application/x-www-form-urlencoded"
}

url = f"{api_base}/shops/{shop_id}/shipping-profiles"

payload = {
    "title": "Standard UK Shipping",
    "origin_country_iso": "GB",
    "origin_postal_code": "SW1A 1AA",
    "primary_cost": "4.99",
    "secondary_cost": "1.99",
    "min_processing_time": 1,
    "max_processing_time": 3,
    "processing_time_unit": "business_days",
    "destination_country_iso": "GB",
    "min_delivery_days": 2,
    "max_delivery_days": 5
}

r = requests.post(url, headers=headers, data=payload, timeout=30)

print("STATUS:", r.status_code)
print(r.text[:2000])

Path("app/logs/etsy_shipping_profile_create.json").write_text(
    r.text,
    encoding="utf-8"
)

data = r.json()
profile_id = data.get("shipping_profile_id") or data.get("id")

if profile_id:
    env = Path(".env")
    txt = env.read_text(encoding="utf-8-sig")
    if "ETSY_SHIPPING_PROFILE_ID=" not in txt:
        txt += f"\nETSY_SHIPPING_PROFILE_ID={profile_id}\n"
    else:
        import re
        txt = re.sub(r"^ETSY_SHIPPING_PROFILE_ID=.*$", f"ETSY_SHIPPING_PROFILE_ID={profile_id}", txt, flags=re.M)
    env.write_text(txt, encoding="utf-8")
    print("ETSY_SHIPPING_PROFILE_ID=", profile_id)
