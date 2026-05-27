from pathlib import Path

p=Path("app/campaign_approval_queue.py")

text=p.read_text(encoding="utf-8-sig")

p.write_text(
    text,
    encoding="utf-8"
)

print("BOM removed from campaign_approval_queue.py")
