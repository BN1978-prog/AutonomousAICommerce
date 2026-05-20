import os
import json
import time
import uuid
import hashlib
import requests
from pathlib import Path
from datetime import datetime, timezone

ENV=Path(".env")
OUT=Path("app/logs/meta_test_event.json")

for line in ENV.read_text(encoding="utf-8").splitlines():
    if "=" not in line or line.strip().startswith("#"):
        continue
    k,v=line.split("=",1)
    os.environ[k.strip()] = v.strip().strip('"').strip("'")

pixel=os.getenv("META_PIXEL_ID")
token=os.getenv("META_ACCESS_TOKEN")

if not pixel:
    raise SystemExit("Missing META_PIXEL_ID")

if not token:
    raise SystemExit("Missing META_ACCESS_TOKEN")

def sha256(value):
    return hashlib.sha256(
        value.strip().lower().encode("utf-8")
    ).hexdigest()

event_id=str(uuid.uuid4())
external_id=sha256("autonomous-ai-commerce-test-user")

url=f"https://graph.facebook.com/v19.0/{pixel}/events"

payload={
    "data":[
        {
            "event_name":"PageView",
            "event_time":int(time.time()),
            "event_id":event_id,
            "action_source":"website",
            "event_source_url":"https://aicommerce9.wpcomstaging.com/",
            "user_data":{
                "external_id":[external_id],
                "client_ip_address":"127.0.0.1",
                "client_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AutonomousAICommerceTest/1.0"
            },
            "custom_data":{
                "content_name":"AutonomousAICommerce Pixel Test",
                "content_category":"system_test"
            }
        }
    ],
    "test_event_code":os.getenv("META_TEST_EVENT_CODE","")
}

if not payload["test_event_code"]:
    payload.pop("test_event_code")

r=requests.post(
    url,
    params={"access_token":token},
    json=payload,
    timeout=30
)

try:
    response=r.json()
except Exception:
    response={"raw":r.text}

result={
    "ok":200 <= r.status_code < 300,
    "status_code":r.status_code,
    "event_id":event_id,
    "response":response,
    "created_at":datetime.now(timezone.utc).isoformat()
}

OUT.write_text(json.dumps(result,indent=2),encoding="utf-8")

print(json.dumps(result,indent=2))
