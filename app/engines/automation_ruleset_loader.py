
from pathlib import Path
import json


RULESETS_FOLDER = Path("data/rulesets")


def load_rulesets() -> dict:
    RULESETS_FOLDER.mkdir(parents=True, exist_ok=True)

    files = list(RULESETS_FOLDER.glob("*.json"))

    rulesets = []

    for file in files:
        try:
            rulesets.append({
                "ok": True,
                "file": str(file),
                "data": json.loads(file.read_text(encoding="utf-8-sig"))
            })
        except Exception as e:
            rulesets.append({
                "ok": False,
                "file": str(file),
                "error": str(e)
            })

    return {
        "ok": True,
        "folder": str(RULESETS_FOLDER),
        "count": len(rulesets),
        "rulesets": rulesets
    }


