import json
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring


def _load_json_files():
    products = []

    folders = [
        Path("data/published_products"),
        Path("data/products"),
        Path("data/catalog"),
        Path("app/logs")
    ]

    for folder in folders:
        if not folder.exists():
            continue

        for file in folder.glob("*.json"):
            try:
                data = json.loads(file.read_text(encoding="utf-8"))

                if isinstance(data, list):
                    products.extend([x for x in data if isinstance(x, dict)])

                elif isinstance(data, dict):
                    # imported_skus.json style: {"SKU": {"product_id": ...}}
                    if all(isinstance(v, dict) for v in data.values()):
                        for sku, meta in data.items():
                            item = dict(meta)
                            item.setdefault("sku", sku)
                            products.append(item)
                    else:
                        products.append(data)
            except Exception:
                pass

    return products


def _first(*values, default=""):
    for value in values:
        if value not in [None, "", []]:
            return value
    return default


def generate_meta_products_xml():
    products = _load_json_files()

    rss = Element("rss", {
        "version": "2.0",
        "xmlns:g": "http://base.google.com/ns/1.0"
    })

    channel = SubElement(rss, "channel")
    SubElement(channel, "title").text = "AICommerce Global Feed"
    SubElement(channel, "link").text = "https://aicommerce9.wpcomstaging.com"
    SubElement(channel, "description").text = "AICommerce Global automated product feed"

    seen = set()

    for p in products:
        sku = _first(
            p.get("sku"),
            p.get("id"),
            p.get("product_id"),
            p.get("handle")
        )

        if not sku or sku in seen:
            continue

        seen.add(sku)

        title = _first(
            p.get("title"),
            p.get("name"),
            p.get("product_title"),
            sku
        )

        description = _first(
            p.get("description"),
            p.get("body_html"),
            p.get("short_description"),
            title
        )

        price = _first(
            p.get("price"),
            p.get("regular_price"),
            p.get("current_price"),
            default="0.00"
        )

        inventory = _first(
            p.get("inventory"),
            p.get("inventory_quantity"),
            p.get("stock_quantity"),
            p.get("current_inventory"),
            default=1
        )

        try:
            availability = "in stock" if int(float(inventory)) > 0 else "out of stock"
        except Exception:
            availability = "in stock"

        link = _first(
            p.get("permalink"),
            p.get("url"),
            p.get("product_url"),
            default="https://aicommerce9.wpcomstaging.com"
        )

        image_link = _first(
            p.get("image"),
            p.get("image_url"),
            p.get("featured_image"),
            default="https://picsum.photos/300"
        )

        item = SubElement(channel, "item")
        SubElement(item, "g:id").text = str(sku)
        SubElement(item, "g:title").text = str(title)
        SubElement(item, "g:description").text = str(description)
        SubElement(item, "g:link").text = str(link)
        SubElement(item, "g:image_link").text = str(image_link)
        SubElement(item, "g:availability").text = availability
        SubElement(item, "g:condition").text = "new"
        SubElement(item, "g:price").text = f"{price} GBP"
        SubElement(item, "g:brand").text = "AICommerce Global"

    return tostring(rss, encoding="utf-8", xml_declaration=True)


def main():
    out_dir = Path("data/catalog")
    out_dir.mkdir(parents=True, exist_ok=True)

    xml = generate_meta_products_xml()
    out = out_dir / "meta-products.xml"
    out.write_bytes(xml)

    print("META FEED GENERATED:", out)
    print("SIZE:", out.stat().st_size)


if __name__ == "__main__":
    main()
