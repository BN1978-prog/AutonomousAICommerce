from pathlib import Path

p = Path("app/channels/ebay_gateway.py")
s = p.read_text(encoding="utf-8")

s = s.replace(
    '"title": product.get("title") or product.get("name") or sku,',
    '"title": (product.get("title") or product.get("name") or sku)[:80],'
)

p.write_text(s, encoding="utf-8")
print("eBay title length patched")
