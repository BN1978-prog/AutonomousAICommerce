from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8")

text=text.replace(
    'if status=="FAILED":',
    'if status in ["FAILED","ERROR"]:'
)

p.write_text(text,encoding="utf-8")

print("error handler fixed")
