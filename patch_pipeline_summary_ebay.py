from pathlib import Path

p=Path("app/pipeline_summary.py")
s=p.read_text(encoding="utf-8")

s=s.replace(
    'if meta.get("ebay_listing_id"):',
    'if meta.get("ebay_listing_id") or meta.get("ebay_status") == "published":'
)

p.write_text(s,encoding="utf-8")
print("pipeline summary eBay counter patched")
