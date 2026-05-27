from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8-sig")

anchor='run_step("daily_summary", "python -m app.daily_summary")'
replacement='''run_step("daily_summary", "python -m app.daily_summary")
run_step("system_status_report", "python -m app.system_status_report")'''

if 'system_status_report' not in text:
    text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")
print("system_status_report added to autopilot")
