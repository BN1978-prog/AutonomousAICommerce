import json
from pathlib import Path
from datetime import datetime, timezone

EVENTS = Path("app/logs/shopify_crm_events.json")
OUT = Path("app/logs/crm_personalized_drafts.json")

data = json.loads(EVENTS.read_text(encoding="utf-8-sig"))
events = data.get("events", [])

drafts = []

for e in events:
    event_type = e.get("event_type")
    email = e.get("email")
    name = e.get("first_name") or "there"

    if not email:
        continue

    if event_type == "win_back":
        subject = "We saved something special for you"
        body = f"Hi {name}, come back and discover new pet products selected for you."
    elif event_type == "order_confirmation":
        subject = "Your order has been received"
        body = f"Hi {name}, thank you for your order. We are preparing it and will update you soon."
    elif event_type == "review_request":
        subject = "How was your order?"
        body = f"Hi {name}, we hope you love your product. Please leave a quick review and help other customers."
    else:
        subject = "A quick update from us"
        body = f"Hi {name}, we have an update for you."

    drafts.append({
        "event_type": event_type,
        "to": email,
        "subject": subject,
        "body": body,
        "status": "draft_only",
        "send_enabled": False
    })

OUT.write_text(json.dumps({
    "created_at": datetime.now(timezone.utc).isoformat(),
    "drafts_created": len(drafts),
    "drafts": drafts,
    "send_enabled": False,
    "status": "CRM_PERSONALIZED_DRAFTS_READY"
}, indent=2), encoding="utf-8")

print("Personalized CRM drafts created:", len(drafts))
print(OUT)
