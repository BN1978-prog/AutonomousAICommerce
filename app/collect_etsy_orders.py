import json
import os
import re
import requests
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv(override=True)

OUT = Path("app/logs/etsy_orders.json")
ENV = Path(".env")

def clean(v):
    return str(v or "").replace("\r", "").replace("\n", "").strip()

def refresh_etsy_token():
    client_id = clean(os.getenv("ETSY_CLIENT_ID") or os.getenv("ETSY_API_KEY"))
    refresh_token = clean(os.getenv("ETSY_REFRESH_TOKEN"))

    if not client_id or not refresh_token:
        return {"ok": False, "status": "missing_refresh_config"}

    r = requests.post(
        "https://api.etsy.com/v3/public/oauth/token",
        data={
            "grant_type": "refresh_token",
            "client_id": client_id,
            "refresh_token": refresh_token
        },
        timeout=30
    )

    try:
        data = r.json()
    except Exception:
        data = {"raw": r.text}

    if r.status_code not in [200, 201] or "access_token" not in data:
        return {"ok": False, "status_code": r.status_code, "response": data}

    if ENV.exists():
        text = ENV.read_text(encoding="utf-8-sig")

        def upsert(key, value, text):
            value = clean(value)
            if re.search(rf"^{key}=.*$", text, flags=re.M):
                return re.sub(rf"^{key}=.*$", f"{key}={value}", text, flags=re.M)
            return text.rstrip() + f"\n{key}={value}\n"

        text = upsert("ETSY_ACCESS_TOKEN", data["access_token"], text)

        if data.get("refresh_token"):
            text = upsert("ETSY_REFRESH_TOKEN", data["refresh_token"], text)

        ENV.write_text(text, encoding="utf-8")

    os.environ["ETSY_ACCESS_TOKEN"] = clean(data["access_token"])

    if data.get("refresh_token"):
        os.environ["ETSY_REFRESH_TOKEN"] = clean(data["refresh_token"])

    return {
        "ok": True,
        "status": "etsy_token_refreshed",
        "access_len": len(clean(data["access_token"]))
    }

def etsy_request_receipts():
    api_base = clean(os.getenv("ETSY_API_BASE") or "https://openapi.etsy.com/v3/application").rstrip("/")
    api_key = clean(os.getenv("ETSY_API_KEY") or os.getenv("ETSY_CLIENT_ID"))
    token = clean(os.getenv("ETSY_ACCESS_TOKEN"))
    shop_id = clean(os.getenv("ETSY_SHOP_ID"))

    if not api_key or not token or not shop_id:
        return None, {
            "ok": False,
            "status": "missing_config",
            "missing": {
                "ETSY_API_KEY": not bool(api_key),
                "ETSY_ACCESS_TOKEN": not bool(token),
                "ETSY_SHOP_ID": not bool(shop_id)
            }
        }

    headers = {
        "x-api-key": api_key,
        "Authorization": "Bearer " + token
    }

    url = f"{api_base}/shops/{shop_id}/receipts"

    r = requests.get(
        url,
        headers=headers,
        params={
            "limit": 50,
            "was_paid": "true",
            "was_shipped": "false"
        },
        timeout=30
    )

    try:
        data = r.json()
    except Exception:
        data = {"raw": r.text}

    return r, data

r, data = etsy_request_receipts()

refreshed = None

if r is not None and r.status_code == 401 and "invalid_token" in str(data):
    refreshed = refresh_etsy_token()
    if refreshed.get("ok"):
        load_dotenv(override=True)
        r, data = etsy_request_receipts()

if r is None:
    print("ETSY ORDERS:", data.get("status"))
    OUT.write_text("[]", encoding="utf-8")
    raise SystemExit

print("STATUS:", r.status_code)

if refreshed:
    print("REFRESH:", json.dumps(refreshed))

if r.status_code not in [200, 201]:
    print(json.dumps(data)[:1000])
    OUT.write_text("[]", encoding="utf-8")
    raise SystemExit

receipts = data.get("results", []) if isinstance(data, dict) else []

orders = []

for receipt in receipts:
    receipt_id = receipt.get("receipt_id")

    txs = receipt.get("transactions") or []
    for item in txs:
        sku = item.get("sku") or item.get("product_data", {}).get("sku")

        if not sku:
            continue

        price_data = item.get("price") or {}
        amount = price_data.get("amount", 0)
        divisor = price_data.get("divisor", 100)
        sale_price = float(amount or 0) / float(divisor or 100)

        orders.append({
            "order_id": str(receipt_id),
            "channel_order_name": str(receipt_id),
            "channel": "etsy",
            "sku": sku,
            "quantity": int(item.get("quantity", 1) or 1),
            "paid": bool(receipt.get("was_paid")),
            "sale_price": sale_price,
            "shipping_address": {
                "name": receipt.get("name"),
                "address1": receipt.get("first_line"),
                "address2": receipt.get("second_line"),
                "city": receipt.get("city"),
                "province": receipt.get("state"),
                "zip": receipt.get("zip"),
                "country_code": receipt.get("country_iso"),
            },
            "raw": {
                "receipt_id": receipt_id,
                "transaction_id": item.get("transaction_id"),
                "was_paid": receipt.get("was_paid"),
                "was_shipped": receipt.get("was_shipped")
            },
            "collected_at": datetime.now(timezone.utc).isoformat()
        })

OUT.write_text(json.dumps(orders, indent=2, ensure_ascii=False), encoding="utf-8")

print("ETSY ORDERS:", len(orders))
print("REPORT:", OUT)
