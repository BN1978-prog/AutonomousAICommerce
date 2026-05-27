from pathlib import Path

p=Path("app/system_status_report.py")
text=p.read_text(encoding="utf-8-sig")

text=text.replace("→","->")

p.write_text(text,encoding="utf-8")

print("Unicode symbols fixed")
