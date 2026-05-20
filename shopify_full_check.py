from dotenv import dotenv_values
import requests

print("="*60)
print("SHOPIFY ENV CHECK")
print("="*60)

env=dotenv_values(".env")

keys=[
"SHOPIFY_STORE_URL",
"SHOPIFY_CLIENT_ID",
"SHOPIFY_CLIENT_SECRET",
"SHOPIFY_ACCESS_TOKEN",
"SHOPIFY_ADMIN_TOKEN",
"SHOPIFY_API_VERSION"
]

for k in keys:
    v=env.get(k,"") or ""
    print(f"{k:30} {'SET' if v else 'EMPTY'} | len={len(v)} | prefix={v[:8]}")

print("\n"+"="*60)
print("TOKEN TEST")
print("="*60)

shop=env.get("SHOPIFY_STORE_URL","").replace("https://","")
token=env.get("SHOPIFY_ACCESS_TOKEN","")
api=env.get("SHOPIFY_API_VERSION","2025-01")

if not shop:
    print("STORE_URL missing")
    quit()

if not token:
    print("ACCESS_TOKEN missing")
    quit()

url=f"https://{shop}/admin/api/{api}/shop.json"

try:
    r=requests.get(
        url,
        headers={
            "X-Shopify-Access-Token":token
        },
        timeout=15
    )

    print("status:",r.status_code)

    if r.status_code==200:
        data=r.json()
        print("CONNECTED")
        print("shop:",data["shop"]["name"])
        print("domain:",data["shop"]["domain"])

    else:
        print(r.text[:1000])

except Exception as e:
    print("ERROR:",e)

print("\n"+"="*60)
print("RAW SHOPIFY LINES")
print("="*60)

with open(".env","r",encoding="utf-8") as f:
    for line in f:
        if line.startswith("SHOPIFY_"):
            print(line.strip())
