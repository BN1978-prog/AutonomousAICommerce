import json
import os
import requests
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv
from app.order_processing_ledger import is_stage_done, mark_stage

load_dotenv(override=True)

TRACKING = Path("app/logs/tracking_updates.json")
OUT = Path("app/logs/shopify_fulfillment_sync.json")

DRY_RUN = os.getenv("SHOPIFY_FULFILLMENT_DRY_RUN", "true").lower() == "true"

SHOPIFY_STORE_URL = os.getenv("SHOPIFY_STORE_URL", "").strip().rstrip("/")
SHOPIFY_TOKEN = (
    os.getenv("SHOPIFY_ADMIN_TOKEN")
    or os.getenv("SHOPIFY_ACCESS_TOKEN")
    or os.getenv("SHOPIFY_ADMIN_ACCESS_TOKEN")
    or ""
).strip()
SHOPIFY_API_VERSION = os.getenv("SHOPIFY_API_VERSION", "2025-01").strip()

if SHOPIFY_STORE_URL and not SHOPIFY_STORE_URL.startswith(("http://", "https://")):
    SHOPIFY_STORE_URL = "https://" + SHOPIFY_STORE_URL

headers = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

def shopify_get_fulfillment_orders(order_id):
    url = f"{SHOPIFY_STORE_URL}/admin/api/{SHOPIFY_API_VERSION}/orders/{order_id}/fulfillment_orders.json"
    r = requests.get(url, headers=headers, timeout=30)
    try:
        data = r.json()
    except Exception:
        data = {"raw": r.text}
    return r.status_code, data

def shopify_create_fulfillment(fulfillment_order_id, tracking_number, carrier):
    url = f"{SHOPIFY_STORE_URL}/admin/api/{SHOPIFY_API_VERSION}/fulfillments.json"
    payload = {
        "fulfillment": {
            "notify_customer": True,
            "tracking_info": {
                "number": tracking_number,
                "company": carrier
            },
            "line_items_by_fulfillment_order": [
                {
                    "fulfillment_order_id": fulfillment_order_id
                }
            ]
        }
    }

    r = requests.post(url, headers=headers, json=payload, timeout=30)

    try:
        data = r.json()
    except Exception:
        data = {"raw": r.text}

    return r.status_code, data, payload

updates = json.loads(TRACKING.read_text(encoding="utf-8-sig")) if TRACKING.exists() else []
results = []

for item in updates:
    order_id = item.get("order_id")
    sku = item.get("sku")
    channel = item.get("channel") or "shopify"
    tracking_number = item.get("tracking_number")
    carrier = item.get("carrier") or "Other"

    if channel != "shopify":
        results.append({
            "order_id": order_id,
            "sku": sku,
            "channel": channel,
            "status": "skipped_non_shopify_channel"
        })
        continue

    if str(order_id or "").upper().startswith("TEST"):
        results.append({
            "order_id": order_id,
            "sku": sku,
            "status": "blocked_test_order"
        })
        continue

    if is_stage_done(order_id, sku, channel, "shopify_fulfillment_synced"):
        results.append({
            "order_id": order_id,
            "sku": sku,
            "status": "skipped_already_fulfilled_in_ledger"
        })
        continue

    if not tracking_number:
        results.append({
            "order_id": order_id,
            "sku": sku,
            "status": "skipped_waiting_tracking_number"
        })
        continue

    if not SHOPIFY_STORE_URL or not SHOPIFY_TOKEN:
        results.append({
            "order_id": order_id,
            "sku": sku,
            "status": "blocked_missing_shopify_config"
        })
        continue

    fo_status, fo_data = shopify_get_fulfillment_orders(order_id)
    fulfillment_orders = fo_data.get("fulfillment_orders", []) if isinstance(fo_data, dict) else []

    open_fo = None
    for fo in fulfillment_orders:
        if fo.get("status") in ["open", "in_progress", "scheduled"]:
            open_fo = fo
            break

    if not open_fo:
        results.append({
            "order_id": order_id,
            "sku": sku,
            "status": "blocked_no_open_fulfillment_order",
            "fulfillment_orders_status_code": fo_status,
            "fulfillment_orders_response": fo_data
        })
        continue

    fulfillment_order_id = open_fo.get("id")

    if DRY_RUN:
        row = {
            "order_id": order_id,
            "sku": sku,
            "dry_run": True,
            "status": "prepared_not_sent_to_shopify",
            "fulfillment_order_id": fulfillment_order_id,
            "tracking_number": tracking_number,
            "carrier": carrier
        }
        results.append(row)
        continue

    status_code, response, payload = shopify_create_fulfillment(
        fulfillment_order_id,
        tracking_number,
        carrier
    )

    ok = status_code in [200, 201]

    row = {
        "order_id": order_id,
        "sku": sku,
        "dry_run": False,
        "status": "fulfilled_in_shopify" if ok else "shopify_fulfillment_api_error",
        "status_code": status_code,
        "fulfillment_order_id": fulfillment_order_id,
        "payload": payload,
        "response": response
    }

    results.append(row)

    if ok:
        mark_stage(order_id, sku, channel, "shopify_fulfillment_synced", row)

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "status": "SHOPIFY_FULFILLMENT_SYNC_CHECKED",
    "dry_run": DRY_RUN,
    "updates_seen": len(updates),
    "results": results
}

OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(report, indent=2, ensure_ascii=False))
