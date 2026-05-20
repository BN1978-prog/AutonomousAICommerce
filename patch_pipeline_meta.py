from pathlib import Path
p=Path("run_publish.ps1")

s=p.read_text(encoding="utf-8")

line='python -m app.feeds.meta_shopify_feed'

if line not in s:
    s += "`n"+line

p.write_text(s,encoding="utf-8")

print("META FEED ADDED TO PIPELINE")
