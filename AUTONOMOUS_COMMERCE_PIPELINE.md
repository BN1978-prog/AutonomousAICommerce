# Autonomous Commerce Live Pipeline

Official order fulfillment entrypoint:

python -m app.autonomous_fulfillment_runner

This runner executes:

1. autonomous_runtime_mode
2. collect_shopify_orders
3. collect_incoming_orders
4. supplier_purchase_queue
5. cj_order_draft_creator
6. cj_payload_builder
7. cj_customer_address_validator
8. autonomous_commerce_live_gate
9. cj_purchase_executor
10. tracking_sync
11. shopify_fulfillment_sync

Readiness check:

python -m app.autonomous_commerce_readiness

Live CJ purchase is controlled by:

app/logs/autonomous_commerce_live_gate.json
CJ_PURCHASE_DRY_RUN environment variable

Do not use old manual order routers as primary flow:
- app/autonomous_order_router.py
- app/order_orchestrator.py
