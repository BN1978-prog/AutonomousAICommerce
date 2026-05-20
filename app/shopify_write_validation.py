import os
import json
import requests
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime, timezone

ENV=Path(".env")
REGISTRY=Path("app/logs/imported_skus.json")
OUT=Path("app/logs/shopify_write_validation.json")

def load_env(path):
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line=line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k,v=line.split("=",1)
        os.environ[k.strip()]=v.strip().strip('"').strip("'")

def shop_domain(value):
    if value.startswith("http://") or value.startswith("https://"):
        return urlparse(value).netloc.rstrip("/")
    return value.strip().strip("/")

load_env(ENV)

shop=shop_domain(os.getenv("SHOPIFY_STORE_URL"))
token=os.getenv("SHOPIFY_ACCESS_TOKEN") or os.getenv("SHOPIFY_ADMIN_TOKEN")
api_version=os.getenv("SHOPIFY_API_VERSION","2025-01")

data=json.loads(REGISTRY.read_text(encoding="utf-8"))

sku=None
item=None

for k,v in data.items():
    if v.get("product_id") and v.get("pipeline_active",True) is True:
        sku=k
        item=v
        break

if not sku:
    raise SystemExit("No valid product found")

product_id=item["product_id"]

url=f"https://{shop}/admin/api/{api_version}/products/{product_id}/metafields.json"

payload={
    "metafield":{
        "namespace":"autopilot",
        "key":"validation",
        "type":"single_line_text_field",
        "value":"ok"
    }
}

headers={
    "X-Shopify-Access-Token":token,
    "Content-Type":"application/json"
}

r=requests.post(url,headers=headers,json=payload,timeout=30)

result={
    "sku":sku,
    "product_id":product_id,
    "ok":200 <= r.status_code < 300,
    "status_code":r.status_code,
    "response":r.text[:1000],
    "checked_at":datetime.now(timezone.utc).isoformat()
}

OUT.write_text(json.dumps(result,indent=2),encoding="utf-8")

print(json.dumps(result,indent=2))
