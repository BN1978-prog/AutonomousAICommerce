from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8-sig")

anchor='run_step("crm_readiness_summary", "python -m app.crm_readiness_summary")'

replacement='''run_step("crm_readiness_summary", "python -m app.crm_readiness_summary")
run_step("etsy_connection_status", "python -m app.etsy_connection_status")
run_step("etsy_autopilot", "python -m app.etsy_autopilot")'''

if 'etsy_autopilot' not in text:
    text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")
print("Etsy added to autopilot")
