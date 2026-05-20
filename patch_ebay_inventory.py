from pathlib import Path

p = Path("app/channels/ebay_gateway.py")
s = p.read_text(encoding="utf-8")

insert = '''

def ebay_create_inventory_item(sku, title, image_url):
    from app.channels.ebay_gateway import ebay_headers, ebay_config
    import requests

    h = ebay_headers()
    cfg = ebay_config()

    headers = h["headers"]
    headers["Content-Language"] = "en-US"
    headers["X-EBAY-C-MARKETPLACE-ID"] = "EBAY_US"

    payload = {
        "product": {
            "title": title,
            "description": title,
            "imageUrls": [image_url],
            "aspects": {
                "Type": ["General"],
                "Brand": ["Unbranded"]
            }
        },
        "condition": "NEW",
        "availability": {
            "shipToLocationAvailability": {
                "quantity": 10
            }
        }
    }

    r = requests.put(
        cfg["api_base"] + "/sell/inventory/v1/inventory_item/" + sku,
        headers=headers,
        json=payload
    )

    return {
        "ok": r.status_code in [200, 201, 204],
        "status_code": r.status_code,
        "response": r.json() if r.text else {}
    }
'''

if "def ebay_create_inventory_item" not in s:
    s = s + insert

p.write_text(s, encoding="utf-8")
print("ebay_create_inventory_item added")
