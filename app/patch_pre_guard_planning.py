from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8-sig")

# remove later duplicate block if exists
text=text.replace('run_step("exploration_engine_v2", "python -m app.exploration_engine_v2")\nrun_step("build_priority_queue", "python -m app.build_priority_queue")\nrun_step("publish_execution_plan", "python -m app.publish_execution_plan")\n','')

anchor='run_step("crm_readiness_summary", "python -m app.crm_readiness_summary")'

insert='''run_step("crm_readiness_summary", "python -m app.crm_readiness_summary")
run_step("exploration_engine_v2", "python -m app.exploration_engine_v2")
run_step("build_priority_queue", "python -m app.build_priority_queue")
run_step("publish_execution_plan", "python -m app.publish_execution_plan")'''

text=text.replace(anchor,insert)

p.write_text(text,encoding="utf-8")
print("Exploration/priority/publish plan moved before daily guard")
