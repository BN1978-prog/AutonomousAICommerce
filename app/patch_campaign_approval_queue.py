from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8-sig")

anchor='run_step("campaign_hub","python -m app.campaign_hub")'

replacement='''run_step("campaign_hub","python -m app.campaign_hub")
run_step("campaign_approval_queue","python -m app.campaign_approval_queue")'''

if 'campaign_approval_queue' not in text:
    text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")
print("campaign_approval_queue added")
