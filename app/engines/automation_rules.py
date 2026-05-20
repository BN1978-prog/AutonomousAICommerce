
def save_automation_ruleset(name: str, rules: list) -> dict:
    import json
    from pathlib import Path
    from datetime import datetime

    folder = Path("data/automation_rules")
    folder.mkdir(parents=True, exist_ok=True)

    record = {
        "name": name,
        "rules": rules,
        "updated_at": datetime.now().isoformat()
    }

    path = folder / f"{name}.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")

    return {
        "ok": True,
        "path": str(path),
        "record": record
    }


def load_automation_ruleset(name: str) -> dict:
    import json
    from pathlib import Path

    path = Path("data/automation_rules") / f"{name}.json"

    if not path.exists():
        return {
            "ok": False,
            "message": f"ruleset not found: {name}"
        }

    return {
        "ok": True,
        "path": str(path),
        "record": json.loads(path.read_text(encoding="utf-8"))
    }


def list_automation_rulesets() -> dict:
    import json
    from pathlib import Path

    folder = Path("data/automation_rules")
    folder.mkdir(parents=True, exist_ok=True)

    records = []

    for file in folder.glob("*.json"):
        try:
            records.append(json.loads(file.read_text(encoding="utf-8")))
        except Exception as e:
            records.append({
                "ok": False,
                "file": str(file),
                "error": str(e)
            })

    return {
        "ok": True,
        "count": len(records),
        "rulesets": records
    }

