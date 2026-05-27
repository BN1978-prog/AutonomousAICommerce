from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8")

anchor='run_step("negative_roi_auto_pause","python -m app.negative_roi_auto_pause")'

replacement='''
run_step("negative_roi_auto_pause","python -m app.negative_roi_auto_pause")
run_step("hourly_budget_monitor","python -m app.hourly_budget_monitor")'''

if 'hourly_budget_monitor' not in text:
    text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")

print("hourly_budget_monitor added to autopilot")
