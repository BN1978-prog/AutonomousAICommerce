from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8-sig")

anchor='run_step("action_executor","python -m app.action_executor")'
replacement='''run_step("action_executor","python -m app.action_executor")
run_step("social_content_generator","python -m app.social_content_generator")'''

if 'social_content_generator' not in text:
    text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")
print("social_content_generator added")
