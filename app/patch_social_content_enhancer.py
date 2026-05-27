from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8-sig")

anchor='run_step("social_content_generator","python -m app.social_content_generator")'
replacement='''run_step("social_content_generator","python -m app.social_content_generator")
run_step("social_content_enhancer","python -m app.social_content_enhancer")'''

if 'social_content_enhancer' not in text:
    text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")
print("social_content_enhancer added")
