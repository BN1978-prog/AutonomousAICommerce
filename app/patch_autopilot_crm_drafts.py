from pathlib import Path

p = Path("app/autopilot_runner.py")
text = p.read_text(encoding="utf-8-sig")

target = 'run_step("daily_summary", "python -m app.daily_summary")'
insert = '''
run_step("shopify_crm_events", "python -m app.shopify_crm_events")
run_step("crm_personalized_drafts", "python -m app.crm_personalized_drafts")
run_step("daily_summary", "python -m app.daily_summary")'''.strip()

if "crm_personalized_drafts" not in text:
    text = text.replace(target, insert)

p.write_text(text, encoding="utf-8")
print("CRM personalized drafts added to autopilot_runner")
