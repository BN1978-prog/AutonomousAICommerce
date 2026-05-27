from app.alert_dispatcher import notify
import json
from pathlib import Path
from datetime import datetime, timezone

HUB = Path("app/logs/campaign_hub.json")
OUT = Path("app/logs/campaign_approval_queue.json")

data = json.loads(HUB.read_text(encoding="utf-8-sig")) if HUB.exists() else {}

queue = []

for c in data.get("campaigns", []):
    queue.append({
        "sku": c.get("sku"),
        "social_content_ready": c.get("social_content_ready"),
        "meta_draft_ready": c.get("meta_draft_ready"),
        "google_draft_ready": c.get("google_draft_ready"),
        "owner_approved": False,
        "approval_status": "WAITING_OWNER_APPROVAL",
        "allowed_next_actions": [
            "prepare_meta_paused_campaign",
            "prepare_google_paused_campaign"
        ]
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "items": len(queue),
    "queue": queue,
    "live_money_spending": False,
    "status": "CAMPAIGN_APPROVAL_QUEUE_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
