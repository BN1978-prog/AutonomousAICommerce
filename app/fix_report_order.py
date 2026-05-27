from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8-sig")

old='''run_step("daily_summary", "python -m app.daily_summary")
    run_step("system_status_report", "python -m app.system_status_report")'''

new='''run_step("system_status_report", "python -m app.system_status_report")
    run_step("daily_summary", "python -m app.daily_summary")'''

text=text.replace(old,new)

p.write_text(text,encoding="utf-8")

print("Fixed report order")
