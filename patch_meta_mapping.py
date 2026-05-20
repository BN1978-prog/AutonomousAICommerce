from pathlib import Path

p=Path("app/feeds/meta_feed.py")
s=p.read_text(encoding="utf-8")

old = '''
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

        image_link = _first(
            p.get("image"),
            p.get("image_url"),
            p.get("featured_image"),
            default="https://picsum.photos/300"
        )
'''

new = '''
        title = _first(
            p.get("title"),
            p.get("product",{}).get("title"),
            p.get("shopify_title"),
            p.get("name"),
            p.get("product_title"),
            sku
        )

        description = _first(
            p.get("description"),
            p.get("product",{}).get("description"),
            p.get("body_html"),
            p.get("short_description"),
            p.get("bullets"),
            title
        )

        price = _first(
            p.get("dynamic_price"),
            p.get("price"),
            p.get("regular_price"),
            p.get("current_price"),
            default="0.00"
        )

        image_link = _first(
            p.get("image"),
            p.get("image_url"),
            p.get("featured_image"),
            (p.get("product",{}).get("imageUrls") or [None])[0],
            default="https://picsum.photos/300"
        )
'''

s=s.replace(old,new)

p.write_text(s,encoding="utf-8")
print("META MAPPING PATCHED")
