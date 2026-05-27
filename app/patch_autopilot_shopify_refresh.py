from pathlib import Path

p = Path("app/autopilot_runner.py")
text = p.read_text(encoding="utf-8-sig")

old = 'guard = run_step("daily_publish_guard", "python -m app.daily_publish_guard", allow_codes=[0,10])'
new = 'run_step("refresh_shopify_token", "python -m app.refresh_shopify_token")\n\nguard = run_step("daily_publish_guard", "python -m app.daily_publish_guard", allow_codes=[0,10])'

if "refresh_shopify_token" not in text:
    text = text.replace(old, new)

p.write_text(text, encoding="utf-8")
print("refresh_shopify_token added")
