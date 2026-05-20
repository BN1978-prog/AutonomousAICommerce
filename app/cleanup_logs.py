from pathlib import Path
from datetime import datetime, timedelta

LOG_DIRS = [
    r"C:\Users\omen\AutonomousAICommerce\app\logs\supplier_raw",
    r"C:\Users\omen\AutonomousAICommerce\app\logs\daily_runs",
]

KEEP_DAYS = 14

def cleanup_directory(path_str):
    path = Path(path_str)

    if not path.exists():
        return

    cutoff = datetime.now() - timedelta(days=KEEP_DAYS)

    removed = 0

    for file in path.glob("*"):
        if not file.is_file():
            continue

        modified = datetime.fromtimestamp(file.stat().st_mtime)

        if modified < cutoff:
            file.unlink()
            removed += 1

    print(f"{path.name}: removed {removed} old files")

def main():
    print("=== LOG CLEANUP ===")

    for directory in LOG_DIRS:
        cleanup_directory(directory)

if __name__ == "__main__":
    main()
