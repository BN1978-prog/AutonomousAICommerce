import os, json, requests
from pathlib import Path

env = Path(".env")
for line in env.read_text(encoding="utf-8").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k,v = line.split("=",1)
        os.environ[k.strip()] = v.strip()

token = os.getenv("META_PAGE_ACCESS_TOKEN")
r = requests.get(
    "https://graph.facebook.com/v19.0/me/permissions",
    params={"access_token": token},
    timeout=30
)
print(json.dumps(r.json(), indent=2))
