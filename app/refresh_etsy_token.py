import os
import re
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(override=True)

client_id = os.getenv("ETSY_CLIENT_ID") or os.getenv("ETSY_API_KEY")
refresh_token = os.getenv("ETSY_REFRESH_TOKEN")

if not client_id or not refresh_token:
    raise SystemExit("Missing ETSY_CLIENT_ID or ETSY_REFRESH_TOKEN")

r = requests.post(
    "https://api.etsy.com/v3/public/oauth/token",
    data={
        "grant_type": "refresh_token",
        "client_id": client_id,
        "refresh_token": refresh_token
    },
    timeout=30
)

print("STATUS:", r.status_code)
print(r.text[:1000])

data = r.json()

if r.status_code not in [200, 201] or "access_token" not in data:
    raise SystemExit("Etsy refresh failed")

env = Path(".env")
text = env.read_text(encoding="utf-8-sig")

def upsert(key, value, text):
    value = str(value).replace("\r", "").replace("\n", "")
    if re.search(rf"^{key}=.*$", text, flags=re.M):
        return re.sub(rf"^{key}=.*$", f"{key}={value}", text, flags=re.M)
    return text.rstrip() + f"\n{key}={value}\n"

text = upsert("ETSY_ACCESS_TOKEN", data["access_token"], text)

if data.get("refresh_token"):
    text = upsert("ETSY_REFRESH_TOKEN", data["refresh_token"], text)

env.write_text(text, encoding="utf-8")

print("ETSY TOKEN REFRESHED")
print("ACCESS LEN:", len(data["access_token"]))
print("REFRESH LEN:", len(data.get("refresh_token", "")))
