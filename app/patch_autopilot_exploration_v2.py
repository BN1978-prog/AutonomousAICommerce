from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8-sig")

anchor='run_step("exploration_engine", "python -m app.exploration_engine")'

replacement='''run_step("exploration_engine", "python -m app.exploration_engine")
run_step("exploration_engine_v2", "python -m app.exploration_engine_v2")'''

if 'exploration_engine_v2' not in text:
    text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")

print("Exploration v2 added to autopilot")
