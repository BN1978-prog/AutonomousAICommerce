
def execute_actions(decisions: dict) -> dict:
    executed = []

    for decision in decisions.get("decisions", []):
        if not decision.get("matched"):
            continue

        action = decision.get("action", {})
        action_type = action.get("type")

        if action_type == "log":
            executed.append({
                "ok": True,
                "rule_id": decision.get("rule_id"),
                "type": "log",
                "message": action.get("message")
            })
        else:
            executed.append({
                "ok": False,
                "rule_id": decision.get("rule_id"),
                "type": action_type,
                "error": "unsupported action type"
            })

    return {
        "ok": True,
        "count": len(executed),
        "executed": executed
    }

