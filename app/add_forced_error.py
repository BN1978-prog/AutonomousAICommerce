from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8")

anchor='run_step("send_telegram_summary","python -m app.send_telegram_summary")'

inject='''
run_step("send_telegram_summary","python -m app.send_telegram_summary")
run_step("forced_test_error","python nonexistent_file.py")
'''

if "forced_test_error" not in text:
    text=text.replace(anchor,inject)

p.write_text(text,encoding="utf-8")

print("forced error added")
