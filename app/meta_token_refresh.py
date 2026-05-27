import json
import os
import re
import requests
from pathlib import Path
from datetime import datetime, timezone

ENV=Path(".env")
OUT=Path("app/logs/meta_token_refresh.json")

def env_text():
    return ENV.read_text(encoding="utf-8")

def env_get(key):
    t=env_text()
    m=re.search(
        rf"^{re.escape(key)}=(.*)$",
        t,
        flags=re.MULTILINE
    )
    return m.group(1).strip() if m else None

def env_set(key,value):

    t=env_text()

    p=rf"^{re.escape(key)}=.*$"

    if re.search(
        p,
        t,
        flags=re.MULTILINE
    ):

        t=re.sub(
            p,
            f"{key}={value}",
            t,
            flags=re.MULTILINE
        )

    else:

        t+=f"\n{key}={value}"

    ENV.write_text(
        t,
        encoding="utf-8"
    )

APP_ID=env_get("META_APP_ID")
APP_SECRET=env_get("META_APP_SECRET")
TOKEN=env_get("META_ACCESS_TOKEN")

r=requests.get(
"https://graph.facebook.com/v19.0/oauth/access_token",
params={

"grant_type":
"fb_exchange_token",

"client_id":
APP_ID,

"client_secret":
APP_SECRET,

"fb_exchange_token":
TOKEN

},
timeout=30
)

data=r.json()

report={

"created_at":
datetime.now(
timezone.utc
).isoformat(),

"status_code":
r.status_code,

"response":
data

}

if r.status_code==200:

    token=data.get(
    "access_token"
    )

    if token:

        env_set(
        "META_ACCESS_TOKEN",
        token
        )

        report[
        "status"
        ]="refreshed"

OUT.write_text(
json.dumps(
report,
indent=2
),
encoding="utf-8"
)

print(
json.dumps(
report,
indent=2
)
)
