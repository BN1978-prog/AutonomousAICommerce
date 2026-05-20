from dotenv import load_dotenv
load_dotenv(override=True)

import os, requests, json

token=os.getenv("META_ACCESS_TOKEN","").strip()
catalog_id=os.getenv("META_CATALOG_ID","").strip()
business_id=os.getenv("META_BUSINESS_ID","").strip()

print("=== META CONFIG ===")
print("TOKEN_LEN:",len(token))
print("CATALOG_ID:",catalog_id)
print("BUSINESS_ID:",business_id)

if not token or "???_" in token:
    print("META_ACCESS_TOKEN missing or placeholder")
    raise SystemExit

url="https://graph.facebook.com/v20.0/me"
r=requests.get(url,params={"access_token":token},timeout=30)

print("=== META /me ===")
print("STATUS:",r.status_code)
try:
    print(json.dumps(r.json(),indent=2))
except Exception:
    print(r.text)

if catalog_id and "???_" not in catalog_id:
    url=f"https://graph.facebook.com/v20.0/{catalog_id}"
    r=requests.get(url,params={"access_token":token},timeout=30)
    print("=== META CATALOG ===")
    print("STATUS:",r.status_code)
    try:
        print(json.dumps(r.json(),indent=2))
    except Exception:
        print(r.text)
