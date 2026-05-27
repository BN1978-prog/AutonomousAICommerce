from pathlib import Path

p=Path("app/auto_scaling_score.py")
text=p.read_text(encoding="utf-8")

if "from app.alert_dispatcher import notify" not in text:
    text="from app.alert_dispatcher import notify\n"+text

anchor='''
OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
'''

insert='''
try:
    for item in report["scale_ready"]:

        payload = (
            f"Product: {item['sku']}\\n"
            f"Score: {item['score']}\\n"
            f"Sales: {item['sales']}\\n"
            f"Clicks: {item['clicks']}\\n\\n"
            f"Recommended: PREPARE_SCALING_REVIEW"
        )

        notify("SCALE_CANDIDATE", payload)

        print(f"SCALE ALERT SENT: {item['sku']}")

except Exception as e:
    print("scale alert skipped:", e)

'''

if "SCALE ALERT SENT" not in text:
    text=text.replace(anchor, insert + anchor)

p.write_text(text,encoding="utf-8")

print("scale alerts connected")
