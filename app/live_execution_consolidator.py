import json
from pathlib import Path
from datetime import datetime, timezone
from app.alert_dispatcher import notify

META = Path("app/logs/meta_live_execution_result.json")
GOOGLE = Path("app/logs/google_live_execution_result.json")
OUT = Path("app/logs/live_execution_consolidated.json")

meta = json.loads(META.read_text(encoding="utf-8")) if META.exists() else {}
google = json.loads(GOOGLE.read_text(encoding="utf-8")) if GOOGLE.exists() else {}

meta_results = meta.get("results", [])
google_results = google.get("results", [])

all_results = meta_results + google_results

real_api_calls = len([x for x in all_results if x.get("real_api_called")])
real_money_spent = sum(float(x.get("real_money_spent", 0)) for x in all_results)

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "meta_campaigns": len(meta_results),
    "google_campaigns": len(google_results),
    "total_campaigns_checked": len(all_results),
    "real_api_calls": real_api_calls,
    "real_money_spent": real_money_spent,
    "results": all_results,
    "status": "LIVE_EXECUTION_CONSOLIDATED_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

try:
    payload = (
        f"Live execution consolidated\n"
        f"Meta checked: {len(meta_results)}\n"
        f"Google checked: {len(google_results)}\n"
        f"Real API calls: {real_api_calls}\n"
        f"Real money spent: ${real_money_spent}\n"
        f"Status: {report['status']}"
    )

    notify("CEO_DASHBOARD", payload)

    print("LIVE EXECUTION CONSOLIDATED ALERT SENT")

except Exception as e:
    print("consolidated alert skipped:", e)

print(json.dumps(report, indent=2))
