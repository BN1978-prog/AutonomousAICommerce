import os
import requests


def etsy_config():
    return {
        "api_base": os.getenv("ETSY_API_BASE", "https://openapi.etsy.com/v3/application").rstrip("/"),
        "api_key": os.getenv("ETSY_API_KEY") or os.getenv("ETSY_CLIENT_ID"),
        "access_token": os.getenv("ETSY_ACCESS_TOKEN"),
        "shop_id": os.getenv("ETSY_SHOP_ID"),
    }


def etsy_headers():
    cfg = etsy_config()

    if not cfg["api_key"] or not cfg["access_token"]:
        return {
            "ok": False,
            "status": "missing_etsy_auth",
            "missing": {
                "ETSY_API_KEY": not bool(cfg["api_key"]),
                "ETSY_ACCESS_TOKEN": not bool(cfg["access_token"])
            }
        }

    return {
        "ok": True,
        "headers": {
            "x-api-key": cfg["api_key"],
            "Authorization": "Bearer " + cfg["access_token"],
            "Content-Type": "application/x-www-form-urlencoded"
        }
    }


def etsy_create_draft_listing(product: dict) -> dict:
    cfg = etsy_config()
    h = etsy_headers()

    if not h.get("ok"):
        return h

    if not cfg["shop_id"]:
        return {
            "ok": False,
            "status": "missing_etsy_shop_id"
        }

    url = f"{cfg['api_base']}/shops/{cfg['shop_id']}/listings"

    title = (product.get("title") or product.get("name") or product.get("sku") or "Product")[:140]
    description = product.get("description") or title
    price = str(product.get("price") or "9.99")
    quantity = int(product.get("quantity") or product.get("inventory") or 10)

    payload = {
        "title": title,
        "description": description,
        "price": price,
        "quantity": quantity,
        "who_made": "i_did",
        "when_made": os.getenv("ETSY_WHEN_MADE", "2020_2025"),
        "taxonomy_id": int(os.getenv("ETSY_DEFAULT_TAXONOMY_ID", "1")),
        "type": "physical",
        "is_supply": "true",
        "state": "draft",
        "shipping_profile_id": os.getenv("ETSY_SHIPPING_PROFILE_ID", ""),
        "return_policy_id": os.getenv("ETSY_RETURN_POLICY_ID", "")
    }

    payload = {k: v for k, v in payload.items() if v not in ["", None]}

    r = requests.post(
        url,
        headers=h["headers"],
        data=payload,
        timeout=30
    )

    try:
        data = r.json()
    except Exception:
        data = {"raw": r.text}

    status = "etsy_create_draft_listing_failed"
    if r.status_code in [200, 201]:
        status = "etsy_draft_listing_created"
    elif isinstance(data, dict) and "readiness_state_id" in str(data):
        status = "blocked_by_shop_readiness_state"

    return {
        "ok": r.status_code in [200, 201],
        "status": status,
        "status_code": r.status_code,
        "mode": "etsy_create_draft_listing",
        "sku": product.get("sku"),
        "payload": payload,
        "listing_id": data.get("listing_id") or data.get("listingId") or data.get("id"),
        "response": data
    }
