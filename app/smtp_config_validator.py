import json
import os
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv(override=True)

OUT = Path("app/logs/smtp_config_validator.json")

values = {
    "SMTP_HOST": os.getenv("SMTP_HOST", ""),
    "SMTP_PORT": os.getenv("SMTP_PORT", ""),
    "SMTP_USER": os.getenv("SMTP_USER", ""),
    "SMTP_PASSWORD": os.getenv("SMTP_PASSWORD", ""),
    "SMTP_FROM_EMAIL": os.getenv("SMTP_FROM_EMAIL", "")
}

placeholder_values = [
    "your_email@gmail.com",
    "your_app_password",
    "",
    "CHANGE_ME",
    "changeme"
]

missing = []
placeholders = []

for key, value in values.items():
    if not value:
        missing.append(key)

    if value in placeholder_values:
        placeholders.append(key)

ready = not missing and not placeholders

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "values_present": {k: bool(v) for k, v in values.items()},
    "missing": missing,
    "placeholders": placeholders,
    "smtp_ready_for_real_send": ready,
    "status": "SMTP_CONFIG_READY" if ready else "SMTP_CONFIG_TEMPLATE_ONLY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
