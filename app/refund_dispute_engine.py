import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/refund_dispute_engine.json")

rules = [
    {
        "type":"refund_request",
        "auto_action":"collect_order_information",
        "enabled":True
    },
    {
        "type":"order_cancel",
        "auto_action":"check_fulfillment_status",
        "enabled":True
    },
    {
        "type":"chargeback",
        "auto_action":"flag_high_priority",
        "enabled":True
    },
    {
        "type":"delivery_issue",
        "auto_action":"collect_tracking_data",
        "enabled":True
    },
    {
        "type":"damaged_item",
        "auto_action":"request_photo_evidence",
        "enabled":True
    }
]

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "rules_count": len(rules),
    "enabled_rules": len([r for r in rules if r["enabled"]]),
    "rules": rules,
    "status":"REFUND_ENGINE_READY"
}

OUT.write_text(
    json.dumps(report, indent=2),
    encoding="utf-8"
)

print(json.dumps(report, indent=2))
