
def evaluate_rules(state: dict, rulesets: dict) -> dict:

    decisions=[]

    for rs in rulesets["rulesets"]:

        if not rs["ok"]:
            continue

        data=rs["data"]

        if not data.get("enabled",False):
            continue

        for rule in data.get("rules",[]):

            if not rule.get("enabled",False):
                continue

            condition=rule["condition"]

            field=condition["field"]
            operator=condition["operator"]
            expected=condition["value"]

            actual=None

            if field=="daemon.running":
                actual=state.get("running")

            matched=False

            if operator=="eq":
                matched=(actual==expected)

            decisions.append({
                "rule_id":rule["id"],
                "matched":matched,
                "actual":actual,
                "expected":expected,
                "action":rule["action"]
            })

    return {
        "ok":True,
        "count":len(decisions),
        "decisions":decisions
    }

