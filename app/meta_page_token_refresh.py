import os, json, requests, re
from pathlib import Path
from datetime import datetime, timezone

ENV = Path(".env")
OUT = Path("app/logs/meta_page_token_refresh.json")

def load_env():
    if ENV.exists():
        for line in ENV.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()

def update_env(key, value):
    text = ENV.read_text(encoding="utf-8") if ENV.exists() else ""
    pattern = rf"^{re.escape(key)}=.*$"
    if re.search(pattern, text, flags=re.MULTILINE):
        text = re.sub(pattern, f"{key}={value}", text, flags=re.MULTILINE)
    else:
        text += f"\n{key}={value}"
    ENV.write_text(text.strip() + "\n", encoding="utf-8")

load_env()

user_token = os.getenv("META_ACCESS_TOKEN")
page_id = os.getenv("META_PAGE_ID")

result = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "page_id": page_id,
    "status": "unknown"
}

r = requests.get(
    "https://graph.facebook.com/v19.0/me/accounts",
    params={"access_token": user_token},
    timeout=30
)

result["me_accounts_status"] = r.status_code

try:
    data = r.json()
except Exception:
    data = {"raw": r.text}

result["response"] = data

page_token = None

for page in data.get("data", []):
    if str(page.get("id")) == str(page_id):
        page_token = page.get("access_token")
        result["page_found"] = True
        result["page_name"] = page.get("name")
        break

if page_token:
    update_env("META_PAGE_ACCESS_TOKEN", page_token)
    result["status"] = "page_token_refreshed"
else:
    result["status"] = "page_token_not_found"

OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
