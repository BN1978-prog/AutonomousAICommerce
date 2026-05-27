from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8")

anchor='run_step("live_backend_router","python -m app.live_backend_router")'

replacement='''
run_step("live_backend_router","python -m app.live_backend_router")
run_step("meta_live_campaign_builder","python -m app.meta_live_campaign_builder")'''

if 'meta_live_campaign_builder' not in text:
    text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")

print("meta_live_campaign_builder added to autopilot")
