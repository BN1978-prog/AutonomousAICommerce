import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/daily_report.json")

FILES = {
    "dashboard":"app/logs/system_status_dashboard.json",
    "production":"app/logs/production_readiness_report.json",
    "sales":"app/logs/real_sales_mode.json",
    "control":"app/logs/global_commerce_control_panel.json",
    "blockers":"app/logs/external_blockers_monitor.json"
}

def read_json(path):

    p=Path(path)

    if not p.exists():
        return {}

    try:
        return json.loads(
            p.read_text(
                encoding="utf-8"
            )
        )

    except:
        return {}

dashboard=read_json(
FILES["dashboard"]
)

production=read_json(
FILES["production"]
)

sales=read_json(
FILES["sales"]
)

control=read_json(
FILES["control"]
)

blockers=read_json(
FILES["blockers"]
)

report={

"created_at":
datetime.now(
timezone.utc
).isoformat(),

"system":{

"status":
dashboard.get(
"system_status"
),

"production":
dashboard.get(
"production_readiness"
),

"safe":
dashboard.get(
"safe_to_continue"
)

},

"sales":{

"mode":
dashboard.get(
"real_sales_mode"
),

"queue":
dashboard.get(
"purchase_queue_size"
),

"revenue":
sales.get(
"total_revenue",
0
)

},

"ads":{

"live_money_spending":
dashboard.get(
"live_money_spending"
),

"google":
dashboard.get(
"google_status"
),

"meta":
dashboard.get(
"meta_activation"
)

},

"blockers":{

"count":
blockers.get(
"blockers_count"
),

"items":
blockers.get(
"blockers",
[]
)

},

"summary":{

"healthy":
dashboard.get(
"system_status"
)=="HEALTHY",

"safe_to_continue":
dashboard.get(
"safe_to_continue"
),

"ready_for_real_sales":
control.get(
"real_sales_mode"
)!="disabled"

}

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
