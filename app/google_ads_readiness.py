import os
import json
from pathlib import Path
from datetime import datetime, timezone

ENV=Path(".env")
OUT=Path("app/logs/google_ads_readiness.json")

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

required={
    "GOOGLE_ADS_DEVELOPER_TOKEN":os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"),
    "GOOGLE_ADS_CLIENT_ID":os.getenv("GOOGLE_ADS_CLIENT_ID"),
    "GOOGLE_ADS_CLIENT_SECRET":os.getenv("GOOGLE_ADS_CLIENT_SECRET"),
    "GOOGLE_ADS_REFRESH_TOKEN":os.getenv("GOOGLE_ADS_REFRESH_TOKEN"),
    "GOOGLE_ADS_CUSTOMER_ID":os.getenv("GOOGLE_ADS_CUSTOMER_ID")
}

missing=[
    k for k,v in required.items()
    if not v
]

report={
    "created_at":datetime.now(timezone.utc).isoformat(),
    "ok":len(missing)==0,
    "status":"ready" if len(missing)==0 else "missing_env",
    "missing":missing,
    "present":[k for k,v in required.items() if v]
}

OUT.write_text(json.dumps(report,indent=2),encoding="utf-8")

print(json.dumps(report,indent=2))
