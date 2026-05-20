import os
import base64
import requests


EBAY_API_BASE = os.getenv("EBAY_API_BASE", "https://api.ebay.com")
EBAY_TOKEN_URL = os.getenv("EBAY_TOKEN_URL", "https://api.ebay.com/identity/v1/oauth2/token")


def ebay_config():
    return {
        "client_id": os.getenv("EBAY_CLIENT_ID"),
        "client_secret": os.getenv("EBAY_CLIENT_SECRET"),
        "refresh_token": os.getenv("EBAY_REFRESH_TOKEN"),
        "marketplace_id": os.getenv("EBAY_MARKETPLACE_ID", "EBAY_GB"),
        "api_base": EBAY_API_BASE,
        "token_url": EBAY_TOKEN_URL
    }


def ebay_get_access_token():
    direct_token = os.getenv("EBAY_ACCESS_TOKEN")
    if direct_token:
        return {
            "ok": True,
            "access_token": direct_token,
            "expires_in": None,
            "token_type": "Bearer"
        }

    cfg = ebay_config()

    missing = [
        k for k, v in cfg.items()
        if k in ["client_id", "client_secret", "refresh_token"] and not v
    ]

    if missing:
        return {
            "ok": False,
            "missing": missing
        }

    raw = f"{cfg['client_id']}:{cfg['client_secret']}".encode("utf-8")
    basic = base64.b64encode(raw).decode("utf-8")

    r = requests.post(
        cfg["token_url"],
        headers={
            "Authorization": f"Basic {basic}",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data={
            "grant_type": "refresh_token",
            "refresh_token": cfg["refresh_token"],
            "scope": "https://api.ebay.com/oauth/api_scope/sell.inventory"
        },
        timeout=30
    )

    try:
        data = r.json()
    except Exception:
        data = {"raw": r.text}

    if r.status_code != 200:
        return {
            "ok": False,
            "status_code": r.status_code,
            "error": data
        }

    return {
        "ok": True,
        "access_token": data.get("access_token"),
        "expires_in": data.get("expires_in"),
        "token_type": data.get("token_type")
    }


def ebay_headers():
    token = ebay_get_access_token()

    if not token.get("ok"):
        return token

    return {
        "ok": True,
        "headers": {
            "Authorization": f"Bearer {token['access_token']}",
            "Content-Type": "application/json",
            "Content-Language": "en-GB",
            "X-EBAY-C-MARKETPLACE-ID": ebay_config()["marketplace_id"]
        }
    }


def ebay_live_check():
    token = ebay_get_access_token()

    if not token.get("ok"):
        return {
            "ok": False,
            "stage": "token",
            "result": token
        }

    return {
        "ok": True,
        "channel": "ebay",
        "configured": True,
        "token_type": token.get("token_type"),
        "expires_in": token.get("expires_in")
    }


def ebay_get_inventory_item(sku: str):
    h = ebay_headers()

    if not h.get("ok"):
        return h

    url = f"{ebay_config()['api_base']}/sell/inventory/v1/inventory_item/{sku}"

    r = requests.get(
        url,
        headers=h["headers"],
        timeout=30
    )

    try:
        data = r.json()
    except Exception:
        data = {"raw": r.text}

    if r.status_code == 404:
        return {
            "ok": False,
            "message": f"SKU {sku} not found on eBay",
            "status_code": 404
        }

    return {
        "ok": r.status_code == 200,
        "status_code": r.status_code,
        "sku": sku,
        "response": data
    }


def ebay_create_inventory_item(sku: str, product: dict) -> dict:
    h = ebay_headers()

    if not h.get("ok"):
        return h

    url = f"{ebay_config()['api_base']}/sell/inventory/v1/inventory_item/{sku}"

    payload = {
        "availability": {
            "shipToLocationAvailability": {
                "quantity": int(product.get("quantity", 1) or 1)
            }
        },
        "condition": "NEW",
        "product": {
            "title": (product.get("title") or product.get("name") or sku)[:80],
            "description": product.get("description") or product.get("short_description") or "Product",
            "aspects": product.get("aspects") or {},
            "imageUrls": product.get("imageUrls") or product.get("images") or []
        }
    }

    headers = h["headers"]
    headers["Content-Language"] = "en-US"
    headers["X-EBAY-C-MARKETPLACE-ID"] = "EBAY_US"

    r = requests.put(
        url,
        headers=headers,
        json=payload,
        timeout=30
    )

    try:
        data = r.json()
    except Exception:
        data = {"raw": r.text}

    return {
        "ok": r.status_code in [200, 201, 204],
        "status_code": r.status_code,
        "sku": sku,
        "payload": payload,
        "response": data
    }


def ebay_create_offer(sku: str, price: float, quantity: int = 1) -> dict:
    h = ebay_headers()

    if not h.get("ok"):
        return h

    url = f"{ebay_config()['api_base']}/sell/inventory/v1/offer"

    payload = {
        "sku": sku,
        "marketplaceId": ebay_config()["marketplace_id"],
        "format": "FIXED_PRICE",
        "availableQuantity": int(quantity),
        "pricingSummary": {
            "price": {
                "value": str(price),
                "currency": os.getenv("DEFAULT_CURRENCY", "USD")
            }
        },
        "listingDescription": "Non-slip silicone pet feeding bowl. AI selected product.",
        "categoryId": "20759",
        "merchantLocationKey": "default"
    }

    r = requests.post(
        url,
        headers=h["headers"],
        json=payload,
        timeout=30
    )

    try:
        data = r.json()
    except Exception:
        data = {"raw": r.text}

    return {
        "ok": r.status_code in [200, 201],
        "status_code": r.status_code,
        "sku": sku,
        "payload": payload,
        "response": data
    }


def ebay_create_location() -> dict:
    h = ebay_headers()

    if not h.get("ok"):
        return h

    url = f"{ebay_config()['api_base']}/sell/inventory/v1/location/default"

    payload = {
        "name": "Main Warehouse",
        "location": {
            "address": {
                "addressLine1": "1 Test Street",
                "city": "London",
                "postalCode": "SW1A1AA",
                "country": "GB"
            }
        },
        "locationTypes": ["WAREHOUSE"]
    }

    r = requests.post(
        url,
        headers=h["headers"],
        json=payload,
        timeout=30
    )

    try:
        data = r.json()
    except Exception:
        data = {"raw": r.text}

    return {
        "ok": r.status_code in [200,201,204],
        "status_code": r.status_code,
        "response": data
    }


def ebay_publish_offer(offer_id: str) -> dict:
    h = ebay_headers()

    if not h.get("ok"):
        return h

    url = f"{ebay_config()['api_base']}/sell/inventory/v1/offer/{offer_id}/publish"

    r = requests.post(
        url,
        headers=h["headers"],
        timeout=30
    )

    try:
        data = r.json()
    except Exception:
        data = {"raw": r.text}

    return {
        "ok": r.status_code in [200, 201],
        "status_code": r.status_code,
        "offer_id": offer_id,
        "response": data
    }



