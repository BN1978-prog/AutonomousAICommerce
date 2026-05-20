from pathlib import Path

p=Path("app/publish_ebay_from_imports.py")
s=p.read_text(encoding="utf-8")

old='''        imports[sku]["ebay_status"] = "published"

        IMPORTS.write_text(
            json.dumps(imports, indent=2),
            encoding="utf-8"
        )'''

new='''        imports[sku]["ebay_status"] = "published"

        published[sku] = {
            "offer_id": offer_id,
            "listing_id": listing_id
        }

        IMPORTS.write_text(
            json.dumps(imports, indent=2),
            encoding="utf-8"
        )

        EBAY_LOG.write_text(
            json.dumps(published, indent=2),
            encoding="utf-8"
        )'''

s=s.replace(old,new)

p.write_text(s,encoding="utf-8")
print("EBAY LOGGING PATCHED")
