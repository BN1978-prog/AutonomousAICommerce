import json
import os
import re
import requests
from pathlib import Path
from datetime import datetime, timezone

ENV = Path(".env")
OUT = Path("app/logs/shopify_token_auto_repair.json")

SHOP = os.getenv("SHOPIFY_SHOP_DOMAIN","aicommerce-test-store-2.myshopify.com")
CLIENT_ID = os.getenv("SHOPIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SHOPIFY_CLIENT_SECRET")
TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")

def update_env(key,value):

    text=""

    if ENV.exists():
        text=ENV.read_text(encoding="utf-8")

    pattern=rf"^{re.escape(key)}=.*$"

    if re.search(pattern,text,flags=re.MULTILINE):

        text=re.sub(
            pattern,
            f"{key}={value}",
            text,
            flags=re.MULTILINE
        )

    else:

        text += f"\n{key}={value}"

    ENV.write_text(
        text.strip()+"\n",
        encoding="utf-8"
    )

def check_token(token):

    if not token:
        return False,"missing"

    r=requests.get(
        f"https://{SHOP}/admin/api/2025-01/shop.json",
        headers={
            "X-Shopify-Access-Token":token
        },
        timeout=30
    )

    if r.status_code==200:
        return True,"token_valid"

    return False,f"http_{r.status_code}"

def repair():

    body={
        "grant_type":"client_credentials",
        "client_id":CLIENT_ID,
        "client_secret":CLIENT_SECRET
    }

    r=requests.post(
        f"https://{SHOP}/admin/oauth/access_token",
        json=body,
        timeout=30
    )

    if r.status_code not in [200,201]:

        return None,\
               f"http_{r.status_code}",\
               r.text

    data=r.json()

    token=data.get("access_token")

    if not token:

        return None,\
               "missing_token",\
               str(data)

    return token,"repaired",""

report={

"created_at":
datetime.now(timezone.utc).isoformat()

}

ok,status=check_token(TOKEN)

report["initial_status"]=status

if not ok:

    report["repair_attempted"]=True

    token,status,error=repair()

    report["repair_status"]=status

    if token:

        update_env(
            "SHOPIFY_ACCESS_TOKEN",
            token
        )

        update_env(
            "SHOPIFY_SHOP_DOMAIN",
            SHOP
        )

        report["env_updated"]=True

        ok2,status2=check_token(token)

        report["final_status"]=status2

    else:

        report["error"]=error

else:

    report["status"]="already_valid"

OUT.write_text(
    json.dumps(
        report,
        indent=2
    ),
    encoding="utf-8"
)

print(
json.dumps(
report,
indent=2
)
)
