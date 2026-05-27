import os, json, requests
from pathlib import Path
from datetime import datetime, timezone

ENV = Path(".env")
OUT = Path("app/logs/etsy_oauth_exchange.json")

for line in ENV.read_text(encoding="utf-8-sig").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k,v=line.split("=",1)
        os.environ[k.strip()] = v.strip()

def update_env(key, value):
    lines = ENV.read_text(encoding="utf-8-sig").splitlines()
    found = False
    for i,line in enumerate(lines):
        if line.startswith(key + "="):
            lines[i] = key + "=" + value
            found = True
    if not found:
        lines.append(key + "=" + value)
    ENV.write_text("\n".join(lines) + "\n", encoding="utf-8")

client_id = os.getenv("ETSY_CLIENT_ID") or os.getenv("ETSY_API_KEY")
redirect_uri = os.getenv("ETSY_REDIRECT_URI")
code = os.getenv("ETSY_AUTH_CODE")
verifier_path = Path("app/logs/etsy_pkce_verifier.txt")
verifier = verifier_path.read_text(encoding="utf-8").strip() if verifier_path.exists() else ""

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "ok": False
}

if not client_id or not redirect_uri or not code or not verifier:
    report["status"] = "missing_client_redirect_code_or_pkce_verifier"
else:
    r = requests.post(
        "https://api.etsy.com/v3/public/oauth/token",
        data={
            "grant_type": "authorization_code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "code": code,
            "code_verifier": verifier
        },
        timeout=30
    )

    report["status_code"] = r.status_code

    try:
        data = r.json()
    except Exception:
        data = {"raw": r.text}

    report["response"] = {
        k: ("***" if "token" in k else v)
        for k,v in data.items()
    }

    if r.status_code == 200 and data.get("access_token"):
        update_env("ETSY_ACCESS_TOKEN", data.get("access_token"))
        if data.get("refresh_token"):
            update_env("ETSY_REFRESH_TOKEN", data.get("refresh_token"))
        report["ok"] = True
        report["status"] = "ETSY_OAUTH_TOKENS_SAVED"
    else:
        report["status"] = "ETSY_OAUTH_EXCHANGE_FAILED"

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
