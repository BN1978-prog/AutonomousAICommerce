from app.suppliers.seo_mapper import build_seo_tags, detect_product_type

def to_shopify_product_payload(product):
    shopify_product = {
        "title": product["title"],
        "body_html": product["description"],
        "vendor": product["vendor"],
        "product_type": detect_product_type(product),
        "tags": ", ".join(build_seo_tags(product)),
        "status": "draft",
        "variants": [
            {
                "sku": product["sku"],
                "price": product["price"],
                "inventory_quantity": product["inventory"]
            }
        ]
    }

    if product.get("image"):
        shopify_product["images"] = [
            {
                "src": product["image"]
            }
        ]

    return {
        "product": shopify_product
    }
