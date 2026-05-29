import json
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring

SHOP_URL = "https://aicommerce9.wpcomstaging.com"
DRAFTS = Path("app/logs/shopify_drafts")
OUT = Path("data/catalog/meta-products.xml")


def get_product(data):
    return data.get("result", {}).get("response", {}).get("product", {})


def get_first_variant(product):
    variants = product.get("variants", [])
    return variants[0] if variants and isinstance(variants[0], dict) else {}


def get_image(product):
    image = product.get("image")
    if isinstance(image, dict) and image.get("src"):
        return image["src"]

    images = product.get("images", [])
    if images and isinstance(images[0], dict) and images[0].get("src"):
        return images[0]["src"]

    return ""


def valid_price(price):
    try:
        return float(price) > 0
    except Exception:
        return False


def generate_meta_products_xml():
    rss = Element("rss", {
        "version": "2.0",
        "xmlns:g": "http://base.google.com/ns/1.0"
    })

    channel = SubElement(rss, "channel")
    SubElement(channel, "title").text = "AICommerce Shopify Feed"
    SubElement(channel, "link").text = SHOP_URL
    SubElement(channel, "description").text = "AICommerce Shopify product feed for Meta Commerce"

    seen = set()

    for file in sorted(DRAFTS.glob("*.json")):
        try:
            data = json.loads(file.read_text(encoding="utf-8-sig"))
        except Exception:
            continue

        product = get_product(data)
        if not product:
            continue

        variant = get_first_variant(product)
        sku = variant.get("sku")
        title = product.get("title")
        description = product.get("body_html") or title
        handle = product.get("handle")
        price = variant.get("price")
        inventory = variant.get("inventory_quantity", 1)
        image = get_image(product)

        if not sku or sku in seen:
            continue
        if not title or not handle:
            continue
        if not valid_price(price):
            continue
        if not image or "picsum.photos" in image or "example.com" in image:
            continue

        seen.add(sku)

        try:
            availability = "in stock" if int(float(inventory)) > 0 else "out of stock"
        except Exception:
            availability = "in stock"

        item = SubElement(channel, "item")
        SubElement(item, "g:id").text = str(sku)
        SubElement(item, "g:title").text = str(title)
        SubElement(item, "g:description").text = str(description)
        SubElement(item, "g:link").text = f"{SHOP_URL}/products/{handle}"
        SubElement(item, "g:image_link").text = str(image)
        SubElement(item, "g:availability").text = availability
        SubElement(item, "g:condition").text = "new"
        SubElement(item, "g:price").text = f"{price} GBP"
        SubElement(item, "g:brand").text = product.get("vendor") or "AICommerce Global"

    return tostring(rss, encoding="utf-8", xml_declaration=True)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    xml = generate_meta_products_xml()
    OUT.write_bytes(xml)
    print("META FEED GENERATED:", OUT)
    print("SIZE:", OUT.stat().st_size)


if __name__ == "__main__":
    main()
