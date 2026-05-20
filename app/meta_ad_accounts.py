import os
import json
import requests
from pathlib import Path
from datetime import datetime, timezone

ENV=Path(".env")
OUT=Path("app/logs/meta_ad_accounts.json")

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

token=os.getenv("META_ACCESS_TOKEN")

if not token:
    raise SystemExit("Missing META_ACCESS_TOKEN")

url="https://graph.facebook.com/v19.0/me/adaccounts"

r=requests.get(
    url,
    params={
        "access_token":token,
        "fields":"id,name,account_status,currency,timezone_name"
    },
    timeout=30
)

result={
    "ok":200 <= r.status_code < 300,
    "status_code":r.status_code,
    "response":r.json() if r.text else {},
    "checked_at":datetime.now(timezone.utc).isoformat()
}

OUT.write_text(
    json.dumps(result,indent=2),
    encoding="utf-8"
)

print(json.dumps(result,indent=2))
