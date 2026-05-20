import json
from pathlib import Path

REGISTRY=Path("app/logs/imported_skus.json")
SUMMARY=Path("app/logs/seo_push_summary.json")
QUALITY=Path("app/logs/seo_quality_report.json")
REPUSH=Path("app/logs/seo_repush_execution.json")
OUT=Path("app/logs/system_health_dashboard.json")

registry=json.loads(REGISTRY.read_text(encoding="utf-8"))
summary=json.loads(SUMMARY.read_text(encoding="utf-8"))
quality=json.loads(QUALITY.read_text(encoding="utf-8"))
repush=json.loads(REPUSH.read_text(encoding="utf-8"))

dashboard={

    "registry_total":
        len(registry),

    "push_operations":
        summary["total_operations"],

    "successful_pushes":
        summary["successful"],

    "failed_pushes":
        summary["failed"],

    "quality_issues":
        len(quality),

    "repush_operations":
        len(repush),

    "live_push":
        summary["live_push"],

    "system_status":
        "HEALTHY"
        if (
            summary["failed"]==0
            and len(quality)==0
        )
        else "WARNING"
}

OUT.write_text(
    json.dumps(
        dashboard,
        indent=2
    ),
    encoding="utf-8"
)

print(json.dumps(
    dashboard,
    indent=2
))
