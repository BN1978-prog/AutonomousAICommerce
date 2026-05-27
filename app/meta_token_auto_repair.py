import json
import os
import re
import requests
from pathlib import Path
from datetime import datetime, timezone

ENV = Path(".env")
OUT = Path("app/logs/meta_token_auto_repair.json")

def read_env():
    return ENV.read_text(encoding="utf-8") if ENV.exists() else ""

def get_env_value(text,key):
    m = re.search(
        rf"^{re.escape(key)}=(.*)$",
        text,
        flags=re.MULTILINE
    )
    return m.group(1).strip() if m else None

def update_env(key,value):

    text=read_env()

    pattern=rf"^{re.escape(key)}=.*$"

    if re.search(
        pattern,
        text,
        flags=re.MULTILINE
    ):

        text=re.sub(
            pattern,
            f"{key}={value}",
            text,
            flags=re.MULTILINE
        )

    else:

        text += f"\n{key}={value}"

    ENV.write_text(
        text.strip()+"\n",
        encoding="utf-8"
    )

def check(token):

    r=requests.get(
        "https://graph.facebook.com/v19.0/me",
        params={
            "access_token":token
        },
        timeout=30
    )

    try:
        data=r.json()
    except:
        data={}

    if r.status_code==200:
        return True,"valid",data

    return False,f"http_{r.status_code}",data

envText=read_env()

token=get_env_value(
    envText,
    "META_ACCESS_TOKEN"
)

report={

"created_at":
datetime.now(
timezone.utc
).isoformat()

}

ok,status,data=check(token)

report["initial_status"]=status

if not ok:

    update_env(
        "META_ACCESS_TOKEN",
        token
    )

    ok2,status2,data2=check(token)

    report["final_status"]=status2
    report["meta_response"]=data2

else:

    report["status"]="already_valid"

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
