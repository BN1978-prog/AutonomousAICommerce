import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(override=True)

from app.channels.ebay_gateway import (
    ebay_create_inventory_item,
    ebay_create_offer,
    ebay_publish_offer,
)

IMPORTS = Path("app/logs/imported_skus.json")
EBAY_LOG = Path("app/logs/ebay_published_skus.json")

published = {}
if EBAY_LOG.exists():
    published = json.loads(EBAY_LOG.read_text(encoding="utf-8"))

imports = json.loads(IMPORTS.read_text(encoding="utf-8"))

for sku, meta in imports.items():
    if not (sku.startswith("CJ") or sku.startswith("PET-BOWL")):
        continue

    if sku in published and published[sku].get("status") == "published":
        print(f"{sku}: already published")
        continue

    print(f"Preparing eBay inventory for {sku}")

    product = {
        "title": meta.get("title") or sku,
        "description": meta.get("description") or "AI selected CJdropshipping product.",
        "quantity": meta.get("inventory") or 10,
        "imageUrls": meta.get("imageUrls") or meta.get("images") or ["https://i.ebayimg.com/images/g/0yAAAOSwD9BlrQqA/s-l1600.jpg"],
        "aspects": {
            "Brand": ["Unbranded"],
            "Type": ["General"]
        }
    }

    inv = ebay_create_inventory_item(sku, product)
    print("INVENTORY:")
    print(json.dumps(inv, indent=2))

    if not inv.get("ok"):
        published[sku] = {"status": "inventory_failed", "response": inv}
        continue

    offer = ebay_create_offer(sku, 6.74, 10)

    if offer.get("ok"):
        offer_id = offer["response"]["offerId"]
    else:
        errors = offer.get("response", {}).get("errors", [])
        msg = errors[0].get("message", "") if errors else ""

        if "already exists" in msg.lower():
            offer_id = errors[0].get("parameters", [{}])[0].get("value")
        else:
            print(f"{sku}: offer failed")
            print(json.dumps(offer, indent=2))
            published[sku] = {"status": "offer_failed", "response": offer}
            continue

    from app.channels.ebay_gateway import ebay_headers, ebay_config
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
    print(json.dumps(result, indent=2))

    if result.get("ok"):
        listing_id = (
            result.get("response", {})
            .get("listingId")
        )

        imports[sku]["ebay_offer_id"] = offer_id
        imports[sku]["ebay_listing_id"] = listing_id
        imports[sku]["ebay_status"] = "published"

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
        )


    published[sku] = {
        "status": "published" if result.get("ok") else "publish_failed",
        "offer_id": offer_id,
        "response": result,
    }

EBAY_LOG.write_text(json.dumps(published, indent=2), encoding="utf-8")
print("DONE")
