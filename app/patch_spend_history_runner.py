from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8")

anchor='run_step("auto_spend_executor","python -m app.auto_spend_executor")'

replacement='''
run_step("auto_spend_executor","python -m app.auto_spend_executor")
run_step("spend_history_tracker","python -m app.spend_history_tracker")'''

if 'spend_history_tracker' not in text:
    text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")

print("spend_history_tracker added to autopilot")
