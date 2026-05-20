import os
import requests


def woocommerce_live_check():
    store = os.getenv("WOOCOMMERCE_STORE_URL", "").rstrip("/")
    consumer_key = os.getenv("WOOCOMMERCE_CONSUMER_KEY")
    consumer_secret = os.getenv("WOOCOMMERCE_CONSUMER_SECRET")

    if not store or not consumer_key or not consumer_secret:
        return {
            "ok": False,
            "status": "not_configured",
            "missing": {
                "WOOCOMMERCE_STORE_URL": not bool(store),
                "WOOCOMMERCE_CONSUMER_KEY": not bool(consumer_key),
                "WOOCOMMERCE_CONSUMER_SECRET": not bool(consumer_secret)
            }
        }

    url = f"{store}/wp-json/wc/v3/system_status"

    try:
        r = requests.get(
            url,
            auth=(consumer_key, consumer_secret),
            timeout=30
        )

        data = r.json()

        return {
            "ok": r.status_code == 200,
            "status_code": r.status_code,
            "store": store,
            "woocommerce": data
        }

    except Exception as e:
        return {
            "ok": False,
            "store": store,
            "error": str(e)
        }
import os
import requests


def wc_config():
    return {
        "store": os.getenv("WOOCOMMERCE_STORE_URL", "").rstrip("/"),
        "key": os.getenv("WOOCOMMERCE_CONSUMER_KEY"),
        "secret": os.getenv("WOOCOMMERCE_CONSUMER_SECRET")
    }


def wc_publish_product(product: dict) -> dict:
    cfg = wc_config()

    url = f"{cfg['store']}/wp-json/wc/v3/products"

    payload = {
        "name": product.get("title") or product.get("name"),
        "type": "simple",
        "regular_price": str(product.get("price", "0")),
        "description": product.get("description", ""),
        "short_description": product.get("short_description", product.get("description", "")),
        "sku": product.get("sku"),
        "manage_stock": True,
        "stock_quantity": int(product.get("inventory", 0)),
        "status": product.get("status", "draft")
    }

    r = requests.post(
        url,
        auth=(cfg["key"], cfg["secret"]),
        json=payload,
        timeout=30
    )

    data = r.json()

    return {
        "ok": r.status_code in [200, 201],
        "status_code": r.status_code,
        "mode": "woocommerce_publish_product",
        "sku": product.get("sku"),
        "product_id": data.get("id"),
        "response": data
    }
import os
import requests


def wc_config():
    return {
        "store": os.getenv("WOOCOMMERCE_STORE_URL", "").rstrip("/"),
        "key": os.getenv("WOOCOMMERCE_CONSUMER_KEY"),
        "secret": os.getenv("WOOCOMMERCE_CONSUMER_SECRET")
    }


def wc_publish_product(product: dict) -> dict:
    cfg = wc_config()

    url = f"{cfg['store']}/wp-json/wc/v3/products"

    payload = {
        "name": product.get("title") or product.get("name"),
        "type": "simple",
        "regular_price": str(product.get("price", "0")),
        "description": product.get("description", ""),
        "short_description": product.get("short_description", product.get("description", "")),
        "sku": product.get("sku"),
        "manage_stock": True,
        "stock_quantity": int(product.get("inventory", 0)),
        "status": product.get("status", "draft")
    }

    r = requests.post(
        url,
        auth=(cfg["key"], cfg["secret"]),
        json=payload,
        timeout=30
    )

    data = r.json()

    return {
        "ok": r.status_code in [200, 201],
        "status_code": r.status_code,
        "mode": "woocommerce_publish_product",
        "sku": product.get("sku"),
        "product_id": data.get("id"),
        "response": data
    }

def wc_find_product_by_sku(sku: str) -> dict:
    cfg = wc_config()
    url = f"{cfg['store']}/wp-json/wc/v3/products"

    r = requests.get(
        url,
        auth=(cfg["key"], cfg["secret"]),
        params={"sku": sku},
        timeout=30
    )

    data = r.json()

    if r.status_code != 200:
        return {
            "ok": False,
            "status_code": r.status_code,
            "error": data
        }

    if not data:
        return {
            "ok": False,
            "message": f"SKU {sku} not found"
        }

    product = data[0]

    return {
        "ok": True,
        "product": product,
        "product_id": product.get("id")
    }


def wc_update_price(sku: str, price: float) -> dict:
    found = wc_find_product_by_sku(sku)

    if not found.get("ok"):
        return found

    cfg = wc_config()
    product_id = found["product_id"]
    url = f"{cfg['store']}/wp-json/wc/v3/products/{product_id}"

    r = requests.put(
        url,
        auth=(cfg["key"], cfg["secret"]),
        json={
            "regular_price": str(price)
        },
        timeout=30
    )

    data = r.json()

    return {
        "ok": r.status_code in [200, 201],
        "status_code": r.status_code,
        "mode": "woocommerce_update_price",
        "sku": sku,
        "product_id": product_id,
        "price": price,
        "response": data
    }


def wc_update_inventory(sku: str, quantity: int) -> dict:
    found = wc_find_product_by_sku(sku)

    if not found.get("ok"):
        return found

    cfg = wc_config()
    product_id = found["product_id"]
    url = f"{cfg['store']}/wp-json/wc/v3/products/{product_id}"

    r = requests.put(
        url,
        auth=(cfg["key"], cfg["secret"]),
        json={
            "manage_stock": True,
            "stock_quantity": int(quantity),
            "stock_status": "instock" if int(quantity) > 0 else "outofstock"
        },
        timeout=30
    )

    data = r.json()

    return {
        "ok": r.status_code in [200, 201],
        "status_code": r.status_code,
        "mode": "woocommerce_update_inventory",
        "sku": sku,
        "product_id": product_id,
        "quantity": int(quantity),
        "response": data
    }


def wc_archive_product(sku: str) -> dict:
    found = wc_find_product_by_sku(sku)

    if not found.get("ok"):
        return found

    cfg = wc_config()
    product_id = found["product_id"]
    url = f"{cfg['store']}/wp-json/wc/v3/products/{product_id}"

    r = requests.put(
        url,
        auth=(cfg["key"], cfg["secret"]),
        json={
            "status": "draft"
        },
        timeout=30
    )

    data = r.json()

    return {
        "ok": r.status_code in [200, 201],
        "status_code": r.status_code,
        "mode": "woocommerce_archive_product",
        "sku": sku,
        "product_id": product_id,
        "status": "draft",
        "response": data
    }


def wc_get_products(limit: int = 10) -> dict:
    cfg = wc_config()

    if not cfg["store"] or not cfg["key"] or not cfg["secret"]:
        return {
            "ok": False,
            "status": "not_configured"
        }

    url = f"{cfg['store']}/wp-json/wc/v3/products"

    r = requests.get(
        url,
        auth=(cfg["key"], cfg["secret"]),
        params={"per_page": limit},
        timeout=30
    )

    try:
        data = r.json()
    except Exception:
        data = {"raw": r.text}

    return {
        "ok": r.status_code == 200,
        "status_code": r.status_code,
        "count": len(data) if isinstance(data, list) else 0,
        "products": data
    }

