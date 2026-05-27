from pathlib import Path

p=Path("app/meta_live_executor.py")
text=p.read_text(encoding="utf-8")

text=text.replace(
    '"special_ad_categories": [],',
    '"special_ad_categories": "[]",'
)

p.write_text(text,encoding="utf-8")

print("Meta special_ad_categories fixed")
