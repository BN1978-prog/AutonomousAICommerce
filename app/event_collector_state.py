import json
from pathlib import Path
from datetime import datetime, timezone

OUT=Path("app/logs/event_collector_state.json")

state={
    "created_at":datetime.now(timezone.utc).isoformat(),
    "sources":{
        "shopify_orders":True,
        "shopify_add_to_cart":True,
        "ebay_sales":True,
        "google_clicks":False,
        "meta_clicks":False
    },
    "event_learning_enabled":False,
    "reason":"waiting_for_google_meta_connection"
}

OUT.write_text(
    json.dumps(state,indent=2),
    encoding="utf-8"
)

print(json.dumps(state,indent=2))
