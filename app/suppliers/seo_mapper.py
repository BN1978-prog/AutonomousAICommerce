def build_seo_tags(product):
    tags = []

    title = product.get("title", "").lower()
    vendor = product.get("vendor", "")

    if vendor:
        tags.append(vendor)

    if "premium" in title:
        tags.append("premium")

    if "smart" in title:
        tags.append("smart")

    if "portable" in title:
        tags.append("portable")

    tags.append("ai-selected")
    tags.append("draft-review")

    return list(dict.fromkeys(tags))

def detect_product_type(product):
    title = product.get("title", "").lower()

    if "led" in title:
        return "Lighting"

    if "usb" in title or "wireless" in title or "smart" in title:
        return "Electronics"

    return "General"
