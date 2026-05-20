
def run_automation_tick() -> dict:

    from datetime import datetime
    from app.engines.automation_ruleset_loader import load_rulesets
    from app.engines.rule_engine import evaluate_rules
    from app.engines.action_executor import execute_actions
    from app.engines.decision_logger import write_decision_log
    from app.engines.daemon_restore import automation_daemon_state

    result = {
        "ok": True,
        "kind": "automation_tick",
        "started_at": datetime.now().isoformat(),
        "steps": []
    }

    rulesets = load_rulesets()
    decisions = evaluate_rules(automation_daemon_state, rulesets)
    actions = execute_actions(decisions)

    result["steps"].append({
        "name": "rulesets",
        "ok": True,
        "count": rulesets["count"]
    })

    result["steps"].append({
        "name": "rule_engine",
        "ok": True,
        "decisions": decisions["count"]
    })

    result["steps"].append({
        "name": "actions",
        "ok": True,
        "executed": actions["count"]
    })

    result["decisions"] = decisions
    result["actions"] = actions
    result["finished_at"] = datetime.now().isoformat()

    log_result = write_decision_log(result)

    result["steps"].append({
        "name": "decision_log",
        "ok": log_result["ok"],
        "path": log_result["path"]
    })

    result["decision_log"] = log_result

    return result

