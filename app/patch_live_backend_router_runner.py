from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8")

anchor='run_step("live_spend_permission_gate","python -m app.live_spend_permission_gate")'

replacement='''
run_step("live_spend_permission_gate","python -m app.live_spend_permission_gate")
run_step("live_backend_router","python -m app.live_backend_router")'''

if 'live_backend_router' not in text:
    text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")

print("live_backend_router added to autopilot")
