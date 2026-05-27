import os, json, smtplib
from pathlib import Path
from email.mime.text import MIMEText
from datetime import datetime, timezone

ENV = Path(".env")
OUT = Path("app/logs/send_daily_summary.json")
SUMMARY = Path("app/logs/daily_summary.txt")

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
    if not SUMMARY.exists():
        raise RuntimeError("daily_summary.txt not found")

    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASSWORD")
    from_email = os.getenv("SMTP_FROM_EMAIL") or user
    to_email = os.getenv("OWNER_EMAIL") or user

    if not all([host, port, user, password, from_email, to_email]):
        raise RuntimeError("missing SMTP config")

    body = SUMMARY.read_text(encoding="utf-8")

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = "AICommerce Daily Autopilot Summary"
    msg["From"] = from_email
    msg["To"] = to_email

    with smtplib.SMTP(host, port, timeout=30) as smtp:
        smtp.starttls()
        smtp.login(user, password)
        smtp.send_message(msg)

    report.update({
        "sent": True,
        "to": to_email,
        "status": "DAILY_SUMMARY_SENT"
    })

except Exception as e:
    report["status"] = "DAILY_SUMMARY_SEND_FAILED"
    report["error"] = str(e)

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
