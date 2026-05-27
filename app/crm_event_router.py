import json
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("app/logs/crm_event_router.json")

def read_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return {}

sales = read_json("app/logs/real_sales_mode.json")
orders = read_json("app/logs/shopify_order_address_collector.json")
drafts = read_json("app/logs/crm_draft_outbox.json")

events = []

if sales.get("has_real_sales") is True:
    events.append({
        "event": "order_created",
        "flow": "order_confirmation",
        "status": "ready_to_queue"
    })

if orders.get("orders_seen", 0) > 0:
    events.append({
        "event": "customer_detected",
        "flow": "welcome_or_post_purchase",
        "status": "ready_to_queue"
    })

# ???? add_to_cart ??????? ???, ????????? ??? waiting.
events.append({
    "event": "cart_abandoned",
    "flow": "abandoned_cart",
    "status": "waiting_for_cart_events"
})

events.append({
    "event": "order_delivered",
    "flow": "review_request",
    "status": "waiting_for_delivery_event"
})

report = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "events_detected": len(events),
    "events": events,
    "drafts_available": drafts.get("drafts_created", 0),
    "status": "CRM_EVENT_ROUTER_READY"
}

OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
