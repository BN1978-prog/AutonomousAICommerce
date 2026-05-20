from dotenv import load_dotenv
load_dotenv(override=True)

import os
import base64
import urllib.parse
import httpx
import re
from pathlib import Path

code = os.environ.get("code") or globals().get("code")

client_id = os.getenv("EBAY_CLIENT_ID")
client_secret = os.getenv("EBAY_CLIENT_SECRET")
runame = os.getenv("EBAY_REDIRECT_URI")

basic = base64.b64encode(
    f"{client_id}:{client_secret}".encode()
).decode()

headers = {
    "Authorization": "Basic " + basic,
    "Content-Type": "application/x-www-form-urlencoded"
}

payload = {
    "grant_type":"authorization_code",
    "code": urllib.parse.unquote(code),
    "redirect_uri":runame
}

r = httpx.post(
    "https://api.ebay.com/identity/v1/oauth2/token",
    headers=headers,
    data=payload,
    timeout=60
)

data = r.json()

if "access_token" not in data:
    print(data)
    raise Exception("Token exchange failed")

access = data["access_token"]
refresh = data["refresh_token"]

p = Path(".env")
txt = p.read_text(encoding="utf-8")

def replace_or_add(name,val,txt):
    if re.search(rf"^{name}=.*$",txt,flags=re.M):
        return re.sub(
            rf"^{name}=.*$",
            f"{name}={val}",
            txt,
            flags=re.M
        )
    return txt+f"\n{name}={val}"

txt = replace_or_add("EBAY_ACCESS_TOKEN",access,txt)
txt = replace_or_add("EBAY_REFRESH_TOKEN",refresh,txt)

p.write_text(txt,encoding="utf-8")

print("SUCCESS")
print("ACCESS LEN:",len(access))
print("REFRESH LEN:",len(refresh))

