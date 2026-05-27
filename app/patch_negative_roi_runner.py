from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8")

anchor='run_step("spend_history_tracker","python -m app.spend_history_tracker")'

replacement='''
run_step("spend_history_tracker","python -m app.spend_history_tracker")
run_step("negative_roi_auto_pause","python -m app.negative_roi_auto_pause")'''

if 'negative_roi_auto_pause' not in text:
    text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")

print("negative_roi_auto_pause added to autopilot")
