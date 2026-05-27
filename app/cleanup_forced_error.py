from pathlib import Path

p=Path("app/autopilot_runner.py")
text=p.read_text(encoding="utf-8")

text=text.replace(
    'run_step("forced_test_error","python nonexistent_file.py")',
    ''
)

p.write_text(text,encoding="utf-8")

print("forced_test_error removed")
