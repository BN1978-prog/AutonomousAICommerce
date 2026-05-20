from pathlib import Path

p=Path("app/promotion_actions.py")
s=p.read_text(encoding="utf-8")

old='''    if item.get("ebay_listing_id") is None:
        sku_actions.append("verify_ebay_listing_id")'''

new='''    if (
        item.get("ebay_listing_id") is None
        and item.get("ebay_status") != "published"
    ):
        sku_actions.append("verify_ebay_listing_id")'''

s=s.replace(old,new)

p.write_text(
    s,
    encoding="utf-8"
)

print("promotion rule patched")
