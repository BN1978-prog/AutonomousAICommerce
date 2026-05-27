from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8-sig")

old='''
status = "OK" if r.returncode == 0 else "FAILED"
'''

new='''
status = "OK" if r.returncode == 0 else "FAILED"

if status=="FAILED":
    try:
        send_alert(
            "SYSTEM ERROR",
            f"Step: {name}\n\nCommand:\n{cmd}"
        )
    except Exception:
        pass
'''

if old in text:
    text=text.replace(old,new)

p.write_text(text,encoding="utf-8")

print("system error alerts added")
