import json
import shutil
from pathlib import Path
from datetime import datetime, timezone

STAMP = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
BACKUP_DIR = Path("app/backups") / STAMP
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

FILES = [
    ".env",
    "app/logs/system_status_dashboard.json",
    "app/logs/last_known_good_state.json",
    "app/logs/recovery_report.json",
    "app/logs/daily_report.json",
    "app/logs/alerts.json",
    "app/logs/production_readiness_report.json",
    "app/logs/global_commerce_control_panel.json",
    "app/logs/external_blockers_monitor.json"
]

copied = []
missing = []

for f in FILES:
    src = Path(f)
    if src.exists():
        dst = BACKUP_DIR / src.name
        shutil.copy2(src, dst)
        copied.append(str(src))
    else:
        missing.append(str(src))

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "backup_dir": str(BACKUP_DIR),
    "copied": copied,
    "missing": missing,
    "status": "BACKUP_OK"
}

Path("app/logs/backup_report.json").write_text(
    json.dumps(report, indent=2),
    encoding="utf-8"
)

print(json.dumps(report, indent=2))
