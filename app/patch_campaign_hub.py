from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8-sig")

anchor='run_step("google_ad_drafts_from_content","python -m app.google_ad_drafts_from_content")'

replacement='''run_step("google_ad_drafts_from_content","python -m app.google_ad_drafts_from_content")
run_step("campaign_hub","python -m app.campaign_hub")'''

if 'campaign_hub' not in text:
    text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")
print("campaign_hub added")
