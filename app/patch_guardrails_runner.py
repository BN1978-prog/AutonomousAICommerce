from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8")

anchor='run_step("auto_scaling_score","python -m app.auto_scaling_score")'

replacement='''
run_step("auto_scaling_score","python -m app.auto_scaling_score")
run_step("product_guardrails","python -m app.product_guardrails")'''

if 'product_guardrails' not in text:
    text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")

print("product_guardrails added to autopilot")
