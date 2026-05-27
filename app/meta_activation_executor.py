import json
from pathlib import Path
from datetime import datetime, timezone

PLAN = Path("app/logs/meta_safe_activation_plan.json")
GUARD = Path("app/logs/meta_activation_guard.json")
OUT = Path("app/logs/meta_activation_executor.json")

plan = json.loads(PLAN.read_text(encoding="utf-8")) if PLAN.exists() else {}
guard = json.loads(GUARD.read_text(encoding="utf-8")) if GUARD.exists() else {}

enabled = bool(guard.get("meta_activation_enabled", False))

actions = []
blocked = []

for p in plan.get("plans", []):
    if not enabled:
        blocked.append({
            **p,
            "reason": "meta_activation_disabled_by_guard"
        })
        continue

    actions.append({
        **p,
        "action": "would_activate_meta_campaign",
        "mode": "guard_passed_but_api_call_not_implemented",
        "status": "ready_for_live_activation_code"
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "mode": "meta_activation_executor_guarded",
    "meta_activation_enabled": enabled,
    "actions_ready": len(actions),
    "blocked": blocked,
    "actions": actions,
    "live_money_spending": False,
    "status": "blocked_by_meta_activation_guard" if blocked and not actions else "ready_for_live_activation_code"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
