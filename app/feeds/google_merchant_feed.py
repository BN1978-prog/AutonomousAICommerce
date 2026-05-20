from dotenv import load_dotenv
load_dotenv(override=True)

import os, json, html
import requests
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring

from app.channels.shopify_config import ShopifyConfig

store = ShopifyConfig.get_store().replace("https://","").replace("http://","").rstrip("/")
token = ShopifyConfig.get_token()

headers = {"X-Shopify-Access-Token": token}

imports = json.loads(Path("app/logs/imported_skus.json").read_text(encoding="utf-8"))

rss = Element("rss", {
    "version": "2.0",
    "xmlns:g": "http://base.google.com/ns/1.0"
})

channel = SubElement(rss, "channel")
SubElement(channel, "title").text = "AICommerce Global Feed"
SubElement(channel, "link").text = f"https://{store}"
SubElement(channel, "description").text = "AICommerce Global Shopify product feed"

count = 0

for sku, meta in imports.items():
    product_id = meta.get("product_id")
    if not product_id:
        continue

    url = f"https://{store}/admin/api/2024-01/products/{product_id}.json"
    r = None

    for attempt in range(3):
        try:
            r = requests.get(url, headers=headers, timeout=15)
            break
        except requests.exceptions.RequestException as e:
            print("RETRY", sku, attempt + 1, str(e)[:120])

    if r is None:
        print("SKIP", sku, "timeout")
        continue

    if r.status_code != 200:
        print("SKIP", sku, r.status_code)
        continue

    product = r.json().get("product", {})
    variants = product.get("variants", [])
    images = product.get("images", [])

    variant = variants[0] if variants else {}
    image = images[0].get("src") if images else "https://picsum.photos/300"

    price = variant.get("price") or meta.get("last_price") or "0.00"
    inventory = variant.get("inventory_quantity", 1)

    try:
        availability = "in stock" if int(inventory) > 0 else "out of stock"
    except Exception:
        availability = "in stock"

    item = SubElement(channel, "item")
    SubElement(item, "g:id").text = sku
    SubElement(item, "g:title").text = product.get("title") or sku
    SubElement(item, "g:description").text = html.unescape(product.get("body_html") or product.get("title") or sku)
    SubElement(item, "g:link").text = f"https://{store}/products/{product.get('handle','')}"
    SubElement(item, "g:image_link").text = image
    SubElement(item, "g:availability").text = availability
    SubElement(item, "g:condition").text = "new"
    SubElement(item, "g:price").text = f"{price} GBP"
    SubElement(item, "g:brand").text = product.get("vendor") or "AICommerce Global"

    count += 1

out_dir = Path("data/catalog")
out_dir.mkdir(parents=True, exist_ok=True)

out = out_dir / "google-merchant-products.xml"
out.write_bytes(tostring(rss, encoding="utf-8", xml_declaration=True))

print("GOOGLE MERCHANT FEED GENERATED:", out)
print("PRODUCTS:", count)
print("SIZE:", out.stat().st_size)
