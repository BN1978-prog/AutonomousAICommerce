import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/crm_message_generator.json")

templates = [
    {
        "flow": "abandoned_cart",
        "subject": "You left something behind",
        "body": "Your selected items are still waiting for you. Complete your order before they are gone.",
        "send_enabled": False
    },
    {
        "flow": "order_confirmation",
        "subject": "Your order has been received",
        "body": "Thank you for your order. We are preparing it and will update you soon.",
        "send_enabled": False
    },
    {
        "flow": "review_request",
        "subject": "How was your order?",
        "body": "We hope you love your product. Please leave a quick review and help other customers.",
        "send_enabled": False
    },
    {
        "flow": "win_back",
        "subject": "We saved something special for you",
        "body": "Come back and discover new products selected for you.",
        "send_enabled": False
    }
]

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "templates_created": len(templates),
    "send_enabled": False,
    "templates": templates,
    "status": "CRM_MESSAGES_READY_DRAFT_ONLY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
