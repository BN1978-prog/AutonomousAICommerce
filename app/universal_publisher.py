
import json
import os
import requests
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv

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
        "note": "LIVE mode currently supports Shopify draft publishing only."
    }

    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
