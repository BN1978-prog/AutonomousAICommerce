import os
import requests
from pathlib import Path

for line in Path(".env").read_text(
encoding="utf-8-sig"
).splitlines():

    if "=" in line:
        k,v=line.split("=",1)
        os.environ[k]=v

token=os.getenv("TELEGRAM_BOT_TOKEN")
chat=os.getenv("TELEGRAM_CHAT_ID")

url=f"https://api.telegram.org/bot{token}/sendMessage"

r=requests.post(
    url,
    json={
        "chat_id":chat,
        "text":"AICommerce Telegram connected successfully ✅"
    }
)

print(r.status_code)
print(r.text)
