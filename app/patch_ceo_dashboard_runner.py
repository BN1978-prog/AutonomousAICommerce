from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8")

anchor='run_step("roi_simulation","python -m app.roi_simulation")'

replacement='''
run_step("roi_simulation","python -m app.roi_simulation")
run_step("ceo_dashboard","python -m app.ceo_dashboard")'''

if 'ceo_dashboard' not in text:
    text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")

print("ceo_dashboard added to autopilot")
