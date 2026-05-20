import json
from pathlib import Path
from datetime import datetime, timezone

TRAFFIC=Path("app/logs/traffic_mode.json")
SALES=Path("app/logs/real_sales_mode.json")
PAID=Path("app/logs/paid_ads_status.json")
OUT=Path("app/logs/traffic_readiness.json")

traffic=json.loads(TRAFFIC.read_text(encoding="utf-8"))
sales=json.loads(SALES.read_text(encoding="utf-8"))
paid=json.loads(PAID.read_text(encoding="utf-8"))

sources=traffic.get("traffic_sources",[])
enabled_sources=[x for x in sources if x.get("enabled") is True]

active_paid=paid.get("active_paid_sources",[])

readiness={
    "created_at":datetime.now(timezone.utc).isoformat(),
    "organic_sources_live":len(enabled_sources),
    "paid_sources_connected":len(active_paid),
    "active_paid_sources":active_paid,
    "has_real_sales":sales.get("has_real_sales"),
    "traffic_learning_ready":paid.get("paid_ads_ready",False),
    "reason":"paid_source_connected" if paid.get("paid_ads_ready",False) else "paid_sources_not_connected"
}

OUT.write_text(json.dumps(readiness,indent=2),encoding="utf-8")

print(json.dumps(readiness,indent=2))
