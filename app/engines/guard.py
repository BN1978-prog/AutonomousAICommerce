def apply_publish_guard(queue: dict, product: dict) -> dict:
    scale = queue.get("scale_recommendation", {})
    jobs = queue.get("jobs", [])

    min_margin = float(product.get("min_margin") or 45)
    min_inventory = int(product.get("min_inventory") or 1)
    min_demand = float(product.get("min_demand") or 55)

    approved = []
    blocked = []

    demand_score = float(scale.get("demand", {}).get("demand_score") or 0)
    scale_action = scale.get("recommended_action")

    for job in jobs:
        margin = 0

        price = float(job.get("payload", {}).get("price") or 0)
        profit = float(job.get("estimated_net_profit") or 0)

        if price > 0:
            margin = round((profit / price) * 100, 2)

        reasons = []

        if margin < min_margin:
            reasons.append("margin_below_threshold")

        if int(job.get("allocated_inventory") or 0) < min_inventory:
            reasons.append("inventory_below_threshold")

        if job.get("compliance_risk") != "low":
            reasons.append("compliance_not_low")

        if demand_score < min_demand:
            reasons.append("demand_below_threshold")

        if scale_action in ["hold", "disable_or_ignore"]:
            reasons.append("scale_action_blocks_publish")

        guarded_job = {
            **job,
            "guard_margin_percent": margin,
            "guard_status": "approved" if not reasons else "blocked",
            "guard_reasons": reasons
        }

        if reasons:
            blocked.append(guarded_job)
        else:
            approved.append(guarded_job)

    return {
        "ok": True,
        "mode": "guard_preview_only",
        "summary": {
            "approved_jobs": len(approved),
            "blocked_jobs": len(blocked),
            "scale_action": scale_action,
            "demand_score": demand_score
        },
        "approved_jobs": approved,
        "blocked_jobs": blocked
    }
