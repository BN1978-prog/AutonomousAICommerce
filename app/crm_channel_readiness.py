import json
import os
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv(override=True)

OUT = Path("app/logs/crm_channel_readiness.json")

PLACEHOLDERS = [
    "",
    "your_email@gmail.com",
    "your_app_password",
    "CHANGE_ME",
    "changeme"
]

providers = {
    "smtp": {
        "required": [
            "SMTP_HOST",
            "SMTP_USER",
            "SMTP_PASSWORD",
            "SMTP_FROM_EMAIL"
        ]
    },
    "sendgrid": {
        "required": [
            "SENDGRID_API_KEY",
            "SENDGRID_FROM_EMAIL"
        ]
    },
    "twilio_sms": {
        "required": [
            "TWILIO_ACCOUNT_SID",
            "TWILIO_AUTH_TOKEN",
            "TWILIO_FROM_PHONE"
        ]
    }
}

results = []

for name, cfg in providers.items():
    missing = []
    placeholders = []

    for key in cfg["required"]:
        value = os.getenv(key, "")

        if not value:
            missing.append(key)

        if value in PLACEHOLDERS:
            placeholders.append(key)

    results.append({
        "provider": name,
        "ready": len(missing) == 0 and len(placeholders) == 0,
        "missing": missing,
        "placeholders": placeholders
    })

ready = [r for r in results if r["ready"]]

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "providers": results,
    "ready_providers": [r["provider"] for r in ready],
    "send_allowed": False,
    "status": "CRM_CHANNEL_READY" if ready else "CRM_CHANNEL_NOT_CONNECTED"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
