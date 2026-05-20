def build_publish_queue_preview(product: dict, orchestrator: dict, scale: dict) -> dict:
    jobs = []

    scale_action = scale.get("recommended_action")
    scale_score = scale.get("scale_score")

    for item in orchestrator.get("publish_plan", []):
        if not item.get("publish"):
            continue

        if scale_action in ["hold", "disable_or_ignore"]:
            continue

        if int(item.get("allocated_inventory") or 0) <= 0:
            continue

        jobs.append({
            "job_id": f"{product.get('sku')}-{item.get('channel')}",
            "scale_action": scale_action,
            "scale_score": scale_score,
            "sku": product.get("sku"),
            "channel": item.get("channel"),
            "priority": item.get("priority"),
            "routing_order": item.get("routing_order"),
            "status": "queued_preview",
            "allocated_inventory": item.get("allocated_inventory"),
            "estimated_net_profit": item.get("estimated_net_profit"),
            "compliance_risk": item.get("compliance_risk"),
            "payload": item.get("listing_payload")
        })

    jobs = sorted(
        jobs,
        key=lambda x: (
            0 if x["priority"] == "high" else 1,
            x["routing_order"]
        )
    )

    return {
        "ok": True,
        "mode": "preview_only",
        "message": "Publish queue generated only. No API calls made.",
        "scale_recommendation": scale,
        "summary": {
            "queued_jobs": len(jobs),
            "scale_action": scale_action,
            "scale_score": scale_score,
            "channels": [x["channel"] for x in jobs]
        },
        "jobs": jobs
    }
