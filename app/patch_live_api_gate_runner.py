from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8")

anchor='run_step("live_campaign_registry","python -m app.live_campaign_registry")'

replacement='''
run_step("live_campaign_registry","python -m app.live_campaign_registry")
run_step("live_api_execution_gate","python -m app.live_api_execution_gate")'''

if 'live_api_execution_gate' not in text:
    text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")

print("live_api_execution_gate added to autopilot")
