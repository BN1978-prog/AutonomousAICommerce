import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/system_maintenance_planner.json")

plan = {
    "hourly":[
        "run channel_self_healer",
        "run external_blockers_monitor",
        "run master_system_health",
        "run backup_manager"
    ],

    "daily":[
        "run autopilot_runner",
        "run roi_engine",
        "run crm_health_check",
        "run supplier_fallback_engine",
        "run inventory_sync_guard"
    ],

    "weekly":[
        "review blocked products",
        "review Google API status",
        "review Meta activation readiness",
        "review Amazon verification status"
    ]
}

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "hourly_tasks": len(plan["hourly"]),
    "daily_tasks": len(plan["daily"]),
    "weekly_tasks": len(plan["weekly"]),
    "maintenance_plan": plan,
    "status":"SYSTEM_MAINTENANCE_READY"
}

OUT.write_text(
    json.dumps(report,indent=2),
    encoding="utf-8"
)

print(json.dumps(report,indent=2))
