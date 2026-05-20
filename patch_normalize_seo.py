from pathlib import Path

p = Path("app/suppliers/normalize_product.py")
s = p.read_text(encoding="utf-8")

if "from app.seo_optimizer import" not in s:
    s = s.replace(
        "from app.suppliers.listing_optimizer import optimize_listing_text",
        "from app.suppliers.listing_optimizer import optimize_listing_text\nfrom app.seo_optimizer import shopify_title, bullet_points, seo_tags"
    )

s = s.replace(
    '"title": optimized.get("title", title),',
    '"title": shopify_title(optimized.get("title", title)),'
)

s = s.replace(
    '"vendor": vendor,',
    '"vendor": vendor,\n        "bullets": bullet_points({**raw, "raw": raw, "vendor": vendor}),\n        "seo_tags": seo_tags({**raw, "raw": raw, "vendor": vendor}),'
)

p.write_text(s, encoding="utf-8")
print("normalize_product SEO patched")
