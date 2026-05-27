from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8")

anchor='run_step("emergency_stop_validator","python -m app.emergency_stop_validator")'

replacement='''
run_step("emergency_stop_validator","python -m app.emergency_stop_validator")
run_step("live_spend_permission_gate","python -m app.live_spend_permission_gate")'''

if 'live_spend_permission_gate' not in text:
    text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")

print("live_spend_permission_gate added to autopilot")
