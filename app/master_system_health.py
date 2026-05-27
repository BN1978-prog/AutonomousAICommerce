import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/master_system_health.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

files = {
    "dashboard": "app/logs/system_status_dashboard.json",
    "recovery": "app/logs/recovery_report.json",
    "backup": "app/logs/backup_report.json",
    "budget": "app/logs/budget_controller.json",
    "roi": "app/logs/roi_engine.json",
    "crm": "app/logs/crm_final_gate.json",
    "supplier": "app/logs/supplier_fallback_engine.json",
    "inventory": "app/logs/inventory_sync_guard.json",
    "compliance": "app/logs/compliance_layer.json",
    "quality": "app/logs/product_quality_filter.json",
    "alerts": "app/logs/alerts.json",
    "niche": "app/logs/niche_exclusion_summary.json"
}

data = {k: read_json(v) for k, v in files.items()}

checks = {
    "core_healthy": data["dashboard"].get("system_status") == "HEALTHY",
    "safe_mode": data["dashboard"].get("live_money_spending") is False,
    "recovery_ok": data["recovery"].get("status") == "RECOVERY_OK",
    "backup_ok": data["backup"].get("status") == "BACKUP_OK",
    "budget_safe": data["budget"].get("budget_status") == "BUDGET_SAFE_MODE",
    "roi_ready": data["roi"].get("status") in ["ROI_WAITING_FOR_SALES", "ROI_ACTIVE"],

    # CRM blocked by guard is safe until real SMTP + owner confirmation + queue exist
    "crm_safe": data["crm"].get("status") in [
        "CRM_FINAL_GATE_BLOCKED",
        "CRM_FINAL_GATE_READY",
        "CRM_HEALTHY_SAFE_MODE"
    ],

    "supplier_ready": data["supplier"].get("status") == "SUPPLIER_FALLBACK_READY",
    "inventory_guard_ready": data["inventory"].get("status") == "INVENTORY_SYNC_GUARD_READY",
    "compliance_ready": data["compliance"].get("status") in ["COMPLIANCE_OK", "COMPLIANCE_BLOCKS_PRESENT"],
    "quality_ready": data["quality"].get("status") == "PRODUCT_QUALITY_FILTER_OK",
    "pet_niche_safe": data["niche"].get("status") == "PET_NICHE_SAFE",
    "no_critical_alerts": data["alerts"].get("critical_count", 0) == 0
}

failed = [k for k, v in checks.items() if not v]

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "checks": checks,
    "failed_checks": failed,
    "failed_count": len(failed),
    "external_blockers": data["dashboard"].get("external_blockers", []),
    "pet_niche": data["niche"],
    "crm_status": data["crm"].get("status"),
    "status": "MASTER_SYSTEM_HEALTHY_SAFE_MODE" if not failed else "MASTER_SYSTEM_ATTENTION_REQUIRED"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
