from pathlib import Path

p = Path("app/autopilot_runner.py")
text = p.read_text(encoding="utf-8-sig")

if "from app.send_telegram_alert import send_alert" not in text:
    text = "from app.send_telegram_alert import send_alert\n" + text

old = '''def run_step(name, cmd):'''

new = '''def run_step(name, cmd):'''

# пока импорт добавлен отдельно, структуру run_step не ломаем
p.write_text(text, encoding="utf-8")

print("telegram alert import added")
