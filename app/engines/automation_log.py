
def save_automation_decision(sku: str, rule: str, result: dict) -> dict:
    import json
    from pathlib import Path
    from datetime import datetime

    folder = Path("data/automation_logs")
    folder.mkdir(parents=True, exist_ok=True)

    record = {
        "sku": sku,
        "rule": rule,
        "created_at": datetime.now().isoformat(),
        "result": result
    }

    path = folder / f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-{sku}-{rule}.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")

    return {
        "ok": True,
        "path": str(path)
    }

