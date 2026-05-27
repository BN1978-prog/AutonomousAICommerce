from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8")

anchor='run_step("google_live_campaign_builder","python -m app.google_live_campaign_builder")'

replacement='''
run_step("google_live_campaign_builder","python -m app.google_live_campaign_builder")
run_step("live_campaign_registry","python -m app.live_campaign_registry")'''

if 'live_campaign_registry' not in text:
    text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")

print("live_campaign_registry added to autopilot")
