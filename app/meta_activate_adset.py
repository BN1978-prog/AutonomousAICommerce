import json
import os
from pathlib import Path
import requests

RESULT = Path("app/logs/meta_ad_builder_result.json")

env_path = Path(".env")
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8-sig").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip()

ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
API_VERSION = os.getenv("META_API_VERSION", "v22.0")

data = json.loads(RESULT.read_text(encoding="utf-8"))

for item in data["results"]:
    adset_id = item["adset_id"]

    url = f"https://graph.facebook.com/{API_VERSION}/{adset_id}"

    payload = {
        "status": "ACTIVE",
        "access_token": ACCESS_TOKEN
    }

    r = requests.post(url, data=payload, timeout=30)

    print({
        "adset_id": adset_id,
        "http_status": r.status_code,
        "response": r.text
    })
