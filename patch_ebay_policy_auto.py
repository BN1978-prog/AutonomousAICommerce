from pathlib import Path

p = Path("app/publish_ebay_from_imports.py")
s = p.read_text(encoding="utf-8")

old = '''    result = ebay_publish_offer(offer_id)
    print("PUBLISH:")
    print(json.dumps(result, indent=2))'''

new = '''    from app.channels.ebay_gateway import ebay_headers, ebay_config
    import requests

    h = ebay_headers()
    cfg = ebay_config()

    r = requests.get(
        cfg["api_base"] + "/sell/inventory/v1/offer/" + offer_id,
        headers=h["headers"],
        timeout=30
    )

    offer_data = r.json()
    offer_data.setdefault("listingPolicies", {})
    offer_data["listingPolicies"]["fulfillmentPolicyId"] = "394964752023"

    u = requests.put(
        cfg["api_base"] + "/sell/inventory/v1/offer/" + offer_id,
        headers=h["headers"],
        json=offer_data,
        timeout=30
    )

    print("POLICY UPDATE:", u.status_code)
    if u.text:
        print(u.text)

    result = ebay_publish_offer(offer_id)
    print("PUBLISH:")
    print(json.dumps(result, indent=2))'''

s = s.replace(old, new)

p.write_text(s, encoding="utf-8")
print("fulfillment policy auto-attach patched")
