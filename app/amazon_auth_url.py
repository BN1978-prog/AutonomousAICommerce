import os
from pathlib import Path
from urllib.parse import urlencode

for line in Path(".env").read_text(encoding="utf-8-sig").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k,v=line.split("=",1)
        os.environ[k.strip()] = v.strip()

client_id=os.getenv("AMAZON_LWA_CLIENT_ID")
redirect_uri=os.getenv("AMAZON_REDIRECT_URI")

url="https://sellercentral.amazon.com/apps/authorize/consent?" + urlencode({
    "application_id": client_id,
    "redirect_uri": redirect_uri,
    "state": "aicommerce_auth"
})

print(url)
