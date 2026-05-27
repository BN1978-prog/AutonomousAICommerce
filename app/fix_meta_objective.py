from pathlib import Path

files = [
    Path("app/meta_live_campaign_builder.py"),
    Path("app/meta_live_executor.py")
]

for p in files:
    if p.exists():
        text=p.read_text(encoding="utf-8")
        text=text.replace('"objective": "SALES"', '"objective": "OUTCOME_SALES"')
        text=text.replace('item.get("objective", "SALES")', 'item.get("objective", "OUTCOME_SALES")')
        p.write_text(text,encoding="utf-8")
        print("fixed", p)
