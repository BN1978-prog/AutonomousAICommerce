
def save_daemon_state(state: dict) -> dict:
    import json
    from pathlib import Path
    from datetime import datetime

    folder = Path("data/automation_state")
    folder.mkdir(parents=True, exist_ok=True)

    state["saved_at"] = datetime.now().isoformat()

    path = folder / "daemon_state.json"
    path.write_text(json.dumps(state, indent=2), encoding="utf-8")

    return {
        "ok": True,
        "path": str(path),
        "state": state
    }


def load_daemon_state() -> dict:
    import json
    from pathlib import Path

    path = Path("data/automation_state") / "daemon_state.json"

    if not path.exists():
        return {
            "ok": False,
            "message": "daemon state not found"
        }

    return {
        "ok": True,
        "path": str(path),
        "state": json.loads(path.read_text(encoding="utf-8"))
    }

