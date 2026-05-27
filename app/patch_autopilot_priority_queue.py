from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8-sig")

anchor='run_step("exploration_engine_v2", "python -m app.exploration_engine_v2")'
replacement='''run_step("exploration_engine_v2", "python -m app.exploration_engine_v2")
run_step("build_priority_queue", "python -m app.build_priority_queue")'''

if 'build_priority_queue' not in text:
    text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")
print("build_priority_queue added to autopilot")
