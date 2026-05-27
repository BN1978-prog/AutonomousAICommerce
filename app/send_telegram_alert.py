import os
import requests
from pathlib import Path

for line in Path(".env").read_text(encoding="utf-8-sig").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k, v = line.split("=", 1)
        os.environ[k.strip()] = v.strip()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT = os.getenv("TELEGRAM_CHAT_ID")

def send_alert(title, message):
    text = f"🚨 {title}\n\n{message}"

    r = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={"chat_id": CHAT, "text": text},
        timeout=30
    )

    print(r.status_code)
    print(r.text)

if __name__ == "__main__":
    send_alert(
        "SYSTEM TEST",
        "Telegram alerts connected successfully ✅"
    )
