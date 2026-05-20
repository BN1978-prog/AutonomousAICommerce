import os
import requests
from dotenv import load_dotenv,set_key

load_dotenv()

ENV_FILE=".env"

SHOP=os.getenv("SHOPIFY_STORE_URL","").replace("https://","")
CLIENT_ID=os.getenv("SHOPIFY_CLIENT_ID","")
CLIENT_SECRET=os.getenv("SHOPIFY_CLIENT_SECRET","")
TOKEN=os.getenv("SHOPIFY_ACCESS_TOKEN","")
API_VERSION=os.getenv("SHOPIFY_API_VERSION","2025-01")

def validate(token):
    url=f"https://{SHOP}/admin/api/{API_VERSION}/shop.json"

    r=requests.get(
        url,
        headers={"X-Shopify-Access-Token":token},
        timeout=20
    )

    return r.status_code,r.text


def refresh():

    body={
        "grant_type":"client_credentials",
        "client_id":CLIENT_ID,
        "client_secret":CLIENT_SECRET
    }

    r=requests.post(
        f"https://{SHOP}/admin/oauth/access_token",
        json=body,
        timeout=20
    )

    if r.status_code!=200:
        return False,r.text

    data=r.json()

    token=data.get("access_token")

    if not token:
        return False,"No access token returned"

    set_key(ENV_FILE,"SHOPIFY_ACCESS_TOKEN",token)
    set_key(ENV_FILE,"SHOPIFY_ADMIN_TOKEN",token)

    return True,token


status,response=validate(TOKEN)

if status==200:
    print("Shopify token OK")

elif status==401:

    print("Token invalid -> refreshing")

    ok,result=refresh()

    if ok:

        status2,_=validate(result)

        if status2==200:
            print("New token saved into .env")
        else:
            print("Refresh succeeded but token still invalid")

    else:
        print("Refresh failed:")
        print(result)

else:
    print(response)
