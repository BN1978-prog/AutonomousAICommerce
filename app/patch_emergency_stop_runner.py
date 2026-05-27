from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8")

anchor='run_step("hourly_budget_monitor","python -m app.hourly_budget_monitor")'

replacement='''
run_step("hourly_budget_monitor","python -m app.hourly_budget_monitor")
run_step("emergency_stop_validator","python -m app.emergency_stop_validator")'''

if 'emergency_stop_validator' not in text:
    text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")

print("emergency_stop_validator added to autopilot")
