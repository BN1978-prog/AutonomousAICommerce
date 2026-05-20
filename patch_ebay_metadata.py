from pathlib import Path

p=Path("app/publish_ebay_from_imports.py")
s=p.read_text(encoding="utf-8")

old='''    print("PUBLISH:")
    print(json.dumps(result, indent=2))'''

new='''    print("PUBLISH:")
    print(json.dumps(result, indent=2))

    if result.get("ok"):
        listing_id = (
            result.get("response", {})
            .get("listingId")
        )

        imports[sku]["ebay_offer_id"] = offer_id
        imports[sku]["ebay_listing_id"] = listing_id
        imports[sku]["ebay_status"] = "published"

        IMPORTS.write_text(
            json.dumps(imports, indent=2),
            encoding="utf-8"
        )
'''

s=s.replace(old,new)

p.write_text(s,encoding="utf-8")
print("eBay publish metadata patched")
