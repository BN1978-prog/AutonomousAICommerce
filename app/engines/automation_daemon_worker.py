
import threading
import time

daemon_thread = None
daemon_stop_event = threading.Event()


def daemon_loop(state: dict):
    while True:

        if daemon_stop_event.is_set():
            state["running"] = False
            break
        try:
            from app.engines.automation_tick import run_automation_tick

            state["running"] = True
            state["runs"] = state.get("runs", 0) + 1
            state["last_error"] = None

            tick_result = run_automation_tick()
            tick_result["run"] = state["runs"]

            state["last_result"] = tick_result

            time.sleep(10)

        except Exception as e:
            import traceback

            state["last_error"] = traceback.format_exc()

            time.sleep(10)
            continue


def start_daemon(state: dict) -> dict:
    global daemon_thread

    if daemon_thread and daemon_thread.is_alive():
        return {
            "ok": True,
            "message": "daemon already running"
        }

    daemon_stop_event.clear()

    daemon_thread = threading.Thread(
        target=daemon_loop,
        args=(state,),
        daemon=True
    )

    daemon_thread.start()

    return {
        "ok": True,
        "message": "daemon started"
    }


def stop_daemon(state: dict) -> dict:
    daemon_stop_event.set()
    state["running"] = False

    return {
        "ok": True,
        "message": "daemon stop requested"
    }


def daemon_status(state: dict) -> dict:
    return {
        "ok": True,
        "thread_alive": bool(daemon_thread and daemon_thread.is_alive()),
        "state": state
    }


