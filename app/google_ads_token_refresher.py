import json
import os
from pathlib import Path
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv(override=True)

OUT = Path("app/logs/google_ads_token_refresher.json")
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

client_id = os.getenv("GOOGLE_ADS_CLIENT_ID", "")
client_secret = os.getenv("GOOGLE_ADS_CLIENT_SECRET", "")
refresh_token = os.getenv("GOOGLE_ADS_REFRESH_TOKEN", "")

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "ok": False,
    "status": None
}

if not client_id or not client_secret:
    report["status"] = "missing_google_oauth_client_credentials"

elif not refresh_token:
    report["status"] = "missing_google_ads_refresh_token"

else:
    try:
        r = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token,
                "grant_type": "refresh_token"
            },
            timeout=30
        )

        report["status_code"] = r.status_code

        try:
            data = r.json()
        except:
            data = {"raw": r.text}

        access_token = data.get("access_token")

        if r.status_code == 200 and access_token:
            update_env("GOOGLE_ADS_ACCESS_TOKEN", access_token)
            report["ok"] = True
            report["status"] = "google_ads_access_token_refreshed"
            report["expires_in"] = data.get("expires_in")
            report["env_updated"] = "GOOGLE_ADS_ACCESS_TOKEN"
        else:
            report["status"] = "google_ads_access_token_refresh_failed"
            report["response"] = data

    except Exception as e:
        report["status"] = "exception"
        report["error"] = str(e)

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
