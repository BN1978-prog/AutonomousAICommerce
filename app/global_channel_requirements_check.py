import json
import os
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv(override=True)

OUT = Path("app/logs/global_channel_requirements_check.json")

requirements = {
    "amazon": [
        "AMAZON_LWA_CLIENT_ID",
        "AMAZON_LWA_CLIENT_SECRET",
        "AMAZON_REFRESH_TOKEN",
        "AMAZON_SELLER_ID",
        "AMAZON_MARKETPLACE_ID"
    ],
    "tiktok_shop": [
        "TIKTOK_SHOP_APP_KEY",
        "TIKTOK_SHOP_APP_SECRET",
        "TIKTOK_SHOP_ACCESS_TOKEN",
        "TIKTOK_SHOP_REFRESH_TOKEN",
        "TIKTOK_SHOP_ID",
        "TIKTOK_SHOP_REGION"
    ],
    "tiktok_ads": [
        "TIKTOK_ADS_ACCESS_TOKEN",
        "TIKTOK_ADS_ADVERTISER_ID",
        "TIKTOK_ADS_PIXEL_ID"
    ],
    "aliexpress": [
        "ALIEXPRESS_APP_KEY",
        "ALIEXPRESS_APP_SECRET",
        "ALIEXPRESS_ACCESS_TOKEN",
        "ALIEXPRESS_REFRESH_TOKEN"
    ]
}

channels = []

for channel, keys in requirements.items():
    missing = []

    for key in keys:
        if not os.getenv(key):
            missing.append(key)

    channels.append({
        "channel": channel,
        "required_keys": keys,
        "missing": missing,
        "ready": len(missing) == 0
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "channels_checked": len(channels),
    "ready_channels": [c["channel"] for c in channels if c["ready"]],
    "not_ready_channels": [c["channel"] for c in channels if not c["ready"]],
    "channels": channels,
    "status": "GLOBAL_CHANNEL_REQUIREMENTS_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
