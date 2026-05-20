import os
import json
import requests
from pathlib import Path
from datetime import datetime, timezone

ENV=Path(".env")
OUT=Path("app/logs/meta_business_assets.json")

def load_env():
    for line in ENV.read_text(encoding="utf-8").splitlines():
        if "=" not in line or line.strip().startswith("#"):
            continue
        k,v=line.split("=",1)
        os.environ[k.strip()]=v.strip().strip('"').strip("'")

def call(path,params=None):
    token=os.getenv("META_ACCESS_TOKEN")
    url=f"https://graph.facebook.com/v19.0/{path}"
    p=params or {}
    p["access_token"]=token
    r=requests.get(url,params=p,timeout=30)
    return {
        "ok":200 <= r.status_code < 300,
        "status_code":r.status_code,
        "data":r.json() if r.text else {}
    }

load_env()

bid=os.getenv("META_BUSINESS_ID")

if not bid:
    raise SystemExit("Missing META_BUSINESS_ID")

result={
    "created_at":datetime.now(timezone.utc).isoformat(),
    "business_id":bid,
    "owned_ad_accounts":call(f"{bid}/owned_ad_accounts",{"fields":"id,name,account_status,currency"}),
    "client_ad_accounts":call(f"{bid}/client_ad_accounts",{"fields":"id,name,account_status,currency"}),
    "owned_pixels":call(f"{bid}/owned_pixels",{"fields":"id,name"}),
    "owned_product_catalogs":call(f"{bid}/owned_product_catalogs",{"fields":"id,name"}),
    "owned_pages":call(f"{bid}/owned_pages",{"fields":"id,name"})
}

OUT.write_text(json.dumps(result,indent=2),encoding="utf-8")

print(json.dumps(result,indent=2))
