import json
from pathlib import Path
from datetime import datetime, timezone

PAID=Path("app/logs/paid_ads_status.json")
EVENTS=Path("app/logs/event_collector_state.json")
OUT=Path("app/logs/traffic_mode.json")

paid=json.loads(PAID.read_text(encoding="utf-8"))
events=json.loads(EVENTS.read_text(encoding="utf-8"))

google_ready=paid.get("google_ads",{}).get("ok",False)
meta_ready=paid.get("meta_ads",{}).get("ok",False)

google_clicks=events.get("sources",{}).get("google_clicks",False)
meta_clicks=events.get("sources",{}).get("meta_clicks",False)

traffic={
    "created_at":datetime.now(timezone.utc).isoformat(),
    "traffic_sources":[
        {
            "source":"google",
            "enabled":google_ready,
            "status":"ready_waiting_clicks" if google_ready and not google_clicks else "clicks_live"
        },
        {
            "source":"meta",
            "enabled":meta_ready,
            "status":"ready_waiting_clicks" if meta_ready and not meta_clicks else "clicks_live"
        },
        {
            "source":"ebay",
            "enabled":True,
            "status":"organic_live"
        },
        {
            "source":"shopify",
            "enabled":True,
            "status":"store_live"
        }
    ],
    "traffic_learning_enabled": google_ready or meta_ready or google_clicks or meta_clicks,
    "reason":"paid_sources_ready_waiting_clicks"
}

OUT.write_text(json.dumps(traffic,indent=2),encoding="utf-8")
print(json.dumps(traffic,indent=2))
