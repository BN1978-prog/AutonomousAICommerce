
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

updates = json.loads(TRACKING.read_text(encoding="utf-8-sig")) if TRACKING.exists() else []

results = []

for item in updates:
    order_id = item.get("order_id")
    sku = item.get("sku")
    channel = item.get("channel") or "shopify"
    tracking_number = item.get("tracking_number")
    carrier = item.get("carrier") or "Other"

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

    payload = {
        "fulfillment": {
            "tracking_number": tracking_number,
            "tracking_company": carrier,
            "notify_customer": True
        }
    }

    if DRY_RUN:
        row = {
            "order_id": order_id,
            "sku": sku,
            "dry_run": True,
            "status": "prepared_not_sent_to_shopify",
            "payload": payload
        }
        results.append(row)
        mark_stage(order_id, sku, channel, "shopify_fulfillment_synced", row)
        continue

    row = {
        "order_id": order_id,
        "sku": sku,
        "dry_run": False,
        "status": "live_fulfillment_api_not_implemented_yet",
        "payload": payload
    }
    results.append(row)

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "status": "SHOPIFY_FULFILLMENT_SYNC_CHECKED",
    "dry_run": DRY_RUN,
    "updates_seen": len(updates),
    "results": results
}

OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(report, indent=2, ensure_ascii=False))
