import json
import os
from pathlib import Path
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv(override=True)

OUT = Path("app/logs/amazon_oauth_exchange.json")
ENV = Path(".env")

def update_env(key, value):
    text = ENV.read_text(encoding="utf-8") if ENV.exists() else ""
    lines = text.splitlines()
    found = False

    for i, line in enumerate(lines):
        if line.startswith(key + "="):
            lines[i] = key + "=" + value
            found = True

    if not found:
        lines.append(key + "=" + value)

    ENV.write_text("\n".join(lines) + "\n", encoding="utf-8")

client_id = os.getenv("AMAZON_LWA_CLIENT_ID", "")
client_secret = os.getenv("AMAZON_LWA_CLIENT_SECRET", "")
auth_code = os.getenv("AMAZON_AUTH_CODE", "")

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "ok": False,
    "status": None
}

if not client_id or not client_secret:
    report["status"] = "missing_lwa_client_credentials"

elif not auth_code:
    report["status"] = "missing_AMAZON_AUTH_CODE"

else:
    try:
        r = requests.post(
            "https://api.amazon.com/auth/o2/token",
            data={
                "grant_type": "authorization_code",
                "code": auth_code,
                "client_id": client_id,
                "client_secret": client_secret
            },
            timeout=30
        )

        report["status_code"] = r.status_code

        try:
            data = r.json()
        except:
            data = {"raw": r.text}

        report["response"] = data

        refresh_token = data.get("refresh_token")

        if r.status_code == 200 and refresh_token:
            update_env("AMAZON_REFRESH_TOKEN", refresh_token)
            report["ok"] = True
            report["status"] = "amazon_refresh_token_saved"
            report["env_updated"] = "AMAZON_REFRESH_TOKEN"
        else:
            report["status"] = "amazon_oauth_exchange_failed"

    except Exception as e:
        report["status"] = "exception"
        report["error"] = str(e)

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
