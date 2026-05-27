from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8-sig")

anchor='run_step("meta_ad_drafts_from_content","python -m app.meta_ad_drafts_from_content")'

replacement='''run_step("meta_ad_drafts_from_content","python -m app.meta_ad_drafts_from_content")
run_step("google_ad_drafts_from_content","python -m app.google_ad_drafts_from_content")'''

if 'google_ad_drafts_from_content' not in text:
    text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")
print("google_ad_drafts_from_content added")
