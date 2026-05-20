import json
from pathlib import Path
from datetime import datetime, timezone

CONFIG=Path("app/logs/autonomy_limits.json")
QUEUE=Path("app/logs/supplier_purchase_queue.json")
STATUS=Path("app/logs/autonomous_fulfillment_status.json")

limits={
  "created_at": datetime.now(timezone.utc).isoformat(),
  "mode": "safe_autonomous",
  "auto_buy_enabled": True,
  "max_order_cost": 50,
  "max_daily_autobuy": 300,
  "min_margin_percent": 25,
  "require_real_paid_order": True,
  "dashboard_read_only": True
}

queue=[]

status={
  "created_at": datetime.now(timezone.utc).isoformat(),
  "autonomous_fulfillment_ready": True,
  "waiting_for": "real_paid_orders",
  "logic": [
    "collect real paid orders",
    "check supplier cost",
    "check margin and limits",
    "create supplier purchase queue",
    "after supplier tracking update Shopify"
  ],
  "limits_file": str(CONFIG),
  "queue_file": str(QUEUE)
}

CONFIG.write_text(json.dumps(limits,indent=2),encoding="utf-8")
QUEUE.write_text(json.dumps(queue,indent=2),encoding="utf-8")
STATUS.write_text(json.dumps(status,indent=2),encoding="utf-8")

print(json.dumps(status,indent=2))
