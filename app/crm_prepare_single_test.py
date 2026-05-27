from pathlib import Path
import json
from datetime import datetime, timezone

Path("app/logs/crm_owner_confirmed.json").write_text(
    json.dumps({
        "created_at": datetime.now(timezone.utc).isoformat(),
        "owner_confirmed": True,
        "confirmed_by": "local_owner",
        "note": "Owner approved limited CRM send test"
    }, indent=2),
    encoding="utf-8"
)

Path("app/logs/crm_queue.json").write_text(
    json.dumps({
        "created_at": datetime.now(timezone.utc).isoformat(),
        "queue_size": 1,
        "items": [
            {
                "flow": "win_back",
                "to": "fenix1978n@gmail.com",
                "subject": "CRM test email",
                "body": "Hi Nicolai, this is a safe CRM SMTP test from AICommerce. Real send limit is 1 per day.",
                "status": "queued_test"
            }
        ]
    }, indent=2),
    encoding="utf-8"
)

print("CRM owner confirmed and 1 test queue item created")
