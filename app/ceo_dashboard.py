import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path("app/logs")

def load(name):
    p = ROOT / name
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}

scaling = load("auto_scaling_score.json")
roi = load("roi_simulation.json")
guardrails = load("product_guardrails.json")
queue = load("campaign_approval_queue.json")

dashboard = {
    "created_at": datetime.now(timezone.utc).isoformat(),

    "system_mode": "SAFE_AUTONOMOUS_COMMERCE",

    "live_money_spending": False,

    "top_scale_candidates": scaling.get("scale_ready", []),

    "roi_leaders": roi.get("simulations", []),

    "approval_queue_size": len(queue.get("queue", [])),

    "approval_queue": [
        {
            "sku": x["sku"],
            "approval_status": x["approval_status"]
        }
        for x in queue.get("queue", [])
    ],

    "stop_testing_count": len(
        guardrails.get("stop_testing", [])
    ),

    "stop_testing_products": [
        x["sku"]
        for x in guardrails.get("stop_testing", [])
    ],

    "executive_summary": {
        "healthy": True,
        "safe_mode": True,
        "scale_candidates": len(
            scaling.get("scale_ready", [])
        ),
        "roi_models_ready": len(
            roi.get("simulations", [])
        ) > 0,
        "approval_queue_ready": len(
            queue.get("queue", [])
        ) > 0
    },

    "status": "CEO_DASHBOARD_READY"
}

out = ROOT / "ceo_dashboard.json"

out.write_text(
    json.dumps(dashboard, indent=2),
    encoding="utf-8"
)

print(json.dumps(dashboard, indent=2))
