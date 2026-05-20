from pathlib import Path

src = Path("app/feeds/meta_shopify_feed.py")
dst = Path("app/feeds/google_merchant_feed.py")

s = src.read_text(encoding="utf-8")

s = s.replace(
    'out = out_dir / "meta-products-shopify.xml"',
    'out = out_dir / "google-merchant-products.xml"'
)

s = s.replace(
    'META SHOPIFY FEED GENERATED:',
    'GOOGLE MERCHANT FEED GENERATED:'
)

dst.write_text(s, encoding="utf-8")

print("google merchant feed created")
