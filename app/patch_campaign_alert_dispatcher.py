from pathlib import Path

p=Path("app/alert_dispatcher.py")
text=p.read_text(encoding="utf-8")

old='''
        "WINNER_PRODUCT":
        lambda p: send_alert(
            "WINNER PRODUCT",
            p
        )
'''

new='''
        "WINNER_PRODUCT":
        lambda p: send_alert(
            "WINNER PRODUCT",
            p
        ),

        "CAMPAIGN_WAITING_APPROVAL":
        lambda p: send_alert(
            "CAMPAIGN READY",
            p
        )
'''

text=text.replace(old,new)

p.write_text(text,encoding="utf-8")

print("campaign approval alert added")
