from pathlib import Path
from datetime import datetime, timezone, timedelta

LOG_DIR = Path("app/logs")
ARCHIVE_DIR = LOG_DIR / "archive"
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

KEEP_DAYS = 30
cutoff = datetime.now(timezone.utc) - timedelta(days=KEEP_DAYS)

protected = {
    "product_catalog.json",
    "product_performance.json",
    "published_posts.json",
    "autopilot_decisions.json",
    "daily_summary.txt",
    "daily_publish_lock.json"
}

moved = 0

for f in LOG_DIR.glob("*"):
    if not f.is_file():
        continue

    if f.name in protected:
        continue

    modified = datetime.fromtimestamp(f.stat().st_mtime, timezone.utc)

    if modified < cutoff:
        target = ARCHIVE_DIR / f.name
        f.replace(target)
        moved += 1

print("Log cleanup complete")
print("Moved old files:", moved)
