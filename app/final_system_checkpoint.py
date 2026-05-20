import json
from pathlib import Path
from datetime import datetime, timezone

HEALTH=Path("app/logs/system_health_dashboard.json")
OUT=Path("app/logs/final_system_checkpoint.json")

health=json.loads(
    HEALTH.read_text(
        encoding="utf-8"
    )
)

checkpoint={
    "checkpoint_name":"seo_multichannel_pipeline_stable",
    "created_at":datetime.now(timezone.utc).isoformat(),
    "status":health.get("system_status"),
    "registry_total":health.get("registry_total"),
    "push_operations":health.get("push_operations"),
    "successful_pushes":health.get("successful_pushes"),
    "failed_pushes":health.get("failed_pushes"),
    "quality_issues":health.get("quality_issues"),
    "repush_operations":health.get("repush_operations"),
    "live_push":health.get("live_push"),
    "safe_to_continue":health.get("system_status")=="HEALTHY"
}

OUT.write_text(
    json.dumps(
        checkpoint,
        indent=2
    ),
    encoding="utf-8"
)

print(json.dumps(checkpoint,indent=2))
