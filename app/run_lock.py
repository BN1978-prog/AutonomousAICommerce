from pathlib import Path
from datetime import datetime, timedelta

LOCK_FILE = Path(r"C:\Users\omen\AutonomousAICommerce\app\logs\run.lock")

MAX_LOCK_AGE_MINUTES = 120

def acquire_lock():
    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)

    if LOCK_FILE.exists():
        try:
            timestamp = LOCK_FILE.read_text(encoding="utf-8").strip()
            created = datetime.fromisoformat(timestamp)

            if datetime.now() - created > timedelta(minutes=MAX_LOCK_AGE_MINUTES):
                print("Removing stale lock file...")
                LOCK_FILE.unlink()
            else:
                raise RuntimeError("Another import run is already active.")
        except Exception:
            raise RuntimeError("Lock file exists and could not be validated.")

    LOCK_FILE.write_text(datetime.now().isoformat(), encoding="utf-8")

def release_lock():
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()
