def build_marketplace_routing(product: dict, decision: dict) -> dict:
    decisions = decision.get("decisions", [])

    routing_plan = []

    for idx, channel in enumerate(decisions):
        recommendation = channel.get("recommendation")
        score = float(channel.get("decision_score") or 0)

        if recommendation == "best_channel":
            priority = "high"
        elif recommendation == "good_channel":
            priority = "medium"
        else:
            priority = "low"

        publish = score >= 70

        routing_plan.append({
            "channel": channel.get("channel"),
            "priority": priority,
            "publish": publish,
            "decision_score": score,
            "estimated_profit": channel.get("estimated_net_profit"),
            "compliance_risk": channel.get("compliance_risk"),
            "routing_order": idx + 1
        })

    immediate_publish = [
        x for x in routing_plan
        if x["publish"]
    ]

    hold_channels = [
        x for x in routing_plan
        if not x["publish"]
    ]

    return {
        "ok": True,
        "product": {
            "title": product.get("title"),
            "sku": product.get("sku"),
            "price": product.get("price")
        },
        "primary_channel": immediate_publish[0] if immediate_publish else None,
        "immediate_publish_channels": immediate_publish,
        "hold_channels": hold_channels,
        "routing_plan": routing_plan
    }


def build_inventory_routing(product: dict, routing: dict) -> dict:
    total_inventory = int(product.get("inventory") or 0)
    publish_channels = routing.get("immediate_publish_channels", [])

    allocations = []

    if not publish_channels or total_inventory <= 0:
        return {
            "ok": True,
            "total_inventory": total_inventory,
            "allocations": [],
            "message": "No inventory allocation needed."
        }

    remaining = total_inventory

    for channel in publish_channels:
        score = float(channel.get("decision_score") or 0)

        if channel.get("routing_order") == 1:
            allocation_percent = 40
        elif score >= 80:
            allocation_percent = 20
        elif score >= 70:
            allocation_percent = 10
        else:
            allocation_percent = 5

        allocated = max(1, int(total_inventory * allocation_percent / 100))

        if allocated > remaining:
            allocated = remaining

        remaining -= allocated

        allocations.append({
            "channel": channel.get("channel"),
            "routing_order": channel.get("routing_order"),
            "priority": channel.get("priority"),
            "decision_score": score,
            "allocated_inventory": allocated,
            "allocation_percent": allocation_percent
        })

        if remaining <= 0:
            break

    return {
        "ok": True,
        "sku": product.get("sku"),
        "total_inventory": total_inventory,
        "allocated_total": sum(x["allocated_inventory"] for x in allocations),
        "unallocated_inventory": remaining,
        "oversell_protection": True,
        "allocations": allocations
    }
