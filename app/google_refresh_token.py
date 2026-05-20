import os
import json
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

ENV=Path(".env")

values={}

for line in ENV.read_text(encoding="utf-8").splitlines():
    if "=" not in line or line.strip().startswith("#"):
        continue
    k,v=line.split("=",1)
    values[k.strip()]=v.strip().strip('"').strip("'")

client_id=values.get("GOOGLE_ADS_CLIENT_ID") or values.get("GOOGLE_CLIENT_ID")
client_secret=values.get("GOOGLE_ADS_CLIENT_SECRET") or values.get("GOOGLE_CLIENT_SECRET")

if not client_id or not client_secret:
    raise SystemExit("Missing Google client id/secret in .env")

client_config={
    "installed":{
        "client_id":client_id,
        "client_secret":client_secret,
        "auth_uri":"https://accounts.google.com/o/oauth2/auth",
        "token_uri":"https://oauth2.googleapis.com/token",
        "redirect_uris":["http://localhost"]
    }
}

flow=InstalledAppFlow.from_client_config(
    client_config,
    scopes=["https://www.googleapis.com/auth/adwords"]
)

creds=flow.run_local_server(
    port=0,
    prompt="consent"
)

refresh=creds.refresh_token

if not refresh:
    raise SystemExit("No refresh token returned. Remove app access in Google Account permissions and try again.")

lines=ENV.read_text(encoding="utf-8").splitlines()

lines=[
    x for x in lines
    if not x.startswith("GOOGLE_ADS_REFRESH_TOKEN=")
]

lines.append(f"GOOGLE_ADS_REFRESH_TOKEN={refresh}")

ENV.write_text(
    "\n".join(lines)+"\n",
    encoding="utf-8"
)

print("GOOGLE_ADS_REFRESH_TOKEN saved to .env")
