import os, json
from pathlib import Path
import requests

for line in Path(".env").read_text(encoding="utf-8-sig").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k,v=line.split("=",1)
        os.environ[k.strip()] = v.strip()

ACCESS_TOKEN=os.getenv("META_ACCESS_TOKEN")
API_VERSION=os.getenv("META_API_VERSION","v22.0")

ads=[
    "52564379055836",
    "52564383631236"
]

for ad_id in ads:
    url=f"https://graph.facebook.com/{API_VERSION}/{ad_id}"
    params={
        "fields":"id,name,status,effective_status,adset_id,creative",
        "access_token":ACCESS_TOKEN
    }
    r=requests.get(url,params=params,timeout=30)
    print("AD",ad_id)
    print(r.status_code)
    print(r.text)
    print()
