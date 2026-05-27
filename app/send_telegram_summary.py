import os
import requests
import json
from pathlib import Path
from datetime import datetime, timezone

ENV = Path(".env")
SUMMARY = Path("app/logs/daily_summary.txt")
OUT = Path("app/logs/send_telegram_summary.json")

for line in ENV.read_text(encoding="utf-8-sig").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k,v=line.split("=",1)
        os.environ[k.strip()] = v.strip()

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "sent": False,
    "status": "NOT_SENT"
}

try:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat:
        raise RuntimeError("missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID")

    if not SUMMARY.exists():
        raise RuntimeError("daily_summary.txt not found")

    text = SUMMARY.read_text(encoding="utf-8")

    if len(text) > 3500:
        text = text[:3500] + "\n\n...truncated"

    r = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={
            "chat_id": chat,
            "text": text
        },
        timeout=30
    )

    report["status_code"] = r.status_code
    report["response"] = r.text[:500]

    if r.status_code == 200:
        report["sent"] = True
        report["status"] = "TELEGRAM_SUMMARY_SENT"
    else:
        report["status"] = "TELEGRAM_SEND_FAILED"

except Exception as e:
    report["status"] = "TELEGRAM_SEND_FAILED"
    report["error"] = str(e)

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
