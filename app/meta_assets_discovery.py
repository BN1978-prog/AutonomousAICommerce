import os
import json
import requests
from pathlib import Path
from datetime import datetime, timezone

ENV=Path(".env")
OUT=Path("app/logs/meta_assets_discovery.json")

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

result={
    "created_at":datetime.now(timezone.utc).isoformat(),
    "me":call("me",{"fields":"id,name"}),
    "businesses":call("me/businesses",{"fields":"id,name,verification_status"}),
    "adaccounts":call("me/adaccounts",{"fields":"id,name,account_status,currency"}),
    "pages":call("me/accounts",{"fields":"id,name"}),
}

OUT.write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps(result,indent=2))
