from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8-sig")

anchor='run_step("daily_summary", "python -m app.daily_summary")'

replacement='''run_step("daily_summary", "python -m app.daily_summary")
run_step("send_daily_summary", "python -m app.send_daily_summary")'''

if 'send_daily_summary' not in text:
    text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")

print("send_daily_summary added")
