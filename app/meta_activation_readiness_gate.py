import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/meta_activation_readiness_gate.json")

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
meta_plan = read_json("app/logs/meta_safe_activation_plan.json")

confirmation_file = Path("app/logs/OWNER_CONFIRM_META_ACTIVATION.json")

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
    "meta_plan_ready": meta_plan.get("status") == "META_SAFE_ACTIVATION_PLAN_READY",
    "owner_confirmation_file_exists": confirmation_file.exists()
}

missing = [k for k, v in checks.items() if not v]

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "checks": checks,
    "missing_requirements": missing,
    "activation_allowed": False,
    "reason": "owner_confirmation_required" if not confirmation_file.exists() else "guard_still_blocks_activation",
    "status": "META_ACTIVATION_GATE_WAITING_OWNER_CONFIRMATION" if not confirmation_file.exists() else "META_ACTIVATION_GATE_READY_BUT_NOT_EXECUTED"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
