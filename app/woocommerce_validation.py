import os
import json
import requests
from pathlib import Path
from datetime import datetime, timezone

ENV=Path(".env")
OUT=Path("app/logs/woocommerce_validation.json")

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
)

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

if not url or not ck or not cs:
    result={
        "ok":False,
        "status":"missing_env",
        "has_url":bool(url),
        "has_consumer_key":bool(ck),
        "has_consumer_secret":bool(cs),
        "checked_at":datetime.now(timezone.utc).isoformat()
    }
    OUT.write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2))
    raise SystemExit()

url=url.rstrip("/")
endpoint=f"{url}/wp-json/wc/v3/products"

r=requests.get(
    endpoint,
    auth=(ck,cs),
    params={"per_page":1},
    timeout=30
)

result={
    "ok":200 <= r.status_code < 300,
    "status_code":r.status_code,
    "endpoint":endpoint,
    "response":r.text[:1500],
    "checked_at":datetime.now(timezone.utc).isoformat()
}

OUT.write_text(json.dumps(result,indent=2),encoding="utf-8")

print(json.dumps(result,indent=2))
