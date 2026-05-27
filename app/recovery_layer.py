import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/recovery_report.json")

CURRENT = Path("app/logs/system_status_dashboard.json")
GOOD = Path("app/logs/last_known_good_state.json")

def read_json(path):
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except:
        return {}

current = read_json(CURRENT)
good = read_json(GOOD)

checks = []

def compare(key):
    old = good.get(key)
    new = current.get(key)

    status = "same" if old == new else "changed"

    checks.append({
        "field": key,
        "last_known_good": old,
        "current": new,
        "status": status
    })

for key in [
    "system_status",
    "production_readiness",
    "status",
    "safe_to_continue",
    "live_money_spending",
    "channel_self_healer",
    "external_blockers_count",
    "meta_funnel",
    "google_status",
    "real_sales_mode",
    "purchase_queue_size"
]:
    compare(key)

critical = []

for c in checks:
    if c["field"] == "system_status" and c["current"] != "HEALTHY":
        critical.append(c)

    if c["field"] == "safe_to_continue" and c["current"] is not True:
        critical.append(c)

    if c["field"] == "live_money_spending" and c["current"] is not False:
        critical.append(c)

    if c["field"] == "status" and c["current"] != "PRODUCTION_READY_SAFE_MODE":
        critical.append(c)

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "checks": checks,
    "critical_changes": critical,
    "critical_changes_count": len(critical),
    "status": "RECOVERY_OK" if not critical else "RECOVERY_ATTENTION_REQUIRED"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
