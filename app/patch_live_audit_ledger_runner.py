from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8")

anchor='run_step("live_execution_consolidator","python -m app.live_execution_consolidator")'

replacement='''
run_step("live_execution_consolidator","python -m app.live_execution_consolidator")
run_step("live_spend_audit_ledger","python -m app.live_spend_audit_ledger")'''

if 'live_spend_audit_ledger' not in text:
    text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")

print("live_spend_audit_ledger added to autopilot")
