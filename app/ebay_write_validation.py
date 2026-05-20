import os
import json
import requests
from pathlib import Path
from datetime import datetime, timezone

ENV=Path(".env")
REGISTRY=Path("app/logs/imported_skus.json")
OUT=Path("app/logs/ebay_write_validation.json")

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

token=(
    os.getenv("EBAY_ACCESS_TOKEN")
    or os.getenv("EBAY_OAUTH_TOKEN")
    or os.getenv("EBAY_USER_TOKEN")
)

base_url=os.getenv(
    "EBAY_API_BASE",
    "https://api.ebay.com"
)

if not token:
    raise SystemExit("Missing eBay token")

registry=json.loads(
    REGISTRY.read_text(
        encoding="utf-8"
    )
)

sku=None
offer_id=None

for k,v in registry.items():
    if v.get("ebay_offer_id"):
        sku=k
        offer_id=v["ebay_offer_id"]
        break

if not offer_id:
    raise SystemExit("No ebay_offer_id found")

headers={
    "Authorization":f"Bearer {token}",
    "Content-Type":"application/json",
    "Accept":"application/json",
    "Content-Language":"en-US"
}

url=f"{base_url}/sell/inventory/v1/offer/{offer_id}"

r=requests.get(
    url,
    headers=headers,
    timeout=30
)

result={
    "sku":sku,
    "offer_id":offer_id,
    "ok":r.status_code==200,
    "status_code":r.status_code,
    "response":r.text[:2000],
    "checked_at":datetime.now(
        timezone.utc
    ).isoformat()
}

OUT.write_text(
    json.dumps(
        result,
        indent=2
    ),
    encoding="utf-8"
)

print(
    json.dumps(
        result,
        indent=2
    )
)
