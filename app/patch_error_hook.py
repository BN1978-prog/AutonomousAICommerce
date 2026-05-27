from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8")

anchor='''
status = "OK" if p.returncode in allow_codes else "ERROR"
'''

inject='''
status = "OK" if p.returncode in allow_codes else "ERROR"

if status in ["FAILED","ERROR"]:
    try:
        send_alert(
            "SYSTEM ERROR",
            f"Step: {name}\n\nCommand:\n{command}"
        )
    except Exception as e:
        print("Alert error:",e)
'''

if anchor in text:
    text=text.replace(anchor,inject)

p.write_text(text,encoding="utf-8")

print("telegram error hook inserted")
