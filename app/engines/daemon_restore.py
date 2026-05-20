
automation_daemon_state = {
    "running": False,
    "runs": 0,
    "last_result": None,
    "last_error": None
}


def restore_daemon_if_needed():
    from app.engines.automation_state import load_daemon_state
    from app.engines.automation_daemon_worker import start_daemon

    result = load_daemon_state()

    if not result["ok"]:
        return {
            "restored": False,
            "reason": "state file not found"
        }

    state = result["state"]
    automation_daemon_state.update(state)

    if automation_daemon_state.get("running"):
        started = start_daemon(automation_daemon_state)

        return {
            "restored": True,
            "daemon_running": True,
            "worker": started
        }

    return {
        "restored": False,
        "daemon_running": False,
        "state": automation_daemon_state
    }

