from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8")

anchor='run_step("live_execution_reporter","python -m app.live_execution_reporter")'

replacement='''
run_step("live_execution_reporter","python -m app.live_execution_reporter")
run_step("live_mode_final_lock","python -m app.live_mode_final_lock")'''

if 'live_mode_final_lock' not in text:
    text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")

print("live_mode_final_lock added to autopilot")
