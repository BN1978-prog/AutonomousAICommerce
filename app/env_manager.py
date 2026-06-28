from pathlib import Path
import os

ENV_PATH = Path(".env")

def load_local_env():
    """
    Local only: load .env if file exists.
    Railway/production may not have .env, so this must never fail.
    """
    if not ENV_PATH.exists():
        return False

    for line in ENV_PATH.read_text(encoding="utf-8-sig", errors="ignore").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value

    return True

def get_env(name, default=""):
    return os.getenv(name, default)

def env_file_exists():
    return ENV_PATH.exists()

# safe load at import
load_local_env()
