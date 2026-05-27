import json
from pathlib import Path
from datetime import datetime, timezone

ROI = Path("app/logs/roi_simulation.json")
CFG = Path("app/config/auto_spend_guardrails.json")
OUT = Path("app/logs/auto_launch_decisions.json")

roi = json.loads(ROI.read_text(encoding="utf-8"))
cfg = json.loads(CFG.read_text(encoding="utf-8"))

decisions = []

for item in roi.get("simulations", []):
    approved = (
        cfg["allow_live_spending"]
        and not cfg["emergency_stop"]
        and item["risk_score"] in cfg["allowed_risk_levels"]
        and item["estimated_roi_percent"] >= cfg["min_roi_percent"]
        and item["recommended_daily_budget"] <= cfg["max_campaign_budget"]
    )

    decisions.append({
        "sku": item["sku"],
        "risk_score": item["risk_score"],
        "estimated_roi_percent": item["estimated_roi_percent"],
        "recommended_daily_budget": item["recommended_daily_budget"],
        "auto_launch_approved": approved,
        "launch_mode": "AUTO_LAUNCH_ALLOWED" if approved else "MANUAL_REVIEW_REQUIRED"
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "mode": cfg["mode"],
    "emergency_stop": cfg["emergency_stop"],
    "live_spending_enabled": cfg["allow_live_spending"],
    "decisions": decisions,
    "status": "AUTO_LAUNCH_ENGINE_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

print(json.dumps(report, indent=2))
