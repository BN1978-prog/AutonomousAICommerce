import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/roi_engine.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

sales = read_json("app/logs/real_sales_mode.json")
budget = read_json("app/logs/budget_controller.json")
dashboard = read_json("app/logs/system_status_dashboard.json")

revenue = float(sales.get("total_revenue", 0) or 0)
has_sales = sales.get("has_real_sales") is True

# ???? ???????? ??????? ?? ????????, ??????? spend = 0
ad_spend = 0.0
profit = revenue - ad_spend

roi = None
if ad_spend > 0:
    roi = round((profit / ad_spend) * 100, 2)

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "mode": "waiting_for_real_sales" if not has_sales else "roi_tracking_active",
    "has_real_sales": has_sales,
    "total_revenue": revenue,
    "ad_spend": ad_spend,
    "estimated_profit": profit,
    "roi_percent": roi,
    "live_money_spending": dashboard.get("live_money_spending"),
    "budget_status": budget.get("budget_status"),
    "safe_to_update_roi": has_sales and ad_spend > 0,
    "status": "ROI_WAITING_FOR_SALES" if not has_sales else "ROI_ACTIVE"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
