import json
from pathlib import Path
from datetime import datetime, timezone

SRC = Path("app/logs/campaign_executor.json")
OUT = Path("app/logs/google_campaign_live_creator.json")

data = json.loads(SRC.read_text(encoding="utf-8-sig"))

payloads = []

for c in data.get("campaigns", []):
    if "google_ads" not in c.get("channels", []):
        continue

    payloads.append({
        "sku": c.get("sku"),
        "campaign_name": "AICommerce Google Test - " + c.get("title", c.get("sku")),
        "title": c.get("title"),
        "budget": min(c.get("daily_test_budget", 5), 5),
        "status": "PAUSED",
        "spend_enabled": False,
        "mode": "payload_only_no_api_call",
        "channel": "google_ads"
    })

OUT.write_text(json.dumps({
    "created_at": datetime.now(timezone.utc).isoformat(),
    "mode": "google_payload_only_safe_mode",
    "google_live_api_enabled": False,
    "payloads_created": len(payloads),
    "payloads": payloads,
    "live_api_call_enabled": False,
    "live_money_spending": False,
    "status": "google_campaign_payloads_ready" if payloads else "no_google_campaigns"
}, indent=2), encoding="utf-8")

print("Google payloads created:", len(payloads))
