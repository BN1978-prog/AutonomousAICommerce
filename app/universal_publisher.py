
import json
from pathlib import Path
from datetime import datetime, timezone

DRAFTS = Path("app/logs/universal_listing_drafts.json")
REGISTRY = Path("app/logs/imported_skus.json")
OUT = Path("app/logs/universal_publisher.json")

PUBLISH_MODE = "DRY_RUN"

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

            row["channels"][channel] = {
                "enabled": True,
                "status": "ready_for_publish",
                "payload_preview": payload
            }

        results.append(row)

    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "UNIVERSAL_PUBLISHER_DRY_RUN",
        "mode": PUBLISH_MODE,
        "drafts": len(drafts),
        "results": results,
        "note": "No marketplace API calls were made."
    }

    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
