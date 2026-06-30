
import json
import os
import requests
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv

from app.channels.ebay_gateway import (
    ebay_create_inventory_item,
    ebay_create_offer,
    ebay_publish_offer,
)

load_dotenv()

DRAFTS = Path("app/logs/universal_listing_drafts.json")
REGISTRY = Path("app/logs/imported_skus.json")
OUT = Path("app/logs/universal_publisher.json")

PUBLISH_MODE = os.getenv("UNIVERSAL_PUBLISH_MODE", "DRY_RUN").upper()
CHANNELS = [x.strip().lower() for x in os.getenv("UNIVERSAL_PUBLISH_CHANNELS", "shopify").split(",") if x.strip()]

SHOPIFY_STORE_URL = os.getenv("SHOPIFY_STORE_URL", "").strip().rstrip("/")
SHOPIFY_TOKEN = (
    os.getenv("SHOPIFY_ACCESS_TOKEN")
    or os.getenv("SHOPIFY_ADMIN_TOKEN")
    or os.getenv("SHOPIFY_ADMIN_ACCESS_TOKEN")
    or ""
).strip()
SHOPIFY_API_VERSION = os.getenv("SHOPIFY_API_VERSION", "2025-01").strip()

def shopify_publish_draft(sku, payload):
    if not SHOPIFY_STORE_URL or not SHOPIFY_TOKEN:
        return {
            "ok": False,
            "status": "missing_shopify_env"
        }

    url = f"{SHOPIFY_STORE_URL}/admin/api/{SHOPIFY_API_VERSION}/products.json"
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_TOKEN,
        "Content-Type": "application/json"
    }

    product = {
        "product": {
            "title": payload.get("title"),
            "body_html": payload.get("body_html", ""),
            "vendor": payload.get("vendor", "AICommerce"),
            "product_type": payload.get("product_type", "General"),
            "status": "draft",
            "tags": payload.get("tags", ""),
            "variants": payload.get("variants", []),
            "images": payload.get("images", [])
        }
    }

    r = requests.post(url, headers=headers, json=product, timeout=30)

    try:
        data = r.json()
    except Exception:
        data = {"text": r.text[:2000]}

    ok = 200 <= r.status_code < 300 and data.get("product")

    return {
        "ok": ok,
        "status": "published_draft" if ok else "api_error",
        "status_code": r.status_code,
        "response": data
    }


def ebay_publish_listing(sku, payload, item=None):
    item = item or {}

    images = [
        img.get("src") if isinstance(img, dict) else img
        for img in (payload.get("images") or [])
        if img
    ]

    if not images:
        images = [
            img.get("src") if isinstance(img, dict) else img
            for img in (item.get("images") or item.get("imageUrls") or [])
            if img
        ]

    if not images and item.get("image"):
        images = [item.get("image")]

    product = {
        "title": payload.get("title") or item.get("title") or sku,
        "description": payload.get("body_html") or item.get("description") or item.get("title") or "Product",
        "quantity": 10,
        "imageUrls": images,
        "aspects": {
            "Brand": ["Unbranded"],
            "Type": ["General"]
        }
    }

    inv = ebay_create_inventory_item(sku, product)

    if not inv.get("ok"):
        return {
            "ok": False,
            "status": "inventory_failed",
            "response": inv
        }

    variants = payload.get("variants") or [{}]
    price = float(variants[0].get("price") or payload.get("price") or 0)

    offer = ebay_create_offer(sku=sku, price=price, quantity=10)

    if not offer.get("ok"):
        errors = (offer.get("response") or {}).get("errors") or []
        msg = errors[0].get("message", "") if errors else ""
        existing_offer_id = None

        if "already exists" in msg.lower():
            for param in errors[0].get("parameters", []):
                if param.get("name") == "offerId":
                    existing_offer_id = param.get("value")
                    break

        if existing_offer_id:
            offer_id = existing_offer_id
        else:
            return {
                "ok": False,
                "status": "offer_failed",
                "response": offer
            }
    else:
        offer_id = offer["response"].get("offerId")

    try:
        from app.channels.ebay_gateway import ebay_headers, ebay_config
        import requests

        h = ebay_headers()
        cfg = ebay_config()

        if h.get("ok") and offer_id:
            get_offer = requests.get(
                cfg["api_base"] + "/sell/inventory/v1/offer/" + str(offer_id),
                headers=h["headers"],
                timeout=30
            )

            if get_offer.status_code == 200:
                offer_data = get_offer.json()
                offer_data.setdefault("listingPolicies", {})
                offer_data["listingPolicies"]["fulfillmentPolicyId"] = os.getenv(
                    "EBAY_FULFILLMENT_POLICY_ID",
                    "394964752023"
                )

                requests.put(
                    cfg["api_base"] + "/sell/inventory/v1/offer/" + str(offer_id),
                    headers=h["headers"],
                    json=offer_data,
                    timeout=30
                )
    except Exception:
        pass

    try:
        from app.channels.ebay_gateway import ebay_headers, ebay_config
        import requests

        h = ebay_headers()
        cfg = ebay_config()

        if h.get("ok") and offer_id:
            get_offer = requests.get(
                cfg["api_base"] + "/sell/inventory/v1/offer/" + str(offer_id),
                headers=h["headers"],
                timeout=30
            )

            if get_offer.status_code == 200:
                offer_data = get_offer.json()
                offer_data.setdefault("listingPolicies", {})
                offer_data["listingPolicies"]["fulfillmentPolicyId"] = os.getenv(
                    "EBAY_FULFILLMENT_POLICY_ID",
                    "394964752023"
                )

                requests.put(
                    cfg["api_base"] + "/sell/inventory/v1/offer/" + str(offer_id),
                    headers=h["headers"],
                    json=offer_data,
                    timeout=30
                )
    except Exception:
        pass

    publish = ebay_publish_offer(offer_id)

    return {
        "ok": publish.get("ok"),
        "status": "published" if publish.get("ok") else "publish_failed",
        "offer_id": offer_id,
        "response": publish.get("response"),
        "publish": publish
    }


def main():
    drafts = json.loads(DRAFTS.read_text(encoding="utf-8-sig")) if DRAFTS.exists() else {}
    registry = json.loads(REGISTRY.read_text(encoding="utf-8-sig")) if REGISTRY.exists() else {}

    results = []

    for sku, draft in drafts.items():
        item = registry.get(sku, {})
        channels = draft.get("publish_targets", {})
        marketplace_payloads = draft.get("marketplace_payloads", {})

        row = {
            "sku": sku,
            "mode": PUBLISH_MODE,
            "status": "planned",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "title": draft.get("title"),
            "price": draft.get("price"),
            "channels": {}
        }

        for channel, enabled in channels.items():
            if channel not in CHANNELS and PUBLISH_MODE != "DRY_RUN":
                row["channels"][channel] = {
                    "enabled": enabled,
                    "status": "skipped_channel_not_enabled"
                }
                continue

            if not enabled:
                row["channels"][channel] = {
                    "enabled": False,
                    "status": "skipped_disabled"
                }
                continue

            payload = marketplace_payloads.get(channel)
            if not payload:
                row["channels"][channel] = {
                    "enabled": True,
                    "status": "missing_payload"
                }
                continue

            already = (item.get("channels") or {}).get(channel) or {}
            if already.get("product_id") or already.get("listing_id") or already.get("offer_id"):
                row["channels"][channel] = {
                    "enabled": True,
                    "status": "skipped_already_exists",
                    "existing": already
                }
                continue

            if PUBLISH_MODE == "DRY_RUN":
                row["channels"][channel] = {
                    "enabled": True,
                    "status": "ready_for_publish",
                    "payload_preview": payload
                }
                continue

            if PUBLISH_MODE == "LIVE" and channel == "shopify":
                result = shopify_publish_draft(sku, payload)
                row["channels"][channel] = result

                if result.get("ok"):
                    product = result["response"]["product"]
                    item.setdefault("channels", {}).setdefault("shopify", {})
                    item["channels"]["shopify"]["product_id"] = product.get("id")
                    item["channels"]["shopify"]["product_url"] = None
                    item["channels"]["shopify"]["status"] = "draft"
                    item["channels"]["shopify"]["published_at"] = datetime.now(timezone.utc).isoformat()
                    item["product_id"] = product.get("id")
                    item["status"] = "shopify_draft_created"
                continue

            if PUBLISH_MODE == "LIVE" and channel == "ebay":
                result = ebay_publish_listing(sku, payload, item)
                row["channels"][channel] = result

                if result.get("ok"):
                    item.setdefault("channels", {}).setdefault("ebay", {})
                    item["channels"]["ebay"]["offer_id"] = result.get("offer_id")
                    item["channels"]["ebay"]["status"] = "published"
                    item["channels"]["ebay"]["published_at"] = datetime.now(timezone.utc).isoformat()
                    item["ebay_offer_id"] = result.get("offer_id")
                    item["ebay_status"] = "published"

                continue

            row["channels"][channel] = {
                "enabled": True,
                "status": "live_not_implemented_for_channel"
            }

        results.append(row)

    REGISTRY.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")

    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "UNIVERSAL_PUBLISHER_" + PUBLISH_MODE,
        "mode": PUBLISH_MODE,
        "enabled_channels": CHANNELS,
        "drafts": len(drafts),
        "results": results,
        "note": "LIVE mode currently supports Shopify draft publishing and eBay publishing via Inventory API."
    }

    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    output = json.dumps(report, indent=2, ensure_ascii=False)

    try:
        print(output)
    except UnicodeEncodeError:
        print(output.encode("ascii", errors="backslashreplace").decode("ascii"))


if __name__ == "__main__":
    main()
