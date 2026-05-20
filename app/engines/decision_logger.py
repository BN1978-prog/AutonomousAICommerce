
from pathlib import Path
import json
from datetime import datetime


LOG_FOLDER = Path("data/decision_logs")


def write_decision_log(tick_result: dict) -> dict:
    LOG_FOLDER.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    path = LOG_FOLDER / f"decision_log_{ts}.json"

    payload = {
        "ok": True,
        "written_at": datetime.now().isoformat(),
        "tick": tick_result
    }

    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    return {
        "ok": True,
        "path": str(path)
    }

