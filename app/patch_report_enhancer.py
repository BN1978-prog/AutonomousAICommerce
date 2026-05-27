from pathlib import Path

p=Path("app/system_status_report.py")
text=p.read_text(encoding="utf-8-sig")

old='''- social_content_generator: OK'''

new='''- social_content_generator: OK
- social_content_enhancer: OK'''

if "social_content_enhancer" not in text:
    text=text.replace(old,new)

p.write_text(text,encoding="utf-8")

print("enhancer added to report")
