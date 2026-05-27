import json
import os
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv(override=True)

OUT = Path("app/logs/crm_provider_config_check.json")

PLACEHOLDERS = [
    "",
    "your_email@gmail.com",
    "your_app_password",
    "CHANGE_ME",
    "changeme"
]

providers = {
    "smtp": [
        "SMTP_HOST",
        "SMTP_PORT",
        "SMTP_USER",
        "SMTP_PASSWORD",
        "SMTP_FROM_EMAIL"
    ],
    "sendgrid": [
        "SENDGRID_API_KEY",
        "SENDGRID_FROM_EMAIL"
    ],
    "twilio_sms": [
        "TWILIO_ACCOUNT_SID",
        "TWILIO_AUTH_TOKEN",
        "TWILIO_FROM_PHONE"
    ]
}

results = []

for provider, keys in providers.items():
    missing = []
    placeholders = []

    for key in keys:
        value = os.getenv(key, "")

        if not value:
            missing.append(key)

        if value in PLACEHOLDERS or value.startswith("PASTE_"):
            placeholders.append(key)

    results.append({
        "provider": provider,
        "ready": len(missing) == 0 and len(placeholders) == 0,
        "missing": missing,
        "placeholders": placeholders
    })

ready = [x["provider"] for x in results if x["ready"]]

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "providers": results,
    "ready_providers": ready,
    "send_allowed": False,
    "status": "CRM_PROVIDER_CONFIG_READY" if ready else "CRM_PROVIDER_CONFIG_TEMPLATE_ONLY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
