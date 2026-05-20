import os
import json
import requests
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime, timezone, timedelta

ENV=Path(".env")
OUT=Path("app/logs/shopify_orders_sales.json")

def load_env(path):
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line=line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k,v=line.split("=",1)
        os.environ[k.strip()]=v.strip().strip('"').strip("'")

def normalize_shop(value):
    if value.startswith("http://") or value.startswith("https://"):
        return urlparse(value).netloc.rstrip("/")
    return value.strip().strip("/")

load_env(ENV)

shop=normalize_shop(os.getenv("SHOPIFY_STORE_URL"))
token=os.getenv("SHOPIFY_ACCESS_TOKEN") or os.getenv("SHOPIFY_ADMIN_TOKEN")
api_version=os.getenv("SHOPIFY_API_VERSION","2025-01")

created_at_min=(
    datetime.now(timezone.utc)-timedelta(days=30)
).isoformat()

url=f"https://{shop}/admin/api/{api_version}/orders.json"

headers={
    "X-Shopify-Access-Token":token,
    "Content-Type":"application/json"
}

params={
    "status":"any",
    "limit":250,
    "created_at_min":created_at_min,
    "fields":"id,name,created_at,total_price,currency,financial_status,line_items"
}

r=requests.get(
    url,
    headers=headers,
    params=params,
    timeout=30
)

result={
    "ok":200 <= r.status_code < 300,
    "status_code":r.status_code,
    "orders":[],
    "checked_at":datetime.now(timezone.utc).isoformat()
}

if result["ok"]:
    orders=r.json().get("orders",[])
    for order in orders:
        result["orders"].append({
            "order_id":order.get("id"),
            "name":order.get("name"),
            "created_at":order.get("created_at"),
            "total_price":order.get("total_price"),
            "currency":order.get("currency"),
            "financial_status":order.get("financial_status"),
            "line_items":[
                {
                    "sku":x.get("sku"),
                    "title":x.get("title"),
                    "quantity":x.get("quantity"),
                    "price":x.get("price")
                }
                for x in order.get("line_items",[])
            ]
        })
else:
    result["response"]=r.text[:2000]

OUT.write_text(json.dumps(result,indent=2),encoding="utf-8")

print("SHOPIFY ORDERS OK:",result["ok"])
print("STATUS:",result["status_code"])
print("ORDERS:",len(result["orders"]))
