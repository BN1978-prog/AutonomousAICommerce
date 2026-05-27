from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8")

anchor='run_step("daily_summary","python -m app.daily_summary")'

replacement='''
run_step("daily_summary","python -m app.daily_summary")
run_step("auto_scaling_score","python -m app.auto_scaling_score")'''

if 'auto_scaling_score' not in text:
    text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")

print("auto_scaling_score added to autopilot")
