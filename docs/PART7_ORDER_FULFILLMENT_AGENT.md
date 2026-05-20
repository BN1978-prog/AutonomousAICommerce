# Part 7 — Order Fulfillment Agent

This module adds the controlled order execution layer.

## What it does

- Accepts a marketplace order fulfillment request.
- Fetches the supplier product from the registered supplier adapter.
- Re-runs the advanced profit/risk governor before any purchase.
- Supports dry-run approval for safe testing.
- Blocks execution if margins, return risk, supplier risk, budget, stock, or settings fail.
- Creates the supplier purchase order only when:
  - the governor approves,
  - `dry_run=false`, and
  - `ENABLE_AUTONOMOUS_PURCHASE=true`.

## Endpoint

`POST /fulfillment/process`

## Safety design

The module keeps raw shipping details only at the supplier execution boundary. Production systems should encrypt PII, use idempotency keys, and connect only to official supplier APIs.
