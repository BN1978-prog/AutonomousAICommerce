import os, json, smtplib
from pathlib import Path
from datetime import datetime, timezone
from email.message import EmailMessage

ENV = Path(".env")
for line in ENV.read_text(encoding="utf-8-sig").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k, v = line.split("=", 1)
        os.environ[k.strip()] = v.strip()

QUEUE = Path("app/logs/crm_queue.json")
GATE = Path("app/logs/crm_final_gate.json")
OUT = Path("app/logs/crm_send_one_test.json")

gate = json.loads(GATE.read_text(encoding="utf-8-sig")) if GATE.exists() else {}
queue = json.loads(QUEUE.read_text(encoding="utf-8-sig")) if QUEUE.exists() else {}

if gate.get("status") != "CRM_FINAL_GATE_READY":
    print("Final gate not ready")
    raise SystemExit(1)

items = queue.get("queue") or queue.get("items") or []

if not items:
    print("CRM queue empty")
    raise SystemExit(1)

item = items[0]

to_email = item.get("to") or item.get("email")
subject = item.get("subject", "CRM test email")
body = item.get("body", "CRM test email from AICommerce.")

if to_email != "fenix1978n@gmail.com":
    print("Blocked: test sender only allows fenix1978n@gmail.com")
    raise SystemExit(1)

host = os.getenv("SMTP_HOST")
port = int(os.getenv("SMTP_PORT", "587"))
user = os.getenv("SMTP_USER")
password = os.getenv("SMTP_PASSWORD")
from_email = os.getenv("SMTP_FROM_EMAIL") or user

msg = EmailMessage()
msg["From"] = from_email
msg["To"] = to_email
msg["Subject"] = subject
msg.set_content(body)

with smtplib.SMTP(host, port, timeout=30) as smtp:
    smtp.starttls()
    smtp.login(user, password)
    smtp.send_message(msg)

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "sent": True,
    "to": to_email,
    "subject": subject,
    "status": "CRM_ONE_TEST_EMAIL_SENT"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
