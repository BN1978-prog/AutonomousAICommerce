import json, os
from pathlib import Path
import requests

env_path = Path(".env")
for line in env_path.read_text(encoding="utf-8-sig").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k,v=line.split("=",1)
        os.environ[k.strip()] = v.strip()

ACCESS_TOKEN=os.getenv("META_ACCESS_TOKEN")
API_VERSION=os.getenv("META_API_VERSION","v22.0")

adsets=[
    "52564379015836",
    "52564383617836"
]

for adset_id in adsets:
    url=f"https://graph.facebook.com/{API_VERSION}/{adset_id}"
    params={
        "fields":"id,name,status,effective_status,promoted_object,campaign_id,daily_budget",
        "access_token":ACCESS_TOKEN
    }
    r=requests.get(url,params=params,timeout=30)
    print("ADSET",adset_id)
    print(r.status_code)
    print(r.text)
    print()
