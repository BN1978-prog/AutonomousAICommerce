from dotenv import load_dotenv
load_dotenv(override=True)

import os, base64, httpx, re
from pathlib import Path


def refresh_ebay_access_token():
    client_id = os.getenv("EBAY_CLIENT_ID")
    client_secret = os.getenv("EBAY_CLIENT_SECRET")
    refresh_token = os.getenv("EBAY_REFRESH_TOKEN")

    basic = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    headers = {
        "Authorization": "Basic " + basic,
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "scope": "https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/sell.inventory https://api.ebay.com/oauth/api_scope/sell.account https://api.ebay.com/oauth/api_scope/sell.fulfillment",
    }

    r = httpx.post(
        "https://api.ebay.com/identity/v1/oauth2/token",
        headers=headers,
        data=data,
        timeout=60,
    )

    payload = r.json()

    if "access_token" not in payload:
        print(payload)
        raise Exception("eBay token refresh failed")

    access = payload["access_token"]

    p = Path(".env")
    txt = p.read_text(encoding="utf-8")
    txt = re.sub(r"^EBAY_ACCESS_TOKEN=.*$", "EBAY_ACCESS_TOKEN=" + access, txt, flags=re.M)
    p.write_text(txt, encoding="utf-8")

    print("EBAY ACCESS TOKEN REFRESHED")
    print("LEN:", len(access))


if __name__ == "__main__":
    refresh_ebay_access_token()
