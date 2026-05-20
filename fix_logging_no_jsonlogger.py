from pathlib import Path
import shutil

ROOT = Path(r"C:\Users\omen\AutonomousAICommerce")
FILE = ROOT / "app" / "production" / "logging_config.py"

if not FILE.exists():
    raise SystemExit("ERROR: app/production/logging_config.py not found")

backup = FILE.with_suffix(".py.bak_no_jsonlogger")
if not backup.exists():
    shutil.copy2(FILE, backup)

FILE.write_text("""
import logging
import os

def configure_logging():
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger = logging.getLogger()
    logger.setLevel(log_level)

    if logger.handlers:
        return

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def get_logger(name: str):
    configure_logging()
    return logging.getLogger(name)
""".strip() + "\\n", encoding="utf-8")

print("Fixed logging_config.py. pythonjsonlogger removed.")