import json
from pathlib import Path
from datetime import datetime, timezone

SRC = Path("app/logs/auto_scaling_score.json")
OUT = Path("app/logs/roi_simulation.json")

data = json.loads(SRC.read_text(encoding="utf-8"))

simulations=[]

for item in data.get("scale_ready",[]):

    score = item["score"]
    sales = item["sales"]
    clicks = item["clicks"]

    conversion_rate = round((sales / clicks) * 100, 2) if clicks else 0

    estimated_cpc = 0.18
    estimated_product_margin = 12.50

    estimated_ad_spend = round(clicks * estimated_cpc, 2)

    estimated_profit = round(
        (sales * estimated_product_margin) - estimated_ad_spend,
        2
    )

    roi_percent = round(
        (estimated_profit / estimated_ad_spend) * 100,
        2
    ) if estimated_ad_spend else 0

    risk_score = (
        "LOW"
        if roi_percent >= 200 else
        "MEDIUM"
        if roi_percent >= 50 else
        "HIGH"
    )

    recommended_daily_budget = (
        25 if risk_score=="LOW" else
        10 if risk_score=="MEDIUM" else
        5
    )

    simulations.append({
        "sku": item["sku"],
        "conversion_rate_percent": conversion_rate,
        "estimated_cpc": estimated_cpc,
        "estimated_ad_spend": estimated_ad_spend,
        "estimated_profit": estimated_profit,
        "estimated_roi_percent": roi_percent,
        "risk_score": risk_score,
        "recommended_daily_budget": recommended_daily_budget,
        "recommended_action": (
            "SAFE_TO_SCALE_REVIEW"
            if risk_score in ["LOW","MEDIUM"]
            else "KEEP_TESTING"
        )
    })

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "simulations": simulations,
    "live_money_spending": False,
    "status": "ROI_SIMULATION_READY_SAFE_MODE"
}

OUT.write_text(
    json.dumps(report, indent=2),
    encoding="utf-8"
)

print(json.dumps(report, indent=2))
