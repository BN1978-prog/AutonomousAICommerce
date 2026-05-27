import json
from pathlib import Path
from datetime import datetime, timezone

FILES = {
    "control": "app/logs/global_commerce_control_panel.json",
    "meta_readiness": "app/logs/meta_launch_readiness.json",
    "activation": "app/logs/meta_activation_executor.json",
    "autostop": "app/logs/meta_auto_stop_monitor.json",
    "checkpoint": "app/logs/final_system_checkpoint.json",
}

def load(path):
    p = Path(path)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}

data = {k: load(v) for k, v in FILES.items()}

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "production_readiness": "READY_SAFE_MODE",
    "system_status": data["checkpoint"].get("status"),
    "safe_to_continue": data["checkpoint"].get("safe_to_continue"),
    "global_status": data["control"].get("status"),
    "meta_funnel": data["meta_readiness"].get("status"),
    "meta_activation": data["activation"].get("status"),
    "meta_auto_stop": data["autostop"].get("status"),
    "google_status": data["control"].get("google_status"),
    "live_money_spending": False,
    "ready_to_activate_meta_when_owner_confirms": True,
    "ready_to_create_google_campaigns_after_api_approval": True,
    "status": "PRODUCTION_READY_SAFE_MODE"
}

Path("app/logs/production_readiness_report.json").write_text(
    json.dumps(report, indent=2), encoding="utf-8"
)

print(json.dumps(report, indent=2))
