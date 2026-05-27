import json
from pathlib import Path
from datetime import datetime, timezone

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "thresholds": {
        "100": {
            "mode": "MICRO_BUDGET",
            "max_daily_spend_gbp": 5
        },
        "250": {
            "mode": "SCALE_TESTING",
            "max_daily_spend_gbp": 20
        },
        "1000": {
            "mode": "FULL_AUTOPILOT",
            "max_daily_spend_gbp": 100
        }
    },
    "status": "BUDGET_SCALING_RULES_ACTIVE"
}

Path("app/logs/budget_scaling_rules.json").write_text(
    json.dumps(report, indent=2),
    encoding="utf-8"
)

print(json.dumps(report, indent=2))
