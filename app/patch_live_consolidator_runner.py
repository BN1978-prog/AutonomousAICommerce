from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8")

anchor='run_step("google_live_executor","python -m app.google_live_executor")'

replacement='''
run_step("google_live_executor","python -m app.google_live_executor")
run_step("live_execution_consolidator","python -m app.live_execution_consolidator")'''

if 'live_execution_consolidator' not in text:
    text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")

print("live_execution_consolidator added to autopilot")
