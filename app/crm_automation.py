import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/crm_automation_status.json")

flows = [
    {
        "name":"abandoned_cart",
        "trigger":"cart_abandoned",
        "delay_minutes":30,
        "enabled":True
    },
    {
        "name":"order_confirmation",
        "trigger":"order_created",
        "delay_minutes":0,
        "enabled":True
    },
    {
        "name":"review_request",
        "trigger":"order_delivered",
        "delay_days":7,
        "enabled":True
    },
    {
        "name":"repeat_customer",
        "trigger":"repeat_purchase_detected",
        "enabled":True
    },
    {
        "name":"win_back",
        "trigger":"customer_inactive_30_days",
        "enabled":True
    }
]

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "flows_count": len(flows),
    "enabled_flows": len([f for f in flows if f["enabled"]]),
    "flows": flows,
    "status":"CRM_AUTOMATION_READY"
}

OUT.write_text(
    json.dumps(report,indent=2),
    encoding="utf-8"
)

print(json.dumps(report,indent=2))
