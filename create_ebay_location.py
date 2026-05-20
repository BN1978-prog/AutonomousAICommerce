from dotenv import load_dotenv
load_dotenv(override=True)

import os,requests,json

token=os.getenv("EBAY_ACCESS_TOKEN")

headers={
    "Authorization":"Bearer "+token,
    "Content-Type":"application/json"
}

url="https://api.ebay.com/sell/inventory/v1/location/default"

payload={
    "name":"MainWarehouse",
    "merchantLocationStatus":"ENABLED",
    "location":{
        "address":{
            "addressLine1":"London",
            "city":"London",
            "stateOrProvince":"London",
            "postalCode":"SW1A1AA",
            "country":"GB"
        }
    }
}

r=requests.post(
    url,
    headers=headers,
    json=payload,
    timeout=30
)

print("STATUS:",r.status_code)

try:
    print(json.dumps(r.json(),indent=2))
except:
    print(r.text)

