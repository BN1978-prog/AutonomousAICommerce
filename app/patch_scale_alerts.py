from pathlib import Path

p=Path("app/alert_dispatcher.py")
text=p.read_text(encoding="utf-8")

old='''
        "CAMPAIGN_WAITING_APPROVAL":
        lambda p: send_alert(
            "CAMPAIGN READY",
            p
        )
'''

new='''
        "CAMPAIGN_WAITING_APPROVAL":
        lambda p: send_alert(
            "CAMPAIGN READY",
            p
        ),

        "SCALE_CANDIDATE":
        lambda p: send_alert(
            "SCALE CANDIDATE",
            p
        )
'''

text=text.replace(old,new)

p.write_text(text,encoding="utf-8")

print("scale candidate alerts added")
