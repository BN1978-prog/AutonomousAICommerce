import json
from pathlib import Path
from datetime import datetime, timezone

logs={
    "token":"app/logs/token_manager_status.json",
    "channels":"app/logs/channel_validation_checkpoint.json",
    "feeds":"app/logs/feed_channel_validation.json",
    "traffic":"app/logs/traffic_readiness.json",
    "sales":"app/logs/real_sales_mode.json",
    "paid":"app/logs/paid_ads_status.json"
}

def load(path):
    p=Path(path)
    if not p.exists():
        return None

    try:
        return json.loads(
            p.read_text(
                encoding="utf-8"
            )
        )
    except:
        return None

token=load(logs["token"])
channels=load(logs["channels"])
feeds=load(logs["feeds"])
traffic=load(logs["traffic"])
sales=load(logs["sales"])
paid=load(logs["paid"])

report={
    "created_at":datetime.now(
        timezone.utc
    ).isoformat(),

    "shopify_ok":
        channels and
        channels["channels"].get(
            "shopify"
        )=="live_read_write_confirmed",

    "ebay_ok":
        channels and
        channels["channels"].get(
            "ebay"
        )=="live_read_write_confirmed",

    "woocommerce_ok":
        channels and
        channels["channels"].get(
            "woocommerce"
        )=="live_read_write_confirmed",

    "google_feed_ok":
        feeds and
        feeds[0]["ok"],

    "meta_feed_ok":
        feeds and
        feeds[1]["ok"],

    "paid_ads_ready":
        paid and
        paid.get(
            "paid_ads_ready",
            False
        ),

    "traffic_learning_ready":
        traffic and
        traffic.get(
            "traffic_learning_ready",
            False
        ),

    "real_sales_mode":
        sales.get(
            "mode",
            "unknown"
        ) if sales else "unknown"
}

report["all_core_channels_ok"]=all([
    report["shopify_ok"],
    report["ebay_ok"],
    report["woocommerce_ok"],
    report["google_feed_ok"],
    report["meta_feed_ok"]
])

Path(
    "app/logs/channel_live_test.json"
).write_text(
    json.dumps(
        report,
        indent=2
    ),
    encoding="utf-8"
)

print(
    json.dumps(
        report,
        indent=2
    )
)
