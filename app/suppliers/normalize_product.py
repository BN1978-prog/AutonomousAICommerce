from app.suppliers.pricing import apply_pricing_rules
from app.suppliers.listing_optimizer import optimize_listing_text
from app.seo_optimizer import shopify_title, bullet_points, seo_tags


def _first_price(value):
    if value is None:
        return None
    text = str(value).replace("--", " ").replace("-", " ")
    parts = []
    for x in text.split():
        try:
            parts.append(float(x))
        except Exception:
            pass
    return parts[0] if parts else None


def normalize_supplier_product(raw):
    sku = raw.get("sku") or raw.get("productSku") or raw.get("pid")
    title = raw.get("title") or raw.get("productNameEn") or raw.get("productName")
    description = raw.get("description") or raw.get("remark") or title
    image = raw.get("image") or raw.get("productImage")
    vendor = raw.get("vendor") or raw.get("supplierName") or "CJdropshipping"

    price = raw.get("price")
    if price is None:
        price = _first_price(raw.get("sellPrice"))

    if not sku or not title or price is None:
        raise ValueError("Invalid supplier product: missing sku/title/price")

    price = float(price)
    sell_price = apply_pricing_rules(price)

    optimized = optimize_listing_text({
        "title": title,
        "description": description,
        "vendor": vendor,
        "bullets": bullet_points({**raw, "raw": raw, "vendor": vendor}),
        "seo_tags": seo_tags({**raw, "raw": raw, "vendor": vendor}),
    })

    return {
        "sku": sku,
        "title": shopify_title(optimized.get("title", title)),
        "description": optimized.get("description", description),
        "vendor": vendor,
        "bullets": bullet_points({**raw, "raw": raw, "vendor": vendor}),
        "seo_tags": seo_tags({**raw, "raw": raw, "vendor": vendor}),
        "cost": price,
        "price": sell_price,
        "image": image,
        "inventory": int(raw.get("inventory") or raw.get("stock") or raw.get("listedNum") or 10),
        "raw": raw,
    }
