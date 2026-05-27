import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/amazon_connection_status.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

req = read_json("app/logs/global_channel_requirements_check.json")

amazon = {}

for ch in req.get("channels", []):
    if ch.get("channel") == "amazon":
        amazon = ch

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "channel": "amazon",
    "lwa_credentials_saved": "AMAZON_LWA_CLIENT_ID" not in amazon.get("missing", []) and "AMAZON_LWA_CLIENT_SECRET" not in amazon.get("missing", []),
    "marketplace_id_saved": "AMAZON_MARKETPLACE_ID" not in amazon.get("missing", []),
    "missing": amazon.get("missing", []),
    "ready": amazon.get("ready", False),
    "status": "AMAZON_PARTIAL_CONNECTED_WAITING_AUTHORIZATION" if amazon.get("missing") else "AMAZON_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
