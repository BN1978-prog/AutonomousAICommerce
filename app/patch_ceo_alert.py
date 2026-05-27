from pathlib import Path

p=Path("app/alert_dispatcher.py")
text=p.read_text(encoding="utf-8")

old='''
        "SCALE_CANDIDATE":
        lambda p: send_alert(
            "SCALE CANDIDATE",
            p
        )
'''

new='''
        "SCALE_CANDIDATE":
        lambda p: send_alert(
            "SCALE CANDIDATE",
            p
        ),

        "CEO_DASHBOARD":
        lambda p: send_alert(
            "CEO DASHBOARD",
            p
        )
'''

text=text.replace(old,new)

p.write_text(text,encoding="utf-8")

print("CEO dashboard alert added")
