import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/deployment_readiness_checklist.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

master = read_json("app/logs/master_system_health.json")
dashboard = read_json("app/logs/system_status_dashboard.json")
crm = read_json("app/logs/crm_final_gate.json")
smtp = read_json("app/logs/smtp_config_validator.json")
niche = read_json("app/logs/niche_exclusion_summary.json")
amazon = read_json("app/logs/supplier_fallback_engine.json")

checklist = [
    {
        "item": "Core autopilot",
        "ready": master.get("status") == "MASTER_SYSTEM_HEALTHY_SAFE_MODE"
    },
    {
        "item": "Token self-healing",
        "ready": dashboard.get("channel_self_healer") == "all_channels_ok_no_repair_needed"
    },
    {
        "item": "Safe mode",
        "ready": dashboard.get("live_money_spending") is False
    },
    {
        "item": "Pet niche protected",
        "ready": niche.get("status") == "PET_NICHE_SAFE"
    },
    {
        "item": "CRM safe mode",
        "ready": crm.get("status") == "CRM_FINAL_GATE_BLOCKED"
    },
    {
        "item": "SMTP real provider",
        "ready": smtp.get("status") == "SMTP_CONFIG_READY"
    },
    {
        "item": "Google Basic Access",
        "ready": "DEVELOPER_TOKEN_NOT_APPROVED_OR_TEST_ONLY" not in str(dashboard.get("google_status"))
    },
    {
        "item": "Amazon SP-API",
        "ready": not any(
            s.get("name") == "amazon" and s.get("ready") is False
            for s in amazon.get("suppliers", [])
        )
    },
    {
        "item": "Real sales data",
        "ready": dashboard.get("real_sales_mode") != "waiting_for_sales"
    }
]

not_ready = [x for x in checklist if not x["ready"]]

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "ready_count": len([x for x in checklist if x["ready"]]),
    "not_ready_count": len(not_ready),
    "checklist": checklist,
    "not_ready": not_ready,
    "status": "DEPLOYMENT_READY_SAFE_MODE" if len(not_ready) <= 4 else "DEPLOYMENT_PARTIAL_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
