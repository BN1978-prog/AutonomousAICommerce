import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/crm_action_planner.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

segments = read_json("app/logs/customer_segmentation.json")
crm = read_json("app/logs/crm_automation_status.json")

actions = []

segment_counts = segments.get("segments", {})

if segment_counts.get("new_customers", 0) > 0:
    actions.append({
        "segment": "new_customers",
        "action": "send_welcome_flow",
        "status": "ready"
    })

if segment_counts.get("repeat_customers", 0) > 0:
    actions.append({
        "segment": "repeat_customers",
        "action": "send_loyalty_offer",
        "status": "ready"
    })

if segment_counts.get("high_value_customers", 0) > 0:
    actions.append({
        "segment": "high_value_customers",
        "action": "priority_support_and_vip_offer",
        "status": "ready"
    })

if segment_counts.get("inactive_customers", 0) > 0:
    actions.append({
        "segment": "inactive_customers",
        "action": "send_win_back_flow",
        "status": "ready"
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "crm_flows_available": crm.get("enabled_flows", 0),
    "actions_created": len(actions),
    "actions": actions,
    "status": "CRM_ACTIONS_WAITING_FOR_CUSTOMERS" if not actions else "CRM_ACTIONS_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
