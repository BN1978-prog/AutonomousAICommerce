import json, os
from pathlib import Path
from datetime import datetime, timezone

ENV = Path(".env")

if ENV.exists():
    for line in ENV.read_text(encoding="utf-8-sig").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k,v=line.split("=",1)
            os.environ[k.strip()] = v.strip()

config_keys = [
    "ETSY_API_KEY",
    "ETSY_CLIENT_ID",
    "ETSY_CLIENT_SECRET",
    "ETSY_REDIRECT_URI"
]

runtime_keys = [
    "ETSY_SHOP_ID",
    "ETSY_ACCESS_TOKEN",
    "ETSY_REFRESH_TOKEN"
]

config_missing = [k for k in config_keys if not os.getenv(k)]
runtime_missing = [k for k in runtime_keys if not os.getenv(k)]

if config_missing:
    status = "ETSY_WAITING_CONFIGURATION"
elif runtime_missing:
    status = "ETSY_WAITING_PERSONAL_APPROVAL_OR_OAUTH"
else:
    status = "ETSY_READY"

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "channel": "etsy",
    "config_missing": config_missing,
    "runtime_missing": runtime_missing,
    "ready": status == "ETSY_READY",
    "status": status,
    "note": "If OAuth returns 403 API key not active, wait for Etsy Personal Approval."
}

Path("app/logs/etsy_connection_status.json").write_text(
    json.dumps(report, indent=2),
    encoding="utf-8"
)

print(json.dumps(report, indent=2))
