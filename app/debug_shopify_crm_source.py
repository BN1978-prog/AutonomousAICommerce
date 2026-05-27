import os, json, requests
from pathlib import Path

for line in Path(".env").read_text(encoding="utf-8-sig").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k,v=line.split("=",1)
        os.environ[k.strip()]=v.strip()

shop=os.getenv("SHOPIFY_SHOP_DOMAIN") or os.getenv("SHOPIFY_STORE_URL")
token=os.getenv("SHOPIFY_ADMIN_TOKEN") or os.getenv("SHOPIFY_ACCESS_TOKEN")
ver=os.getenv("SHOPIFY_API_VERSION","2025-01")

h={"X-Shopify-Access-Token":token}

for name, url in {
    "orders": f"https://{shop}/admin/api/{ver}/orders.json?status=any&limit=5",
    "customers": f"https://{shop}/admin/api/{ver}/customers.json?limit=5"
}.items():
    r=requests.get(url,headers=h,timeout=30)
    print(name, "status:", r.status_code)
    data=r.json()
    items=data.get(name,[])
    print(name, "count:", len(items))
    for x in items:
        print(json.dumps({
            "id": x.get("id"),
            "email": x.get("email"),
            "created_at": x.get("created_at"),
            "name": x.get("name") or x.get("first_name")
        }, indent=2))
