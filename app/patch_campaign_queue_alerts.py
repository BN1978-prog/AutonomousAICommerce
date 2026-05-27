from pathlib import Path

p=Path("app/campaign_approval_queue.py")
text=p.read_text(encoding="utf-8")

if "from app.alert_dispatcher import notify" not in text:
    text="from app.alert_dispatcher import notify\n"+text

anchor='''
OUT.write_text(
'''

insert='''
try:
    queue = report.get("queue", [])

    if queue:
        top = queue[0]

        sku = top.get("sku","unknown")

        payload = (
            f"Product: {sku}\n"
            f"Meta draft: READY\n"
            f"Google draft: READY\n\n"
            f"Waiting for owner approval"
        )

        notify("CAMPAIGN_WAITING_APPROVAL", payload)

        print(f"CAMPAIGN ALERT SENT: {sku}")

except Exception as e:
    print("campaign approval alert skipped:", e)

'''

if "CAMPAIGN ALERT SENT" not in text:
    text=text.replace(anchor, insert + anchor)

p.write_text(text,encoding="utf-8")

print("campaign approval alerts connected")
