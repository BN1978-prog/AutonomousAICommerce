import json
from pathlib import Path
from datetime import datetime, timezone

SALES=Path("app/logs/real_sales_report_filtered.json")
OUT=Path("app/logs/real_sales_mode.json")

sales=json.loads(SALES.read_text(encoding="utf-8"))

has_sales=sales.get("total_quantity",0)>0

mode={
    "created_at":datetime.now(timezone.utc).isoformat(),
    "has_real_sales":has_sales,
    "mode":"real_sales_active" if has_sales else "waiting_for_sales",
    "total_quantity":sales.get("total_quantity",0),
    "total_revenue":sales.get("total_revenue",0),
    "safe_to_update_roi":has_sales
}

OUT.write_text(json.dumps(mode,indent=2),encoding="utf-8")

print(json.dumps(mode,indent=2))
