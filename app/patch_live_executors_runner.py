from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8")

anchor='run_step("live_mode_final_lock","python -m app.live_mode_final_lock")'

replacement='''
run_step("live_mode_final_lock","python -m app.live_mode_final_lock")
run_step("meta_live_executor","python -m app.meta_live_executor")
run_step("google_live_executor","python -m app.google_live_executor")'''

if 'meta_live_executor' not in text:
    text=text.replace(anchor,replacement)

p.write_text(text,encoding="utf-8")

print("live executors added to autopilot")
