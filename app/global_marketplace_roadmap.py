import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/global_marketplace_roadmap.json")

channels = [
    {
        "channel": "shopify",
        "type": "storefront",
        "status": "connected",
        "priority": 1
    },
    {
        "channel": "woocommerce",
        "type": "storefront",
        "status": "connected",
        "priority": 2
    },
    {
        "channel": "ebay",
        "type": "marketplace",
        "status": "connected",
        "priority": 3
    },
    {
        "channel": "amazon",
        "type": "marketplace",
        "status": "pending_identity_verification",
        "priority": 4,
        "required": [
            "SP_API",
            "LWA_CLIENT_ID",
            "LWA_CLIENT_SECRET",
            "REFRESH_TOKEN",
            "SELLER_ID",
            "MARKETPLACE_ID"
        ]
    },
    {
        "channel": "tiktok_shop",
        "type": "marketplace",
        "status": "not_connected_yet",
        "priority": 5,
        "required": [
            "TikTok Shop seller account",
            "Open API app",
            "access token",
            "shop cipher",
            "seller region"
        ]
    },
    {
        "channel": "aliexpress",
        "type": "supplier_marketplace",
        "status": "not_connected_yet",
        "priority": 6,
        "required": [
            "AliExpress affiliate or dropshipping access",
            "API credentials",
            "product search",
            "order API"
        ]
    },
    {
        "channel": "cjdropshipping",
        "type": "supplier",
        "status": "connected",
        "priority": 7
    },
    {
        "channel": "google_ads",
        "type": "ads",
        "status": "waiting_basic_access",
        "priority": 8
    },
    {
        "channel": "meta_ads",
        "type": "ads",
        "status": "connected_paused_safe_mode",
        "priority": 9
    },
    {
        "channel": "tiktok_ads",
        "type": "ads",
        "status": "not_connected_yet",
        "priority": 10,
        "required": [
            "TikTok Ads account",
            "developer app",
            "access token",
            "advertiser ID",
            "pixel ID"
        ]
    }
]

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "vision": "global_autonomous_commerce_system",
    "channels_total": len(channels),
    "connected": [c for c in channels if "connected" in c["status"]],
    "pending": [c for c in channels if "pending" in c["status"] or "waiting" in c["status"]],
    "not_connected": [c for c in channels if c["status"] == "not_connected_yet"],
    "channels": channels,
    "status": "GLOBAL_MARKETPLACE_ROADMAP_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
