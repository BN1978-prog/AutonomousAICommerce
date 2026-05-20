import os
import json
import requests
from pathlib import Path
from datetime import datetime, timezone

ENV=Path(".env")
OUT=Path("app/logs/woocommerce_write_validation.json")

def load_env(path):
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line=line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k,v=line.split("=",1)
        os.environ[k.strip()]=v.strip().strip('"').strip("'")

load_env(ENV)

url=(
    os.getenv("WOOCOMMERCE_STORE_URL")
    or os.getenv("WOO_STORE_URL")
    or os.getenv("WC_STORE_URL")
).rstrip("/")

ck=(
    os.getenv("WOOCOMMERCE_CONSUMER_KEY")
    or os.getenv("WOO_CONSUMER_KEY")
    or os.getenv("WC_CONSUMER_KEY")
)

cs=(
    os.getenv("WOOCOMMERCE_CONSUMER_SECRET")
    or os.getenv("WOO_CONSUMER_SECRET")
    or os.getenv("WC_CONSUMER_SECRET")
)

products=requests.get(
    f"{url}/wp-json/wc/v3/products",
    auth=(ck,cs),
    params={"per_page":1},
    timeout=30
)

if products.status_code!=200:
    result={
        "ok":False,
        "stage":"read_before_write",
        "status_code":products.status_code,
        "response":products.text[:1500],
        "checked_at":datetime.now(timezone.utc).isoformat()
    }
    OUT.write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2))
    raise SystemExit()

product=products.json()[0]
product_id=product["id"]

payload={
    "meta_data":[
        {
            "key":"autopilot_validation",
            "value":"ok"
        }
    ]
}

write=requests.put(
    f"{url}/wp-json/wc/v3/products/{product_id}",
    auth=(ck,cs),
    json=payload,
    timeout=30
)

result={
    "ok":200 <= write.status_code < 300,
    "product_id":product_id,
    "stage":"write_meta_validation",
    "status_code":write.status_code,
    "response":write.text[:1500],
    "checked_at":datetime.now(timezone.utc).isoformat()
}

OUT.write_text(json.dumps(result,indent=2),encoding="utf-8")

print(json.dumps(result,indent=2))
