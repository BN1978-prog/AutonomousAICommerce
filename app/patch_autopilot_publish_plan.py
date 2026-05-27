from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8-sig")

anchor='run_step("build_priority_queue", "python -m app.build_priority_queue")'
replacement='''run_step("build_priority_queue", "python -m app.build_priority_queue")
run_step("publish_execution_plan", "python -m app.publish_execution_plan")'''

if 'publish_execution_plan' not in text:
    text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")
print("publish_execution_plan added to autopilot")
