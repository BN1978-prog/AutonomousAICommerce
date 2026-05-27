from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8")

anchor='run_step("live_api_execution_gate","python -m app.live_api_execution_gate")'

replacement='''
run_step("live_api_execution_gate","python -m app.live_api_execution_gate")
run_step("live_execution_reporter","python -m app.live_execution_reporter")'''

if 'live_execution_reporter' not in text:
    text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")

print("live_execution_reporter added to autopilot")
