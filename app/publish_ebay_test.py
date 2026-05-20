from dotenv import load_dotenv
load_dotenv(override=True)

import json
from app.channels.ebay_gateway import ebay_create_offer, ebay_publish_offer

SKU = "PET-BOWL-001-US"

offer = ebay_create_offer(SKU, 12.70, 50)

if offer.get("ok"):
    offer_id = offer["response"]["offerId"]

    published = ebay_publish_offer(offer_id)

    print("PUBLISHED:")
    print(json.dumps(published, indent=2))

else:
    errors = offer.get("response", {}).get("errors", [])

    if errors and "already exists" in errors[0].get("message", "").lower():
        print("Offer already exists - skipping")
    else:
        print(json.dumps(offer, indent=2))
