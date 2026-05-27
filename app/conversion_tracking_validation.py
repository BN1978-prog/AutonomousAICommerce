import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/conversion_tracking_validation.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

events = read_json("app/logs/event_learning_sync.json")
dashboard = read_json("app/logs/system_status_dashboard.json")
meta_validation = read_json("app/logs/meta_token_validation.json")

sources = events.get("sources", {})

checks = {
    "shopify_orders": sources.get("shopify_orders") is True,
    "shopify_add_to_cart": sources.get("shopify_add_to_cart") is True,
    "ebay_sales": sources.get("ebay_sales") is True,
    "meta_clicks_or_events": sources.get("meta_clicks") is True,
    "google_clicks": sources.get("google_clicks") is True,
    "meta_token_valid": meta_validation.get("ok") is True
}

missing = [k for k, v in checks.items() if not v]

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "checks": checks,
    "missing_or_waiting": missing,
    "event_learning_enabled": events.get("event_learning_enabled"),
    "last_meta_event_at": events.get("last_meta_event_at"),
    "last_meta_event_id": events.get("last_meta_event_id"),
    "google_status": dashboard.get("google_status"),
    "status": "CONVERSION_TRACKING_READY" if not missing else "CONVERSION_TRACKING_PARTIAL"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
