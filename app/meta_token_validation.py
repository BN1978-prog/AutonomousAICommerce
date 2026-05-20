import os
import json
import requests
from pathlib import Path
from datetime import datetime, timezone

ENV=Path(".env")
OUT=Path("app/logs/meta_token_validation.json")

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
    result={
        "ok":False,
        "status":"missing_token",
        "checked_at":datetime.now(timezone.utc).isoformat()
    }
else:
    r=requests.get(
        "https://graph.facebook.com/v19.0/me",
        params={
            "access_token":token,
            "fields":"id,name"
        },
        timeout=30
    )

    result={
        "ok":200 <= r.status_code < 300,
        "status_code":r.status_code,
        "status":"valid" if 200 <= r.status_code < 300 else "invalid_token",
        "response":r.json() if r.text else {},
        "checked_at":datetime.now(timezone.utc).isoformat()
    }

OUT.write_text(
    json.dumps(result,indent=2),
    encoding="utf-8"
)

print(json.dumps(result,indent=2))
