import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/external_blockers_monitor.json")

FILES = {
    "external_platform_blockers": Path("app/logs/external_platform_blockers.json"),
    "production_readiness": Path("app/logs/production_readiness_report.json"),
    "global_control_panel": Path("app/logs/global_commerce_control_panel.json")
}

def read_json(path):
    if not path.exists():
        return {}

    try:
        return json.loads(path.read_text(encoding="utf-8"))

    except:
        return {}

external = read_json(FILES["external_platform_blockers"])
production = read_json(FILES["production_readiness"])
global_panel = read_json(FILES["global_control_panel"])

blockers = []

for b in external.get("blockers",[]):

    platform = b.get("platform")

    if not any(x.get("platform")==platform for x in blockers):

        blockers.append({
            "source":"external_platform_blockers",
            "platform":platform,
            "status":b.get("status"),
            "reason":b.get("reason"),
            "action_required":b.get("action_required")
        })

google_status = production.get("google_status")

if (
    google_status
    and "blocked" in str(google_status).lower()
    and not any(x.get("platform")=="google_ads" for x in blockers)
):

    blockers.append({
        "source":"production_readiness_report",
        "platform":"google_ads",
        "status":google_status,
        "reason":"google_access_or_permission_block"
    })

meta_activation = production.get("meta_activation")

if (
    meta_activation
    and "blocked" in str(meta_activation).lower()
):

    blockers.append({
        "source":"production_readiness_report",
        "platform":"meta_ads",
        "status":meta_activation,
        "reason":"owner_safety_guard"
    })

if production.get("live_money_spending") is False:
    safety_status="safe_no_live_spend"
else:
    safety_status="warning_live_money_spending_enabled"

report={

    "created_at":datetime.now(
        timezone.utc
    ).isoformat(),

    "blockers_count":len(blockers),

    "blockers":blockers,

    "safety_status":safety_status,

    "system_status":
    production.get("system_status"),

    "production_readiness":
    production.get("production_readiness"),

    "global_status":
    production.get("global_status"),

    "ready_to_activate_meta_when_owner_confirms":
    production.get(
        "ready_to_activate_meta_when_owner_confirms"
    ),

    "ready_to_create_google_campaigns_after_api_approval":
    production.get(
        "ready_to_create_google_campaigns_after_api_approval"
    ),

    "status":
    "READY_NO_EXTERNAL_BLOCKERS"
    if len(blockers)==0
    else "EXTERNAL_BLOCKERS_PRESENT"
}

OUT.write_text(
    json.dumps(
        report,
        indent=2
    ),
    encoding="utf-8"
)

print(
json.dumps(
report,
indent=2
)
)
