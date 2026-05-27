import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/google_activation_readiness_gate.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

dashboard = read_json("app/logs/system_status_dashboard.json")
budget = read_json("app/logs/budget_controller.json")
compliance = read_json("app/logs/compliance_layer.json")
quality = read_json("app/logs/product_quality_filter.json")
google_creator = read_json("app/logs/google_campaign_live_creator.json")
blockers = read_json("app/logs/external_blockers_monitor.json")

google_blocked = any(
    b.get("platform") == "google_ads"
    and "DEVELOPER_TOKEN_NOT_APPROVED_OR_TEST_ONLY" in str(b.get("reason"))
    for b in blockers.get("blockers", [])
)

checks = {
    "system_healthy": dashboard.get("system_status") == "HEALTHY",
    "safe_to_continue": dashboard.get("safe_to_continue") is True,
    "no_live_money_spending_now": dashboard.get("live_money_spending") is False,
    "budget_safe": budget.get("budget_status") == "BUDGET_SAFE_MODE",
    "compliance_ok_or_controlled": compliance.get("status") in [
        "COMPLIANCE_OK",
        "COMPLIANCE_BLOCKS_PRESENT"
    ],
    "quality_filter_ok": quality.get("status") == "PRODUCT_QUALITY_FILTER_OK",
    "google_api_not_blocked": not google_blocked
}

missing = [k for k, v in checks.items() if not v]

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "checks": checks,
    "missing_requirements": missing,
    "google_blocked": google_blocked,
    "activation_allowed": False,
    "reason": "waiting_google_basic_access" if google_blocked else "owner_confirmation_required",
    "status": "GOOGLE_ACTIVATION_WAITING_BASIC_ACCESS" if google_blocked else "GOOGLE_ACTIVATION_GATE_READY_BUT_NOT_EXECUTED"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
