from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8")

anchor='run_step("ceo_dashboard","python -m app.ceo_dashboard")'

replacement='''
run_step("ceo_dashboard","python -m app.ceo_dashboard")
run_step("auto_launch_engine","python -m app.auto_launch_engine")
run_step("auto_spend_executor","python -m app.auto_spend_executor")'''

if 'auto_launch_engine' not in text:
    text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")

print("auto launch and spend executor added to autopilot")
