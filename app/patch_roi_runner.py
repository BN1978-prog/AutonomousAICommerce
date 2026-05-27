from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8")

anchor='run_step("product_guardrails","python -m app.product_guardrails")'

replacement='''
run_step("product_guardrails","python -m app.product_guardrails")
run_step("roi_simulation","python -m app.roi_simulation")'''

if 'roi_simulation' not in text:
    text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")

print("roi_simulation added to autopilot")
