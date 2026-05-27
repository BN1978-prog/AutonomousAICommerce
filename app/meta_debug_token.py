import os, json, requests
from pathlib import Path

for line in Path(".env").read_text(encoding="utf-8-sig").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k,v=line.split("=",1)
        os.environ[k.strip()]=v.strip()

app_token = os.getenv("META_APP_ID") + "|" + os.getenv("META_APP_SECRET")
token = os.getenv("META_PAGE_ACCESS_TOKEN") or os.getenv("META_ACCESS_TOKEN")

r = requests.get(
    "https://graph.facebook.com/debug_token",
    params={
        "input_token": token,
        "access_token": app_token
    },
    timeout=30
)

print(json.dumps(r.json(), indent=2))
